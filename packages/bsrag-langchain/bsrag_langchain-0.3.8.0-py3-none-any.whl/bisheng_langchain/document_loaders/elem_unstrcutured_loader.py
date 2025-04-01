# flake8: noqa  # 禁用 flake8 代码检查
"""使用语义分割器加载 PDF."""
import base64  # 导入 base64 模块，用于 base64 编码和解码
import logging  # 导入 logging 模块，用于日志记录
import os  # 导入 os 模块，用于操作系统相关的功能
from typing import List  # 导入 List 类型注解
import requests  # 导入 requests 库，用于发送 HTTP 请求
from langchain.docstore.document import Document  # 导入 Langchain 的 Document 类，用于表示文档
from langchain.document_loaders.pdf import BasePDFLoader  # 导入 Langchain 的 BasePDFLoader 类，作为 PDF 加载器的基类
logger = logging.getLogger(__name__)  # 获取名为 __name__ 的 logger 实例

def merge_partitions(partitions):
    """合并分区数据.
    将非结构化文档解析 API 返回的分区数据合并成一个文本内容和一个元数据字典。
    Args:
        partitions: 分区数据列表，每个元素是一个字典，包含 'type' (分区类型), 'text' (分区文本), 'metadata' (元数据)。
    Returns:
        Tuple[str, Dict]: 合并后的文本内容和元数据字典。
    """
    text_elem_sep = '\n'  # 文本元素分隔符
    doc_content = []  # 初始化文档内容列表
    is_first_elem = True  # 标记是否为第一个元素
    last_label = ''  # 上一个分区的类型标签
    prev_length = 0  # 之前内容的长度
    metadata = dict(bboxes=[], pages=[], indexes=[], types=[], levels=[])  # 初始化元数据字典，用于存储 bbox, 页码, 索引, 类型, 层级信息
    for part in partitions:  # 遍历分区数据列表
        label, text = part['type'], part['text']  # 获取分区类型和文本
        extra_data = part['metadata']['extra_data']  # 获取额外元数据
        offset = 0  # 初始化偏移量
        if is_first_elem:  # 如果是第一个元素
            if label == 'Title':  # 如果是标题类型
                f_text = text + '\n'  # 标题后添加换行符
            else:  # 如果不是标题类型
                f_text = text  # 直接使用文本
            doc_content.append(f_text)  # 添加到文档内容列表
            is_first_elem = False  # 设置为非第一个元素
        else:  # 如果不是第一个元素
            if last_label == 'Title' and label == 'Title':  # 如果上一个和当前都是标题类型
                doc_content.append('\n' + text)  # 添加单换行符和文本
                offset = 1  # 设置偏移量为 1
            elif label == 'Title':  # 如果当前是标题类型
                doc_content.append('\n\n' + text)  # 添加双换行符和文本
                offset = 2  # 设置偏移量为 2
            elif label == 'Table':  # 如果当前是表格类型
                doc_content.append('\n\n' + text)  # 添加双换行符和文本
                offset = 2  # 设置偏移量为 2
            else:  # 如果是其他类型
                if last_label == 'Table':  # 如果上一个是表格类型
                    doc_content.append(text_elem_sep * 2 + text)  # 添加双倍元素分隔符和文本
                    offset = 2  # 设置偏移量为 2
                else:  # 如果上一个不是表格类型
                    doc_content.append(text_elem_sep + text)  # 添加元素分隔符和文本
                    offset = 1  # 设置偏移量为 1
        last_label = label  # 更新上一个分区的类型标签
        metadata['bboxes'].extend(list(map(lambda x: list(map(int, x)), extra_data['bboxes'])))  # 提取并添加 bbox 信息
        metadata['pages'].extend(extra_data['pages'])  # 添加页码信息
        metadata['types'].extend(extra_data['types'])  # 添加类型信息
        metadata['levels'].extend(extra_data['levels'])  # 添加层级信息
        indexes = extra_data['indexes']  # 获取索引信息
        up_indexes = [[s + prev_length + offset, e + prev_length + offset] for (s, e) in indexes]  # 更新索引信息，考虑之前内容的长度和偏移量
        metadata['indexes'].extend(up_indexes)  # 添加更新后的索引信息
        prev_length += len(doc_content[-1])  # 更新之前内容的长度
    content = ''.join(doc_content)  # 合并文档内容列表为字符串
    return content, metadata  # 返回合并后的内容和元数据

class ElemUnstructuredLoader(BasePDFLoader):
    """ElemUnstructuredLoader 类，继承自 BasePDFLoader，使用 unstructured API 加载 PDF 文档并进行语义分割。
    使用 pypdf 加载 PDF，并在字符级别进行分块。 虚拟版本
    加载器还在元数据中存储页码。
    """

    def __init__(self, file_name: str, file_path: str, unstructured_api_key: str = None, unstructured_api_url: str = None, start: int = 0, n: int = None, verbose: bool = False,
                 kwargs: dict = {}) -> None:
        """使用文件路径初始化 ElemUnstructuredLoader 对象.
        Args:
            file_name (str): 文件名。
            file_path (str): 文件路径。
            unstructured_api_key (str, optional): unstructured API 密钥，默认为 None。
            unstructured_api_url (str, optional): unstructured API URL，默认为 None。
            start (int): 分区起始页码，默认为 0。
            n (int): 分区页数，默认为 None，表示所有页。
            verbose (bool): 是否启用详细日志输出，默认为 False。
            kwargs (dict): 传递给 unstructured API 的额外参数字典，默认为空字典。
        """
        self.unstructured_api_url = unstructured_api_url  # 设置 unstructured API URL
        self.unstructured_api_key = unstructured_api_key  # 设置 unstructured API 密钥
        self.headers = {'Content-Type': 'application/json'}  # 设置 HTTP 请求头，指定 Content-Type 为 application/json
        self.file_name = file_name  # 设置文件名
        self.start = start  # 设置分区起始页码
        self.n = n  # 设置分区页数
        self.extra_kwargs = kwargs  # 设置额外参数
        self.partitions = None  # 初始化分区数据为 None
        super().__init__(file_path)  # 调用父类 BasePDFLoader 的初始化方法

    def load(self) -> List[Document]:
        """将给定路径加载为 Document 页面列表.
        调用 unstructured API 对 PDF 文件进行分区解析，并将解析结果转换为 Langchain Document 对象列表。
        Returns:
            List[Document]: 包含解析后的文档内容的 Document 对象列表，通常只包含一个 Document 对象。
        """
        b64_data = base64.b64encode(open(self.file_path, 'rb').read()).decode()  # 将文件内容 base64 编码
        parameters = {'start': self.start, 'n': self.n}  # 设置 API 请求参数，包含起始页码和页数
        parameters.update(self.extra_kwargs)  # 合并额外参数
        payload = dict(filename=os.path.basename(self.file_name), b64_data=[b64_data], mode='partition', parameters=parameters)  # 构建 API 请求 payload，包含文件名, base64 编码数据, 解析模式, 参数
        resp = requests.post(self.unstructured_api_url, headers=self.headers, json=payload)  # 发送 POST 请求到 unstructured API
        if resp.status_code != 200:  # 如果 API 响应状态码不是 200，表示请求失败
            raise Exception(f'文件分区 {os.path.basename(self.file_name)} 失败 resp={resp.text}')  # 抛出异常，提示文件分区失败
        resp = resp.json()  # 解析 JSON 响应
        if 200 != resp.get('status_code'):  # 如果 API 返回的状态码不是 200，表示解析服务内部错误
            logger.info(f'文件分区 {os.path.basename(self.file_name)} 错误 resp={resp}')  # 记录错误日志
            raise Exception(f'文件分区错误 {os.path.basename(self.file_name)} 错误 resp={resp}')  # 抛出异常，提示文件分区错误
        partitions = resp['partitions']  # 获取分区数据
        if partitions:  # 如果分区数据不为空
            logger.info(f'content_from_partitions')  # 记录日志，提示内容来自 partitions
            self.partitions = partitions  # 存储分区数据
            content, metadata = merge_partitions(partitions)  # 合并分区数据，获取文本内容和元数据
        elif resp.get('text'):  # 如果分区数据为空，但响应中包含 text 字段
            logger.info(f'content_from_text')  # 记录日志，提示内容来自 text 字段
            content = resp['text']  # 使用 text 字段内容
            metadata = {"bboxes": [], "pages": [], "indexes": [], "types": [], "levels": []}  # 初始化元数据为空字典
        else:  # 如果分区数据和 text 字段都为空
            logger.warning(f'content_is_empty resp={resp}')  # 记录警告日志，提示内容为空
            content = ''  # 设置内容为空字符串
            metadata = {}  # 设置元数据为空字典
        logger.info(f'unstruct_return code={resp.get("status_code")}')  # 记录 API 返回的状态码
        if resp.get('b64_pdf'):  # 如果响应中包含 b64_pdf 字段，表示返回了转换后的 PDF 文件 base64 编码
            with open(self.file_path, 'wb') as f:  # 将 base64 编码的 PDF 数据解码并保存到文件
                f.write(base64.b64decode(resp['b64_pdf']))  # base64 解码并写入文件
        metadata['source'] = self.file_name  # 设置元数据中的 source 字段为文件名
        doc = Document(page_content=content, metadata=metadata)  # 创建 Langchain Document 对象
        return [doc]  # 返回包含 Document 对象的列表

class ElemUnstructuredLoaderV0(BasePDFLoader):
    """ElemUnstructuredLoaderV0 类，继承自 BasePDFLoader，使用 unstructured API 加载各种文件类型并提取文本。
    根据文件格式自动选择合适的解析器，并支持 OCR。
    """

    def __init__(self, file_name: str, file_path: str, unstructured_api_key: str = None, unstructured_api_url: str = None, start: int = 0, n: int = None, verbose: bool = False,
                 kwargs: dict = {}) -> None:
        """使用文件路径初始化 ElemUnstructuredLoaderV0 对象.
        Args:
            file_name (str): 文件名。
            file_path (str): 文件路径。
            unstructured_api_key (str, optional): unstructured API 密钥，默认为 None。
            unstructured_api_url (str, optional): unstructured API URL，默认为 None。
            start (int): 分区起始页码，默认为 0 (text 模式下无效)。
            n (int): 分区页数，默认为 None (text 模式下无效)。
            verbose (bool): 是否启用详细日志输出，默认为 False。
            kwargs (dict): 传递给 unstructured API 的额外参数字典，默认为空字典。
        """
        self.unstructured_api_url = unstructured_api_url  # 设置 unstructured API URL
        self.unstructured_api_key = unstructured_api_key  # 设置 unstructured API 密钥
        self.start = start  # 设置分区起始页码 (text 模式下无效)
        self.n = n  # 设置分区页数 (text 模式下无效)
        self.headers = {'Content-Type': 'application/json'}  # 设置 HTTP 请求头
        self.file_name = file_name  # 设置文件名
        self.extra_kwargs = kwargs  # 设置额外参数
        super().__init__(file_path)  # 调用父类 BasePDFLoader 的初始化方法

    def load(self) -> List[Document]:
        """加载文件并返回 Document 列表.
        调用 get_text_metadata 方法获取文件内容和元数据，并创建 Langchain Document 对象。
        Returns:
            List[Document]: 包含加载的文件内容的 Document 对象列表，通常只包含一个 Document 对象。
        """
        page_content, metadata = self.get_text_metadata()  # 获取文件内容和元数据
        doc = Document(page_content=page_content, metadata=metadata)  # 创建 Langchain Document 对象
        return [doc]  # 返回包含 Document 对象的列表

    def get_text_metadata(self):
        """获取文件文本内容和元数据.
        调用 unstructured API 的 text 模式解析文件，如果解析失败，则尝试转换为 PDF 后再进行 partition 模式解析。
        Returns:
            Tuple[str, Dict]: 文件文本内容和元数据字典。
        Raises:
            Exception: 如果文件解析失败，抛出异常。
        """
        b64_data = base64.b64encode(open(self.file_path, 'rb').read()).decode()  # 将文件内容 base64 编码
        payload = dict(filename=os.path.basename(self.file_name), b64_data=[b64_data], mode='text')  # 构建 API 请求 payload，指定 text 模式
        payload.update({'start': self.start, 'n': self.n})  # 合并 start 和 n 参数 (text 模式下无效)
        payload.update(self.extra_kwargs)  # 合并额外参数
        resp = requests.post(self.unstructured_api_url, headers=self.headers, json=payload)  # 发送 POST 请求到 unstructured API，使用 text 模式
        # 说明文件解析成功
        if resp.status_code == 200 and resp.json().get('status_code') == 200:  # 如果 API 响应状态码为 200 且返回状态码也为 200
            res = resp.json()  # 解析 JSON 响应
            return res['text'], {'source': self.file_name}  # 返回 text 字段内容和包含 source 字段的元数据字典
        # 说明文件解析失败，pdf文件直接返回报错
        if self.file_name.endswith('.pdf'):  # 如果文件名以 .pdf 结尾，表示原始文件是 PDF 文件
            raise Exception(f'文件文本提取 {os.path.basename(self.file_name)} 失败 resp={resp.text}')  # 抛出异常，提示 PDF 文件文本提取失败
        # 非 pdf 文件，先将文件转为 pdf 格式，然后再执行 partition 模式解析文档
        # 把文件转为 pdf
        resp = requests.post(self.unstructured_api_url, headers=self.headers,
            json={'filename': os.path.basename(self.file_name), 'b64_data': [b64_data], 'mode': 'topdf', })  # 发送 POST 请求到 unstructured API，使用 topdf 模式将文件转换为 PDF
        if resp.status_code != 200 or resp.json().get('status_code') != 200:  # 如果 API 响应状态码不是 200 或返回状态码不是 200，表示 PDF 转换失败
            raise Exception(f'文件转换为 PDF {os.path.basename(self.file_name)} 失败 resp={resp.text}')  # 抛出异常，提示文件转换为 PDF 失败
        # 解析 pdf 文件
        payload['mode'] = 'partition'  # 设置 payload 的 mode 为 partition，使用分区模式解析 PDF
        payload['b64_data'] = [resp.json()['b64_pdf']]  # 使用转换后的 PDF 文件的 base64 编码数据
        payload['filename'] = os.path.basename(self.file_name) + '.pdf'  # 更新 payload 的 filename 为 PDF 文件名
        resp = requests.post(self.unstructured_api_url, headers=self.headers, json=payload)  # 再次发送 POST 请求到 unstructured API，使用 partition 模式解析 PDF
        if resp.status_code != 200 or resp.json().get('status_code') != 200:  # 如果 API 响应状态码不是 200 或返回状态码不是 200，表示 PDF 分区解析失败
            raise Exception(f'文件分区 {os.path.basename(self.file_name)} 失败 resp={resp.text}')  # 抛出异常，提示 PDF 文件分区解析失败
        res = resp.json()  # 解析 JSON 响应
        partitions = res['partitions']  # 获取分区数据
        if not partitions:  # 如果分区数据为空
            raise Exception(f'文件分区结果为空 {os.path.basename(self.file_name)} resp={resp.text}')  # 抛出异常，提示文件分区结果为空
        # 拼接结果为文本
        content, _ = merge_partitions(partitions)  # 合并分区数据，获取文本内容 (忽略元数据)
        return content, {'source': self.file_name}  # 返回合并后的文本内容和包含 source 字段的元数据字典
