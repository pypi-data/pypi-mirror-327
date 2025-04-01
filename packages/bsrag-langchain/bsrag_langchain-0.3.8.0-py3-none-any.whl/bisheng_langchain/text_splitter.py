# flake8: noqa  # 禁用 flake8 代码检查
from __future__ import annotations  # 启用类型注解的延迟评估
import bisect  # 导入 bisect 模块，用于二分查找
import copy  # 导入 copy 模块，用于对象复制
import logging  # 导入 logging 模块，用于日志记录
import re  # 导入 re 模块，用于正则表达式操作
from abc import ABC, abstractmethod  # 导入 ABC 和 abstractmethod，用于创建抽象基类和抽象方法
from collections import Counter  # 导入 Counter 类，用于计数
from dataclasses import dataclass  # 导入 dataclass 装饰器，用于创建数据类
from enum import Enum  # 导入 Enum 类，用于创建枚举类型
from typing import (AbstractSet, Any, Callable, Collection, Dict, Iterable, List, Literal, Optional, Sequence, Tuple, Type, TypedDict, TypeVar, Union, cast)  # 导入 typing 模块的各种类型注解
from langchain.docstore.document import Document  # 导入 Langchain 的 Document 类，用于表示文档
from langchain.schema import BaseDocumentTransformer  # 导入 Langchain 的 BaseDocumentTransformer 类，用于文档转换
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 导入 Langchain 的 RecursiveCharacterTextSplitter 类，用于递归字符文本分割
import uuid  # 导入 uuid 模块，用于生成 UUID
logger = logging.getLogger(__name__)  # 获取名为 __name__ 的 logger 实例

def _split_text_with_regex(text: str, separator: str, keep_separator: bool, separator_rule: str) -> List[str]:
    """使用正则表达式分割文本.
    根据提供的分隔符和规则，使用正则表达式分割文本。
    Args:
        text (str): 要分割的文本。
        separator (str): 分隔符正则表达式。
        keep_separator (bool): 是否在分割后的文本块中保留分隔符。
        separator_rule (str): 分隔符规则，可以是 "before" (分隔符在文本块前) 或 "after" (分隔符在文本块后)。
    Returns:
        List[str]: 分割后的文本块列表。
    """
    # 现在我们有了分隔符，分割文本
    if separator:  # 如果分隔符不为空
        if keep_separator:  # 如果需要保留分隔符
            # 模式中的括号使分隔符保留在结果中
            _splits = re.split(f'({separator})', text)  # 使用正则表达式分割文本，分隔符保留在结果列表中
            if separator_rule == "before":  # 如果分隔符规则为 "before"
                splits = [_splits[i] + _splits[i + 1] for i in range(1, len(_splits), 2)]  # 将分隔符添加到前一个文本块
                if len(_splits) % 2 == 0:  # 如果分割后的列表长度为偶数
                    splits += _splits[-1:]  # 添加最后一个文本块
                splits = [_splits[0]] + splits  # 将第一个文本块添加到列表开头
            else:  # 如果分隔符规则为 "after" (默认)
                splits = [_splits[i - 1] + _splits[i] for i in range(1, len(_splits), 2)]  # 将分隔符添加到后一个文本块
                splits = splits + [_splits[-1]]  # 添加最后一个文本块
        else:  # 如果不需要保留分隔符
            splits = re.split(separator, text)  # 使用正则表达式分割文本，分隔符不保留在结果列表中
    else:  # 如果分隔符为空
        splits = list(text)  # 将文本按字符分割成列表
    return [s for s in splits if s != '']  # 移除空字符串

class IntervalSearch(object):
    """间隔搜索类.
    用于在间隔列表中进行搜索，找到给定间隔的索引范围。
    """

    def __init__(self, inters):
        """初始化 IntervalSearch 对象.
        Args:
            inters: 间隔列表，每个间隔表示为一个包含两个元素的列表或元组，例如 [[1, 3], [5, 7], [9, 12]]。
        """
        arrs = []
        for inter in inters:  # 遍历间隔列表
            arrs.extend(inter)  # 将每个间隔的起始和结束点添加到 arrs 列表中
        self.arrs = arrs  # 存储所有间隔的起始和结束点
        self.n = len(self.arrs)  # 存储点的数量

    def _norm_bound(self, ind, v):
        """规范化边界索引.
        根据索引和值，规范化边界索引，确保索引在有效范围内。
        Args:
            ind (int): 边界索引。
            v: 值。
        Returns:
            int: 规范化后的边界索引。
        """
        # [1,3,5,7,9,12]
        # ind=4,8 is empty interval
        # ind=15 is exceed interval
        new_ind = None
        if ind >= self.n:  # 如果索引超出范围
            new_ind = self.n - 1  # 设置为最后一个索引
        elif ind <= 0:  # 如果索引小于等于 0
            new_ind = 0  # 设置为 0
        elif self.arrs[ind] == v:  # 如果索引对应的值等于给定值
            new_ind = ind  # 索引不变
        elif ind % 2 == 0:  # 如果索引为偶数
            if v > self.arrs[ind - 1] and v < self.arrs[ind]:  # 如果值在索引前一个点和当前点之间
                new_ind = ind - 1  # 设置为前一个索引
            else:
                new_ind = ind  # 索引不变
        else:  # 如果索引为奇数
            new_ind = ind  # 索引不变
        return new_ind  # 返回规范化后的索引

    def find(self, inter) -> List[int, int]:
        """查找间隔对应的索引范围.
        在间隔列表中查找给定间隔对应的索引范围。
        Args:
            inter: 给定间隔，例如 [2, 6]。
        Returns:
            List[int, int]: 索引范围列表，包含起始索引和结束索引。
        """
        low_bound1 = bisect.bisect_left(self.arrs, inter[0])  # 二分查找左边界
        low_bound2 = bisect.bisect_left(self.arrs, inter[1])  # 二分查找右边界
        lb1 = self._norm_bound(low_bound1, inter[0])  # 规范化左边界索引
        lb2 = self._norm_bound(low_bound2, inter[1])  # 规范化右边界索引
        return [lb1 // 2, lb2 // 2]  # 返回索引范围，除以 2 是因为 self.arrs 列表是原始间隔列表长度的两倍

class ElemCharacterTextSplitter(RecursiveCharacterTextSplitter):
    """
    ElemCharacterTextSplitter 类，继承自 RecursiveCharacterTextSplitter，用于按字符递归分割文本。
    todo: 类描述待补充
    """

    def __init__(self, separators: Optional[List[str]] = None, separator_rule: Optional[List[str]] = None, is_separator_regex: bool = False, keep_separator: bool = True,
            **kwargs: Any, ) -> None:
        """创建 ElemCharacterTextSplitter 对象.
        Args:
            separators (Optional[List[str]]): 分隔符列表，用于文本分割，默认为 ['\n\n', '\n', ' ', '']。
            separator_rule (Optional[List[str]]): 分隔符规则列表，与 separators 列表对应，定义分隔符的使用方式，默认为 ['after', 'after', 'after', 'after']。
            is_separator_regex (bool): 是否将分隔符视为正则表达式，默认为 False。
            keep_separator (bool): 分割后的文本块是否保留分隔符，默认为 True。
            **kwargs (Any): 传递给 RecursiveCharacterTextSplitter 父类的其他参数。
        """
        super().__init__(separators=separators, keep_separator=keep_separator, **kwargs)
        self._separators = separators or ['\n\n', '\n', ' ', '']  # 设置分隔符列表，默认为 ['\n\n', '\n', ' ', '']
        self._separator_rule = separator_rule or ['after' for _ in range(4)]  # 设置分隔符规则列表，默认为 ['after', 'after', 'after', 'after']
        self.separator_rule = {one: self._separator_rule[index] for index, one in enumerate(separators)}  # 创建分隔符到规则的字典映射
        self._is_separator_regex = is_separator_regex  # 设置是否将分隔符视为正则表达式

    def split_documents(self, documents: Iterable[Document]) -> List[Document]:
        """分割文档列表.
        将文档列表中的每个文档分割成多个文档块。
        Args:
            documents (Iterable[Document]): 包含 Document 对象的 Iterable 对象。
        Returns:
            List[Document]: 分割后的 Document 对象列表。
        """
        texts, metadatas = [], []
        for doc in documents:  # 遍历文档列表
            texts.append(doc.page_content)  # 提取文档内容
            metadatas.append(doc.metadata)  # 提取文档元数据
        return self.create_documents(texts, metadatas=metadatas)  # 调用 create_documents 方法创建分割后的文档

    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        """按分隔符分割文本并返回文本块列表.
        递归地按分隔符分割文本，并返回分割后的文本块列表。
        Args:
            text (str): 要分割的文本。
            separators (List[str]): 分隔符列表。
        Returns:
            List[str]: 分割后的文本块列表。
        """
        final_chunks = []  # 初始化最终文本块列表
        # 获取要使用的适当分隔符
        separator = separators[-1]  # 默认使用最后一个分隔符
        separator_rule = 'after'  # 默认分隔符规则为 'after'
        new_separators = []  # 初始化新的分隔符列表
        for i, _s in enumerate(separators):  # 遍历分隔符列表
            _separator = _s if self._is_separator_regex else re.escape(_s)  # 如果分隔符不是正则表达式，则进行转义
            separator_rule = self.separator_rule[_s]  # 获取分隔符规则
            if _s == '':  # 如果分隔符为空字符串
                separator = _s  # 设置分隔符为空字符串
                break  # 跳出循环
            if re.search(_separator, text):  # 如果在文本中找到分隔符
                separator = _s  # 设置分隔符为当前分隔符
                new_separators = separators[i + 1:]  # 更新新的分隔符列表，移除已使用的分隔符及其之前的分隔符
                break  # 跳出循环
        _separator = separator if self._is_separator_regex else re.escape(separator)  # 再次处理分隔符
        splits = _split_text_with_regex(text, _separator, self._keep_separator, separator_rule)  # 使用正则表达式分割文本
        # 现在合并内容，递归分割更长的文本。
        _good_splits = []  # 初始化好的文本块列表
        _separator = '' if self._keep_separator else separator  # 设置合并文本块时的分隔符，如果保留分隔符则为空字符串，否则为当前分隔符
        for s in splits:  # 遍历分割后的文本块
            if self._length_function(s) < self._chunk_size:  # 如果文本块长度小于 chunk_size
                _good_splits.append(s)  # 添加到好的文本块列表
            else:  # 如果文本块长度大于等于 chunk_size
                if _good_splits:  # 如果好的文本块列表不为空
                    merged_text = self._merge_splits(_good_splits, _separator)  # 合并好的文本块
                    final_chunks.extend(merged_text)  # 添加到最终文本块列表
                    _good_splits = []  # 清空好的文本块列表
                if not new_separators:  # 如果没有新的分隔符
                    final_chunks.append(s)  # 将当前文本块添加到最终文本块列表
                else:  # 如果有新的分隔符
                    other_info = self._split_text(s, new_separators)  # 递归分割文本块
                    final_chunks.extend(other_info)  # 添加到最终文本块列表
        if _good_splits:  # 如果好的文本块列表不为空
            merged_text = self._merge_splits(_good_splits, _separator)  # 合并好的文本块
            final_chunks.extend(merged_text)  # 添加到最终文本块列表
        return final_chunks  # 返回最终文本块列表

    def split_text(self, text: str) -> List[str]:
        """分割文本.
        使用预定义的分隔符列表分割文本。
        Args:
            text (str): 要分割的文本。
        Returns:
            List[str]: 分割后的文本块列表。
        """
        return self._split_text(text, self._separators)  # 调用 _split_text 方法进行文本分割

    def create_documents(self, texts: List[str], metadatas: Optional[List[dict]] = None) -> List[Document]:
        """从文本列表创建文档列表.
        将文本列表中的每个文本分割成多个文档块，并根据元数据信息，为每个文档块添加 bbox, chunk_type 等元数据信息。
        Args:
            texts (List[str]): 包含文本字符串的列表。
            metadatas (Optional[List[dict]]): 与文本列表对应的元数据列表，默认为 None。
        Returns:
            List[Document]: 创建的 Document 对象列表。
        """
        documents = []  # 初始化文档列表
        for i, text in enumerate(texts):  # 遍历文本列表
            index = -1  # 初始化索引
            # metadata = copy.deepcopy(_metadatas[i])
            indexes = metadatas[i].get('indexes', [])  # 获取索引信息
            pages = metadatas[i].get('pages', [])  # 获取页码信息
            types = metadatas[i].get('types', [])  # 获取类型信息
            bboxes = metadatas[i].get('bboxes', [])  # 获取 bbox 信息
            searcher = IntervalSearch(indexes)  # 创建 IntervalSearch 对象
            split_texts = self.split_text(text)  # 分割文本
            for chunk in split_texts:  # 遍历分割后的文本块
                new_metadata = copy.deepcopy(metadatas[i])  # 复制元数据
                if indexes and bboxes:  # 如果存在索引和 bbox 信息
                    index = text.find(chunk, index + 1)  # 查找文本块在原始文本中的索引
                    inter0 = [index, index + len(chunk) - 1]  # 计算文本块的间隔
                    norm_inter = searcher.find(inter0)  # 查找间隔对应的索引范围
                    new_metadata['chunk_bboxes'] = []  # 初始化 chunk_bboxes 列表
                    for j in range(norm_inter[0], norm_inter[1] + 1):  # 遍历索引范围
                        new_metadata['chunk_bboxes'].append({'page': pages[j], 'bbox': bboxes[j]})  # 添加 chunk_bbox 信息，包含页码和 bbox
                    c = Counter([types[j] for j in norm_inter])  # 统计索引范围内类型出现次数
                    chunk_type = c.most_common(1)[0][0]  # 获取出现次数最多的类型作为 chunk_type
                    new_metadata['chunk_type'] = chunk_type  # 设置 chunk_type
                    new_metadata['source'] = metadatas[i].get('source', '')  # 设置 source
                new_doc = Document(page_content=chunk, metadata=new_metadata)  # 创建 Document 对象
                documents.append(new_doc)  # 添加到文档列表
        return documents  # 返回文档列表

class ElemCharacterTextByTitleSplitter(RecursiveCharacterTextSplitter):
    """
    ElemCharacterTextByTitleSplitter 类，继承自 RecursiveCharacterTextSplitter，用于按标题分割文本。
    todo: 类描述待补充
    """

    def __init__(self, separators: Optional[List[str]] = None, separator_rule: Optional[List[str]] = None, is_separator_regex: bool = False, keep_separator: bool = True,
            **kwargs: Any, ) -> None:
        """创建 ElemCharacterTextByTitleSplitter 对象.
        Args:
            separators (Optional[List[str]]): 分隔符列表，用于文本分割，默认为 ['\n\n', '\n', ' ', '']。
            separator_rule (Optional[List[str]]): 分隔符规则列表，与 separators 列表对应，定义分隔符的使用方式，默认为 ['after', 'after', 'after', 'after']。
            is_separator_regex (bool): 是否将分隔符视为正则表达式，默认为 False。
            keep_separator (bool): 分割后的文本块是否保留分隔符，默认为 True。
            **kwargs (Any): 传递给 RecursiveCharacterTextSplitter 父类的其他参数。
        """
        super().__init__(separators=separators, keep_separator=keep_separator, **kwargs)
        self._separators = separators or ['\n\n', '\n', ' ', '']  # 设置分隔符列表，默认为 ['\n\n', '\n', ' ', '']
        self._separator_rule = separator_rule or ['after' for _ in range(4)]  # 设置分隔符规则列表，默认为 ['after', 'after', 'after', 'after']
        self.separator_rule = {one: self._separator_rule[index] for index, one in enumerate(separators)}  # 创建分隔符到规则的字典映射
        self._is_separator_regex = is_separator_regex  # 设置是否将分隔符视为正则表达式

    def split_documents(self, documents: Iterable[Document]) -> List[Document]:
        """分割文档列表.
        将文档列表中的每个文档分割成多个文档块。
        Args:
            documents (Iterable[Document]): 包含 Document 对象的 Iterable 对象。
        Returns:
            List[Document]: 分割后的 Document 对象列表。
        """
        texts, metadatas = [], []
        for doc in documents:  # 遍历文档列表
            texts.append(doc.page_content)  # 提取文档内容
            metadatas.append(doc.metadata)  # 提取文档元数据
        return self.create_documents(texts=texts, metadatas=metadatas)  # 调用 create_documents 方法创建分割后的文档

    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        """按分隔符分割文本并返回文本块列表.
        递归地按分隔符分割文本，并返回分割后的文本块列表。
        Args:
            text (str): 要分割的文本。
            separators (List[str]): 分隔符列表。
        Returns:
            List[str]: 分割后的文本块列表。
        """
        final_chunks = []
        # Get appropriate separator to use
        separator = separators[-1]
        separator_rule = 'after'
        new_separators = []
        for i, _s in enumerate(separators):
            _separator = _s if self._is_separator_regex else re.escape(_s)
            separator_rule = self.separator_rule[_s]
            if _s == '':
                separator = _s
                break
            if re.search(_separator, text):
                separator = _s
                new_separators = separators[i + 1:]
                break
        _separator = separator if self._is_separator_regex else re.escape(separator)
        splits = _split_text_with_regex(text, _separator, self._keep_separator, separator_rule)
        # Now go merging things, recursively splitting longer texts.
        _good_splits = []
        _separator = '' if self._keep_separator else separator
        for s in splits:
            if self._length_function(s) < self._chunk_size:
                _good_splits.append(s)
            else:
                if _good_splits:
                    merged_text = self._merge_splits(_good_splits, _separator)
                    final_chunks.extend(merged_text)
                    _good_splits = []
                if not new_separators:
                    final_chunks.append(s)
                else:
                    other_info = self._split_text(s, new_separators)
                    final_chunks.extend(other_info)
        if _good_splits:
            merged_text = self._merge_splits(_good_splits, _separator)
            final_chunks.extend(merged_text)
        return final_chunks

    def split_text(self, text: str) -> List[str]:
        """分割文本.
        此方法重写父类方法，直接返回包含原始文本的列表，不进行分割。
        实际分割逻辑在 create_documents 方法中实现。
        Args:
            text (str): 要分割的文本。
        Returns:
            List[str]: 包含原始文本的列表，不进行分割。
        """
        return [text]  # 直接返回包含原始文本的列表，不进行分割

    def create_documents(self, texts: List[str], metadatas: Optional[List[dict]] = None) -> List[Document]:
        """从文本列表创建文档列表.
        将文本列表中的每个文本根据标题进行分割，并根据元数据信息，为每个文档块添加 chunk_bboxes, chunk_type, parents 等元数据信息。
        Args:
            texts (List[str]): 包含文本字符串的列表。
            metadatas (Optional[List[dict]]): 与文本列表对应的元数据列表，默认为 None。
        Returns:
            List[Document]: 创建的 Document 对象列表。
        """
        documents = []  # 初始化文档列表
        for i, text in enumerate(texts):  # 遍历文本列表
            index = -1  # 初始化索引
            # metadata = copy.deepcopy(_metadatas[i])
            indexes = metadatas[i].get('indexes', [])  # 获取索引信息
            pages = metadatas[i].get('pages', [])  # 获取页码信息
            types = metadatas[i].get('types', [])  # 获取类型信息
            bboxes = metadatas[i].get('bboxes', [])  # 获取 bbox 信息
            title_indexes = []  # 初始化标题索引列表
            title_contents = []  # 初始化标题内容列表
            level = metadatas[i].get('levels', [])  # 获取层级信息
            current_titles = []  # 初始化当前标题列表

            def find_content_titles():
                """查找内容标题.
                返回当前标题列表。
                """
                return current_titles  # 返回当前标题列表

            def add_current_title(new_title: dict, current_titles: List[dict]):
                """添加当前标题.
                将新的标题信息添加到当前标题列表中，并维护标题层级关系。
                Args:
                    new_title (dict): 新的标题信息字典，包含 level, title, id, page 等键。
                    current_titles (List[dict]): 当前标题列表。
                Returns:
                    List[dict]: 更新后的当前标题列表。
                """
                insert_index = -1  # 默认为-1，表示没有找到插入位置
                for i in range(len(current_titles)):  # 遍历当前标题列表
                    if current_titles[i]['level'] <= new_title['level']:  # 查找插入位置，根据标题层级判断
                        insert_index = i  # 找到插入位置
                        break
                parent_title = []  # 初始化父标题列表
                if insert_index == -1:  # 如果没有找到插入位置，表示新标题层级最高
                    parent_title = current_titles  # 父标题为当前所有标题
                else:  # 如果找到插入位置
                    parent_title = current_titles[0:insert_index]  # 父标题为插入位置之前的标题
                parent_id = [p["id"] for p in parent_title]  # 获取父标题 ID 列表
                new_title["parents"] = parent_id  # 设置新标题的 parents 属性为父标题 ID 列表
                if insert_index == -1:  # 如果没有找到插入位置，添加到列表末尾
                    current_titles.append(new_title)  # 添加到当前标题列表末尾
                else:  # 如果找到插入位置，插入到指定位置
                    current_titles.insert(insert_index, new_title)  # 插入到指定位置
                    current_titles = current_titles[:insert_index + 1]  # 截断当前标题列表，保持层级关系
                return current_titles  # 返回更新后的当前标题列表

            new_doc = None  # 初始化新文档对象
            t_type = "Title"  # 初始化文档类型为 "Title"
            new_metadata = {}  # 初始化新元数据字典
            merge_content = ""  # 初始化合并内容字符串
            chunk_end_flag = False  # 初始化分块结束标志
            for index, type_content in enumerate(types):  # 遍历类型列表和内容
                current_page = pages[index]  # 获取当前页码
                id = str(uuid.uuid4())  # 生成 UUID 作为文档 ID
                if type_content != "title" and t_type != "title" and not chunk_end_flag:  # 如果当前内容不是标题且上一个内容也不是标题且分块未结束
                    merge_content += text[indexes[index][0]:indexes[index][1] + 1]  # 合并内容
                    if "chunk_bboxes" not in new_metadata:  # 如果 chunk_bboxes 不在元数据中
                        new_metadata = {"source": metadatas[i].get('source', ''), "id": id, 'chunk_bboxes': [], 'page': current_page, "content_type": type_content,
                                        "level": level[index]}  # 初始化元数据
                else:  # 如果当前内容是标题或上一个内容是标题或分块已结束
                    merge_content = text[indexes[index][0]:indexes[index][1] + 1]  # 更新合并内容为当前内容
                    new_metadata = {"source": metadatas[i].get('source', ''), "id": id, 'chunk_bboxes': [], 'page': current_page, "content_type": type_content,
                                    "level": level[index]}  # 初始化元数据
                if self._chunk_size <= len(merge_content) + 50:  # 如果合并内容长度超过 chunk_size 阈值
                    chunk_end_flag = True  # 设置分块结束标志
                new_metadata['chunk_bboxes'].append({'page': pages[index], 'bbox': bboxes[index]})  # 添加 chunk_bbox 信息
                chunk_type = type_content  # 获取分块类型
                new_metadata['chunk_type'] = chunk_type  # 设置 chunk_type
                if type_content != 'title':  # 如果当前内容不是标题
                    parent_title = find_content_titles()  # 查找父标题
                    new_metadata['parents'] = [t_i["id"] for t_i in parent_title]  # 设置 parents 属性为父标题 ID 列表
                else:  # 如果当前内容是标题
                    current_titles = add_current_title({"level": level[index], "title": text[indexes[index][0]:indexes[index][1] + 1], "id": id, "page": current_page},
                        current_titles)  # 添加当前标题到当前标题列表
                    parent_title = find_content_titles()  # 查找父标题
                    if len(parent_title) >= 1:  # 如果父标题列表长度大于等于 1
                        parent_title = parent_title[:-1]  # 移除最后一个父标题，保持层级关系
                    new_metadata['parents'] = [t_i["id"] for t_i in parent_title]  # 设置 parents 属性为父标题 ID 列表
                source = new_metadata["source"]  # 获取 source
                file_name = source.split(".")[0]  # 提取文件名
                new_doc = Document(page_content=f"{file_name}\n{merge_content}", metadata=new_metadata)  # 创建 Document 对象，page_content 包含文件名和合并内容
                if type_content != "title" and t_type != "title" and not chunk_end_flag:  # 如果当前内容不是标题且上一个内容也不是标题且分块未结束
                    pass  # 什么也不做，继续合并内容
                else:  # 否则，添加到文档列表
                    chunk_end_flag = False  # 重置分块结束标志
                    documents.append(new_doc)  # 添加到文档列表
                t_type = type_content  # 更新文档类型为当前内容类型
        return documents  # 返回文档列表
