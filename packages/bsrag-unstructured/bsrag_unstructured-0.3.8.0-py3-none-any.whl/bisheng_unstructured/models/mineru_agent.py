import copy
import hashlib
import os
import sys
import json
import numpy as np
import requests
from PIL import Image
from loguru import logger
from bisheng_unstructured.models.common import (bbox_overlap, get_hori_rect_v2, is_valid_box, join_line_outs, list2box, save_pillow_to_base64, sort_boxes, split_line_image, )
DEFAULT_CONFIG = {"params": {"sort_filter_boxes": True,  # 是否对检测到的框进行排序和过滤
                             "enable_huarong_box_adjust": True,  # 是否启用华容道框调整
                             "rotateupright": False,  # 是否进行文本方向校正
                             "support_long_image_segment": True,  # 是否支持长图分割
                             "split_long_sentence_blank": True,  # 是否分割长句中的空格
                             }, "scene_mapping": {"print": {  # 打印场景配置
    "det": "general_text_det_v2.0",  # 文本检测模型
    "recog": "general_text_reg_nb_v1.0_faster",  # 文本识别模型
}, "hand": {  # 手写场景配置
    "det": "general_text_det_v2.0",  # 文本检测模型
    "recog": "general_text_reg_nb_v1.0_faster",  # 文本识别模型
}, "print_recog": {  # 打印文本识别场景配置
    "recog": "general_text_reg_nb_v1.0_faster",  # 文本识别模型
}, "hand_recog": {  # 手写文本识别场景配置
    "recog": "general_text_reg_nb_v1.0_faster",  # 文本识别模型
}, "det": {  # 文本检测场景配置
    "det": "general_text_det_v2.0",  # 文本检测模型
}, }, }  # 默认配置字典，包含通用参数和场景模型映射

# MinerU Agent Version 0.1, update at 2023.08.18
#  - add predict_with_mask support recog with embedding formula, 2024.01.16
"""MinerU 代理类，用于调用 MinerU 服务进行文档解析和 OCR."""
class MinerUAgent(object):

    def __init__(self, **kwargs):
        """初始化 MinerUAgent 对象."""
        self.ep = kwargs.get("miner_u_ep")  # 从 kwargs 中获取 miner_u_ep 参数，即 MinerU 服务的 endpoint
        self.client = requests.Session()  # 创建 requests.Session 对象，用于保持会话
        self.timeout = 1100  # 设置请求超时时间为 1100 秒
        self.params = {"parse_method": "auto",  # 解析方法，默认为 "auto"，可选 "ocr", "txt"
                       "model_json_path": "",  # 模型 JSON 文件路径，默认为空
                       "is_json_md_dump": True,  # 是否将结果输出为 JSON 和 Markdown 文件，默认为 True
                       "output_dir": "output"  # 输出目录，默认为 "output"
                       }  # 设置默认请求参数
        self.cache_dir = "/data/cache"  # 设置缓存目录为 "/data/cache"
        if not os.path.exists(self.cache_dir):  # 如果缓存目录不存在
            os.makedirs(self.cache_dir, exist_ok=True)  # 创建缓存目录，makedirs 可以递归创建目录

    # def find_cache(self, dir):
    #     """查找缓存目录下的文件."""
    #     files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]  # 获取目录下所有文件
    #     return files  # 返回文件列表

    def _generate_md5_signature(self, file_path):
        """生成文件的 MD5 签名."""
        hash_md5 = hashlib.md5()  # 创建 MD5 哈希对象
        with open(file_path, "rb") as f:  # 以二进制只读模式打开文件
            for chunk in iter(lambda: f.read(4096), b""):  # 迭代读取文件内容，每次读取 4096 字节
                hash_md5.update(chunk)  # 更新哈希对象
        return hash_md5.hexdigest()  # 返回 MD5 签名

    def _generate_cache_filename(self, file_path):
        """根据文件的 MD5 签名生成缓存文件名称."""
        file_md5 = self._generate_md5_signature(file_path)  # 生成文件的 MD5 签名
        # 使用 MD5 签名作为缓存文件名，通常可以加上扩展名，如 .cache
        cache_filename = f"{file_md5}.cache"  # 构建缓存文件名
        return cache_filename  # 返回缓存文件名

    def _find_cache(self, cache_name): 
        """查找缓存文件."""
        cache_file_name = os.path.join(self.cache_dir, cache_name)  # 构建缓存文件完整路径
        if os.path.exists(cache_file_name):  # 如果缓存文件存在
            with open(cache_file_name, 'r', encoding='utf-8') as file:  # 以 UTF-8 编码读取缓存文件
                data = json.load(file)  # 加载 JSON 数据
                return data  # 返回缓存数据
        else:  # 如果缓存文件不存在
            return None  # 返回 None

    def _save_cache(self, cache_name, data):
        """保存数据到缓存文件."""
        cache_file_name = os.path.join(self.cache_dir, cache_name)  # 构建缓存文件完整路径
        with open(cache_file_name, 'w', encoding='utf-8') as file:  # 以 UTF-8 编码写入缓存文件
            json.dump(data, file, ensure_ascii=False, indent=4)  # 将数据以 JSON 格式保存到缓存文件，不使用 ASCII 编码，缩进 4 个空格

    def predict(self, inp):
        """调用 MinerU 服务进行预测."""
        file_path = inp.pop("file_path")  # 从输入字典中移除 "file_path" 键并获取其值，即文件路径
        cache_name = self._generate_cache_filename(file_path)  # 根据文件路径生成缓存文件名
        cache_data = self._find_cache(cache_name)  # 查找缓存数据
        with open(file_path, "rb") as f:  # 以二进制只读模式打开文件
            files = {"pdf_file": f  # 文件上传字段为 "pdf_file"，值为打开的文件对象
                     }
            params = copy.deepcopy(self.params)  # 深拷贝默认请求参数
            try:  # 捕获请求异常
                if cache_data:  # 如果找到缓存数据
                    logger.info(f"找到缓存 file={file_path}")  # 记录日志，提示找到缓存
                    res_json = cache_data  # 使用缓存数据
                else:  # 如果没有找到缓存数据
                    logger.info("开始请求 minerU 服务")  # 记录日志，提示开始请求 MinerU 服务
                    r = self.client.post(url=self.ep, params=params, timeout=self.timeout, files=files)  # 发送 POST 请求到 MinerU 服务
                    res_json = r.json()  # 解析 JSON 响应
                    self._save_cache(cache_name, res_json)  # 保存数据到缓存
                # res_json = self.mock_data()
                logger.info("minerU服务请求成功")  # 记录日志，提示 MinerU 服务请求成功
                pages = res_json["info"]["pdf_info"]  # 从响应 JSON 中获取 "pdf_info" 字段，即页面信息列表
                pages = [{"blocks": p["preproc_blocks"], **p} for p in pages]  # 遍历页面信息列表，将 "preproc_blocks" 字段重命名为 "blocks"
                return pages  # 返回页面信息列表
            except requests.exceptions.Timeout:  # 捕获请求超时异常
                raise Exception(f"timeout in ocr predict")  # 抛出异常，提示 OCR 预测超时
            except Exception as e:  # 捕获其他异常
                exc_type, exc_value, exc_traceback = sys.exc_info()  # 获取异常信息
                raise Exception(f"exception in ocr predict: [{e}]")  # 抛出异常，提示 OCR 预测异常

    def _mock_data(self):
        """加载模拟数据."""
        with open('/mnt/d/data/response_1737084708817.json', 'r', encoding='utf-8') as file:  # 以 UTF-8 编码读取模拟数据文件
            data = json.load(file)  # 加载 JSON 数据
            return data  # 返回模拟数据

    def _get_ep_result(self, ep, inp):
        """发送 POST 请求到指定 endpoint 并获取 JSON 响应."""
        try:  # 捕获请求异常
            r = self.client.post(url=ep, json=inp, timeout=self.timeout)  # 发送 POST 请求
            return r.json()  # 解析 JSON 响应并返回
        except requests.exceptions.Timeout:  # 捕获请求超时异常
            raise Exception(f"timeout in formula agent predict")  # 抛出异常，提示公式识别代理预测超时
        except Exception as e:  # 捕获其他异常
            raise Exception(f"exception in formula agent predict: [{e}]")  # 抛出异常，提示公式识别代理预测异常

    def _predict_with_mask(self, img0, mf_out, scene="print", **kwargs):
        """使用掩码进行预测."""
        img = np.array(img0.copy())  # 将输入图像转换为 NumPy 数组并复制
        for box_info in mf_out:  # 遍历公式识别结果
            if box_info["type"] in ("isolated", "embedding"):  # 如果公式类型为 "isolated" 或 "embedding"
                box = np.asarray(box_info["box"]).reshape((4, 2))  # 将公式边界框坐标转换为 NumPy 数组并调整形状
                xmin, ymin = max(0, int(box[0][0]) - 1), max(0, int(box[0][1]) - 1)  # 计算掩码区域的左上角坐标
                xmax, ymax = (min(img0.size[0], int(box[2][0]) + 1), min(img0.size[1], int(box[2][1]) + 1),)  # 计算掩码区域的右下角坐标
                img[ymin:ymax, xmin:xmax, :] = 255  # 将掩码区域填充为白色 (255)
        masked_image = Image.fromarray(img)  # 将掩码后的 NumPy 数组转换为 PIL Image 对象
        b64_image = save_pillow_to_base64(masked_image)  # 将掩码后的图像转换为 base64 编码
        # b64_image = save_pillow_to_base64(img0)
        params = copy.deepcopy(self.params)  # 深拷贝默认请求参数
        params.update(DEFAULT_CONFIG["scene_mapping"]["det"])  # 更新请求参数为检测场景配置
        req_data = {"param": params, "data": [b64_image]}  # 构建请求数据，包含参数和 base64 编码的图像数据
        det_result = self._get_ep_result(self.ep, req_data)  # 调用 _get_ep_result 方法发送请求并获取检测结果
        bboxes = det_result["result"]["boxes"]  # 从检测结果中获取边界框列表
        # self._visualize(masked_image, bboxes, mf_out)
        EMB_BBOX_THREHOLD = 0.7  # 嵌入框重叠阈值
        text_bboxes = []  # 初始化文本边界框列表
        for bbox in bboxes:  # 遍历检测到的边界框列表
            hori_bbox = get_hori_rect_v2(bbox)  # 获取水平矩形框坐标
            if not is_valid_box(hori_bbox, min_height=8, min_width=2):  # 如果水平矩形框无效，则跳过
                continue
            embed_mfs = []  # 初始化嵌入公式列表
            for box_info in mf_out:  # 遍历公式识别结果
                if box_info["type"] == "embedding":  # 如果公式类型为 "embedding"
                    bb = box_info["box"]  # 获取公式边界框
                    emb_bbox = [bb[0], bb[1], bb[4], bb[5]]  # 提取嵌入公式边界框坐标
                    bbox_iou = bbox_overlap(hori_bbox, emb_bbox)  # 计算水平矩形框和嵌入公式边界框的重叠度
                    if bbox_iou > EMB_BBOX_THREHOLD:  # 如果重叠度大于阈值
                        embed_mfs.append({"position": emb_bbox, "text": box_info["text"], "type": box_info["type"], }  # 添加嵌入公式信息到嵌入公式列表
                        )
            ocr_boxes = split_line_image(hori_bbox, embed_mfs)  # 分割行图像，排除嵌入公式区域
            text_bboxes.extend(ocr_boxes)  # 将分割后的文本边界框添加到文本边界框列表
        # recog the patches，识别文本区域
        recog_data = []  # 初始化识别数据列表
        for bbox in text_bboxes:  # 遍历文本边界框列表
            b64_data = save_pillow_to_base64(masked_image.crop(bbox["position"]))  # 裁剪文本区域图像并转换为 base64 编码
            recog_data.append(b64_data)  # 添加到识别数据列表
        params = copy.deepcopy(self.params)  # 深拷贝默认请求参数
        params.update(DEFAULT_CONFIG["scene_mapping"]["print_recog"])  # 更新请求参数为打印文本识别场景配置
        req_data = {"param": params, "data": recog_data}  # 构建请求数据，包含参数和 base64 编码的图像数据
        recog_result = self._get_ep_result(self.ep, req_data)  # 调用 _get_ep_result 方法发送请求并获取识别结果
        outs = []  # 初始化输出列表
        for bbox, text in zip(text_bboxes, recog_result["result"]["texts"]):  # 遍历文本边界框列表和识别结果文本列表
            bbs = list2box(*bbox["position"])  # 将边界框坐标转换为列表形式
            outs.append({"text": text, "position": bbs, "type": "text"})  # 添加到输出列表，包含文本，位置和类型信息
        for info in mf_out:  # 遍历公式识别结果
            bbs = np.asarray(info["box"]).reshape((4, 2))  # 将公式边界框坐标转换为 NumPy 数组并调整形状
            outs.append({"text": info["text"], "position": bbs, "type": info["type"]})  # 添加到输出列表，包含公式文本，位置和类型信息
        outs = sort_boxes(outs, key="position")  # 按位置排序输出列表
        texts, bboxes, words_info = join_line_outs(outs)  # 合并行输出
        # self._visualize(masked_image, bboxes, [])
        return texts, bboxes, words_info  # 返回文本列表，边界框列表和词信息列表
