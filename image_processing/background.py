"""
背景移除模块
提供图像背景移除功能
"""

import cv2
import numpy as np
from typing import Optional, Tuple


class BackgroundRemover:
    """背景移除器"""
    
    def __init__(self):
        """初始化背景移除器"""
        self._last_mask = None
        
    def remove_background(self, image: np.ndarray, 
                         method: str = "grabcut") -> Optional[np.ndarray]:
        """移除图像背景"""
        try:
            if method == "grabcut":
                return self._remove_with_grabcut(image)
            elif method == "threshold":
                return self._remove_with_threshold(image)
            elif method == "edge":
                return self._remove_with_edge_detection(image)
            else:
                raise ValueError(f"不支持的移除方法: {method}")
                
        except Exception as e:
            print(f"移除背景失败: {e}")
            return None
    
    def _remove_with_grabcut(self, image: np.ndarray) -> np.ndarray:
        """使用GrabCut算法移除背景"""
        try:
            # 创建掩码
            mask = np.zeros(image.shape[:2], np.uint8)
            
            # 创建临时数组
            bgd_model = np.zeros((1, 65), np.float64)
            fgd_model = np.zeros((1, 65), np.float64)
            
            # 定义矩形区域（图像中心区域）
            h, w = image.shape[:2]
            margin = 10
            rect = (margin, margin, w - 2 * margin, h - 2 * margin)
            
            # 执行GrabCut
            cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 
                       5, cv2.GC_INIT_WITH_RECT)
            
            # 创建前景掩码
            mask2 = np.where((mask == 2) | (mask == 0), 0, 255).astype('uint8')
            
            # 应用掩码
            result = cv2.bitwise_and(image, image, mask=mask2)
            
            # 添加Alpha通道
            b, g, r = cv2.split(result)
            rgba = [b, g, r, mask2]
            result_with_alpha = cv2.merge(rgba)
            
            # 保存掩码
            self._last_mask = mask2
            
            return result_with_alpha
            
        except Exception as e:
            print(f"GrabCut移除失败: {e}")
            return image
    
    def _remove_with_threshold(self, image: np.ndarray) -> np.ndarray:
        """使用阈值分割移除背景"""
        try:
            # 转换为灰度图
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            # 应用高斯模糊
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # 应用阈值
            _, thresh = cv2.threshold(blurred, 0, 255, 
                                     cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # 形态学操作
            kernel = np.ones((3, 3), np.uint8)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
            
            # 应用掩码
            result = cv2.bitwise_and(image, image, mask=thresh)
            
            # 添加Alpha通道
            if len(image.shape) == 3:
                b, g, r = cv2.split(result)
                rgba = [b, g, r, thresh]
                result_with_alpha = cv2.merge(rgba)
            else:
                result_with_alpha = cv2.merge([result, thresh])
            
            # 保存掩码
            self._last_mask = thresh
            
            return result_with_alpha
            
        except Exception as e:
            print(f"阈值分割移除失败: {e}")
            return image
    
    def _remove_with_edge_detection(self, image: np.ndarray) -> np.ndarray:
        """使用边缘检测移除背景"""
        try:
            # 转换为灰度图
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            # 应用高斯模糊
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # 边缘检测
            edges = cv2.Canny(blurred, 50, 150)
            
            # 膨胀操作
            kernel = np.ones((3, 3), np.uint8)
            dilated = cv2.dilate(edges, kernel, iterations=2)
            
            # 填充孔洞
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, 
                                         cv2.CHAIN_APPROX_SIMPLE)
            
            # 创建掩码
            mask = np.zeros_like(gray)
            cv2.drawContours(mask, contours, -1, 255, -1)
            
            # 应用掩码
            result = cv2.bitwise_and(image, image, mask=mask)
            
            # 添加Alpha通道
            if len(image.shape) == 3:
                b, g, r = cv2.split(result)
                rgba = [b, g, r, mask]
                result_with_alpha = cv2.merge(rgba)
            else:
                result_with_alpha = cv2.merge([result, mask])
            
            # 保存掩码
            self._last_mask = mask
            
            return result_with_alpha
            
        except Exception as e:
            print(f"边缘检测移除失败: {e}")
            return image
    
    def get_last_mask(self) -> Optional[np.ndarray]:
        """获取最后一个掩码"""
        return self._last_mask
    
    def refine_mask(self, mask: np.ndarray, iterations: int = 2) -> np.ndarray:
        """优化掩码"""
        try:
            # 形态学操作
            kernel = np.ones((3, 3), np.uint8)
            
            # 开运算（去除小噪点）
            refined = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, 
                                      iterations=iterations)
            
            # 闭运算（填充小孔洞）
            refined = cv2.morphologyEx(refined, cv2.MORPH_CLOSE, kernel, 
                                      iterations=iterations)
            
            return refined
            
        except Exception as e:
            print(f"优化掩码失败: {e}")
            return mask
    
    def create_background_mask(self, image: np.ndarray, 
                              bg_color: Tuple[int, int, int] = (255, 255, 255),
                              tolerance: int = 30) -> np.ndarray:
        """创建背景掩码（基于颜色）"""
        try:
            # 转换为HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # 转换背景颜色到HSV
            bg_bgr = np.uint8([[bg_color]])
            bg_hsv = cv2.cvtColor(bg_bgr, cv2.COLOR_BGR2HSV)[0][0]
            
            # 创建掩码
            lower = np.array([max(0, bg_hsv[0] - tolerance),
                            max(0, bg_hsv[1] - tolerance),
                            max(0, bg_hsv[2] - tolerance)])
            upper = np.array([min(179, bg_hsv[0] + tolerance),
                            min(255, bg_hsv[1] + tolerance),
                            min(255, bg_hsv[2] + tolerance)])
            
            mask = cv2.inRange(hsv, lower, upper)
            
            # 反转掩码（前景为白色）
            mask = cv2.bitwise_not(mask)
            
            return mask
            
        except Exception as e:
            print(f"创建背景掩码失败: {e}")
            return np.ones(image.shape[:2], np.uint8) * 255