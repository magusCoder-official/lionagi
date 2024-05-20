"""
Copyright 2024 HaiyangLi

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from lionagi.core.unit.unit import Unit
from lionagi.core.session.branch import Branch


async def chat(
    instruction=None,
    context=None,
    system=None,
    sender=None,
    recipient=None,
    branch=None,
    form=None,
    confidence_score=None,
    reason=False,
    **kwargs,
):
    """
    Performs a chat operation using the specified parameters.

    Args:
        instruction (str, optional): The instruction for the chat.
        context (Any, optional): The context to perform the instruction on.
        system (Any, optional): The system context for the chat.
        sender (str, optional): The sender of the instruction.
        recipient (str, optional): The recipient of the instruction.
        branch (Branch, optional): The branch to use for the chat.
        form (Any, optional): The form to create instruction from.
        confidence_score (float, optional): The confidence score for the operation.
        reason (bool, optional): Whether to include a reason for the operation.
        **kwargs: Additional keyword arguments for the chat operation.

    Returns:
        Any: The result of the chat operation.
    """
    branch = branch or Branch()
    unit = Unit(branch)

    return await unit.chat(
        instruction=instruction,
        context=context,
        system=system,
        sender=sender,
        recipient=recipient,
        form=form,
        confidence_score=confidence_score,
        reason=reason,
        branch=branch,
        **kwargs,
    )


async def select(
    instruction=None,
    context=None,
    system=None,
    sender=None,
    recipient=None,
    choices=None,
    branch=None,
    form=None,
    confidence_score=None,
    reason=False,
    **kwargs,
):
    """
    Performs a select operation using the specified parameters.

    Args:
        instruction (str, optional): The instruction for the selection.
        context (Any, optional): The context to perform the instruction on.
        system (Any, optional): The system context for the selection.
        sender (str, optional): The sender of the instruction.
        recipient (str, optional): The recipient of the instruction.
        choices (list, optional): The choices for the selection.
        branch (Branch, optional): The branch to use for the selection.
        form (Any, optional): The form to create instruction from.
        confidence_score (float, optional): The confidence score for the operation.
        reason (bool, optional): Whether to include a reason for the operation.
        **kwargs: Additional keyword arguments for the selection operation.

    Returns:
        Any: The result of the selection operation.
    """
    branch = branch or Branch()
    unit = Unit(branch)

    return await unit.select(
        instruction=instruction,
        context=context,
        system=system,
        sender=sender,
        recipient=recipient,
        choices=choices,
        form=form,
        confidence_score=confidence_score,
        reason=reason,
        **kwargs,
    )


async def predict(
    instruction=None,
    context=None,
    system=None,
    sender=None,
    recipient=None,
    branch=None,
    form=None,
    confidence_score=None,
    reason=False,
    num_sentences=1, 
    **kwargs,
):
    """
    Performs a predict operation using the specified parameters.

    Args:
        instruction (str, optional): The instruction for the prediction.
        context (Any, optional): The context to perform the instruction on.
        system (Any, optional): The system context for the prediction.
        sender (str, optional): The sender of the instruction.
        recipient (str, optional): The recipient of the instruction.
        branch (Branch, optional): The branch to use for the prediction.
        form (Any, optional): The form to create instruction from.
        confidence_score (float, optional): The confidence score for the operation.
        reason (bool, optional): Whether to include a reason for the operation.
        **kwargs: Additional keyword arguments for the prediction operation.

    Returns:
        Any: The result of the prediction operation.
    """
    branch = branch or Branch()
    unit = Unit(branch)

    return await unit.predict(
        instruction=instruction,
        context=context,
        system=system,
        sender=sender,
        recipient=recipient,
        form=form,
        confidence_score=confidence_score,
        reason=reason,
        num_sentences=num_sentences,
        **kwargs,
    )


async def act(
    instruction=None,
    context=None,
    system=None,
    sender=None,
    recipient=None,
    branch=None,
    form=None,
    confidence_score=None,
    reason=False,
    **kwargs,
):
    """
    Performs an act operation using the specified parameters.

    Args:
        instruction (str, optional): The instruction for the action.
        context (Any, optional): The context to perform the instruction on.
        system (Any, optional): The system context for the action.
        sender (str, optional): The sender of the instruction.
        recipient (str, optional): The recipient of the instruction.
        branch (Branch, optional): The branch to use for the action.
        form (Any, optional): The form to create instruction from.
        confidence_score (float, optional): The confidence score for the operation.
        reason (bool, optional): Whether to include a reason for the operation.
        **kwargs: Additional keyword arguments for the act operation.

    Returns:
        Any: The result of the act operation.
    """
    branch = branch or Branch()
    unit = Unit(branch)

    return await unit.act(
        instruction=instruction,
        context=context,
        system=system,
        sender=sender,
        recipient=recipient,
        form=form,
        confidence_score=confidence_score,
        reason=reason,
        **kwargs,
    )

async def score(
    instruction=None,
    context=None,
    system=None,
    sender=None,
    recipient=None,
    branch=None,
    form=None,
    confidence_score=None,
    reason=False,
    score_range=None,
    include_endpoints=None,
    num_digit=None,
    **kwargs,
):
    
    branch = branch or Branch()
    unit = Unit(branch)

    return await unit.score(
        instruction=instruction,
        context=context,
        system=system,
        sender=sender,
        recipient=recipient,
        form=form,
        confidence_score=confidence_score,
        reason=reason,
        score_range=score_range,
        include_endpoints=include_endpoints,
        num_digit=num_digit,
        **kwargs,
    )
    
    
async def plan(
    instruction=None,
    context=None,
    system=None,
    sender=None,
    recipient=None,
    branch=None,
    form=None,
    confidence_score=None,
    reason=False,
    num_step=3,
    **kwargs,
):
    
    branch = branch or Branch()
    unit = Unit(branch)

    return await unit.plan(
        instruction=instruction,
        context=context,
        system=system,
        sender=sender,
        recipient=recipient,
        form=form,
        confidence_score=confidence_score,
        reason=reason,
        num_step=num_step,
        **kwargs,
    )