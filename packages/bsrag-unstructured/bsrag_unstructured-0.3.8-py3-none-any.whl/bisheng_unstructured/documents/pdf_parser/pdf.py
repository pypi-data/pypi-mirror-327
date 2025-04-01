import json
import re
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, List, Optional, Union
import fitz as pymupdf
import numpy as np
from PIL import Image, ImageOps
from shapely import Polygon
from shapely import box as Rect
from bisheng_unstructured.common import Timer
from bisheng_unstructured.documents.base import Document, Page
from bisheng_unstructured.documents.elements import (ElementMetadata, Table, Text, Title, Image)
from bisheng_unstructured.documents.markdown import (merge_html_tables, merge_md_tables, transform_html_table_to_md, transform_list_to_table, )
from bisheng_unstructured.documents.pdf_parser.blob import Blob
from bisheng_unstructured.models import (FormulaAgent, LayoutAgent, OCRAgent, RTLayoutAgent, RTOCRAgent, RTTableAgent, RTTableDetAgent, TableAgent, TableDetAgent, MinerUAgent)
ZH_CHAR = re.compile("[\u4e00-\u9fa5]")  # 定义正则表达式，用于匹配中文字符
ENG_WORD = re.compile(pattern=r"^[a-zA-Z0-9?><;,{}[\]\-_+=!@#$%\^&*|']*$", flags=re.DOTALL)  # 定义正则表达式，用于匹配英文字符和数字
RE_MULTISPACE_INCLUDING_NEWLINES = re.compile(pattern=r"\s+", flags=re.DOTALL)  # 定义正则表达式，用于匹配包括换行符在内的多个空格

def read_image(path):
    """
    读取图像文件并进行预处理。
    Args:
        path: 图像文件路径。
    Returns:
        PIL.Image.Image: RGB 格式的图像。
    """
    img = Image.open(path)  # 打开图像文件
    img = ImageOps.exif_transpose(img).convert("RGB")  # 根据 EXIF 数据校正图像方向，并转换为 RGB 格式
    return img

def merge_rects(bboxes):
    """
    合并多个边界框为一个最小外接矩形。
    Args:
        bboxes: 边界框列表，每个边界框为 [x0, y0, x1, y1] 格式的列表或 numpy 数组。
    Returns:
        list: 合并后的边界框 [x0, y0, x1, y1]。
    """
    x0 = np.min(bboxes[:, 0])  # 获取所有边界框中最小的 x0 坐标
    y0 = np.min(bboxes[:, 1])  # 获取所有边界框中最小的 y0 坐标
    x1 = np.max(bboxes[:, 2])  # 获取所有边界框中最大的 x1 坐标
    y1 = np.max(bboxes[:, 3])  # 获取所有边界框中最大的 y1 坐标
    return [x0, y0, x1, y1]  # 返回合并后的边界框

def norm_rect(bbox):
    """
    规范化边界框，确保 x0 < x1 且 y0 < y1。
    Args:
        bbox: 边界框 [x0, y0, x1, y1] 格式的列表或 numpy 数组。
    Returns:
        numpy.ndarray: 规范化后的边界框 [x0, y0, x1, y1] 的 numpy 数组。
    """
    x0 = np.min([bbox[0], bbox[2]])  # 确保 x0 是左边界
    x1 = np.max([bbox[0], bbox[2]])  # 确保 x1 是右边界
    y0 = np.min([bbox[1], bbox[3]])  # 确保 y0 是上边界
    y1 = np.max([bbox[1], bbox[3]])  # 确保 y1 是下边界
    return np.asarray([x0, y0, x1, y1])  # 返回规范化后的边界框

def get_hori_rect(rot_rect):
    """
    从旋转矩形中提取水平边界框。
    Args:
        rot_rect: 旋转矩形，格式为长度为 8 的列表或 numpy 数组，表示四个点的坐标。
    Returns:
        list: 水平边界框 [x0, y0, x1, y1]。
    """
    arr = np.asarray(rot_rect, dtype=np.float32).reshape((4, 2))  # 将旋转矩形转换为 numpy 数组，并reshape为 (4, 2) 的形状
    x0 = np.min(arr[:, 0])  # 获取所有点中最小的 x 坐标
    x1 = np.max(arr[:, 0])  # 获取所有点中最大的 x 坐标
    y0 = np.min(arr[:, 1])  # 获取所有点中最小的 y 坐标
    y1 = np.max(arr[:, 1])  # 获取所有点中最大的 y 坐标
    return [float(e) for e in (x0, y0, x1, y1)]  # 返回水平边界框，并将坐标转换为 float 类型

def find_max_continuous_seq(arr):
    """
    在一个排序数组中查找最大连续序列的起始索引和长度。
    Args:
        arr: 排序后的整数数组。
    Returns:
        tuple: (起始索引, 长度) 的元组，起始索引是序列的第一个元素的索引值，长度是序列的长度。
    """
    n = len(arr)  # 获取数组长度
    max_info = (0, 1)  # 初始化最大连续序列信息，默认为 (0, 1)，表示从索引 0 开始，长度为 1
    for i in range(n):  # 遍历数组
        m = 1  # 初始化当前连续序列长度为 1
        for j in range(i + 1, n):  # 从当前索引的下一个索引开始遍历
            if arr[j] - arr[j - 1] == 1:  # 如果当前元素与前一个元素的差为 1，则表示连续
                m += 1  # 增加连续序列长度
            else:
                break  # 如果不连续，则跳出内循环
        if m > max_info[1]:  # 如果当前连续序列长度大于之前的最大长度
            max_info = (i, m)  # 更新最大连续序列信息
    max_info = (max_info[0] + arr[0], max_info[1])  # 计算实际的起始索引值，起始索引值 = 初始索引 + 数组第一个元素的值
    return max_info  # 返回最大连续序列信息

def order_by_tbyx(block_info, th=10):
    """
    根据文本块的 y 坐标和 x 坐标对文本块信息进行排序，并根据阈值 th 调整顺序。
    Args:
        block_info: 文本块信息列表，每个元素为 BlockInfo 对象。
        th: 位置阈值，用于判断两个文本块是否在同一行。
    Returns:
        list: 排序后的文本块信息列表。
    """
    # 首先使用 y1 坐标和 x0 坐标进行排序
    res = sorted(block_info, key=lambda b: (b.bbox[1], b.bbox[0]))
    for i in range(len(res) - 1):  # 遍历排序后的文本块信息列表
        for j in range(i, 0, -1):  # 从当前索引向前遍历
            # 使用位置阈值 th 恢复顺序
            bbox_jplus1 = res[j + 1].bbox  # 获取后一个文本块的边界框
            bbox_j = res[j].bbox  # 获取当前文本块的边界框
            if abs(bbox_jplus1[1] - bbox_j[1]) < th and (bbox_jplus1[0] < bbox_j[0]):  # 如果两个文本块的 y 坐标差小于阈值 th 且后一个文本块的 x 坐标小于当前文本块的 x 坐标，则交换位置
                tmp = deepcopy(res[j])  # 深拷贝当前文本块信息
                res[j] = deepcopy(res[j + 1])  # 将后一个文本块信息赋值给当前位置
                res[j + 1] = deepcopy(tmp)  # 将之前拷贝的当前文本块信息赋值给后一个位置
            else:
                break  # 如果不满足交换条件，则跳出内循环
    return res  # 返回排序后的文本块信息列表

def is_eng_word(word):
    """
    判断单词是否为英文单词或包含数字和特定符号。
    Args:
        word: 要判断的单词字符串。
    Returns:
        bool: 如果是英文单词或包含数字和特定符号，则返回 True，否则返回 False。
    """
    return bool(ENG_WORD.search(word))  # 使用正则表达式 ENG_WORD 搜索单词，返回是否匹配的结果

def rect2polygon(bboxes):
    """
    将边界框列表转换为多边形列表。
    Args:
        bboxes: 边界框列表，每个边界框为 [x0, y0, x1, y1] 格式的列表或 numpy 数组。
    Returns:
        list: 多边形列表，每个多边形为 shapely.Polygon 对象。
    """
    polys = []  # 初始化多边形列表
    for x0, y0, x1, y1 in bboxes:  # 遍历边界框列表
        polys.append([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])  # 将每个边界框转换为多边形坐标，并添加到多边形列表中
    return polys  # 返回多边形列表

def join_lines(texts, is_table=False, lang="eng"):
    """
    连接文本行，根据是否为表格和语言进行不同的连接方式。
    Args:
        texts: 文本行列表。
        is_table: 是否为表格文本，默认为 False。
        lang: 语言类型，默认为 "eng" (英文)，可选 "zh" (中文)。
    Returns:
        str: 连接后的文本字符串。
    """
    if is_table:  # 如果是表格文本
        return "\n".join(texts)  # 使用换行符连接文本行
    PUNC_SET = set([".", ",", ";", "?", "!"])  # 定义英文标点符号集合
    if lang == "eng":  # 如果是英文
        t0 = texts[0]  # 初始化连接后的文本为第一行文本
        for t in texts[1:]:  # 遍历剩余的文本行
            if t0[-1] == "-":  # 如果前一行文本以 "-" 结尾，则去除 "-" 并直接连接当前行文本
                t0 = t0[:-1] + t
            elif t0[-1].isalnum() and t[0].isalnum():  # 如果前一行文本最后一个字符和当前行文本第一个字符都是字母数字，则在中间添加空格
                t0 += " " + t
            elif t0[-1] in PUNC_SET or t[0] in PUNC_SET:  # 如果前一行文本最后一个字符或当前行文本第一个字符是标点符号，则在中间添加空格
                t0 += " " + t
            else:  # 其他情况直接连接
                t0 += t
        return t0  # 返回连接后的文本
    else:  # 如果是中文
        return "".join(texts)  # 直接连接文本行

@dataclass
class BlockInfo:
    """
    文本块信息的 dataclass。
    Attributes:
        bbox: 边界框 [x0, y0, x1, y1]。
        block_text: 文本块内容。
        block_no: 文本块编号。
        block_type: 文本块类型。
        ts: 文本行列表，用于存储原始文本行。
        rs: 文本行边界框列表，用于存储原始文本行边界框。
        ind: 原始文本块索引列表，用于追踪原始文本块的索引。
        ord_ind: 原始文本块的顺序索引，用于排序。
        layout_type: 布局类型，例如文本、表格、图片等。
        html_text: HTML 格式的文本内容。
    """
    bbox: List[Union[float, int]]  # 边界框
    block_text: str  # 文本块内容
    block_no: int  # 文本块编号
    block_type: int  # 文本块类型
    ts: Any = None  # 文本行列表
    rs: Any = None  # 文本行边界框列表
    ind: List[int] = None  # 原始文本块索引列表
    ord_ind: int = None  # 原始文本块顺序索引
    layout_type: int = None  # 布局类型
    html_text: str = None  # HTML 文本内容

class Segment:
    """
    线段类，用于处理线段对齐和重叠等操作。
    """

    def __init__(self, seg):
        """
        初始化 Segment 对象。
        Args:
            seg: 线段，格式为 (x0, x1)。
        """
        self.whole = seg  # 完整线段
        self.segs = []  # 包含的子线段列表

    @staticmethod
    def is_align(seg0, seg1, delta=5, mode=0):
        """
        判断两个线段是否对齐。
        Args:
            seg0: 第一个线段 (x0, x1)。
            seg1: 第二个线段 (x0, x1)。
            delta: 对齐阈值，默认为 5。
            mode: 对齐模式，0 表示边缘对齐，1 表示边缘对齐或中心对齐，默认为 0。
        Returns:
            bool: 如果对齐则返回 True，否则返回 False。
        """
        # mode=0 边缘对齐
        # mode=1, 边缘对齐或中心对齐
        res = Segment.contain(seg0, seg1)  # 判断 seg1 是否包含在 seg0 中
        if not res:  # 如果不包含，则不对齐
            return False
        else:  # 如果包含
            if mode == 1:  # 如果是模式 1，则判断边缘对齐或中心对齐
                r1 = seg1[0] - seg0[0] <= delta or seg0[1] - seg1[1] <= delta  # 判断边缘是否对齐
                c0 = (seg0[0] + seg0[1]) / 2  # 计算 seg0 的中心点
                c1 = (seg1[0] + seg1[1]) / 2  # 计算 seg1 的中心点
                r2 = abs(c1 - c0) <= delta  # 判断中心点是否对齐
                return r1 or r2  # 边缘对齐或中心对齐任一满足则对齐
            else:  # 如果是模式 0，则只判断边缘对齐
                return seg1[0] - seg0[0] <= delta or seg0[1] - seg1[1] <= delta  # 判断边缘是否对齐

    @staticmethod
    def contain(seg0, seg1):
        """
        判断线段 seg1 是否包含在线段 seg0 中。
        Args:
            seg0: 包含线段 (x0, x1)。
            seg1: 被包含线段 (x0, x1)。
        Returns:
            bool: 如果 seg1 包含在 seg0 中则返回 True，否则返回 False。
        """
        return seg0[0] <= seg1[0] and seg0[1] >= seg1[0]  # 判断 seg1 的起始点是否在 seg0 的起始点之后，且 seg1 的起始点是否在 seg0 的结束点之前

    @staticmethod
    def overlap(seg0, seg1):
        """
        判断两个线段是否重叠。
        Args:
            seg0: 第一个线段 (x0, x1)。
            seg1: 第二个线段 (x0, x1)。
        Returns:
            bool: 如果重叠则返回 True，否则返回 False。
        """
        max_x0 = max(seg0[0], seg1[0])  # 获取两个线段起始点中较大的值
        min_x1 = min(seg0[1], seg1[1])  # 获取两个线段结束点中较小的值
        return max_x0 < min_x1  # 如果较大的起始点小于较小的结束点，则表示重叠

    def _merge(self, segs):
        """
        合并多个线段为一个线段。
        Args:
            segs: 线段列表，每个线段为 (x0, x1)。
        Returns:
            tuple: 合并后的线段 (x0, x1)。
        """
        x0s = [s[0] for s in segs]  # 获取所有线段的起始点列表
        x1s = [s[1] for s in segs]  # 获取所有线段的结束点列表
        return (np.min(x0s), np.max(x1s))  # 返回合并后的线段，起始点为所有起始点中的最小值，结束点为所有结束点中的最大值

    def add(self, seg):
        """
        向 Segment 对象添加一个线段，并自动合并重叠的线段。
        Args:
            seg: 要添加的线段 (x0, x1)。
        """
        if not self.segs:  # 如果子线段列表为空，则直接添加
            self.segs.append(seg)
        else:  # 如果子线段列表不为空
            overlaps = []  # 初始化重叠线段列表
            non_overlaps = []  # 初始化非重叠线段列表
            for seg0 in self.segs:  # 遍历已有的子线段
                if Segment.overlap(seg0, seg):  # 判断当前子线段是否与要添加的线段重叠
                    overlaps.append(seg0)  # 如果重叠，则添加到重叠线段列表
                else:
                    non_overlaps.append(seg0)  # 如果不重叠，则添加到非重叠线段列表
            if not overlaps:  # 如果没有重叠线段，则直接添加
                self.segs.append(seg)
            else:  # 如果有重叠线段
                overlaps.append(seg)  # 将要添加的线段也添加到重叠线段列表
                new_seg = self._merge(overlaps)  # 合并所有重叠线段
                non_overlaps.append(new_seg)  # 将合并后的线段添加到非重叠线段列表
                self.segs = non_overlaps  # 更新子线段列表

    def get_free_segment(self, incr_margin=True, margin_threshold=10):
        """
        获取线段中未被占用的自由线段。
        Args:
            incr_margin: 是否考虑边距，如果为 True，则会考虑线段两端的空白区域，默认为 True。
            margin_threshold: 边距阈值，只有当空白区域大于阈值时才会被认为是自由线段，默认为 10。
        Returns:
            list: 自由线段列表，每个自由线段为 (x0, x1)。
        """
        sorted_segs = sorted(self.segs, key=lambda x: x[0])  # 对子线段列表按照起始点排序
        n = len(sorted_segs)  # 获取子线段数量
        free_segs = []  # 初始化自由线段列表
        if incr_margin:  # 如果考虑边距
            if n > 0:  # 如果有子线段
                seg_1st = sorted_segs[0]  # 获取第一个子线段
                if (seg_1st[0] - self.whole[0]) > margin_threshold:  # 如果第一个子线段的起始点与完整线段的起始点之间的距离大于阈值
                    free_segs.append((self.whole[0], seg_1st[0]))  # 添加从完整线段起始点到第一个子线段起始点之间的线段作为自由线段
                seg_last = sorted_segs[-1]  # 获取最后一个子线段
                if (self.whole[1] - seg_last[1]) > margin_threshold:  # 如果完整线段的结束点与最后一个子线段的结束点之间的距离大于阈值
                    free_segs.append((seg_last[1], self.whole[1]))  # 添加从最后一个子线段结束点到完整线段结束点之间的线段作为自由线段
        for i in range(n - 1):  # 遍历相邻的子线段
            x0 = sorted_segs[i][1]  # 获取前一个子线段的结束点
            x1 = sorted_segs[i + 1][0]  # 获取后一个子线段的起始点
            free_segs.append((x0, x1))  # 添加从前一个子线段结束点到后一个子线段起始点之间的线段作为自由线段
        return free_segs  # 返回自由线段列表

class PDFDocument(Document):
    """
    加载带有语义分割的 PDF 文档。
    Loader 也将页码存储在元数据中。
    """

    def __init__(self, file: str, model_params: dict, password: Optional[Union[str, bytes]] = None, is_join_table: bool = True, with_columns: bool = False,
                 support_rotate: bool = False, is_scan: Optional[bool] = None, text_elem_sep: str = "\n", start: int = 0, n: int = None, verbose: bool = False,
                 enhance_table: bool = True, keep_text_in_image: bool = True, support_formula: bool = False, enable_isolated_formula: bool = False, n_parallel: int = 10,
                 **kwargs, ) -> None:
        """
        初始化 PDFDocument 对象。
        Args:
            file: PDF 文件路径。
            model_params: 模型参数字典。
            password: PDF 文件密码，可选。
            is_join_table: 是否合并表格，默认为 True。
            with_columns: 是否支持分栏布局，默认为 False。
            support_rotate: 是否支持旋转页面，默认为 False。
            is_scan: 是否为扫描文档，如果为 None，则自动判断，默认为 None。
            text_elem_sep: 文本元素分隔符，默认为 "\n"。
            start: 起始页码，默认为 0。
            n: 加载页数，如果为 None，则加载所有页，默认为 None。
            verbose: 是否打印详细日志，默认为 False。
            enhance_table: 是否增强表格识别，默认为 True。
            keep_text_in_image: 是否保留图片中的文本，默认为 True。
            support_formula: 是否支持公式识别，默认为 False。
            enable_isolated_formula: 是否启用独立公式识别，默认为 False。
            n_parallel: 并行处理数量，默认为 10。
            **kwargs: 其他关键字参数。
        """
        rt_type = kwargs.get("rt_type", "sdk")  # 获取 rt_type 参数，默认为 "sdk"
        if rt_type in {"sdk", "idp", "ocr_sdk"}:  # 如果 rt_type 为 "sdk", "idp" 或 "ocr_sdk"
            self.layout_agent = LayoutAgent(**model_params)  # 初始化布局检测 Agent
            self.table_agent = TableAgent(**model_params)  # 初始化表格结构识别 Agent
            self.ocr_agent = OCRAgent(**model_params)  # 初始化 OCR Agent
            self.table_det_agent = TableDetAgent(**model_params)  # 初始化表格检测 Agent
            self.miner_agent = MinerUAgent(**model_params)  # 初始化文档结构分析 Agent
        else:  # 如果 rt_type 为其他值，则初始化实时模型 Agent
            self.layout_agent = RTLayoutAgent(**model_params)  # 初始化实时布局检测 Agent
            self.table_agent = RTTableAgent(**model_params)  # 初始化实时表格结构识别 Agent
            self.ocr_agent = RTOCRAgent(**model_params)  # 初始化实时 OCR Agent
            self.table_det_agent = RTTableDetAgent(**model_params)  # 初始化实时表格检测 Agent
            self.miner_agent = MinerUAgent(**model_params)  # 初始化实时文档结构分析 Agent
        self.formula_agent = FormulaAgent(**model_params)  # 初始化公式识别 Agent
        self.with_columns = with_columns  # 是否支持分栏布局
        self.is_join_table = is_join_table  # 是否合并表格
        self.support_rotate = support_rotate  # 是否支持旋转页面
        self.start = start  # 起始页码
        self.n = n  # 加载页数
        self.verbose = verbose  # 是否打印详细日志
        self.text_elem_sep = text_elem_sep  # 文本元素分隔符
        self.file = file  # PDF 文件路径
        self.enhance_table = enhance_table  # 是否增强表格识别
        self.keep_text_in_image = keep_text_in_image  # 是否保留图片中的文本
        self.support_formula = support_formula  # 是否支持公式识别
        self.enable_isolated_formula = enable_isolated_formula  # 是否启用独立公式识别
        self.n_parallel = n_parallel  # 并行处理数量
        self.is_scan = is_scan  # 是否为扫描文档
        self.mode = kwargs.get("mode", "local")  # 获取 mode 参数，默认为 "local"
        super().__init__()  # 调用父类 Document 的初始化方法

    def _get_image_blobs(self, fitz_doc, pdf_reader, n=None, start=0):
        """
        从 PDF 文档中提取图像 Blob 对象。
        Args:
            fitz_doc: pymupdf 文档对象。
            pdf_reader: pypdfium2 PDF 阅读器对象 (注释掉了 pypdfium2，实际未使用).
            n: 提取页数，如果为 None，则提取所有页，默认为 None。
            start: 起始页码，默认为 0。
        Returns:
            tuple: (Blob 对象列表, pymupdf 页面对象列表)。
        """
        blobs = []  # 初始化 Blob 对象列表
        pages = []  # 初始化 pymupdf 页面对象列表
        if not n:  # 如果 n 为 None，则提取所有页
            n = fitz_doc.page_count  # 获取 PDF 文档总页数
        for pg in range(start, start + n):  # 遍历指定页码范围
            bytes_img = None  # 初始化图像字节数据为 None
            page = fitz_doc.load_page(pg)  # 加载指定页码的页面
            pages.append(page)  # 添加页面对象到页面对象列表
            mat = pymupdf.Matrix(1, 1)  # 创建单位矩阵
            try:
                pm = page.get_pixmap(matrix=mat, alpha=False)  # 获取页面像素图
                bytes_img = pm.getPNGData()  # 获取 PNG 格式的图像字节数据
            except Exception:  # 捕获异常
                # 某些 PDF 输入无法从 fitz 获取渲染图像
                # page = pdf_reader.get_page(pg) # 注释掉 pypdfium2 相关代码
                # pil_image = page.render().to_pil() # 注释掉 pypdfium2 相关代码
                # img_byte_arr = io.BytesIO() # 注释掉 pypdfium2 相关代码
                # pil_image.save(img_byte_arr, format="PNG") # 注释掉 pypdfium2 相关代码
                # bytes_img = img_byte_arr.getvalue() # 注释掉 pypdfium2 相关代码
                pass  # 忽略异常，使用 fitz 失败时跳过当前页面的图像提取
            if bytes_img:  # 如果成功获取图像字节数据
                blobs.append(Blob(data=bytes_img))  # 创建 Blob 对象并添加到 Blob 对象列表中
        return blobs, pages  # 返回 Blob 对象列表和页面对象列表

    def _extract_lines_v2(self, textpage):
        """
        使用 extractRAWDICT() 方法从 textpage 中提取文本行信息（版本 2，更精细的字符级别处理）。
        Args:
            textpage: pymupdf 文本页对象。
        Returns:
            tuple: (文本行块信息列表, 文本行单词信息列表)。
        """
        line_blocks = []  # 初始化文本行块信息列表
        line_words_info = []  # 初始化文本行单词信息列表
        page_dict = textpage.extractRAWDICT()  # 使用 extractRAWDICT() 方法提取原始字典数据
        for block in page_dict["blocks"]:  # 遍历页面块
            block_type = block["type"]  # 获取块类型
            block_no = block["number"]  # 获取块编号
            if block_type != 0:  # 如果块类型不为 0 (非文本块)
                bbox = block["bbox"]  # 获取块边界框
                block_text = ""  # 初始化块文本为空字符串
                block_info = BlockInfo(  # 创建 BlockInfo 对象
                    [bbox[0], bbox[1], bbox[2], bbox[3]], block_text, block_no, block_type)
                line_blocks.append(block_info)  # 添加块信息到文本行块信息列表
                line_words_info.append((None, None))  # 添加 (None, None) 到文本行单词信息列表，表示非文本块没有单词信息
            lines = block["lines"]  # 获取块中的文本行
            for line in lines:  # 遍历文本行
                bbox = line["bbox"]  # 获取行边界框
                words = []  # 初始化单词列表
                words_bboxes = []  # 初始化单词边界框列表
                for span in line["spans"]:  # 遍历文本跨度 (span)
                    cont_bboxes = []  # 初始化连续字符边界框列表
                    cont_text = []  # 初始化连续字符文本列表
                    for char in span["chars"]:  # 遍历字符
                        c = char["c"]  # 获取字符
                        if c == " ":  # 如果字符是空格
                            if cont_bboxes:  # 如果有连续字符边界框
                                word_bbox = merge_rects(np.asarray(cont_bboxes))  # 合并连续字符边界框为单词边界框
                                word = "".join(cont_text)  # 连接连续字符文本为单词
                                words.append(word)  # 添加单词到单词列表
                                words_bboxes.append(word_bbox)  # 添加单词边界框到单词边界框列表
                                cont_bboxes = []  # 清空连续字符边界框列表
                                cont_text = []  # 清空连续字符文本列表
                        else:  # 如果字符不是空格
                            cont_bboxes.append(char["bbox"])  # 添加字符边界框到连续字符边界框列表
                            cont_text.append(c)  # 添加字符到连续字符文本列表
                    if cont_bboxes:  # 如果跨度结束后还有连续字符边界框
                        word_bbox = merge_rects(np.asarray(cont_bboxes))  # 合并连续字符边界框为单词边界框
                        word = "".join(cont_text)  # 连接连续字符文本为单词
                        words.append(word)  # 添加单词到单词列表
                        words_bboxes.append(word_bbox)  # 添加单词边界框到单词边界框列表
                if not words_bboxes:  # 如果没有单词边界框，则跳过当前行
                    continue
                line_words_info.append((words, words_bboxes))  # 添加单词信息到文本行单词信息列表
                line_text = "".join([char["c"] for span in line["spans"] for char in span["chars"]])  # 连接所有字符为行文本
                bb0, bb1, bb2, bb3 = merge_rects(np.asarray(words_bboxes))  # 合并单词边界框为行边界框
                block_info = BlockInfo([bb0, bb1, bb2, bb3], line_text, block_no, block_type)  # 创建 BlockInfo 对象
                line_blocks.append(block_info)  # 添加块信息到文本行块信息列表
        return line_blocks, line_words_info  # 返回文本行块信息列表和文本行单词信息列表

    def _extract_lines(self, textpage):
        """
        使用 extractDICT() 方法从 textpage 中提取文本行信息。
        Args:
            textpage: pymupdf 文本页对象。
        Returns:
            tuple: (文本行块信息列表, 文本行单词信息列表)。
        """
        line_blocks = []  # 初始化文本行块信息列表
        line_words_info = []  # 初始化文本行单词信息列表
        page_dict = textpage.extractDICT()  # 使用 extractDICT() 方法提取字典数据
        for block in page_dict["blocks"]:  # 遍历页面块
            block_type = block["type"]  # 获取块类型
            block_no = block["number"]  # 获取块编号
            if block_type != 0:  # 如果块类型不为 0 (非文本块)
                bbox = block["bbox"]  # 获取块边界框
                block_text = ""  # 初始化块文本为空字符串
                block_info = BlockInfo(  # 创建 BlockInfo 对象
                    [bbox[0], bbox[1], bbox[2], bbox[3]], block_text, block_no, block_type)
                line_blocks.append(block_info)  # 添加块信息到文本行块信息列表
                line_words_info.append((None, None))  # 添加 (None, None) 到文本行单词信息列表，表示非文本块没有单词信息
            lines = block["lines"]  # 获取块中的文本行
            for line in lines:  # 遍历文本行
                bbox = line["bbox"]  # 获取行边界框
                line_text = []  # 初始化行文本列表
                words = [span["text"] for span in line["spans"]]  # 获取行中所有跨度的文本列表，作为单词列表
                words_bbox = [span["bbox"] for span in line["spans"]]  # 获取行中所有跨度的边界框列表，作为单词边界框列表
                line_words_info.append((words, words_bbox))  # 添加单词信息到文本行单词信息列表
                line_text = "".join([span["text"] for span in line["spans"]])  # 连接所有跨度文本为行文本
                block_info = BlockInfo(  # 创建 BlockInfo 对象
                    [bbox[0], bbox[1], bbox[2], bbox[3]], line_text, block_no, block_type)
                line_blocks.append(block_info)  # 添加块信息到文本行块信息列表
        return line_blocks, line_words_info  # 返回文本行块信息列表和文本行单词信息列表

    def _extract_blocks(self, textpage, lang):
        """
        使用 extractDICT() 方法从 textpage 中提取文本块信息。
        Args:
            textpage: pymupdf 文本页对象。
            lang: 语言类型，用于文本行连接。
        Returns:
            tuple: (文本块信息列表, 文本块单词信息列表)。
        """
        blocks = []  # 初始化文本块信息列表
        blocks_words_info = []  # 初始化文本块单词信息列表
        page_dict = textpage.extractDICT()  # 使用 extractDICT() 方法提取字典数据
        for block in page_dict["blocks"]:  # 遍历页面块
            block_type = block["type"]  # 获取块类型
            block_no = block["number"]  # 获取块编号
            block_bbox = block["bbox"]  # 获取块边界框
            if block_type != 0:  # 如果块类型不为 0 (非文本块)
                block_text = ""  # 初始化块文本为空字符串
                block_info = BlockInfo(  # 创建 BlockInfo 对象
                    [block_bbox[0], block_bbox[1], block_bbox[2], block_bbox[3]], block_text, block_no, block_type, )
                blocks.append(block_info)  # 添加块信息到文本块信息列表
                blocks_words_info.append((None, None))  # 添加 (None, None) 到文本块单词信息列表，表示非文本块没有单词信息
            lines = block["lines"]  # 获取块中的文本行
            block_words = []  # 初始化块单词列表
            block_words_bbox = []  # 初始化块单词边界框列表
            block_lines = []  # 初始化块文本行列表
            for line in lines:  # 遍历文本行
                block_words.extend([span["text"] for span in line["spans"]])  # 添加行中所有跨度的文本到块单词列表
                block_words_bbox.extend([span["bbox"] for span in line["spans"]])  # 添加行中所有跨度的边界框到块单词边界框列表
                line_text = "".join([span["text"] for span in line["spans"]])  # 连接所有跨度文本为行文本
                block_lines.append(line_text)  # 添加行文本到块文本行列表
            block_text = join_lines(block_lines, False, lang)  # 连接块文本行，得到块文本
            block_info = BlockInfo(  # 创建 BlockInfo 对象
                [block_bbox[0], block_bbox[1], block_bbox[2], block_bbox[3]], block_text, block_no, block_type, )
            blocks.append(block_info)  # 添加块信息到文本块信息列表
            blocks_words_info.append((block_words, block_words_bbox))  # 添加单词信息到文本块单词信息列表
        return blocks, blocks_words_info  # 返回文本块信息列表和文本块单词信息列表

    def _extract_blocks_from_image(self, b64_image, img):
        """
        从图像中提取文本块信息，使用 OCR Agent 进行文本识别。
        Args:
            b64_image: Base64 编码的图像数据。
            img: PIL.Image.Image 对象。
        Returns:
            tuple: (文本块信息列表, 文本块单词信息列表)。
        """
        inp = {"b64_image": b64_image}  # 构建 OCR Agent 的输入
        if self.support_formula:  # 如果支持公式识别
            # 步骤 1. 公式检测
            # 步骤 2. 裁剪公式区域并调用公式识别
            # 步骤 3. 遮盖公式区域并调用通用 OCR
            # 步骤 4. 通过嵌入公式区域分割文本行
            # 步骤 5. 识别分割后的行区域
            # 步骤 6. 合并分割后的行区域并按 tlbr 排序
            inp = {"b64_image": b64_image}  # 构建公式识别 Agent 的输入
            mf_outs = self.formula_agent.predict(inp, img, enable_isolated_formula=self.enable_isolated_formula)  # 调用公式识别 Agent 进行预测
            texts, bboxes, words_info = self.ocr_agent.predict_with_mask(img, mf_outs)  # 使用带掩码的 OCR Agent 进行预测，遮盖公式区域
        else:  # 如果不支持公式识别
            # 获取通用 OCR 结果
            ocr_result = self.ocr_agent.predict(inp)  # 调用 OCR Agent 进行预测
            texts = ocr_result["result"]["ocr_result"]["texts"]  # 获取识别出的文本列表
            bboxes = ocr_result["result"]["ocr_result"]["bboxes"]  # 获取识别出的边界框列表
            words_info = []  # 初始化单词信息列表为空列表
        blocks = []  # 初始化文本块信息列表
        blocks_words_info = []  # 初始化文本块单词信息列表
        block_type = 0  # 初始化块类型为 0
        for i in range(len(texts)):  # 遍历识别出的文本
            block_no = i  # 设置块编号为索引
            block_text = texts[i]  # 获取文本内容
            b0, b1, b2, b3 = get_hori_rect(bboxes[i])  # 获取水平边界框
            block_type = 0  # 默认块类型为 0
            if words_info:  # 如果有单词信息
                if "isolated" in words_info[i][2]:  # 如果单词信息中包含 "isolated" 标签，则表示是独立公式
                    block_type = 1000  # 设置块类型为 1000，表示独立公式
            block_info = BlockInfo([b0, b1, b2, b3], block_text, block_no, block_type)  # 创建 BlockInfo 对象
            blocks.append(block_info)  # 添加块信息到文本块信息列表
            if not words_info:  # 如果没有单词信息
                blocks_words_info.append(([block_text], [[b0, b1, b2, b3]]))  # 创建单词信息，只包含块文本和块边界框
            else:  # 如果有单词信息
                blocks_words_info.append((words_info[i][0], words_info[i][1]))  # 添加单词信息
        return blocks, blocks_words_info  # 返回文本块信息列表和文本块单词信息列表

    def _enhance_table_layout(self, b64_image, layout_blocks):
        """
        增强表格布局，使用独立的表格检测模型来提高表格检测的准确性。
        Args:
            b64_image: Base64 编码的图像数据。
            layout_blocks: 布局检测模型输出的布局块信息。
        Returns:
            tuple: (语义多边形列表, 语义标签列表, 语义表格类别列表)。
        """
        TABLE_ID = 5  # 表格布局类型 ID
        inp = {"b64_image": b64_image}  # 构建表格检测 Agent 的输入
        result = self.table_det_agent.predict(inp)  # 调用表格检测 Agent 进行预测
        # 1: cell 单元格， 2: rowcol 行列
        DEFAULT_TABLE_CATE = 2  # 默认表格类别为行列
        table_layout_cats = []  # 初始化表格布局类别列表
        table_layout = []  # 初始化表格布局信息列表
        for i, bb in enumerate(result["bboxes"]):  # 遍历表格检测结果的边界框
            coords = ((bb[0], bb[1]), (bb[2], bb[3]), (bb[4], bb[5]), (bb[6], bb[7]))  # 构建多边形坐标
            poly = Polygon(coords)  # 创建多边形对象
            table_layout.append((poly, TABLE_ID))  # 添加多边形和表格布局类型 ID 到表格布局信息列表
            if "labels" in result:  # 如果检测结果包含标签信息
                table_layout_cats.append(result["labels"][i])  # 添加标签到表格布局类别列表
            else:  # 如果检测结果不包含标签信息
                table_layout_cats.append(DEFAULT_TABLE_CATE)  # 使用默认表格类别
        general_table_layout = []  # 初始化通用表格布局信息列表
        result_layout = []  # 初始化结果布局信息列表
        for e in layout_blocks["result"]:  # 遍历布局检测模型输出的布局块信息
            bb = e["bbox"]  # 获取布局块边界框
            coords = ((bb[0], bb[1]), (bb[2], bb[3]), (bb[4], bb[5]), (bb[6], bb[7]))  # 构建多边形坐标
            poly = Polygon(coords)  # 创建多边形对象
            label = e["category_id"]  # 获取布局块类别 ID
            if label == TABLE_ID:  # 如果布局块类别为表格
                general_table_layout.append((poly, label))  # 添加多边形和表格布局类型 ID 到通用表格布局信息列表
            else:  # 如果布局块类别不是表格
                result_layout.append((poly, label))  # 添加多边形和布局块类别 ID 到结果布局信息列表
        # 将通用表格布局与特定表格布局合并
        OVERLAP_THRESHOLD = 0.7  # 重叠阈值
        mask = np.zeros(len(general_table_layout))  # 初始化掩码数组，用于标记通用表格布局是否与特定表格布局重叠
        for i, (poly0, cate0) in enumerate(general_table_layout):  # 遍历通用表格布局信息列表
            for poly1, _ in table_layout:  # 遍历特定表格布局信息列表
                biou = poly0.intersection(poly1).area * 1.0 / poly1.area  # 计算交并比 (BIoU)
                if biou >= OVERLAP_THRESHOLD:  # 如果交并比大于或等于阈值，则表示重叠
                    mask[i] = 1  # 标记为重叠
                    break
        semantic_table_cate = [  # 初始化语义表格类别列表
                                  None, ] * len(result_layout) + table_layout_cats  # 将结果布局信息列表的长度填充为 None，然后添加特定表格布局类别列表
        for e in table_layout:  # 遍历特定表格布局信息列表
            result_layout.append(e)  # 将特定表格布局信息添加到结果布局信息列表
        # 禁用布局中的表格信息
        # for i, e in enumerate(general_table_layout):
        #     if mask[i] == 0:
        #         result_layout.append(e)
        #         semantic_table_cate.append(DEFAULT_TABLE_CATE)
        semantic_polys = [e[0] for e in result_layout]  # 提取结果布局信息列表中的多边形列表，作为语义多边形列表
        semantic_labels = [e[1] for e in result_layout]  # 提取结果布局信息列表中的标签列表，作为语义标签列表
        return semantic_polys, semantic_labels, semantic_table_cate  # 返回语义多边形列表、语义标签列表和语义表格类别列表

    def _enhance_texts_info_with_formula(self, b64_image, img, textpage_info):
        """
        使用公式识别增强文本信息，将公式区域从文本块中分离出来。
        Args:
            b64_image: Base64 编码的图像数据。
            img: PIL.Image.Image 对象。
            textpage_info: 文本页信息，可以是文本块信息或文本行信息。
        Returns:
            list: 增强后的文本块信息列表。
        """
        if self.support_formula:  # 如果支持公式识别
            blocks, words = self.formula_agent.predict_with_text_block(b64_image, img, textpage_info, enable_isolated_formula=self.enable_isolated_formula,
                ocr_agent=self.ocr_agent, )  # 调用公式识别 Agent，并结合 OCR Agent 进行预测，分离公式区域
            return blocks, words  # 返回增强后的文本块信息列表和单词信息列表
        else:  # 如果不支持公式识别
            return textpage_info  # 直接返回原始文本页信息

    def _allocate_semantic(self, textpage_info, layout, b64_image, img, is_scan=True, lang="zh", rot_matrix=None):
        """
        根据布局信息和语义信息，为文本块分配语义标签。
        Args:
            textpage_info: 文本页信息，可以是文本块信息或文本行信息。
            layout: 布局检测模型输出的布局信息。
            b64_image: Base64 编码的图像数据。
            img: PIL.Image.Image 对象.
            is_scan: 是否为扫描文档，默认为 True。
            lang: 语言类型，默认为 "zh" (中文)。
            rot_matrix: 旋转矩阵，用于处理旋转页面，默认为 None。
        Returns:
            list: 分配了语义标签的文本块信息列表。
        """
        class_name = ["印章", "图片", "标题", "段落", "表格", "页眉", "页码", "页脚"]  # 布局类别名称列表
        effective_class_inds = [3, 4, 5, 999, 1000]  # 有效的布局类别 ID 列表
        non_conti_class_ids = [6, 7, 8]  # 非连续布局类别 ID 列表
        TEXT_ID = 4  # 文本布局类型 ID
        TABLE_ID = 5  # 表格布局类型 ID
        IMAGE_ID = 2  # 图片布局类型 ID
        LAYOUT_ID = 6  # 布局类型 ID (注释中未使用)
        FORMULA_ID = 1000  # 公式布局类型 ID
        timer = Timer()  # 创建计时器对象
        if not is_scan:  # 如果不是扫描文档，则从文本页信息中提取文本块和单词信息 (针对矢量 PDF)
            # textpage = page.get_textpage()
            # blocks = textpage.extractBLOCKS()
            # blocks, words = self._extract_blocks(textpage)
            # blocks, words = self._extract_lines(textpage)
            # blocks, words = self._extract_lines_v2(textpage)
            # blocks, words = textpage_info
            blocks, words = self._enhance_texts_info_with_formula(b64_image, img, textpage_info)  # 使用公式识别增强文本页信息
        else:  # 如果是扫描文档，则从图像中提取文本块和单词信息 (针对扫描 PDF 或图像)
            blocks, words = self._extract_blocks_from_image(b64_image, img)  # 从图像中提取文本块和单词信息
        timer.toc()  # 记录时间
        # print('---line blocks---')
        # for b in blocks:
        #     print(b)
        # 短语 0. 支持旋转的 PDF 页面，某些 PDF 页面是旋转的
        # 并且旋转矩阵存储在布局中，首先旋转它
        if self.support_rotate and is_scan:  # 如果支持旋转页面且为扫描文档
            rotation_matrix = np.asarray(rot_matrix).reshape((3, 2))  # 将旋转矩阵转换为 numpy 数组并 reshape 为 (3, 2)
            c1 = (rotation_matrix[0, 0] - 1) <= 1e-6  # 判断旋转矩阵的第一个元素是否接近 1
            c2 = (rotation_matrix[1, 1] - 1) <= 1e-6  # 判断旋转矩阵的第五个元素是否接近 1
            is_rotated = c1 and c2  # 如果 c1 和 c2 都为 True，则表示页面没有旋转
            # print('c1/c2', c1, c2)
            if is_rotated:  # 如果页面没有旋转 (实际上这里的逻辑是判断是否需要旋转，is_rotated 命名可能存在歧义)
                # new_blocks = []
                new_words = []  # 初始化新的单词信息列表
                for b, w in zip(blocks, words):  # 遍历文本块信息列表和单词信息列表
                    bbox = np.asarray(b.bbox)  # 获取文本块边界框
                    aug_bbox = bbox.reshape((-1, 2))  # reshape 为 (N, 2)
                    padding = np.ones((len(aug_bbox), 1))  # 创建填充列，值为 1
                    aug_bbox = np.hstack([aug_bbox, padding])  # 水平堆叠，得到增广的边界框坐标
                    bb = np.dot(aug_bbox, rotation_matrix).reshape(-1)  # 应用旋转矩阵
                    bb = norm_rect(bb)  # 规范化边界框
                    b.bbox = [bb[0], bb[1], bb[2], bb[3]]  # 更新文本块边界框
                    # 处理单词信息
                    words_text, words_bb = w  # 获取单词文本列表和单词边界框列表
                    if words_bb is None:  # 如果单词边界框列表为 None，则跳过
                        new_words.append(w)  # 直接添加原始单词信息
                        continue
                    new_words_bb = []  # 初始化新的单词边界框列表
                    for w_b in words_bb:  # 遍历单词边界框列表
                        bbox = np.asarray(w_b)  # 获取单词边界框
                        aug_bbox = bbox.reshape((-1, 2))  # reshape 为 (N, 2)
                        padding = np.ones((len(aug_bbox), 1))  # 创建填充列，值为 1
                        aug_bbox = np.hstack([aug_bbox, padding])  # 水平堆叠，得到增广的边界框坐标
                        bb = np.dot(aug_bbox, rotation_matrix).reshape(-1)  # 应用旋转矩阵
                        bb = norm_rect(bb).tolist()  # 规范化边界框并转换为列表
                        new_words_bb.append(bb)  # 添加到新的单词边界框列表
                    new_words.append((words_text, new_words_bb))  # 添加到新的单词信息列表
                # blocks = new_blocks
                words = new_words  # 更新单词信息列表
        timer.toc()  # 记录时间
        # if not self.with_columns:
        #     blocks = order_by_tbyx(blocks)
        # print('---ori blocks---')
        # for b in blocks:
        #     print(b)
        IMG_BLOCK_TYPE = 1  # 图片块类型 ID
        text_ploys = []  # 初始化文本多边形列表
        text_rects = []  # 初始化文本边界框列表
        texts = []  # 初始化文本列表
        for b in blocks:  # 遍历文本块信息列表
            texts.append(b.block_text)  # 添加文本块内容到文本列表
            text_ploys.append(Rect(*b.bbox))  # 创建矩形多边形对象并添加到文本多边形列表
            text_rects.append(b.bbox)  # 添加文本块边界框到文本边界框列表
        text_rects = np.asarray(text_rects)  # 转换为 numpy 数组
        texts = np.asarray(texts)  # 转换为 numpy 数组
        semantic_polys = []  # 初始化语义多边形列表
        semantic_labels = []  # 初始化语义标签列表
        # 增强表格布局，布局模型中的表格布局不是很准确，
        # 使用独立的表格检测模型来增强
        layout_info = layout  # 获取布局信息
        # print('layout_info', layout_info)
        if self.enhance_table:  # 如果增强表格识别
            semantic_polys, semantic_labels, semantic_table_cate = self._enhance_table_layout(b64_image, layout)  # 使用表格检测模型增强表格布局
        else:  # 如果不增强表格识别，则直接使用布局检测模型输出的布局信息
            for info in layout_info["result"]:  # 遍历布局信息结果
                bbs = info["bbox"]  # 获取布局块边界框
                coords = ((bbs[0], bbs[1]), (bbs[2], bbs[3]), (bbs[4], bbs[5]), (bbs[6], bbs[7]))  # 构建多边形坐标
                semantic_polys.append(Polygon(coords))  # 创建多边形对象并添加到语义多边形列表
                semantic_labels.append(info["category_id"])  # 添加布局块类别 ID 到语义标签列表
            semantic_table_cate = [  # 初始化语义表格类别列表，所有元素默认为 2
                                      2, ] * len(semantic_labels)  # 长度与语义标签列表相同
        # print("---semantic_table_cate", semantic_table_cate)
        timer.toc()  # 记录时间
        # 短语 1. 通过包含矩阵合并连续文本块
        # 1) 计算语义边界框和文本边界框之间的重叠
        # 2) 查找最大连续文本块，并设置阈值保持
        # 3) 合并连续文本块
        # 4) 获取新的文本块
        semantic_bboxes = []  # 初始化语义边界框列表
        for poly in semantic_polys:  # 遍历语义多边形列表
            x, y = poly.exterior.coords.xy  # 获取多边形外部坐标
            semantic_bboxes.append([x[0], y[0], x[1], y[1], x[2], y[2], x[3], y[3]])  # 提取坐标并添加到语义边界框列表
        # 计算包含重叠率
        sem_cnt = len(semantic_polys)  # 获取语义多边形数量
        texts_cnt = len(text_ploys)  # 获取文本多边形数量
        contain_matrix = np.zeros((sem_cnt, texts_cnt))  # 初始化包含矩阵，用于存储语义多边形包含文本多边形的重叠率
        for i in range(sem_cnt):  # 遍历语义多边形
            for j in range(texts_cnt):  # 遍历文本多边形
                inter = semantic_polys[i].intersection(text_ploys[j]).area  # 计算交集面积
                contain_matrix[i, j] = inter * 1.0 / text_ploys[j].area  # 计算包含重叠率，交集面积 / 文本多边形面积
        # print('----------------containing matrix--------')
        # for r in contain_matrix.tolist():
        #     print([round(r_, 2) for r_ in r])
        # print('---text---')
        # for t in texts:
        #     print(t)
        CONTRAIN_THRESHOLD = 0.70  # 包含重叠率阈值
        contain_info = []  # 初始化包含信息列表
        for i in range(sem_cnt):  # 遍历语义多边形
            ind = np.argwhere(contain_matrix[i, :] > CONTRAIN_THRESHOLD)[:, 0]  # 查找包含重叠率大于阈值的文本多边形索引
            if len(ind) == 0:  # 如果没有找到符合条件的文本多边形，则跳过当前语义多边形
                continue
            label = semantic_labels[i]  # 获取语义标签
            if label in non_conti_class_ids:  # 如果语义标签是非连续布局类别 (页眉/页码/页脚)
                n = len(ind)  # 获取符合条件的文本多边形数量
                contain_info.append((None, None, n, label, ind))  # 添加包含信息，起始索引和结束索引为 None，表示非连续，数量为 n，标签为 label，索引为 ind
            else:  # 如果语义标签是连续布局类别 (文本/表格/图片)
                start, n = find_max_continuous_seq(ind)  # 查找索引数组中的最大连续序列
                if n >= 1:  # 如果连续序列长度大于等于 1
                    contain_info.append((start, start + n, n, label, None))  # 添加包含信息，起始索引为 start，结束索引为 start + n，数量为 n，标签为 label，索引为 None (连续区域索引后续确定)
        contain_info = sorted(contain_info, key=lambda x: x[2], reverse=True)  # 对包含信息列表按数量降序排序
        mask = np.zeros(texts_cnt)  # 初始化掩码数组，用于标记文本多边形是否已被处理
        new_block_info = []  # 初始化新的文本块信息列表
        for info in contain_info:  # 遍历包含信息列表
            start, end, n, label, ind = info  # 解包包含信息
            if label in non_conti_class_ids and np.all(mask[ind] == 0):  # 如果是非连续布局类别且对应的文本多边形未被处理
                rect = merge_rects(text_rects[ind])  # 合并对应的文本边界框
                ori_orders = [blocks[i].block_no for i in ind]  # 获取原始文本块的编号列表
                ts = texts[ind]  # 获取对应的文本列表
                rs = text_rects[ind]  # 获取对应的文本边界框列表
                ord_ind = np.min(ori_orders)  # 获取最小的原始文本块编号作为顺序索引
                mask[ind] = 1  # 标记对应的文本多边形已被处理
                new_block_info.append(BlockInfo([rect[0], rect[1], rect[2], rect[3]], "", -1, -1, ts, rs, ind, ord_ind)
                    # 创建新的 BlockInfo 对象，不包含块文本，类型为 -1 (未分配)，原始索引为 ind，顺序索引为 ord_ind
                )
                max_block_type = np.max([blocks[i].block_type for i in ind])  # 获取原始文本块的最大类型
                if max_block_type == FORMULA_ID:  # 如果原始文本块中包含公式
                    new_block_info[-1].layout_type = FORMULA_ID  # 将新块的布局类型设置为公式
            elif np.all(mask[start:end] == 0):  # 如果是连续布局类别且对应的文本多边形未被处理
                rect = merge_rects(text_rects[start:end])  # 合并对应的文本边界框
                ori_orders = [blocks[i].block_no for i in range(start, end)]  # 获取原始文本块的编号列表
                arg_ind = np.argsort(ori_orders)  # 获取排序后的索引
                # print('ori_orders', ori_orders, arg_ind)
                ord_ind = np.min(ori_orders)  # 获取最小的原始文本块编号作为顺序索引
                ts = texts[start:end]  # 获取对应的文本列表
                rs = text_rects[start:end]  # 获取对应的文本边界框列表
                if label == TABLE_ID:  # 如果是表格
                    ts = ts[arg_ind]  # 对文本列表进行排序，保持原始顺序
                    rs = rs[arg_ind]  # 对边界框列表进行排序，保持原始顺序
                pos = np.arange(start, end)  # 创建索引范围
                mask[start:end] = 1  # 标记对应的文本多边形已被处理
                new_block_info.append(BlockInfo([rect[0], rect[1], rect[2], rect[3]], "", -1, -1, ts, rs, pos, ord_ind)
                    # 创建新的 BlockInfo 对象，不包含块文本，类型为 -1 (未分配)，原始索引为 pos，顺序索引为 ord_ind
                )
                max_block_type = np.max([blocks[i].block_type for i in pos])  # 获取原始文本块的最大类型
                if max_block_type == FORMULA_ID:  # 如果原始文本块中包含公式
                    new_block_info[-1].layout_type = FORMULA_ID  # 将新块的布局类型设置为公式
        for i in range(texts_cnt):  # 遍历所有文本多边形
            if mask[i] == 0:  # 如果文本多边形未被处理 (独立的文本块)
                b = blocks[i]  # 获取原始文本块信息
                r = np.asarray(b.bbox)  # 获取原始文本块边界框
                ord_ind = b.block_no  # 获取原始文本块编号作为顺序索引
                new_block_info.append(
                    BlockInfo(b.bbox, "", -1, -1, [texts[i]], [r], [i], ord_ind))  # 创建新的 BlockInfo 对象，包含原始边界框，不包含块文本，类型为 -1 (未分配)，文本和边界框列表只包含当前文本块，原始索引为 i，顺序索引为 ord_ind
                if b.block_type == FORMULA_ID:  # 如果原始文本块类型为公式
                    new_block_info[-1].layout_type = FORMULA_ID  # 将新块的布局类型设置为公式
        timer.toc()  # 记录时间
        if self.with_columns:  # 如果支持分栏布局
            new_blocks = sorted(new_block_info, key=lambda x: x.ord_ind)  # 按顺序索引排序
        else:  # 如果不支持分栏布局
            new_blocks = order_by_tbyx(new_block_info)  # 按从上到下，从左到右排序
        # print('\n\n---new blocks---')
        # for idx, b in enumerate(new_blocks):
        #     print(idx, b)
        text_ploys = []  # 初始化文本多边形列表
        # texts = []
        for b in new_blocks:  # 遍历新的文本块信息列表
            # texts.append(b.ts)
            text_ploys.append(Rect(*b.bbox))  # 创建矩形多边形对象并添加到文本多边形列表
        # 计算重叠率
        sem_cnt = len(semantic_polys)  # 获取语义多边形数量
        texts_cnt = len(text_ploys)  # 获取文本多边形数量
        overlap_matrix = np.zeros((sem_cnt, texts_cnt))  # 初始化重叠矩阵，用于存储语义多边形和文本多边形之间的重叠率
        for i in range(sem_cnt):  # 遍历语义多边形
            for j in range(texts_cnt):  # 遍历文本多边形
                inter = semantic_polys[i].intersection(text_ploys[j]).area  # 计算交集面积
                union = semantic_polys[i].union(text_ploys[j]).area  # 计算并集面积
                overlap_matrix[i, j] = (inter * 1.0) / union  # 计算重叠率，交集面积 / 并集面积
        # print('---overlap_matrix---')
        # for r in overlap_matrix:
        #     print([round(r_, 3) for r_ in r])
        # print('---semantic_labels---', semantic_labels)
        # 短语 2. 通过布局信息分配标签
        # 1) 计算语义边界框和合并后的块边界框之间的重叠率
        # 2) 查找重叠率最高的语义标签，并分配它
        # 3) 对于表格，解析表格布局
        # 4) 对于公式，保持不变
        OVERLAP_THRESHOLD = 0.2  # 重叠率阈值
        # texts_labels = []
        DEF_SEM_LABEL = 999  # 默认语义标签，用于未匹配到语义标签的文本块
        FORMULA_LABEL = 1000  # 公式语义标签
        table_infos = []  # 初始化表格信息列表
        for j in range(texts_cnt):  # 遍历文本多边形
            ind = np.argwhere(overlap_matrix[:, j] > OVERLAP_THRESHOLD)[:, 0]  # 查找重叠率大于阈值的语义多边形索引
            if len(ind) == 0:  # 如果没有找到符合条件的语义多边形
                sem_label = DEF_SEM_LABEL  # 使用默认语义标签
            else:  # 如果找到了符合条件的语义多边形
                c = Counter([semantic_labels[i] for i in ind])  # 统计重叠的语义标签计数
                items = c.most_common()  # 获取计数最多的语义标签
                sem_label = items[0][0]  # 获取计数最多的语义标签
                if len(items) > 1 and TEXT_ID in dict(items):  # 如果有多个语义标签且包含文本标签
                    sem_label = TEXT_ID  # 优先使用文本标签
            # 不要再次分配独立的公式块
            if new_blocks[j].layout_type == FORMULA_ID:  # 如果已经是公式类型，则跳过
                continue
            if sem_label == TABLE_ID:  # 如果语义标签是表格
                b = new_blocks[j]  # 获取文本块信息
                # b_inds = b[-2]
                b_inds = b.ind  # 获取原始文本块索引
                texts = []  # 初始化表格单元格文本列表
                bboxes = []  # 初始化表格单元格边界框列表
                for k in b_inds:  # 遍历原始文本块索引
                    for t, b_ in zip(words[k][0], words[k][1]):  # 遍历原始文本块的单词信息
                        if not t.strip():  # 如果单词文本为空，则跳过
                            continue
                        texts.append(t)  # 添加单词文本到表格单元格文本列表
                        bboxes.append(b_)  # 添加单词边界框到表格单元格边界框列表
                table_bbox = semantic_bboxes[ind[0]]  # 获取表格语义边界框
                table_cate = semantic_table_cate[ind[0]]  # 获取表格语义类别
                table_infos.append((j, texts, bboxes, table_bbox, table_cate))  # 添加表格信息到表格信息列表
            new_blocks[j].layout_type = sem_label  # 分配语义标签给文本块  # texts_labels.append(sem_label)
        timer.toc()  # 记录时间
        # 解析表格布局
        table_layout = []  # 初始化表格布局列表
        for table_info in table_infos:  # 遍历表格信息列表
            block_ind, texts, bboxes, table_bbox, table_cate = table_info  # 解包表格信息
            if not texts:  # 如果表格单元格文本列表为空，则跳过
                continue
            ocr_result = {"texts": texts, "bboxes": rect2polygon(bboxes)}  # 构建表格结构识别模型的 OCR 输入
            scene = "cell" if table_cate == 1 else "rowcol"  # 根据表格类别设置场景，cell: 单元格表格, rowcol: 行列表格
            inp = {"b64_image": b64_image, "ocr_result": json.dumps(ocr_result), "table_bboxes": [table_bbox], "scene": scene, }  # 构建表格结构识别模型的输入
            table_result = self.table_agent.predict(inp)  # 调用表格结构识别模型进行预测
            # print('---table--', ocr_result, table_bbox, table_result)
            h_bbox = get_hori_rect(table_bbox)  # 获取水平表格边界框
            if not table_result["htmls"]:  # 如果表格结构识别失败
                # 表格布局解析失败，手动构建表格
                b = new_blocks[block_ind]  # 获取文本块信息
                html = transform_list_to_table(b.ts)  # 将文本行列表转换为 HTML 表格
                table_layout.append((block_ind, html, h_bbox))  # 添加表格布局信息到表格布局列表，包含块索引，HTML 代码和水平边界框  # print('---missing table---', block_ind, html)
            else:  # 如果表格结构识别成功
                table_layout.append((block_ind, table_result["htmls"][0], h_bbox))  # 添加表格布局信息到表格布局列表，包含块索引，HTML 代码和水平边界框
        for i, table_html, h_bbox in table_layout:  # 遍历表格布局列表
            table_md = transform_html_table_to_md(table_html)  # 将 HTML 表格转换为 Markdown 表格
            text = table_md["text"]  # 获取 Markdown 文本
            html = table_md["html"]  # 获取 HTML 代码
            b = new_blocks[i]  # 获取文本块信息
            b.bbox = [h_bbox[0], h_bbox[1], h_bbox[2], h_bbox[3]]  # 更新文本块边界框为水平边界框
            b.layout_type = TABLE_ID  # 设置布局类型为表格
            b.html_text = html  # 设置 HTML 文本
            b.block_text = text  # 设置块文本为 Markdown 文本
        timer.toc()  # 记录时间
        # print(texts_labels)
        # 过滤未使用的元素
        filtered_blocks = []  # 初始化过滤后的文本块列表
        for b in new_blocks:  # 遍历新的文本块信息列表
            # ori_i = b[6][0]
            # ori_b = blocks[ori_i]
            # block_type = ori_b[-1]
            # 过滤真实 PDF 中的图像块
            if b.block_type == IMG_BLOCK_TYPE:  # 如果是图像块，则跳过
                continue
            # 过滤空文本块
            if np.all([len(t) == 0 for t in b.ts]):  # 如果文本行列表中的所有文本都为空，则跳过
                continue
            label = b.layout_type  # 获取布局类型
            if label == TABLE_ID:  # 如果是表格
                filtered_blocks.append(b)  # 添加到过滤后的文本块列表
            # elif label == LAYOUT_ID:
            #     b.block_text = join_lines(b.ts, False, lang)
            #     filtered_blocks.append(b)
            elif label == IMAGE_ID:  # 如果是图片
                if self.keep_text_in_image:  # 如果保留图片中的文本
                    b.block_text = join_lines(b.ts, False, lang)  # 连接文本行
                    filtered_blocks.append(b)  # 添加到过滤后的文本块列表
            elif label in effective_class_inds:  # 如果是有效的布局类别 (文本/标题/段落等)
                b.block_text = join_lines(b.ts, False, lang)  # 连接文本行
                filtered_blocks.append(b)  # 添加到过滤后的文本块列表
        # print('---filtered_blocks---')
        # for b in filtered_blocks:
        #     print(b)
        timer.toc()  # 记录时间
        # print('_allocate_semantic', timer.get())
        return filtered_blocks  # 返回过滤后的文本块列表

    def _divide_blocks_into_groups(self, blocks):
        """
        将文本块划分为组，用于处理分栏布局。
        Args:
            blocks: 文本块信息列表。
        Returns:
            list: 分组后的文本块列表，每个元素为一个文本块组。
        """
        # 仅支持纯粹的两栏布局，每栏宽度相同
        rects = np.asarray([b.bbox for b in blocks])  # 获取所有文本块的边界框
        min_x0 = np.min(rects[:, 0])  # 获取最小的 x0 坐标
        max_x1 = np.max(rects[:, 2])  # 获取最大的 x1 坐标
        root_seg = (min_x0, max_x1)  # 创建根线段，覆盖整个页面宽度
        root_pc = (min_x0 + max_x1) / 2  # 计算页面中心 x 坐标
        root_offset = 20  # 中心偏移量
        center_seg = (root_pc - root_offset, root_pc + root_offset)  # 创建中心线段
        segment = Segment(root_seg)  # 创建 Segment 对象，表示页面宽度线段
        for r in rects:  # 遍历所有文本块边界框
            segment.add((r[0], r[2]))  # 将文本块的水平线段添加到 Segment 对象中，用于分割列
        COLUMN_THRESHOLD = 0.90  # 列覆盖率阈值
        CENTER_GAP_THRESHOLD = 0.90  # 中心间隙阈值
        free_segs = segment.get_free_segment()  # 获取自由线段，即列之间的间隙
        columns = []  # 初始化列线段列表
        if len(free_segs) == 1 and len(segment.segs) == 2:  # 如果只有一个自由线段且有两个子线段 (分割线)
            free_seg = free_segs[0]  # 获取自由线段
            seg0 = segment.segs[0]  # 获取第一个子线段
            seg1 = segment.segs[1]  # 获取第二个子线段
            cover = seg0[1] - seg0[0] + seg1[1] - seg1[0]  # 计算两列的总宽度
            c0 = cover / (root_seg[1] - root_seg[0])  # 计算列覆盖率
            c1 = Segment.contain(center_seg, free_seg)  # 判断自由线段是否包含在中心线段中，即间隙是否在页面中心
            if c0 > COLUMN_THRESHOLD and c1:  # 如果列覆盖率大于阈值且间隙在页面中心，则认为是两栏布局
                # 两栏布局
                columns.extend([seg0, seg1])  # 添加列线段到列线段列表
        groups = [blocks]  # 默认分组，所有文本块在一个组中
        if columns:  # 如果检测到分栏布局
            groups = [[] for _ in columns]  # 初始化分组列表，每个列一个组
            for b, r in zip(blocks, rects):  # 遍历文本块和边界框
                column_ind = 0  # 默认列索引为 0
                cand_seg = (r[0], r[2])  # 获取文本块的水平线段
                for i, seg in enumerate(columns):  # 遍历列线段列表
                    if Segment.contain(seg, cand_seg):  # 判断文本块的水平线段是否包含在当前列线段中
                        column_ind = i  # 如果包含，则更新列索引
                        break
                groups[i].append(b)  # 将文本块添加到对应的组
        return groups  # 返回分组后的文本块列表

    def _allocate_continuous(self, groups, lang):
        """
        在分组后的文本块中，将连续的文本块和表格合并。
        Args:
            groups: 分组后的文本块列表。
            lang: 语言类型，用于文本行连接。
        Returns:
            list: 合并后的分组文本块列表。
        """
        g_bound = []  # 初始化组边界框列表
        groups = [g for g in groups if g]  # 过滤空组
        for blocks in groups:  # 遍历每个组
            arr = [b.bbox for b in blocks]  # 获取组中所有文本块的边界框
            bboxes = np.asarray(arr)  # 转换为 numpy 数组
            g_bound.append(np.asarray(merge_rects(bboxes)))  # 合并组中所有边界框，得到组边界框并添加到组边界框列表
        LINE_FULL_THRESHOLD = 0.80  # 行满阈值，用于判断是否为完整行
        START_THRESHOLD = 0.8  # 行起始位置阈值，用于判断是否为新行
        SIMI_HEIGHT_THRESHOLD = 0.3  # 行高相似度阈值，用于判断行高是否相似
        SIMI_WIDTH_THRESHOLD = 0.05  # 列宽相似度阈值，用于判断列宽是否相似
        TEXT_ID = 4  # 文本布局类型 ID
        TABLE_ID = 5  # 表格布局类型 ID

        def _get_elem(blocks, is_first=True):
            """
            获取组中第一个或最后一个文本块及其相关信息。
            Args:
                blocks: 文本块列表。
                is_first: 是否获取第一个文本块，默认为 True。
            Returns:
                tuple: (BlockInfo 对象, 布局类型, 边界框, 宽度, 高度)。
            """
            if not blocks:  # 如果文本块列表为空，则返回 None
                return (None, None, None, None, None)
            if is_first:  # 如果获取第一个文本块
                b1 = blocks[0]  # 获取第一个文本块
                b1_label = b1.layout_type  # 获取布局类型
                if b1_label == TABLE_ID:  # 如果是表格
                    r1 = b1.bbox  # 使用块边界框
                else:  # 如果不是表格
                    r1 = b1.rs[0]  # 使用第一个文本行边界框
                r1_w = r1[2] - r1[0]  # 计算宽度
                r1_h = r1[3] - r1[1]  # 计算高度
                return (b1, b1_label, r1, r1_w, r1_h)  # 返回信息
            else:  # 如果获取最后一个文本块
                b0 = blocks[-1]  # 获取最后一个文本块
                b0_label = b0.layout_type  # 获取布局类型
                if b0_label == TABLE_ID:  # 如果是表格
                    r0 = b0.bbox  # 使用块边界框
                else:  # 如果不是表格
                    r0 = b0.rs[-1]  # 使用最后一个文本行边界框
                r0_w = r0[2] - r0[0]  # 计算宽度
                r0_h = r0[3] - r0[1]  # 计算高度
                return (b0, b0_label, r0, r0_w, r0_h)  # 返回信息

        b0, b0_label, r0, r0_w, r0_h = _get_elem(groups[0], False)  # 获取第一个组的最后一个文本块信息
        g0 = g_bound[0]  # 获取第一个组的边界框
        for i in range(1, len(groups)):  # 遍历剩余的组
            b1, b1_label, r1, r1_w, r1_h = _get_elem(groups[i], True)  # 获取当前组的第一个文本块信息
            g1 = g_bound[i]  # 获取当前组的边界框
            # print('\n_allocate_continuous:')
            # print(b0, b0_label, b1, b1_label)
            if b0_label and b0_label == b1_label and b0_label == TEXT_ID:  # 如果前一个块和当前块都是文本类型
                c0 = r0_w / (g0[2] - g0[0])  # 计算前一个块的行宽占组宽的比例
                c1 = (r1[0] - g1[0]) / r1_h  # 计算当前块的行起始位置占行高的比例
                c2 = np.abs(r0_h - r1_h) / r1_h  # 计算行高相似度
                # print('\n\n---conti texts---')
                # print(b0_label, c0, c1, c2,
                #       b0, b0_label, r0, r0_w, r0_h,
                #       b1, b1_label, r1, r1_w, r1_h)
                if c0 > LINE_FULL_THRESHOLD and c1 < START_THRESHOLD and c2 < SIMI_HEIGHT_THRESHOLD:  # 如果满足连续文本行的条件
                    new_text = join_lines([b0.block_text, b1.block_text], lang)  # 连接文本内容
                    joined_lines = np.hstack([b0.ts, b1.ts])  # 合并文本行列表
                    joined_bboxes = np.vstack([b0.rs, b1.rs])  # 合并边界框列表
                    new_pages = b0.pages.copy()  # 复制页码列表
                    new_pages.extend(b1.pages)  # 添加新的页码
                    new_block = b1  # 使用后一个块的信息更新
                    new_block.block_text = new_text  # 更新文本内容
                    new_block.ts = joined_lines  # 更新文本行列表
                    new_block.rs = joined_bboxes  # 更新边界框列表
                    new_block.pages = new_pages  # 更新页码列表
                    groups[i][0] = new_block  # 更新当前组的第一个块为合并后的块
                    groups[i - 1].pop(-1)  # 移除前一个组的最后一个块
            elif self.is_join_table and b0_label and b0_label == b1_label and b0_label == TABLE_ID:  # 如果允许合并表格且前一个块和当前块都是表格类型
                row0 = b0.block_text.split("\n", 1)[0].split(" | ")  # 获取前一个表格的第一行，分割为表头
                row1 = b1.block_text.split("\n", 1)[0].split(" | ")  # 获取当前表格的第一行，分割为表头
                c0 = (r1_w - r0_w) / r0_w  # 计算列宽差异率
                c1 = len(row0) == len(row1)  # 判断表头列数是否相同
                # print('---table join---', c0, c1, row0, row1, r1_w, r0_w)
                if c0 < SIMI_WIDTH_THRESHOLD and c1:  # 如果列宽相似且表头列数相同
                    has_header = np.all([e0 == e1 for e0, e1 in zip(row0, row1)])  # 判断表头是否完全相同
                    new_text = merge_md_tables([b0.block_text, b1.block_text], has_header)  # 合并 Markdown 表格
                    new_html_text = merge_html_tables([b0.html_text, b1.html_text], has_header)  # 合并 HTML 表格
                    new_pages = b0.pages.copy()  # 复制页码列表
                    new_pages.extend(b1.pages)  # 添加新的页码
                    joined_lines = np.hstack([b0.ts, b1.ts])  # 合并文本行列表
                    joined_bboxes = np.vstack([b0.rs, b1.rs])  # 合并边界框列表
                    new_block = b1  # 使用后一个块的信息更新
                    new_bbox = []  # 初始化新的边界框列表
                    new_bbox_text = []  # 初始化新的边界框文本列表
                    if b0.bbox_text is not None:  # 如果前一个块有边界框文本
                        new_bbox_text.extend(b0.bbox_text)  # 添加到新的边界框文本列表
                    else:  # 如果没有
                        new_bbox_text.append(b0.block_text)  # 添加块文本到新的边界框文本列表
                    if b1.bbox_text is not None:  # 如果当前块有边界框文本
                        new_bbox_text.extend(b1.bbox_text)  # 添加到新的边界框文本列表
                    else:  # 如果没有
                        new_bbox_text.append(b1.block_text)  # 添加块文本到新的边界框文本列表
                    new_bbox.extend(b0.bbox)  # 添加前一个块的边界框
                    new_bbox.extend(b1.bbox)  # 添加当前块的边界框
                    new_block.bbox = new_bbox  # 更新块边界框
                    new_block.pages = new_pages  # 更新页码列表
                    new_block.ts = joined_lines  # 更新文本行列表
                    new_block.rs = joined_bboxes  # 更新边界框列表
                    new_block.block_text = new_text  # 更新块文本为合并后的 Markdown 表格
                    new_block.html_text = new_html_text  # 更新 HTML 文本为合并后的 HTML 表格
                    new_block.bbox_text = new_bbox_text  # 更新边界框文本列表
                    groups[i][0] = new_block  # 更新当前组的第一个块为合并后的块
                    groups[i - 1].pop(-1)  # 移除前一个组的最后一个块
            b0, b0_label, r0, r0_w, r0_h = _get_elem(groups[i], False)  # 更新前一个块的信息为当前组的最后一个块
        return groups  # 返回合并后的分组文本块列表

    def id_cov(self, type_str):
        """
        将类型字符串转换为布局类型 ID。
        Args:
            type_str: 类型字符串，例如 "text", "table", "title"。
        Returns:
            int: 布局类型 ID。
        """
        if type_str == "text":
            return 4
        if type_str == "table":
            return 5
        if type_str == "title":
            return 3
        return -1  # 如果类型字符串未匹配，则返回 -1

    def parsing_data(self, block):
        """
        解析单个布局块的数据，提取文本、类型、边界框等信息，并构建元数据。
        Args:
            block: 布局块字典，包含块类型、边界框、文本行等信息。
        Returns:
            list: 解析后的数据列表，每个元素为一个包含元数据的字典。
        """
        res_data = []  # 初始化解析结果数据列表
        bbox_top = block["bbox"]  # 获取块的顶部边界框
        text = ""  # 初始化文本为空字符串
        s = 0  # 初始化文本起始索引为 0

        def built_metadata(type, text, bbox_top, level):
            """
            构建元数据字典。
            Args:
                type: 元素类型，例如 "text", "table", "title"。
                text: 元素文本内容。
                bbox_top: 元素顶部边界框。
                level: 文本级别，例如标题级别。
            Returns:
                dict: 元数据字典。
            """
            return {"type": type, "text": text, "bbox_top": bbox_top, "level": level, "types": [],  # 初始化跨度类型列表
                    "texts": [],  # 初始化跨度文本列表
                    "bboxes": [],  # 初始化跨度边界框列表
                    "indexes": [],  # 初始化跨度索引列表
                    "text_levels": []  # 初始化跨度文本级别列表
                    }

        new_metadata = built_metadata(type=block['type'], text='', bbox_top=bbox_top, level=0)  # 创建初始元数据
        res_data.append(new_metadata)  # 添加到解析结果数据列表
        if block["type"] == "text" or block["type"] == "title":  # 如果块类型为文本或标题
            s = 0  # 重置文本起始索引
            # block_lines = block["lines"]
            block_lines = sorted(block["lines"], key=lambda x: x['index'])  # 对文本行按索引排序
            pre_types = []  # 初始化前一个跨度类型列表
            for line in block_lines:  # 遍历文本行
                for span in line["spans"]:  # 遍历跨度
                    if span['type'] == "image":  # 如果跨度类型为图像，则跳过
                        continue
                    pre_types.append('title' if span['text_level'] > 0 else span['type'])  # 根据文本级别判断跨度类型，标题或原始类型
                    if block['type'] != 'title':  # 如果块类型不是标题
                        if len(pre_types) > 1 and pre_types[-1] != pre_types[-2] and pre_types[-1] in ["text", 'title']:  # 如果跨度类型发生变化且新类型为文本或标题
                            new_metadata = built_metadata(type=pre_types[-1], text="", bbox_top=span['bbox'], level=span['text_level'])  # 创建新的元数据
                            res_data.append(new_metadata)  # 添加到解析结果数据列表
                            text = ""  # 重置文本
                            s = 0  # 重置文本起始索引
                        else:  # 如果跨度类型未变化或新类型不是文本或标题
                            new_metadata["type"] = pre_types[-1]  # 更新元数据类型
                            new_metadata['level'] = span["text_level"]  # 更新元数据级别
                    else:  # 如果块类型是标题
                        new_metadata['level'] = span["text_level"]  # 更新元数据级别
                    if "content" in span:  # 如果跨度包含内容
                        text += span["content"]  # 添加跨度内容到文本
                        new_metadata['types'].append(pre_types[-1])  # 添加跨度类型到类型列表
                        new_metadata['text'] = text  # 更新元数据文本
                        new_metadata['texts'].append(span["content"])  # 添加跨度内容到文本列表
                        new_metadata['bboxes'].append(span["bbox"])  # 添加跨度边界框到边界框列表
                        new_metadata['text_levels'].append(span["text_level"])  # 添加跨度文本级别到级别列表
                        new_metadata['indexes'].append([s, len(text) - 1])  # 添加跨度索引到索引列表
                        s = len(text)  # 更新文本起始索引
                    else:  # 如果跨度不包含内容，则跳过
                        continue
        if block["type"] == "table":  # 如果块类型为表格
            table_blocks = sorted(block["blocks"], key=lambda x: x['index'])  # 对表格块按索引排序
            # table_blocks = block["blocks"]
            for table_block in table_blocks:  # 遍历表格块
                block_type = table_block["type"]  # 获取表格块类型
                block_lines = table_block["lines"]  # 获取表格块文本行
                # block_lines = sorted(table_block["lines"], key=lambda x: x['index'])
                for line in block_lines:  # 遍历文本行
                    for span in line["spans"]:  # 遍历跨度
                        span_content = ""  # 初始化跨度内容为空字符串
                        if span["type"] == "text":  # 如果跨度类型为文本
                            text += span["content"]  # 添加跨度内容到文本
                            span_content = span["content"]  # 设置跨度内容
                        elif span["type"] == "image":  # 如果跨度类型为图像
                            text += span["image_path"]  # 添加图像路径到文本
                            span_content = span["image_path"]  # 设置跨度内容为图像路径
                        elif 'html' in span:  # 如果跨度包含 HTML
                            text += span["html"]  # 添加 HTML 到文本
                            span_content = span["html"]  # 设置跨度内容为 HTML
                        else:  # 如果跨度类型未识别，则跳过
                            continue
                        new_metadata['texts'].append(span_content)  # 添加跨度内容到文本列表
                        new_metadata['bboxes'].append(span["bbox"])  # 添加跨度边界框到边界框列表
                        new_metadata['text_levels'].append(0)  # 添加跨度文本级别 0
                        new_metadata['indexes'].append([s, len(text) - 1])  # 添加跨度索引到索引列表
                        s = len(text)  # 更新文本起始索引
        return res_data  # 返回解析结果数据列表

    def _save_to_pages(self, page_inds):
        """
        将解析后的页面数据转换为 Page 对象列表。
        Args:
            page_inds: 解析后的页面数据列表，每个元素为一个页面字典，包含块信息。
        Returns:
            list: Page 对象列表。
        """
        pages = []  # 初始化 Page 对象列表
        for idx, p in enumerate(page_inds):  # 遍历页面数据列表
            blocks = p["blocks"]  # 获取页面块列表
            page_idx = p["page_idx"]  # 获取页码索引
            page = Page(number=page_idx + 1)  # 创建 Page 对象，页码从 1 开始
            for b in blocks:  # 遍历页面块
                parsed_datas = self.parsing_data(b)  # 解析块数据
                for parsed_data in parsed_datas:  # 遍历解析后的数据
                    block_type = parsed_data['type']  # 获取块类型
                    text = parsed_data['text']  # 获取文本内容
                    bbox_top = parsed_data['bbox_top']  # 获取顶部边界框
                    level = parsed_data['level']  # 获取文本级别
                    types = parsed_data['types']  # 获取跨度类型列表
                    texts = parsed_data['texts']  # 获取跨度文本列表
                    bboxes = parsed_data['bboxes']  # 获取跨度边界框列表
                    indexes = parsed_data['indexes']  # 获取跨度索引列表
                    text_levels = parsed_data["text_levels"]  # 获取跨度文本级别列表
                    extra_data = {"bboxes": [bbox_top]}  # 初始化额外数据，包含顶部边界框
                    extra_data.update({"indexes": [[0, len(text) - 1]],  # 添加块级别的索引范围
                                       "span_texts": texts,  # 添加跨度文本列表
                                       "span_indexes": indexes,  # 添加跨度索引列表
                                       "span_types": types,  # 添加跨度类型列表
                                       "span_bboxes": bboxes,  # 添加跨度边界框列表
                                       "span_pages": [page_idx + 1] * len(indexes),  # 添加跨度页码列表
                                       "span_levels": text_levels,  # 添加跨度级别列表
                                       "block_type": block_type,  # 添加块类型
                                       "pages": [page_idx + 1],  # 添加页码列表
                                       "bbox": bbox_top,  # 添加顶部边界框
                                       "types": [block_type],  # 添加类型列表
                                       "levels": [level]  # 添加级别列表
                                       })
                    element = None  # 初始化元素为 None
                    metadata = ElementMetadata(text_as_html=text, extra_data=extra_data)  # 创建元素元数据
                    if block_type == "table":  # 如果块类型为表格
                        element = Table(text=text, metadata=metadata)  # 创建 Table 元素
                    elif block_type == "title":  # 如果块类型为标题
                        element = Title(text=text, metadata=metadata)  # 创建 Title 元素
                    elif block_type == "text":  # 如果块类型为文本
                        element = Text(text=text, metadata=metadata)  # 创建 Text 元素
                    elif block_type == 'image':  # 如果块类型为图像
                        element = Image(text=text, metadata=metadata)  # 创建 Image 元素
                    page.elements.append(element)  # 将元素添加到页面元素列表
            pages.append(page)  # 将页面添加到页面列表
        return pages  # 返回 Page 对象列表

    def load(self) -> List[Page]:
        """
        加载 PDF 文档并提取页面元素。
        Returns:
            List[Page]: Page 对象列表。
        """
        page_inds = self.miner_agent.predict({"file_path": self.file})  # 使用文档结构分析模型预测页面结构信息
        pages = self._save_to_pages(page_inds)  # 将页面结构信息转换为 Page 对象列表
        return pages  # 返回 Page 对象列表

    @property
    def pages(self) -> List[Page]:
        """
        获取文档的所有页面元素，按顺序排列。
        Returns:
            List[Page]: Page 对象列表。
        """
        if self._pages is None:  # 如果页面列表未加载
            self._pages = self.load()  # 加载页面
        return super().pages  # 调用父类 Document 的 pages 属性，返回页面列表
