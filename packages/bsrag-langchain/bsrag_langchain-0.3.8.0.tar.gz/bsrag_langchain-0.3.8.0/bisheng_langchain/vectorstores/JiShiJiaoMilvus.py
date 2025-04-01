"""Milvus 向量数据库的包装器."""
from __future__ import annotations
import json
import logging
from typing import Any, Callable, Iterable, List, Optional, Tuple, Union
import numpy as np
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.utils import maximal_marginal_relevance
from .milvus import Milvus
logger = logging.getLogger(__name__)
# 默认的 Milvus 连接参数
DEFAULT_MILVUS_CONNECTION = {'host': 'localhost',  # Milvus 主机地址，默认为 localhost
                             'port': '19530',  # Milvus 端口号，默认为 19530
                             'user': '',  # 连接 Milvus 的用户名，默认为空
                             'password': '',  # 连接 Milvus 的密码，默认为空
                             'secure': False,  # 是否启用安全连接 (TLS)，默认为 False
                             }

class JiShiJiaoMilvus(Milvus):
    """
    JiShiJiaoMilvus 类，是对 Milvus 向量数据库的包装，继承自 Milvus 类。
    用于初始化 Milvus 向量数据库的包装器。
    为了使用这个类，你需要安装 `pymilvus` 库并运行 Milvus 服务。
    关于如何运行 Milvus 实例，请参考以下文档：
    https://milvus.io/docs/install_standalone-docker.md
    如果需要托管的 Milvus 服务，请查看以下文档：
    https://zilliz.com/cloud 并使用本项目中找到的 Zilliz 向量存储。
    如果使用 L2/IP 距离度量，强烈建议对数据进行归一化处理。
    Args:
        embedding_function (Embeddings): 用于嵌入文本的函数 (Langchain 的 Embeddings 对象)。
        collection_name (str): 要使用的 Milvus Collection 名称，默认为 "LangChainCollection"。
        connection_args (Optional[dict[str, any]]): 连接 Milvus 的参数字典，默认为 None，使用 DEFAULT_MILVUS_CONNECTION。
        consistency_level (str): Collection 的一致性级别，默认为 "Session"。
        index_params (Optional[dict]): 索引参数字典，默认为 HNSW/AUTOINDEX，取决于服务类型。
        search_params (Optional[dict]): 搜索参数字典，默认为索引的默认参数。
        drop_old (Optional[bool]): 是否删除已存在的 Collection，默认为 False。
    connection_args 参数字典的格式如下，包含以下选项：
        address (str): Milvus 实例的实际地址，例如 "localhost:19530"。
        uri (str): Milvus 实例的 URI，例如 "http://randomwebsite:19530", "tcp:foobarsite:19530", "https://ok.s3.south.com:19530"。
        host (str): Milvus 实例的主机名，默认为 "localhost"，如果只提供端口，PyMilvus 会自动填充默认主机。
        port (str/int): Milvus 实例的端口号，默认为 19530，如果只提供主机，PyMilvus 会自动填充默认端口。
        user (str): 连接 Milvus 实例的用户名，如果提供用户名和密码，将在每个 RPC 调用中添加相关的 Header。
        password (str): 用户名对应的密码，当提供用户名时为必填项。
        secure (bool): 是否启用 TLS，默认为 False，设置为 True 时启用 TLS。
        client_key_path (str): 如果使用 TLS 双向认证，需要指定 client.key 文件的路径。
        client_pem_path (str): 如果使用 TLS 双向认证，需要指定 client.pem 文件的路径。
        ca_pem_path (str): 如果使用 TLS 双向认证，需要指定 ca.pem 文件的路径。
        server_pem_path (str): 如果使用 TLS 单向认证，需要指定 server.pem 文件的路径。
        server_name (str): 如果使用 TLS，需要指定 Common Name。
    示例:
        .. code-block:: python
        from langchain import Milvus
        from langchain.embeddings import OpenAIEmbeddings
        embedding = OpenAIEmbeddings()
        # 连接到本地 Milvus 实例
        milvus_store = Milvus(
            embedding_function = Embeddings,
            collection_name = "LangChainCollection",
            drop_old = True,
        )
    Raises:
        ValueError: 如果未安装 pymilvus Python 包。
    """

    def __init__(self, embedding_function: Embeddings, collection_name: str = 'LangChainCollection', connection_args: Optional[dict[str, Any]] = None,
                 consistency_level: str = 'Session', top_k: Optional[int] = 1, index_params: Optional[dict] = None, search_params: Optional[dict] = None,
                 drop_old: Optional[bool] = False, partition_key: Optional[str] = None,  # 分区键，用于多租户隔离
                 *, primary_field: str = 'pk',  # 主键字段名，默认为 'pk'
                 text_field: str = 'text',  # 文本字段名，默认为 'text'
                 vector_field: str = 'vector',  # 向量字段名，默认为 'vector'
                 partition_field: str = 'knowledge_id'):  # 分区字段名，默认为 'knowledge_id'
        """初始化 Milvus 向量存储."""
        try:
            from pymilvus import Collection, utility
        except ImportError:
            raise ValueError('无法导入 pymilvus Python 包。 '
                             '请使用 `pip install pymilvus` 安装。')
        # 默认的搜索参数，当没有提供搜索参数时使用
        self.default_search_params = {'IVF_FLAT': {'metric_type': 'L2',  # 距离度量类型为 L2 (欧氏距离)
                                                   'params': {'nprobe': 10  # 查询时访问的最近邻簇的数量
                                                              }}, 'IVF_SQ8': {'metric_type': 'L2', 'params': {'nprobe': 10}},
                                      'IVF_PQ': {'metric_type': 'L2', 'params': {'nprobe': 10}}, 'HNSW': {'metric_type': 'L2', 'params': {'ef': 100  # 搜索范围参数，影响搜索精度和性能
                                                                                                                                          }},
                                      'RHNSW_FLAT': {'metric_type': 'L2', 'params': {'ef': 10}}, 'RHNSW_SQ': {'metric_type': 'L2', 'params': {'ef': 10}},
                                      'RHNSW_PQ': {'metric_type': 'L2', 'params': {'ef': 10}}, 'IVF_HNSW': {'metric_type': 'L2', 'params': {'nprobe': 10, 'ef': 10}},
                                      'ANNOY': {'metric_type': 'L2', 'params': {'search_k': 10  # 搜索的最近邻数量
                                                                                }}, 'AUTOINDEX': {'metric_type': 'L2', 'params': {}}, }
        self.top_k = top_k  # 搜索结果 TopK 值
        self.embedding_func = embedding_function  # 嵌入函数
        self.collection_name = collection_name  # Collection 名称
        self.index_params = index_params  # 索引参数
        self.search_params = search_params  # 搜索参数
        self.consistency_level = consistency_level  # 一致性级别
        self.connection_args = connection_args  # 连接参数
        # 为了 Collection 兼容，主键需要是自增 ID 且为 int 类型
        self._primary_field = primary_field
        # 为了兼容性，文本字段需要命名为 "text"
        self._text_field = text_field
        # 为了兼容性，向量字段需要命名为 "vector"
        self._vector_field = vector_field
        # 分区字段名，用于多租户隔离
        self._partition_field = partition_field
        self.partition_key = partition_key  # 分区键值
        self.fields: list[str] = []  # 字段名列表
        # 创建到 Milvus 服务器的连接
        if connection_args is None:
            connection_args = DEFAULT_MILVUS_CONNECTION  # 如果未提供连接参数，则使用默认连接参数
        # if 'timeout' not in connection_args:
        # connection_args['timeout'] = 30
        self.alias = self._create_connection_alias(connection_args)  # 创建连接别名
        self.col: Optional[Collection] = None  # Milvus Collection 对象，初始为 None
        # 获取已存在的 Collection，如果存在
        try:
            if utility.has_collection(self.collection_name, using=self.alias):  # 检查 Collection 是否已存在
                self.col = Collection(self.collection_name, using=self.alias, )  # 加载已存在的 Collection
        except Exception as e:
            logger.error(f'milvus operating error={str(e)}')  # 记录 Milvus 操作错误日志
            self.close_connection(self.alias)  # 关闭连接
            raise e  # 抛出异常
        # 如果需要删除旧的 Collection，则删除它
        if drop_old and isinstance(self.col, Collection):  # 如果 drop_old 为 True 且 Collection 对象存在
            self.col.drop()  # 删除 Collection
            self.col = None  # 将 Collection 对象设置为 None
        # 初始化向量存储
        self._init()

    def similarity_search(self, query: str, k: int = 1, param: Optional[dict] = None, expr: Optional[str] = None, timeout: Optional[int] = None, **kwargs: Any, ) -> List[Document]:
        """
        根据查询字符串执行相似性搜索。
        Args:
            query (str): 要搜索的文本。
            k (int, optional): 返回结果的数量，默认为 1。
            param (dict, optional): 索引类型的搜索参数，默认为 None，使用默认搜索参数。
            expr (str, optional): 过滤表达式，默认为 None，不进行过滤。
            timeout (int, optional): 超时时间，单位为秒，默认为 None，不设置超时。
            kwargs: Collection.search() 的其他关键字参数。
        Returns:
            List[Document]: 搜索结果文档列表。
        """
        if k == 0:
            # pm need to control，控制返回结果数量
            return []
        if self.col is None:
            logger.debug('没有可搜索的现有 Collection。')  # 记录 debug 日志，提示没有 Collection 可供搜索
            return []
        res = self.similarity_search_with_score(query=query,  # 调用 similarity_search_with_score 方法执行相似性搜索，并获取文档和分数
            k=self.top_k, param=param, expr=expr, timeout=timeout, **kwargs)
        return [doc for doc, _ in res]  # 从结果列表中提取文档，忽略分数

    def similarity_search_by_vector(self, embedding: List[float], k: int = 1, param: Optional[dict] = None, expr: Optional[str] = None, timeout: Optional[int] = None,
                                    **kwargs: Any, ) -> List[Document]:
        """
        根据向量执行相似性搜索。
        Args:
            embedding (List[float]): 要搜索的嵌入向量。
            k (int, optional): 返回结果的数量，默认为 1。
            param (dict, optional): 索引类型的搜索参数，默认为 None，使用默认搜索参数。
            expr (str, optional): 过滤表达式，默认为 None，不进行过滤。
            timeout (int, optional): 超时时间，单位为秒，默认为 None，不设置超时。
            kwargs: Collection.search() 的其他关键字参数。
        Returns:
            List[Document]: 搜索结果文档列表。
        """
        if k == 0:
            # pm need to control，控制返回结果数量
            return []
        if self.col is None:
            logger.debug('没有可搜索的现有 Collection。')  # 记录 debug 日志，提示没有 Collection 可供搜索
            return []
        res = self.similarity_search_with_score_by_vector(embedding=embedding,  # 调用 similarity_search_with_score_by_vector 方法执行相似性搜索，并获取文档和分数
            k=k, param=param, expr=expr, timeout=timeout, **kwargs)
        return [doc for doc, _ in res]  # 从结果列表中提取文档，忽略分数

    def similarity_search_with_score(self, query: str, k: int = 1, param: Optional[dict] = None, expr: Optional[str] = None, timeout: Optional[int] = None, **kwargs: Any, ) -> \
            List[Tuple[Document, float]]:
        """
        根据查询字符串执行相似性搜索，并返回带分数的文档结果列表。
        有关搜索参数的更多信息，请查看 pymilvus 文档：
        https://milvus.io/api-reference/pymilvus/v2.2.6/Collection/search().md
        Args:
            query (str): 要搜索的文本。
            k (int, optional): 返回结果的数量，默认为 1。
            param (dict): 指定索引类型的搜索参数，默认为 None，使用默认搜索参数。
            expr (str, optional): 过滤表达式，默认为 None，不进行过滤。
            timeout (int, optional): 超时时间，单位为秒，默认为 None，不设置超时。
            kwargs: Collection.search() 的其他关键字参数。
        Returns:
            List[Tuple[Document, float]]: 文档结果列表，每个元素为 (Document, score) 元组。
        """
        if k == 0:
            # pm need to control，控制返回结果数量
            return []
        if self.col is None:
            logger.debug('没有可搜索的现有 Collection。')  # 记录 debug 日志，提示没有 Collection 可供搜索
            return []
        # 嵌入查询文本
        embedding = self.embedding_func.embed_query(query)  # 使用 embedding_function 将查询文本转换为向量
        res = self.similarity_search_with_score_by_vector(embedding=embedding,  # 调用 similarity_search_with_score_by_vector 方法执行相似性搜索，并获取文档和分数
            k=k, param=param, expr=expr, timeout=timeout, **kwargs)
        return res  # 返回带分数的文档结果列表

    def similarity_search_with_score_by_vector(self, embedding: List[float], k: int = 1, param: Optional[dict] = None, expr: Optional[str] = None, timeout: Optional[int] = None,
                                               **kwargs: Any, ) -> List[Tuple[Document, float]]:
        """
        根据向量执行相似性搜索，并返回带分数的文档结果列表。
        有关搜索参数的更多信息，请查看 pymilvus 文档：
        https://milvus.io/api-reference/pymilvus/v2.2.6/Collection/search().md
        Args:
            embedding (List[float]): 要搜索的嵌入向量。
            k (int, optional): 返回结果的数量，默认为 1。
            param (dict): 指定索引类型的搜索参数，默认为 None，使用默认搜索参数。
            expr (str, optional): 过滤表达式，默认为 None，不进行过滤。
            timeout (int, optional): 超时时间，单位为秒，默认为 None，不设置超时。
            kwargs: Collection.search() 的其他关键字参数。
        Returns:
            List[Tuple[Document, float]]: 文档结果列表，每个元素为 (Document, score) 元组。
        """
        if k == 0:
            # pm need to control，控制返回结果数量
            return []
        if self.col is None:
            logger.debug('没有可搜索的现有 Collection。')  # 记录 debug 日志，提示没有 Collection 可供搜索
            return []
        if param is None:
            param = self.search_params  # 如果未提供搜索参数，则使用默认搜索参数
        # 确定结果元数据字段
        output_fields = self.fields[:]  # 复制字段列表
        output_fields.remove(self._vector_field)  # 移除向量字段，因为不需要返回向量字段
        # partition for multi-tenancy，多租户分区查询
        if self.partition_key:  # 如果设置了分区键
            # add parttion，添加分区过滤条件
            if expr:
                expr = f"{expr} and {self._partition_field}==\"{self.partition_key}\""  # 如果已存在过滤表达式，则追加分区过滤条件
            else:
                expr = f"{self._partition_field}==\"{self.partition_key}\""  # 否则，直接设置分区过滤条件
        if "chunk_id" not in output_fields:
            output_fields.append("chunk_id")  # 如果 output_fields 中不包含 "chunk_id" 字段，则添加
        if "parents" not in output_fields:
            output_fields.append("parents")  # 如果 output_fields 中不包含 "parents" 字段，则添加
        if "chunk_type" not in output_fields:
            output_fields.append("chunk_type")  # 如果 output_fields 中不包含 "chunk_type" 字段，则添加
        # 执行搜索
        res = self.col.search(data=[embedding],  # 查询向量
            anns_field=self._vector_field,  # 向量字段名
            param=param,  # 搜索参数
            limit=k,  # 返回结果数量
            expr=expr,  # 过滤表达式
            output_fields=output_fields,  # 返回的字段
            timeout=timeout,  # 超时时间
            **kwargs,  # 其他关键字参数
        )
        # 组织结果
        ret = []
        for result in res[0]:  # 遍历搜索结果
            meta = {x: result.entity.get(x) for x in output_fields}  # 从结果实体中提取元数据
            doc = Document(page_content=meta.pop(self._text_field), metadata=meta)  # 创建 Document 对象，page_content 为文本字段，metadata 为其他元数据字段
            pair = (doc, result.score)  # 创建 (Document, score) 元组
            ret.append(pair)  # 添加到结果列表
        chs = []
        for (doc, score) in ret:  # 遍历结果列表
            if isinstance(doc.metadata['bbox'], str):
                doc.metadata['bbox'] = json.loads(doc.metadata['bbox'])  # 如果 bbox 字段是字符串，则反序列化为 JSON 对象
            if "chunk_id" in doc.metadata and doc.metadata["chunk_type"] == "title":  # 如果是标题类型的分块
                ch = self._search_chidren(doc=doc, output_fields=output_fields, timeout=timeout, **kwargs)  # 搜索子分块
                # document merge，文档合并
                for c in ch:  # 遍历子分块
                    if isinstance(c.metadata['parents'], str):
                        c.metadata["parents"] = json.loads(c.metadata['parents'])  # 反序列化 parents 字段
                    if isinstance(c.metadata['bbox'], str):
                        c.metadata['bbox'] = json.loads(c.metadata['bbox'])  # 反序列化 bbox 字段
                ch = [s for s in ch if doc.metadata['chunk_id'] in s.metadata['parents']]  # 过滤子分块，只保留 parents 包含当前分块 chunk_id 的子分块
                sorted(ch, key=lambda x: x.metadata['chunk_index'])  # 对子分块按 chunk_index 排序
                for c in ch:  # 遍历排序后的子分块
                    lines = c.page_content.splitlines()  # 按行分割子分块内容
                    # 删除第一行，标题分块的第一行通常是标题本身，不需要重复添加到内容中
                    lines = lines[1:]
                    # 将剩余的行重新拼接成一个字符串
                    page_content = "\n".join(lines)
                    doc.metadata['bbox']['chunk_bboxes'].extend(c.metadata['bbox']['chunk_bboxes'])  # 合并 bbox 信息
                    if c.metadata['chunk_type'] == 'title':
                        doc.page_content += f"\n\n{page_content}"  # 如果子分块也是标题类型，则添加双换行符
                    else:
                        doc.page_content += f"\n{page_content}"  # 否则，添加单换行符
        for (doc, score) in ret:  # 再次遍历结果列表，将 bbox 字段序列化为 JSON 字符串
            if not isinstance(doc.metadata['bbox'], str):
                doc.metadata['bbox'] = json.dumps(doc.metadata['bbox'])  # 如果 bbox 字段不是字符串，则序列化为 JSON 字符串
        return ret  # 返回带分数的文档结果列表

    def _search_chidren(self, doc: Document, output_fields, timeout, **kwargs):
        """搜索子分块"""
        ret = []
        if "chunk_type" in doc.metadata and doc.metadata["chunk_type"] == "title":  # 如果当前文档是标题类型的分块
            expr = f"parents like '%{doc.metadata['chunk_id']}%'"  # 构建过滤表达式，搜索 parents 字段包含当前分块 chunk_id 的文档
            childrens = self.col.query(expr=expr,  # 过滤表达式
                output_fields=output_fields,  # 返回字段
                timeout=timeout,  # 超时时间
                **kwargs,  # 其他关键字参数
            )
            for result in childrens:  # 遍历子分块搜索结果
                meta = {x: result.get(x) for x in output_fields}  # 提取子分块元数据
                doc = Document(page_content=meta.pop(self._text_field), metadata=meta)  # 创建子分块 Document 对象
                ret.append(doc)  # 添加到结果列表
        return ret  # 返回子分块文档列表

    def _rerank_chunk(self, docs):
        """重新排序分块，目前为空实现"""
        pass

    def max_marginal_relevance_search(self, query: str, k: int = 4, fetch_k: int = 20, lambda_mult: float = 0.5, param: Optional[dict] = None, expr: Optional[str] = None,
                                      timeout: Optional[int] = None, **kwargs: Any, ) -> List[Document]:
        """
        执行 MMR (最大边际相关性) 搜索，并返回重排序后的文档结果列表。
        Args:
            query (str): 要搜索的文本。
            k (int, optional): 返回结果的数量，默认为 4。
            fetch_k (int, optional): 用于 MMR 重排序的初始搜索结果数量，默认为 20。
            lambda_mult (float, optional): 介于 0 和 1 之间的数字，用于确定结果多样性的程度，
                0 表示最大多样性，1 表示最小多样性，默认为 0.5。
            param (dict, optional): 索引类型的搜索参数，默认为 None，使用默认搜索参数。
            expr (str, optional): 过滤表达式，默认为 None，不进行过滤。
            timeout (int, optional): 超时时间，单位为秒，默认为 None，不设置超时。
            kwargs: Collection.search() 的其他关键字参数。
        Returns:
            List[Document]: MMR 重排序后的文档结果列表。
        """
        if k == 0:
            # pm need to control，控制返回结果数量
            return []
        if self.col is None:
            logger.debug('没有可搜索的现有 Collection。')  # 记录 debug 日志，提示没有 Collection 可供搜索
            return []
        embedding = self.embedding_func.embed_query(query)  # 嵌入查询文本
        return self.max_marginal_relevance_search_by_vector(embedding=embedding,  # 查询向量
            k=k,  # 返回结果数量
            fetch_k=fetch_k,  # 初始搜索结果数量
            lambda_mult=lambda_mult,  # 多样性参数
            param=param,  # 搜索参数
            expr=expr,  # 过滤表达式
            timeout=timeout,  # 超时时间
            **kwargs,  # 其他关键字参数
        )

    def max_marginal_relevance_search_by_vector(self, embedding: list[float], k: int = 4, fetch_k: int = 20, lambda_mult: float = 0.5, param: Optional[dict] = None,
                                                expr: Optional[str] = None, timeout: Optional[int] = None, **kwargs: Any, ) -> List[Document]:
        """
        根据向量执行 MMR (最大边际相关性) 搜索，并返回重排序后的文档结果列表。
        Args:
            embedding (str): 要搜索的嵌入向量。
            k (int, optional): 返回结果的数量，默认为 4。
            fetch_k (int, optional): 用于 MMR 重排序的初始搜索结果数量，默认为 20。
            lambda_mult (float, optional): 介于 0 和 1 之间的数字，用于确定结果多样性的程度，
                0 表示最大多样性，1 表示最小多样性，默认为 0.5。
            param (dict, optional): 索引类型的搜索参数，默认为 None，使用默认搜索参数。
            expr (str, optional): 过滤表达式，默认为 None，不进行过滤。
            timeout (int, optional): 超时时间，单位为秒，默认为 None，不设置超时。
            kwargs: Collection.search() 的其他关键字参数。
        Returns:
            List[Document]: MMR 重排序后的文档结果列表。
        """
        if k == 0:
            # pm need to control，控制返回结果数量
            return []
        if self.col is None:
            logger.debug('没有可搜索的现有 Collection。')  # 记录 debug 日志，提示没有 Collection 可供搜索
            return []
        if param is None:
            param = self.search_params  # 如果未提供搜索参数，则使用默认搜索参数
        # 确定结果元数据字段
        output_fields = self.fields[:]  # 复制字段列表
        output_fields.remove(self._vector_field)  # 移除向量字段
        # 执行搜索，获取 fetch_k 个初始结果
        res = self.col.search(data=[embedding],  # 查询向量
            anns_field=self._vector_field,  # 向量字段名
            param=param,  # 搜索参数
            limit=fetch_k,  # 返回结果数量，用于 MMR 重排序的初始结果数量
            expr=expr,  # 过滤表达式
            output_fields=output_fields,  # 返回字段
            timeout=timeout,  # 超时时间
            **kwargs,  # 其他关键字参数
        )
        # 组织结果
        ids = []
        documents = []
        scores = []
        for result in res[0]:  # 遍历初始搜索结果
            meta = {x: result.entity.get(x) for x in output_fields}  # 提取元数据
            doc = Document(page_content=meta.pop(self._text_field), metadata=meta)  # 创建 Document 对象
            documents.append(doc)  # 添加到文档列表
            scores.append(result.score)  # 添加到分数列表
            ids.append(result.id)  # 添加到 ID 列表
        vectors = self.col.query(expr=f'{self._primary_field} in {ids}',  # 构建过滤表达式，查询初始搜索结果的向量数据
            output_fields=[self._primary_field, self._vector_field],  # 返回主键和向量字段
            timeout=timeout,  # 超时时间
        )
        # Reorganize the results from query to match search order，重新组织查询结果，使其与搜索顺序一致
        vectors = {x[self._primary_field]: x[self._vector_field] for x in vectors}  # 创建主键到向量的字典映射
        ordered_result_embeddings = [vectors[x] for x in ids]  # 获取与搜索结果顺序一致的向量列表
        # Get the new order of results，使用 MMR 算法对结果进行重排序
        new_ordering = maximal_marginal_relevance(np.array(embedding),  # 查询向量
            ordered_result_embeddings,  # 初始搜索结果的向量列表
            k=k,  # 期望返回的最终结果数量
            lambda_mult=lambda_mult)  # 多样性参数
        # Reorder the values and return，根据 MMR 重排序后的索引列表，重新排序文档结果并返回
        ret = []
        for x in new_ordering:  # 遍历 MMR 重排序后的索引列表
            # Function can return -1 index，MMR 算法可能返回 -1 索引，表示没有选择任何文档
            if x == -1:
                break
            else:
                ret.append(documents[x])  # 添加重排序后的文档到结果列表
        return ret  # 返回 MMR 重排序后的文档结果列表

    @classmethod
    def from_texts(cls, texts: List[str], embedding: Embeddings, metadatas: Optional[List[dict]] = None, collection_name: str = 'LangChainCollection',
                   connection_args: dict[str, Any] = DEFAULT_MILVUS_CONNECTION, consistency_level: str = 'Session', index_params: Optional[dict] = None,
                   search_params: Optional[dict] = None, top_k: int = 1, drop_old: bool = False, no_embedding: bool = False, **kwargs: Any, ) -> Milvus:
        """
        创建 Milvus Collection，使用 HNSW 索引进行索引，并插入数据。
        Args:
            texts (List[str]): 文本数据列表。
            embedding (Embeddings): Embedding 函数 (Langchain 的 Embeddings 对象)。
            metadatas (Optional[List[dict]]): 每个文本的元数据列表，如果存在，默认为 None。
            collection_name (str, optional): 要使用的 Collection 名称，默认为 "LangChainCollection"。
            connection_args (dict[str, Any], optional): 连接参数字典，默认为 DEFAULT_MILVUS_CONNECTION。
            consistency_level (str, optional): 使用的一致性级别，默认为 "Session"。
            index_params (Optional[dict], optional): 使用的索引参数字典，默认为 None。
            search_params (Optional[dict], optional): 使用的搜索参数字典，默认为 None。
            top_k (int, optional): 搜索结果 TopK 值，默认为 1。
            drop_old (Optional[bool], optional): 如果存在同名 Collection，是否删除，默认为 False。
            no_embedding (bool, optional): 是否跳过嵌入向量生成，默认为 False，如果为 True，则需要 texts 参数为向量列表。
            kwargs: 传递给 Milvus 构造函数的其他关键字参数。
        Returns:
            Milvus: Milvus 向量存储对象。
        """
        vector_db = cls(embedding_function=embedding,  # 嵌入函数
            collection_name=collection_name,  # Collection 名称
            connection_args=connection_args,  # 连接参数
            consistency_level=consistency_level,  # 一致性级别
            index_params=index_params,  # 索引参数
            search_params=search_params,  # 搜索参数
            top_k=top_k,  # 搜索结果 TopK 值
            drop_old=drop_old,  # 是否删除已存在的 Collection
            **kwargs,  # 其他关键字参数
        )
        vector_db.add_texts(texts=texts, metadatas=metadatas, no_embedding=no_embedding)  # 添加文本数据到 Milvus
        return vector_db  # 返回 Milvus 向量存储对象

    @staticmethod
    def _relevance_score_fn(distance: float) -> float:
        """将距离归一化为 [0, 1] 范围内的分数."""
        # Todo: normalize the es score on a scale [0, 1]，待办事项：将 Elasticsearch 分数归一化到 [0, 1] 范围
        return 1 - distance  # 返回 1 减去距离，距离越小，分数越高，表示相关性越高

    def _select_relevance_score_fn(self) -> Callable[[float], float]:
        """选择相关性评分函数，这里直接返回 _relevance_score_fn 函数"""
        return self._relevance_score_fn  # 返回 _relevance_score_fn 函数

    def query(self, expr: str, timeout: Optional[int] = None, **kwargs: Any) -> List[Document]:
        """根据 Milvus 表达式查询文档"""
        output_fields = self.fields[:]  # 复制字段列表
        output_fields.remove(self._vector_field)  # 移除向量字段，因为查询不需要返回向量字段
        res = self.col.query(expr=expr,  # Milvus 表达式
            output_fields=output_fields,  # 返回字段
            timeout=timeout,  # 超时时间
            limit=1,  # 返回结果数量限制为 1
            **kwargs,  # 其他关键字参数
        )
        # 组织结果
        ret = []
        for result in res:  # 遍历查询结果
            meta = {x: result.get(x) for x in output_fields}  # 提取元数据
            doc = Document(page_content=meta.pop(self._text_field), metadata=meta)  # 创建 Document 对象
            ret.append(doc)  # 添加到结果列表
        return ret  # 返回文档结果列表
