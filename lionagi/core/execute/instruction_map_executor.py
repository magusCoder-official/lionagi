import asyncio
from pydantic import Field

from lionagi.libs import AsyncUtil

from lionagi.core.mail.schema import BaseMail, MailTransfer
from lionagi.core.mail.mail_manager import MailManager
from lionagi.core.execute.base_executor import BaseExecutor
from lionagi.core.execute.branch_executor import BranchExecutor


class InstructionMapExecutor(BaseExecutor):
    branches: dict[str, BranchExecutor] = Field(default_factory=dict, description="The branches of the instruction mapping.")
    structure_id: str = Field("", description="The ID of the executable structure.")
    mail_transfer: MailTransfer = Field(default_factory=MailTransfer, description="The mail transfer.")
    branch_kwargs: dict = Field(default_factory=dict, description="The keyword arguments for the initializing the branches.")
    num_end_branches: int = Field(0, description="The number of end branches.")
    mail_manager: MailManager = Field(default_factory=MailManager, description="The mail manager.")
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mail_manager = MailManager([self.mail_transfer])


    def transfer_ins(self):
        for key in list(self.pending_ins.keys()):
            while self.pending_ins[key]:
                mail: BaseMail = self.pending_ins[key].popleft()
                if mail.category == "start":
                    self._process_start(mail)
                elif mail.category == "node_list":
                    self._process_node_list(mail)
                elif (mail.category == "node") or (mail.category == "condition") or (mail.category == "end"):
                    mail.sender_id = self.mail_transfer.id_
                    mail.recipient_id = mail.package['request_source']
                    self.mail_transfer.pending_outs.append(mail)

    def transfer_outs(self):
        for key in list(self.mail_transfer.pending_ins.keys()):
            while self.mail_transfer.pending_ins[key]:
                mail: BaseMail = self.mail_transfer.pending_ins[key].popleft()
                if mail.category == "end":
                    self.num_end_branches += 1
                    if self.num_end_branches == len(self.branches):  # tell when structure should stop
                        mail.sender_id = self.id_
                        mail.recipient_id = self.structure_id
                        self.pending_outs.append(mail)
                        self.execute_stop = True
                else:
                    mail.sender_id = self.id_
                    mail.recipient_id = self.structure_id
                    self.pending_outs.append(mail)

    def _process_start(self, start_mail: BaseMail):
        branch = BranchExecutor(verbose=self.verbose, **self.kwargs)
        branch.context = start_mail.package["context"]
        self.branches[branch.id_] = branch
        self.mail_manager.add_sources([branch])
        self.structure_id = start_mail.package["structure_id"]
        mail = BaseMail(sender_id=self.id_,
                        recipient_id=self.structure_id,
                        category="start",
                        package={"request_source": branch.id_, "package": "start"})
        self.pending_outs.append(mail)

    def _process_node_list(self, nl_mail: BaseMail):
        source_branch_id = nl_mail.package["request_source"]
        node_list = nl_mail.package["package"]
        shared_context = self.branches[source_branch_id].context
        shared_context_log = self.branches[source_branch_id].context_log
        base_branch = self.branches[source_branch_id].branch

        first_node_mail = BaseMail(sender_id=self.mail_transfer.id_,
                                   recipient_id=source_branch_id,
                                   category="node",
                                   package={"request_source": source_branch_id, "package": node_list[0]})
        self.mail_transfer.pending_outs.append(first_node_mail)

        for i in range(1, len(node_list)):
            branch = BranchExecutor(verbose=self.verbose,
                                      messages=base_branch.messages.copy(),
                                      service=base_branch.service,
                                      llmconfig=base_branch.llmconfig,
                                      datalogger=base_branch.datalogger)
            branch.context = shared_context
            branch.context_log = shared_context_log
            self.branches[branch.id_] = branch
            self.mail_manager.add_sources([branch])
            node_mail = BaseMail(sender_id=self.mail_transfer.id_,
                                 recipient_id=branch.id_,
                                 category="node",
                                 package={"request_source": source_branch_id, "package": node_list[i]})
            self.mail_transfer.pending_outs.append(node_mail)

    async def forward(self):
        self.transfer_ins()
        self.transfer_outs()
        self.mail_manager.collect_all()
        self.mail_manager.send_all()
        tasks = [branch.forward() for branch in self.branches.values() if branch.pending_ins]
        await AsyncUtil.execute_tasks(*tasks)
        return

    async def execute(self, refresh_time=1):
        while not self.execute_stop:
            await self.forward()
            await asyncio.sleep(refresh_time)
