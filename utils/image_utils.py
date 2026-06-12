"""
图像处理工具模块
提供常用的图像处理函数
"""

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Optional, Tuple, Union


class ImageUtils:
    """图像处理工具类"""
    
    @staticmethod
    def load_image(file_path: Union[str, Path]) -> Optional[np.ndarray]:
        """加载图像文件（支持中文路径）"""
        try:
            # 使用PIL加载（支持中文路径）
            pil_image = Image.open(file_path)
            # 转换为OpenCV格式
            if pil_image.mode == 'RGBA':
                # 保持Alpha通道
                image = np.array(pil_image)
                # PIL是RGB，OpenCV是BGR
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
            else:
                # 转换为BGR
                image = np.array(pil_image.convert('RGB'))
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            return image
        except Exception as e:
            print(f"加载图像失败: {e}")
            return None
    
    @staticmethod
    def save_image(image: np.ndarray, file_path: Union[str, Path], quality: int = 95) -> bool:
        """保存图像文件"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # 根据扩展名选择保存方法
            ext = path.suffix.lower()
            
            if ext in ['.jpg', '.jpeg']:
                # JPEG不支持Alpha通道
                if len(image.shape) == 3 and image.shape[2] == 4:
                    # 移除Alpha通道
                    image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
                cv2.imwrite(str(path), image, [cv2.IMWRITE_JPEG_QUALITY, quality])
            elif ext == '.png':
                cv2.imwrite(str(path), image, [cv2.IMWRITE_PNG_COMPRESSION, 3])
            elif ext == '.webp':
                cv2.imwrite(str(path), image, [cv2.IMWRITE_WEBP_QUALITY, quality])
            else:
                cv2.imwrite(str(path), image)
            
            return True
        except Exception as e:
            print(f"保存图像失败: {e}")
            return False
    
    @staticmethod
    def get_image_size(file_path: Union[str, Path]) -> Optional[Tuple[int, int]]:
        """获取图像尺寸 (width, height)"""
        try:
            pil_image = Image.open(file_path)
            return pil_image.size
        except Exception as e:
            print(f"获取图像尺寸失败: {e}")
            return None
    
    @staticmethod
    def resize_image(image: np.ndarray, 
                     width: Optional[int] = None, 
                     height: Optional[int] = None,
                     scale: Optional[float] = None) -> np.ndarray:
        """调整图像大小"""
        try:
            h, w = image.shape[:2]
            
            if scale is not None:
                new_w = int(w * scale)
                new_h = int(h * scale)
            elif width is not None and height is not None:
                new_w = width
                new_h = height
            elif width is not None:
                ratio = width / w
                new_w = width
                new_h = int(h * ratio)
            elif height is not None:
                ratio = height / h
                new_w = int(w * ratio)
                new_h = height
            else:
                return image
            
            # 使用高质量插值
            interpolation = cv2.INTER_LANCZOS4 if (new_w * new_h > w * h) else cv2.INTER_AREA
            resized = cv2.resize(image, (new_w, new_h), interpolation=interpolation)
            
            return resized
        except Exception as e:
            print(f"调整图像大小失败: {e}")
            return image
    
    @staticmethod
    def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
        """旋转图像"""
        try:
            h, w = image.shape[:2]
            center = (w // 2, h // 2)
            
            # 获取旋转矩阵
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            
            # 计算新图像尺寸
            cos = np.abs(M[0, 0])
            sin = np.abs(M[0, 1])
            new_w = int(h * sin + w * cos)
            new_h = int(h * cos + w * sin)
            
            # 调整旋转矩阵
            M[0, 2] += (new_w - w) / 2
            M[1, 2] += (new_h - h) / 2
            
            # 执行旋转
            rotated = cv2.warpAffine(image, M, (new_w, new_h), 
                                    flags=cv2.INTER_CUBIC,
                                    borderMode=cv2.BORDER_REPLICATE)
            
            return rotated
        except Exception as e:
            print(f"旋转图像失败: {e}")
            return image
    
    @staticmethod
    def flip_image(image: np.ndarray, horizontal: bool = True) -> np.ndarray:
        """翻转图像"""
        try:
            if horizontal:
                return cv2.flip(image, 1)  # 水平翻转
            else:
                return cv2.flip(image, 0)  # 垂直翻转
        except Exception as e:
            print(f"翻转图像失败: {e}")
            return image
    
    @staticmethod
    def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
        """转换为灰度图"""
        try:
            if len(image.shape) == 3:
                return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return image
        except Exception as e:
            print(f"转换为灰度图失败: {e}")
            return image
    
    @staticmethod
    def adjust_brightness(image: np.ndarray, factor: float) -> np.ndarray:
        """调整亮度"""
        try:
            # 调整亮度
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hsv = hsv.astype(np.float32)
            
            # 调整V通道
            hsv[:, :, 2] = hsv[:, :, 2] * factor
            hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
            
            hsv = hsv.astype(np.uint8)
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        except Exception as e:
            print(f"调整亮度失败: {e}")
            return image
    
    @staticmethod
    def adjust_contrast(image: np.ndarray, factor: float) -> np.ndarray:
        """调整对比度"""
        try:
            # 调整对比度
           LAB = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            L, A, B = cv2.split(LAB)
            
            # 调整L通道
            L = L.astype(np.float32)
            L = (L - 128) * factor + 128
            L = np.clip(L, 0, 255)
            L = L.astype(np.uint8)
            
            LAB = cv2.merge([L, A, B])
            return cv2.cvtColor(LAB, cv2.COLOR_LAB2BGR)
        except Exception as e:
            print(f"调整对比度失败: {e}")
            return image
    
    @staticmethod
    def create_thumbnail(image: np.ndarray, size: Tuple[int, int] = (120, 120)) -> np.ndarray:
        """创建缩略图"""
        try:
            h, w = image.shape[:2]
            target_w, target_h = size
            
            # 计算缩放比例
            scale = min(target_w / w, target_h / h)
            new_w = int(w * scale)
            new_h = int(h * scale)
            
            # 缩放图像
            thumbnail = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            
            # 创建白色背景
            background = np.ones((target_h, target_w, 3), dtype=np.uint8) * 255
            
            # 计算居中位置
            x_offset = (target_w - new_w) // 2
            y_offset = (target_h - new_h) // 2
            
            # 将缩略图放在背景上
            if len(thumbnail.shape) == 3 and thumbnail.shape[2] == 4:
                # 有Alpha通道
                alpha = thumbnail[:, :, 3:] / 255.0
                rgb = thumbnail[:, :, :3]
                
                for c in range(3):
                    background[y_offset:y_offset+new_h, x_offset:x_offset+new_w, c] = \
                        (rgb[:, :, c] * alpha + 
                         background[y_offset:y_offset+new_h, x_offset:x_offset+new_w, c] * (1 - alpha))
            else:
                background[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = thumbnail
            
            return background
        except Exception as e:
            print(f"创建缩略图失败: {e}")
            return image