"""Elasticsearch 向量数据库的包装器."""
from __future__ import annotations
import json
import uuid
from abc import ABC
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Optional, Tuple
import jieba.analyse
from langchain.chains.llm import LLMChain
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.llms.base import BaseLLM
from langchain.prompts.prompt import PromptTemplate
from langchain.utils import get_from_dict_or_env
from langchain.vectorstores.base import VectorStore
if TYPE_CHECKING:
    from elasticsearch import Elasticsearch  # noqa: F401

def _default_text_mapping() -> Dict:
    """默认的文本字段映射配置.
    定义 Elasticsearch 索引中 'text' 字段的默认映射，类型为 'text'，用于全文检索。
    """
    return {'properties': {'text': {'type': 'text'}}}

DEFAULT_PROMPT = PromptTemplate(input_variables=['question'], template="""分析给定Question，提取Question中包含的KeyWords，输出列表形式
Examples:
Question: 达梦公司在过去三年中的流动比率如下：2021年：3.74倍；2020年：2.82倍；2019年：2.05倍。
KeyWords: ['过去三年', '流动比率', '2021', '3.74', '2020', '2.82', '2019', '2.05']
----------------
Question: {question}
KeyWords: """, )

class JiShiJiaoElasticKeywordsSearch(VectorStore, ABC):
    """
    JiShiJiaoElasticKeywordsSearch 类，是对 Elasticsearch 关键词搜索引擎的包装，继承自 VectorStore 和 ABC 类。
    此类用于将 Elasticsearch 作为关键词向量数据库进行封装，实现基于关键词的文档检索功能。
    它利用 jieba 库进行中文关键词提取，并可选择性地使用 LLMChain 提升关键词提取的准确性。
    Args:
        elasticsearch_url (str): Elasticsearch 实例的 URL 地址，例如 "http://localhost:9200"。
        index_name (str): Elasticsearch 中用于存储关键词索引的索引名称。
        top_k (Optional[int]): 相似度搜索时返回的最相关文档数量，默认为 1。
        drop_old (Optional[bool]): 初始化时是否删除已存在的同名索引，默认为 False。
        ssl_verify (Optional[Dict[str, Any]]): SSL 验证相关配置字典，用于连接启用了 SSL 的 Elasticsearch 服务，默认为 None。
        llm_chain (Optional[LLMChain]): 用于关键词提取的 LLMChain 对象，如果提供，则使用 LLM 提取关键词，否则使用 jieba 库，默认为 None。
    Raises:
        ImportError: 如果缺少必要的 Python 包 (elasticsearch)。
        ValueError: 如果提供的 Elasticsearch 客户端 URL 格式错误。
    Example:
        创建 JiShiJiaoElasticKeywordsSearch 实例并连接到本地 Elasticsearch 服务：
        .. code-block:: python
            from langchain import ElasticKeywordsSearch
            elastic_keywords_search = ElasticKeywordsSearch(
                elasticsearch_url="http://localhost:9200",
                index_name="my_keywords_index",
            )
        创建 JiShiJiaoElasticKeywordsSearch 实例并连接到需要身份验证的 Elastic Cloud 服务：
        .. code-block:: python
            from langchain import ElasticKeywordsSearch
            elasticsearch_url = "https://<username>:<password>@<cluster_id>.<region_id>.gcp.cloud.es.io:9243"
            elastic_keywords_search = ElasticKeywordsSearch(
                elasticsearch_url=elasticsearch_url,
                index_name="my_keywords_index"
            )
    """

    def __init__(self, elasticsearch_url: str, index_name: str, top_k: Optional[int] = 1, drop_old: Optional[bool] = False, *, ssl_verify: Optional[Dict[str, Any]] = None,
            llm_chain: Optional[LLMChain] = None, ):
        """使用必要的组件初始化 JiShiJiaoElasticKeywordsSearch 实例.
        Args:
            elasticsearch_url (str): Elasticsearch 实例的 URL 地址。
            index_name (str): Elasticsearch 中用于存储关键词索引的索引名称。
            top_k (Optional[int]): 相似度搜索时返回的最相关文档数量，默认为 1。
            drop_old (Optional[bool]): 初始化时是否删除已存在的同名索引，默认为 False。
            ssl_verify (Optional[Dict[str, Any]]): SSL 验证相关配置字典，默认为 None。
            llm_chain (Optional[LLMChain]): 用于关键词提取的 LLMChain 对象，默认为 None。
        Raises:
            ImportError: 如果缺少必要的 Python 包 (elasticsearch)。
            ValueError: 如果提供的 Elasticsearch 客户端 URL 格式错误。
        """
        try:
            import elasticsearch
        except ImportError:
            raise ImportError('无法导入 elasticsearch python 包。 请使用 `pip install elasticsearch` 安装。')
        self.index_name = index_name  # 设置索引名称
        self.llm_chain = llm_chain  # 设置 LLMChain 对象
        self.top_k = top_k  # 设置 TopK 值
        self.drop_old = drop_old  # 设置是否删除旧索引标志
        _ssl_verify = ssl_verify or {}  # 获取 SSL 验证配置，默认为空字典
        self.elasticsearch_url = elasticsearch_url  # 设置 Elasticsearch URL
        self.ssl_verify = _ssl_verify  # 设置 SSL 验证配置
        try:
            self.client = elasticsearch.Elasticsearch(elasticsearch_url, **_ssl_verify)  # 初始化 Elasticsearch 客户端
        except ValueError as e:
            raise ValueError(f'您的 elasticsearch 客户端字符串格式错误。 错误信息: {e} ')
        if drop_old:  # 如果 drop_old 为 True，则删除旧索引
            try:
                self.client.indices.delete(index=index_name)  # 尝试删除索引
            except elasticsearch.exceptions.NotFoundError:  # 如果索引不存在，忽略异常
                pass

    def add_texts(self, texts: Iterable[str], metadatas: Optional[List[dict]] = None, ids: Optional[List[str]] = None, refresh_indices: bool = True, **kwargs: Any, ) -> List[str]:
        """通过关键词运行更多文本并添加到向量存储.
        将提供的文本数据添加到 Elasticsearch 索引中。每个文本都会被索引，并可以附带元数据和自定义 ID。
        Args:
            texts (Iterable[str]): 要添加到向量存储的文本字符串的可迭代对象。
            metadatas (Optional[List[dict]]): 与文本关联的可选元数据列表，列表中的每个字典对应一个文本。
            ids (Optional[List[str]]): 可选的唯一 ID 列表，用于指定每个文本的 ID。如果为 None，则自动生成 UUID。
            refresh_indices (bool): 布尔值，指示是否在添加文本后立即刷新 Elasticsearch 索引，以确保数据立即可搜索，默认为 True。
        Returns:
            List[str]: 返回成功添加到向量存储中文档的 ID 列表。
        """
        try:
            from elasticsearch.exceptions import NotFoundError
            from elasticsearch.helpers import bulk
        except ImportError:
            raise ImportError('无法导入 elasticsearch python 包。 请使用 `pip install elasticsearch` 安装。')
        requests = []  # 初始化请求列表，用于批量操作
        ids = ids or [str(uuid.uuid4()) for _ in texts]  # 如果未提供 IDs，则为每个文本生成 UUID
        mapping = _default_text_mapping()  # 获取默认的文本字段映射
        # 检查索引是否已存在
        try:
            self.client.indices.get(index=self.index_name)  # 尝试获取索引信息
            if texts and self.drop_old:  # 如果存在文本数据且 drop_old 为 True，则删除并重新创建索引
                self.client.indices.delete(index=self.index_name)  # 删除现有索引
                self.create_index(self.client, self.index_name, mapping)  # 创建新的索引
        except NotFoundError:  # 如果索引不存在，则创建新索引
            # TODO would be nice to create index before embedding,
            # just to save expensive steps for last，TODO：最好在嵌入之前创建索引，以节省最后昂贵的步骤
            self.create_index(self.client, self.index_name, mapping)  # 创建新的索引
        for i, text in enumerate(texts):  # 遍历文本数据
            metadata = metadatas[i] if metadatas else {}  # 获取当前文本的元数据，如果 metadatas 为 None，则使用空字典
            request = {'_op_type': 'index',  # 设置操作类型为 'index'，表示索引文档
                '_index': self.index_name,  # 指定索引名称
                'text': text,  # 设置文本内容
                'metadata': metadata,  # 设置元数据
                '_id': ids[i],  # 设置文档 ID
            }
            requests.append(request)  # 将请求添加到请求列表
        bulk(self.client, requests)  # 使用 Elasticsearch 的 bulk API 批量执行索引请求
        if refresh_indices:  # 如果 refresh_indices 为 True，则刷新索引
            self.client.indices.refresh(index=self.index_name)  # 刷新 Elasticsearch 索引，确保数据立即生效
        return ids  # 返回添加的文档 ID 列表

    def similarity_search(self, query: str, k: int = 1, query_strategy: str = 'match_phrase', must_or_should: str = 'should', **kwargs: Any) -> List[Document]:
        """执行相似度搜索，返回 Document 列表.
        根据提供的查询语句，在 Elasticsearch 索引中执行相似度搜索，并返回最相关的文档列表。
        Args:
            query (str): 要查询的文本语句。
            k (int): 返回的最相关文档的数量，默认为 1。
            query_strategy (str): Elasticsearch 查询策略，默认为 'match_phrase' (短语匹配)，可选 'match' (匹配)。
            must_or_should (str): bool 查询的布尔子句类型，默认为 'should' (应该匹配)，可选 'must' (必须匹配)。
            **kwargs (Any): 传递给 Elasticsearch 客户端搜索方法的其他参数。
        Returns:
            List[Document]: 包含相似度搜索结果的 Document 对象列表。
        """
        if k == 0:
            # pm need to control，控制返回结果数量
            return []
        docs_and_scores = self.similarity_search_with_score(query,  # 调用 similarity_search_with_score 获取带分数的文档列表
            k=self.top_k, query_strategy=query_strategy, must_or_should=must_or_should, **kwargs)
        documents = [d[0] for d in docs_and_scores]  # 从带分数的文档列表中提取 Document 对象
        return documents  # 返回 Document 对象列表

    @staticmethod
    def _relevance_score_fn(distance: float) -> float:
        """将距离归一化为 [0, 1] 范围内的分数.
        此方法目前直接返回距离值，实际应用中可能需要根据 Elasticsearch 的评分机制进行归一化。
        """
        # Todo: normalize the es score on a scale [0, 1]，TODO：将 Elasticsearch 分数归一化到 [0, 1] 范围
        return distance  # 直接返回 Elasticsearch 返回的相关性得分

    def _select_relevance_score_fn(self) -> Callable[[float], float]:
        """选择相关性评分函数，这里直接返回 _relevance_score_fn 函数.
        返回用于计算相关性得分的函数，当前实现直接返回 _relevance_score_fn 方法。
        """
        return self._relevance_score_fn  # 返回 _relevance_score_fn 函数

    def similarity_search_with_score(self, query: str, k: int = 1, query_strategy: str = 'match_phrase', must_or_should: str = 'should', **kwargs: Any) -> List[
        Tuple[Document, float]]:
        """执行相似度搜索，返回带分数的 Document 列表.
        根据提供的查询语句，在 Elasticsearch 索引中执行相似度搜索，并返回最相关的文档列表，包含每个文档的相关性得分。
        Args:
            query (str): 要查询的文本语句。
            k (int): 返回的最相关文档的数量，默认为 1。
            query_strategy (str): Elasticsearch 查询策略，默认为 'match_phrase' (短语匹配)，可选 'match' (匹配)。
            must_or_should (str): bool 查询的布尔子句类型，默认为 'should' (应该匹配)，可选 'must' (必须匹配)。
            **kwargs (Any): 传递给 Elasticsearch 客户端搜索方法的其他参数。
        Returns:
            List[Tuple[Document, float]]: 包含相似度搜索结果的 Document 对象和对应得分的元组列表。
        """
        if k == 0:
            # pm need to control，控制返回结果数量
            return []
        assert must_or_should in ['must', 'should'], 'only support must and should.'  # 验证 must_or_should 参数的合法性
        # llm or jiaba extract keywords，使用 LLM 或 jieba 提取关键词
        if self.llm_chain:  # 如果提供了 LLMChain 对象，则使用 LLM 进行关键词提取
            keywords_str = self.llm_chain.run(query)  # 使用 LLMChain 执行查询，获取关键词字符串
            print('llm search keywords:', keywords_str)  # 打印 LLM 提取的关键词
            try:
                keywords = eval(keywords_str)  # 尝试将关键词字符串解析为 Python 列表
                if not isinstance(keywords, list):  # 验证解析结果是否为列表
                    raise ValueError('Keywords extracted by llm is not list.')  # 如果不是列表，则抛出 ValueError 异常
            except Exception as e:  # 捕获解析异常
                print(str(e))  # 打印异常信息
                keywords = jieba.analyse.extract_tags(query, topK=10, withWeight=False)  # 解析失败时，使用 jieba 提取关键词
        else:  # 如果没有提供 LLMChain 对象，则使用 jieba 进行关键词提取
            keywords = jieba.analyse.extract_tags(query, topK=10, withWeight=False)  # 使用 jieba.analyse.extract_tags 提取关键词
            print('jieba search keywords:', keywords)  # 打印 jieba 提取的关键词
        match_query = {'bool': {must_or_should: []}}  # 构建 Elasticsearch bool 查询
        for key in keywords:  # 遍历提取的关键词列表
            match_query['bool'][must_or_should].append({query_strategy: {'text': key}})  # 根据查询策略和关键词构建查询子句
        response = self.client_search(self.client, self.index_name, match_query, size=k)  # 执行 Elasticsearch 搜索
        hits = [hit for hit in response['hits']['hits']]  # 获取搜索结果中的 hits 列表
        docs_and_scores = [(Document(page_content=hit['_source']['text'],  # 创建 Document 对象，使用 _source 中的 text 字段作为 page_content
            metadata=hit['_source']['metadata'],  # 使用 _source 中的 metadata 字段作为 metadata
        ), hit['_score'],  # 获取 Elasticsearch 返回的相关性得分
        ) for hit in hits]  # 构建 Document 和得分的元组列表
        for (doc, score) in docs_and_scores:  # 遍历文档和得分的元组列表，处理 bbox 和子文档
            if isinstance(doc.metadata['bbox'], str):
                doc.metadata['bbox'] = json.loads(doc.metadata['bbox'])  # 如果 bbox 字段是字符串，则反序列化为 JSON 对象
            if "chunk_type" in doc.metadata and doc.metadata["chunk_type"] == 'title':  # 如果文档类型为 'title'，则搜索子文档并合并内容
                child_docs = self._search_child(doc, client=self.client, index_name=self.index_name, k=4)  # 搜索子文档
                # document merge，文档合并
                for c in child_docs:  # 遍历子文档列表
                    if isinstance(c.metadata['parents'], str):
                        c.metadata["parents"] = json.loads(c.metadata['parents'])  # 反序列化子文档的 parents 元数据
                    if isinstance(c.metadata['bbox'], str):
                        c.metadata['bbox'] = json.loads(c.metadata['bbox'])  # 反序列化子文档的 bbox 元数据
                ch = [s for s in child_docs if doc.metadata['chunk_id'] in s.metadata['parents']]  # 筛选子文档，保留 parents 包含当前文档 chunk_id 的子文档
                sorted(child_docs, key=lambda x: x.metadata['chunk_index'])  # 按 chunk_index 对子文档列表排序
                sorted(ch, key=lambda x: x.metadata['chunk_index'])  # 再次按 chunk_index 对筛选后的子文档列表排序
                for c in child_docs:  # 遍历排序后的子文档列表
                    lines = c.page_content.splitlines()  # 将子文档内容按行分割
                    # 删除第一行，标题分块的第一行通常是标题本身，不需要重复添加到内容中
                    lines = lines[1:]
                    # 将剩余的行重新拼接成一个字符串
                    page_content = "\n".join(lines)
                    doc.metadata['bbox']['chunk_bboxes'].extend(c.metadata['bbox']['chunk_bboxes'])  # 合并 bbox 信息
                    if c.metadata['chunk_type'] == 'title':
                        doc.page_content += f"\n\n{page_content}"  # 如果子文档类型为 'title'，则添加双换行符分隔
                    else:
                        doc.page_content += f"\n{page_content}"  # 否则，添加单换行符分隔
        for (doc, score) in docs_and_scores:  # 再次遍历文档和得分的元组列表，处理 bbox 序列化
            if not isinstance(doc.metadata['bbox'], str):
                doc.metadata['bbox'] = json.dumps(doc.metadata['bbox'])  # 如果 bbox 字段不是字符串，则序列化为 JSON 字符串
        return docs_and_scores  # 返回带分数的文档元组列表

    def _search_child(self, doc, client, index_name, k):
        """搜索子文档.
        根据父文档的 chunk_id，在 Elasticsearch 索引中搜索子文档。
        Args:
            doc (Document): 父文档对象。
            client: Elasticsearch 客户端实例。
            index_name (str): Elasticsearch 索引名称。
            k (int): 返回的子文档数量，默认为 4。
        Returns:
            List[Document]: 包含子文档的 Document 对象列表。
        """
        match_query = {"terms": {"metadata.parents": [doc.metadata["chunk_id"]]  # 构建 terms 查询，匹配 metadata.parents 字段包含父文档 chunk_id 的文档
        }}
        response = self.client_search(client, index_name, match_query, size=k)  # 执行 Elasticsearch 搜索
        hits = [hit for hit in response['hits']['hits']]  # 获取搜索结果中的 hits 列表
        docs = [Document(page_content=hit['_source']['text'],  # 创建 Document 对象，使用 _source 中的 text 字段作为 page_content
            metadata={"retrieve_by_child": True, **hit['_source']['metadata']}) for hit in hits]  # 使用 _source 中的 metadata 字段作为 metadata，并添加 retrieve_by_child 标记
        return docs  # 返回子文档的 Document 对象列表

    @classmethod
    def from_texts(cls, texts: List[str], embedding: Embeddings, metadatas: Optional[List[dict]] = None, ids: Optional[List[str]] = None, index_name: Optional[str] = None,
            refresh_indices: bool = True, llm: Optional[BaseLLM] = None, prompt: Optional[PromptTemplate] = DEFAULT_PROMPT, drop_old: Optional[bool] = False,
            **kwargs: Any, ) -> JiShiJiaoElasticKeywordsSearch:
        """从原始文档构建 ElasticKeywordsSearch 包装器.
        这是一个用户友好的接口，用于快速创建和初始化 ElasticKeywordsSearch 实例，并将文本数据添加到 Elasticsearch 索引中。
        Args:
            texts (List[str]): 要添加到向量存储的文本字符串列表。
            embedding (Embeddings): 嵌入模型对象，用于将文本转换为向量 (虽然当前实现未使用向量嵌入，但参数保留以符合 Langchain 接口)。
            metadatas (Optional[List[dict]]): 与文本关联的可选元数据列表。
            ids (Optional[List[str]]): 可选的唯一 ID 列表，用于指定每个文本的 ID。
            index_name (Optional[str]): Elasticsearch 索引名称，如果为 None，则自动生成 UUID 作为索引名称。
            refresh_indices (bool): 布尔值，指示是否在添加文本后立即刷新 Elasticsearch 索引，默认为 True。
            llm (Optional[BaseLLM]): 用于关键词提取的 LLM 模型对象，默认为 None，使用 jieba 提取关键词。
            prompt (Optional[PromptTemplate]): 用于 LLM 关键词提取的 PromptTemplate 对象，默认为 DEFAULT_PROMPT。
            drop_old (Optional[bool]): 初始化时是否删除已存在的同名索引，默认为 False。
            **kwargs (Any): 传递给 JiShiJiaoElasticKeywordsSearch 构造函数的其他关键字参数，例如 elasticsearch_url。
        Returns:
            JiShiJiaoElasticKeywordsSearch: 构建好的 ElasticKeywordsSearch 实例。
        Example:
            使用 OpenAIEmbeddings 和本地 Elasticsearch 服务创建 ElasticKeywordsSearch 实例：
            .. code-block:: python
                from langchain import ElasticKeywordsSearch
                from langchain.embeddings import OpenAIEmbeddings
                embeddings = OpenAIEmbeddings()
                elastic_keywords_search = ElasticKeywordsSearch.from_texts(
                    texts=["文档1内容", "文档2内容", ...],
                    embeddings=embeddings,
                    elasticsearch_url="http://localhost:9200"
                )
        """
        elasticsearch_url = get_from_dict_or_env(kwargs, 'elasticsearch_url', 'ELASTICSEARCH_URL')  # 从 kwargs 或环境变量中获取 elasticsearch_url
        if 'elasticsearch_url' in kwargs:
            del kwargs['elasticsearch_url']  # 从 kwargs 中移除 elasticsearch_url，避免重复传递
        index_name = index_name or uuid.uuid4().hex  # 如果未提供 index_name，则生成 UUID 作为索引名称
        if llm:  # 如果提供了 LLM 模型，则创建 LLMChain 对象
            llm_chain = LLMChain(llm=llm, prompt=prompt)  # 创建 LLMChain 实例，用于关键词提取
            vectorsearch = cls(elasticsearch_url, index_name, llm_chain=llm_chain, drop_old=drop_old, **kwargs)  # 创建 JiShiJiaoElasticKeywordsSearch 实例，并传入 LLMChain 对象
        else:  # 如果未提供 LLM 模型，则不使用 LLMChain
            vectorsearch = cls(elasticsearch_url, index_name, drop_old=drop_old, **kwargs)  # 创建 JiShiJiaoElasticKeywordsSearch 实例
        vectorsearch.add_texts(texts, metadatas=metadatas, ids=ids, refresh_indices=refresh_indices)  # 将文本数据添加到 Elasticsearch 索引
        return vectorsearch  # 返回创建的 JiShiJiaoElasticKeywordsSearch 实例

    def create_index(self, client: Any, index_name: str, mapping: Dict) -> None:
        """创建 Elasticsearch 索引.
        根据 Elasticsearch 版本，使用不同的 API 创建索引，并应用指定的映射配置。
        Args:
            client: Elasticsearch 客户端实例。
            index_name (str): 要创建的索引名称。
            mapping (Dict): 索引的映射配置字典，定义字段类型等。
        """
        version_num = client.info()['version']['number'][0]  # 获取 Elasticsearch 版本号
        version_num = int(version_num)  # 将版本号转换为整数
        if version_num >= 8:  # 如果 Elasticsearch 版本大于等于 8.0，使用 mappings 参数
            client.indices.create(index=index_name, mappings=mapping)  # 使用 mappings 参数创建索引
        else:  # 如果 Elasticsearch 版本小于 8.0，使用 body 参数
            client.indices.create(index=index_name, body={'mappings': mapping})  # 使用 body 参数创建索引

    def client_search(self, client: Any, index_name: str, script_query: Dict, size: int) -> Any:
        """执行 Elasticsearch 客户端搜索.
        根据 Elasticsearch 版本，使用不同的 API 执行搜索操作。
        Args:
            client: Elasticsearch 客户端实例。
            index_name (str): 要搜索的索引名称。
            script_query (Dict): Elasticsearch 查询脚本字典，定义查询条件。
            size (int): 返回的最大结果数量。
        Returns:
            Any: Elasticsearch 搜索结果响应。
        """
        version_num = client.info()['version']['number'][0]  # 获取 Elasticsearch 版本号
        version_num = int(version_num)  # 将版本号转换为整数
        if version_num >= 8:  # 如果 Elasticsearch 版本大于等于 8.0，使用 query 参数
            response = client.search(index=index_name, query=script_query, size=size)  # 使用 query 参数执行搜索
        else:  # 如果 Elasticsearch 版本小于 8.0，使用 body 参数
            response = client.search(index=index_name, body={'query': script_query, 'size': size})  # 使用 body 参数执行搜索
        return response  # 返回 Elasticsearch 搜索响应

    def delete(self, **kwargs: Any) -> None:
        """删除 Elasticsearch 索引.
        删除与当前 JiShiJiaoElasticKeywordsSearch 实例关联的 Elasticsearch 索引。
        """
        # TODO: Check if this can be done in bulk，TODO：检查是否可以批量删除
        self.client.indices.delete(index=self.index_name)  # 删除 Elasticsearch 索引
