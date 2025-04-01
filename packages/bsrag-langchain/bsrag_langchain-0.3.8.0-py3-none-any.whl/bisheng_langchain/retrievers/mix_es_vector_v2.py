from typing import List  # 导入 List 类型注解
from langchain.callbacks.manager import (AsyncCallbackManagerForRetrieverRun, CallbackManagerForRetrieverRun)  # 导入 Langchain 回调管理器
from langchain.schema import BaseRetriever, Document  # 导入 Langchain 基础检索器和文档模型

class JiShiJiaoEsVectorRetriever(BaseRetriever):
    """
    JiShiJiaoEsVectorRetriever 类，用于组合 Elasticsearch 关键词检索器和向量检索器的结果。
    此类集成了 Elasticsearch 关键词检索和向量检索的结果，通过不同的组合策略，
    可以灵活地融合两种检索方式的优点，提升检索效果。
    Args:
        vector_retriever (BaseRetriever): 向量检索器实例，用于执行向量相似度搜索。
        keyword_retriever (BaseRetriever): 关键词检索器实例，用于执行关键词匹配搜索。
        combine_strategy (str): 组合策略，用于指定如何组合关键词检索和向量检索的结果，可选值包括：
            - 'keyword_front': 关键词检索结果在前，向量检索结果在后。
            - 'vector_front': 向量检索结果在前，关键词检索结果在后。
            - 'mix': 混合组合，交替排列关键词检索和向量检索的结果。
            默认为 'keyword_front'。
    """
    vector_retriever: BaseRetriever  # 向量检索器
    keyword_retriever: BaseRetriever  # 关键词检索器
    combine_strategy: str = 'keyword_front'  # 组合策略，默认为 'keyword_front'，关键词检索结果在前

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun, ) -> List[Document]:
        """
        获取给定查询的相关文档列表 (同步方法).
        根据指定的组合策略，融合关键词检索器和向量检索器的检索结果，返回最终的相关文档列表。
        Args:
            query (str): 查询语句。
            run_manager (CallbackManagerForRetrieverRun): 回调管理器，用于处理检索过程中的回调事件。
        Returns:
            List[Document]: 相关文档列表。
        """
        print("jishijiao - _get_relevant_documents")  # 打印日志，标记进入同步检索方法
        # 获取检索器的融合结果。
        vector_docs = self.vector_retriever.get_relevant_documents(query, callbacks=run_manager.get_child())  # 调用向量检索器获取相关文档
        keyword_docs = self.keyword_retriever.get_relevant_documents(query, callbacks=run_manager.get_child())  # 调用关键词检索器获取相关文档
        if self.combine_strategy == 'keyword_front':  # 如果组合策略为 'keyword_front'
            return keyword_docs + vector_docs  # 关键词检索结果在前，向量检索结果在后
        elif self.combine_strategy == 'vector_front':  # 如果组合策略为 'vector_front'
            return vector_docs + keyword_docs  # 向量检索结果在前，关键词检索结果在后
        elif self.combine_strategy == 'mix':  # 如果组合策略为 'mix'
            combine_docs_dict = {}  # 初始化合并文档字典，用于去重
            min_len = min(len(keyword_docs), len(vector_docs))  # 获取关键词和向量检索结果列表的最小长度
            for i in range(min_len):  # 遍历较短的结果列表长度
                combine_docs_dict[keyword_docs[i].page_content] = keyword_docs[i]  # 将关键词检索结果添加到合并文档字典
                combine_docs_dict[vector_docs[i].page_content] = vector_docs[i]  # 将向量检索结果添加到合并文档字典
            for doc in keyword_docs[min_len:]:  # 将关键词检索结果列表中剩余的文档添加到合并文档字典
                combine_docs_dict[doc.page_content] = doc
            for doc in vector_docs[min_len:]:  # 将向量检索结果列表中剩余的文档添加到合并文档字典
                combine_docs_dict[doc.page_content] = doc
            # 将字典的值转换为列表，实现混合组合，并去重
            combine_docs = list(combine_docs_dict.values())  # 将合并文档字典的值转换为列表
            return combine_docs  # 返回合并后的文档列表
        else:  # 如果组合策略不是预定义的值
            raise ValueError(f'Expected combine_strategy to be one of '
                             f'(keyword_front, vector_front, mix),'
                             f'instead found {self.combine_strategy}')  # 抛出 ValueError 异常，提示组合策略无效

    async def _aget_relevant_documents(self, query: str, *, run_manager: AsyncCallbackManagerForRetrieverRun, ) -> List[Document]:
        """
        异步获取给定查询的相关文档列表 (异步方法).
        根据指定的组合策略，异步融合关键词检索器和向量检索器的检索结果，返回最终的相关文档列表。
        Args:
            query (str): 查询语句。
            run_manager (AsyncCallbackManagerForRetrieverRun): 异步回调管理器，用于处理检索过程中的回调事件。
        Returns:
            List[Document]: 相关文档列表。
        """
        print("jishijiao - _aget_relevant_documents")  # 打印日志，标记进入异步检索方法
        # 获取检索器的融合结果。
        vector_docs = await self.vector_retriever.aget_relevant_documents(query, callbacks=run_manager.get_child())  # 异步调用向量检索器获取相关文档
        keyword_docs = await self.keyword_retriever.aget_relevant_documents(query, callbacks=run_manager.get_child())  # 异步调用关键词检索器获取相关文档
        if self.combine_strategy == 'keyword_front':  # 如果组合策略为 'keyword_front'
            return keyword_docs + vector_docs  # 关键词检索结果在前，向量检索结果在后
        elif self.combine_strategy == 'vector_front':  # 如果组合策略为 'vector_front'
            return vector_docs + keyword_docs  # 向量检索结果在前，关键词检索结果在后
        elif self.combine_strategy == 'mix':  # 如果组合策略为 'mix'
            combine_docs_dict = {}  # 初始化合并文档字典，用于去重
            min_len = min(len(keyword_docs), len(vector_docs))  # 获取关键词和向量检索结果列表的最小长度
            for i in range(min_len):  # 遍历较短的结果列表长度
                combine_docs_dict[keyword_docs[i].page_content] = keyword_docs[i]  # 将关键词检索结果添加到合并文档字典
                combine_docs_dict[vector_docs[i].page_content] = vector_docs[i]  # 将向量检索结果添加到合并文档字典
            for doc in keyword_docs[min_len:]:  # 将关键词检索结果列表中剩余的文档添加到合并文档字典
                combine_docs_dict[doc.page_content] = doc
            for doc in vector_docs[min_len:]:  # 将向量检索结果列表中剩余的文档添加到合并文档字典
                combine_docs_dict[doc.page_content] = doc
            # 将字典的值转换为列表，实现混合组合，并去重
            combine_docs = list(combine_docs_dict.values())  # 将合并文档字典的值转换为列表
            return combine_docs  # 返回合并后的文档列表
        else:  # 如果组合策略不是预定义的值
            raise ValueError(f'Expected combine_strategy to be one of '
                             f'(keyword_front, vector_front, mix),'
                             f'instead found {self.combine_strategy}')  # 抛出 ValueError 异常，提示组合策略无效
