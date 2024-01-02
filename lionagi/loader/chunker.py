from enum import Enum
from typing import Union, Callable

from lionagi.bridge.langchain import langchain_text_splitter, from_langchain
from lionagi.bridge.llama_index import llama_index_node_parser, from_llama_index
from lionagi.utils.call_util import lcall
from lionagi.utils.load_utils import file_to_chunks
from lionagi.schema.base_schema import DataNode


class ChunkerType(str, Enum):
    PLAIN = 'plain'
    LANGCHAIN = 'langchain'
    LLAMAINDEX = 'llama_index'
    SELFDEFINED = 'self_defined'


def datanodes_convert(documents, chunker_type):
    for i in range(len(documents)):
        if type(documents[i]) == DataNode:
            if chunker_type == ChunkerType.LLAMAINDEX:
                documents[i] = documents[i].to_llama_index()
            elif chunker_type == ChunkerType.LANGCHAIN:
                documents[i] = documents[i].to_langchain()
    return documents


def text_chunker(documents, args, kwargs):
    def chunk_node(node):
        chunks = file_to_chunks(node.to_dict(), *args, **kwargs)
        lcall(chunks, lambda chunk: chunk.pop('node_id'))
        chunk_nodes = lcall(chunks, lambda x: DataNode(**x))
        return chunk_nodes

    nodes = []
    for doc in documents:
        nodes += chunk_node(doc)
    return nodes


def _datanode_parser(nodes, parser):
    try:
        nodes = parser(nodes)
    except Exception as e:
        raise ValueError(f'DataNode parser {parser} failed. Error:{e}')
    return nodes


def chunk(documents,
          chunker,
          chunker_type=ChunkerType.PLAIN,
          chunker_args=[],
          chunker_kwargs={},
          chunking_kwargs={},
          documents_convert_func=None,
          to_datanode: Union[bool, Callable] = True):
    if chunker_type == ChunkerType.PLAIN:
        try:
            if chunker == 'text_chunker':
                chunker = text_chunker
            nodes = chunker(documents, chunker_args, chunker_kwargs)
            return nodes
        except Exception as e:
            raise ValueError(f'Reader {chunker} is currently not supported. Error: {e}')
    if chunker_type == ChunkerType.LANGCHAIN:
        if documents_convert_func:
            documents = documents_convert_func(documents, 'langchain')
        nodes = langchain_text_splitter(documents, chunker, chunker_args, chunker_kwargs)
        if isinstance(to_datanode, bool) and to_datanode is True:
            if isinstance(documents, str):
                nodes = lcall(nodes, lambda x: DataNode(content=x))
            else:
                nodes = lcall(nodes, from_langchain)
        elif isinstance(to_datanode, Callable):
            nodes = _datanode_parser(nodes, to_datanode)
        return nodes

    elif chunker_type == ChunkerType.LLAMAINDEX:
        if documents_convert_func:
            documents = documents_convert_func(documents, 'llama_index')
        nodes = llama_index_node_parser(documents, chunker, chunker_args, chunker_kwargs, chunking_kwargs)
        if isinstance(to_datanode, bool) and to_datanode is True:
            nodes = lcall(nodes, from_llama_index)
        elif isinstance(to_datanode, Callable):
            nodes = _datanode_parser(nodes, to_datanode)
        return nodes

    elif chunker_type == ChunkerType.SELFDEFINED:
        try:
            splitter = chunker(*chunker_args, **chunker_kwargs)
            nodes = splitter.split(documents, **chunking_kwargs)
        except Exception as e:
            raise ValueError(f'Self defined chunker {chunker} is not valid. Error: {e}')

        if isinstance(to_datanode, bool) and to_datanode is True:
            raise ValueError(f'Please define a valid parser to DataNode.')
        elif isinstance(to_datanode, Callable):
            nodes = _datanode_parser(nodes, to_datanode)
        return nodes

    else:
        raise ValueError(f'{chunker_type} is not supported. Please choose from {list(ChunkerType)}')
    