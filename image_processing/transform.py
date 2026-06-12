"""
图像变换模块
提供各种图像变换功能
"""

import cv2
import numpy as np
from typing import Optional, Tuple


class ImageTransformer:
    """图像变换器"""
    
    def __init__(self):
        """初始化变换器"""
        pass
    
    def rotate(self, image: np.ndarray, angle: float, 
              center: Optional[Tuple[int, int]] = None) -> np.ndarray:
        """旋转图像"""
        try:
            h, w = image.shape[:2]
            
            if center is None:
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
    
    def flip(self, image: np.ndarray, horizontal: bool = True) -> np.ndarray:
        """翻转图像"""
        try:
            if horizontal:
                return cv2.flip(image, 1)  # 水平翻转
            else:
                return cv2.flip(image, 0)  # 垂直翻转
        except Exception as e:
            print(f"翻转图像失败: {e}")
            return image
    
    def scale(self, image: np.ndarray, scale_x: float = 1.0, 
             scale_y: float = 1.0) -> np.ndarray:
        """缩放图像"""
        try:
            h, w = image.shape[:2]
            new_w = int(w * scale_x)
            new_h = int(h * scale_y)
            
            # 根据缩放方向选择插值方法
            if scale_x > 1 or scale_y > 1:
                interpolation = cv2.INTER_CUBIC  # 放大
            else:
                interpolation = cv2.INTER_AREA  # 缩小
            
            scaled = cv2.resize(image, (new_w, new_h), interpolation=interpolation)
            
            return scaled
            
        except Exception as e:
            print(f"缩放图像失败: {e}")
            return image
    
    def crop(self, image: np.ndarray, 
            x: int, y: int, width: int, height: int) -> np.ndarray:
        """裁剪图像"""
        try:
            h, w = image.shape[:2]
            
            # 确保裁剪区域在图像范围内
            x = max(0, min(x, w))
            y = max(0, min(y, h))
            width = min(width, w - x)
            height = min(height, h - y)
            
            if width <= 0 or height <= 0:
                return image
            
            # 裁剪图像
            cropped = image[y:y+height, x:x+width]
            
            return cropped
            
        except Exception as e:
            print(f"裁剪图像失败: {e}")
            return image
    
    def perspective_transform(self, image: np.ndarray, 
                            src_points: np.ndarray, 
                            dst_points: np.ndarray) -> np.ndarray:
        """透视变换"""
        try:
            # 计算透视变换矩阵
            M = cv2.getPerspectiveTransform(src_points, dst_points)
            
            # 获取目标尺寸
            dst_width = int(np.linalg.norm(dst_points[1] - dst_points[0]))
            dst_height = int(np.linalg.norm(dst_points[2] - dst_points[1]))
            
            # 应用透视变换
            transformed = cv2.warpPerspective(image, M, (dst_width, dst_height))
            
            return transformed
            
        except Exception as e:
            print(f"透视变换失败: {e}")
            return image
    
    def affine_transform(self, image: np.ndarray,
                        src_points: np.ndarray,
                        dst_points: np.ndarray) -> np.ndarray:
        """仿射变换"""
        try:
            # 计算仿射变换矩阵
            M = cv2.getAffineTransform(src_points, dst_points)
            
            # 获取目标尺寸
            h, w = image.shape[:2]
            
            # 应用仿射变换
            transformed = cv2.warpAffine(image, M, (w, h))
            
            return transformed
            
        except Exception as e:
            print(f"仿射变换失败: {e}")
            return image
    
    def adjust_brightness(self, image: np.ndarray, factor: float) -> np.ndarray:
        """调整亮度"""
        try:
            # 转换为HSV
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
    
    def adjust_contrast(self, image: np.ndarray, factor: float) -> np.ndarray:
        """调整对比度"""
        try:
            # 转换为LAB
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            # 调整L通道
            l = l.astype(np.float32)
            l = (l - 128) * factor + 128
            l = np.clip(l, 0, 255)
            l = l.astype(np.uint8)
            
            lab = cv2.merge([l, a, b])
            return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
        except Exception as e:
            print(f"调整对比度失败: {e}")
            return image
    
    def apply_blur(self, image: np.ndarray, 
                  blur_type: str = "gaussian", 
                  kernel_size: int = 5) -> np.ndarray:
        """应用模糊效果"""
        try:
            if blur_type == "gaussian":
                return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
            elif blur_type == "median":
                return cv2.medianBlur(image, kernel_size)
            elif blur_type == "average":
                return cv2.blur(image, (kernel_size, kernel_size))
            else:
                return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
                
        except Exception as e:
            print(f"应用模糊失败: {e}")
            return image
    
    def apply_sharpen(self, image: np.ndarray, strength: float = 1.0) -> np.ndarray:
        """应用锐化效果"""
        try:
            # 锐化核
            kernel = np.array([
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]
            ]) * strength
            
            # 调整核的中心值
            kernel[1, 1] = 1 + (kernel[1, 1] - 1) * strength
            
            # 应用锐化
            sharpened = cv2.filter2D(image, -1, kernel)
            
            return sharpened
            
        except Exception as e:
            print(f"应用锐化失败: {e}")
            return image
    
    def create_thumbnail(self, image: np.ndarray, 
                        size: Tuple[int, int] = (120, 120)) -> np.ndarray:
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
                        (rgb[:, :, c] * alpha[:, :, 0] + 
                         background[y_offset:y_offset+new_h, x_offset:x_offset+new_w, c] * (1 - alpha[:, :, 0]))
            else:
                background[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = thumbnail
            
            return background
            
        except Exception as e:
            print(f"创建缩略图失败: {e}")
            return image