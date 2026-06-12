"""
图像加载模块
支持各种图像格式的加载
"""

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Optional, Tuple, Union


class ImageLoader:
    """图像加载器"""
    
    # 支持的图像格式
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif'}
    
    @staticmethod
    def load(file_path: Union[str, Path]) -> Optional[np.ndarray]:
        """加载图像文件"""
        try:
            path = Path(file_path)
            
            # 检查文件是否存在
            if not path.exists():
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            # 检查文件格式
            if path.suffix.lower() not in ImageLoader.SUPPORTED_FORMATS:
                raise ValueError(f"不支持的文件格式: {path.suffix}")
            
            # 使用PIL加载（支持中文路径）
            pil_image = Image.open(path)
            
            # 转换为OpenCV格式
            if pil_image.mode == 'RGBA':
                # 保持Alpha通道
                image = np.array(pil_image)
                # PIL是RGB，OpenCV是BGR
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
            elif pil_image.mode == 'RGB':
                image = np.array(pil_image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            elif pil_image.mode == 'L':
                # 灰度图
                image = np.array(pil_image)
            else:
                # 其他模式转换为RGB
                image = np.array(pil_image.convert('RGB'))
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            return image
            
        except Exception as e:
            print(f"加载图像失败: {e}")
            return None
    
    @staticmethod
    def load_with_info(file_path: Union[str, Path]) -> Tuple[Optional[np.ndarray], dict]:
        """加载图像并返回详细信息"""
        try:
            path = Path(file_path)
            
            # 加载图像
            image = ImageLoader.load(file_path)
            
            if image is None:
                return None, {}
            
            # 获取图像信息
            info = {
                "path": str(path.absolute()),
                "name": path.name,
                "extension": path.suffix.lower(),
                "size": (image.shape[1], image.shape[0]),  # (width, height)
                "channels": image.shape[2] if len(image.shape) == 3 else 1,
                "dtype": str(image.dtype),
                "has_alpha": len(image.shape) == 3 and image.shape[2] == 4,
                "file_size": path.stat().st_size
            }
            
            return image, info
            
        except Exception as e:
            print(f"加载图像信息失败: {e}")
            return None, {}
    
    @staticmethod
    def load_thumbnail(file_path: Union[str, Path], 
                      size: Tuple[int, int] = (120, 120)) -> Optional[np.ndarray]:
        """加载图像缩略图"""
        try:
            path = Path(file_path)
            
            # 使用PIL加载缩略图
            pil_image = Image.open(path)
            pil_image.thumbnail(size, Image.Resampling.LANCZOS)
            
            # 转换为OpenCV格式
            if pil_image.mode == 'RGBA':
                image = np.array(pil_image)
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
            else:
                image = np.array(pil_image.convert('RGB'))
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            return image
            
        except Exception as e:
            print(f"加载缩略图失败: {e}")
            return None
    
    @staticmethod
    def is_supported(file_path: Union[str, Path]) -> bool:
        """检查文件是否为支持的图像格式"""
        try:
            path = Path(file_path)
            return path.suffix.lower() in ImageLoader.SUPPORTED_FORMATS
        except Exception:
            return False
    
    @staticmethod
    def get_image_info(file_path: Union[str, Path]) -> Optional[dict]:
        """获取图像信息（不加载完整图像）"""
        try:
            path = Path(file_path)
            
            if not path.exists():
                return None
            
            # 使用PIL获取基本信息
            with Image.open(path) as pil_image:
                info = {
                    "path": str(path.absolute()),
                    "name": path.name,
                    "extension": path.suffix.lower(),
                    "size": pil_image.size,  # (width, height)
                    "mode": pil_image.mode,
                    "format": pil_image.format,
                    "file_size": path.stat().st_size
                }
            
            return info
            
        except Exception as e:
            print(f"获取图像信息失败: {e}")
            return None