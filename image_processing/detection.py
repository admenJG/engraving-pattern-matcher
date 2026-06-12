"""
图像检测模块
提供图像特征检测功能
"""

import cv2
import numpy as np
from typing import Optional, Tuple, List, Dict, Any


class ImageDetector:
    """图像检测器"""
    
    def __init__(self):
        """初始化检测器"""
        pass
    
    def detect_objects(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """检测图像中的物体"""
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
            
            # 查找轮廓
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, 
                                         cv2.CHAIN_APPROX_SIMPLE)
            
            # 过滤和排序轮廓
            objects = []
            for contour in contours:
                # 计算面积
                area = cv2.contourArea(contour)
                
                # 过滤小轮廓
                if area < 100:
                    continue
                
                # 获取边界矩形
                x, y, w, h = cv2.boundingRect(contour)
                
                # 计算中心点
                center_x = x + w // 2
                center_y = y + h // 2
                
                # 添加到物体列表
                objects.append({
                    "contour": contour,
                    "bbox": (x, y, w, h),
                    "center": (center_x, center_y),
                    "area": area,
                    "aspect_ratio": w / h if h > 0 else 0
                })
            
            # 按面积排序
            objects.sort(key=lambda obj: obj["area"], reverse=True)
            
            return objects
            
        except Exception as e:
            print(f"检测物体失败: {e}")
            return []
    
    def detect_stone_bounds(self, image: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """检测石头边界"""
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
            
            # 查找轮廓
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, 
                                         cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return None
            
            # 找到最大轮廓（假设为石头）
            largest_contour = max(contours, key=cv2.contourArea)
            
            # 获取边界矩形
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # 添加边距
            margin = 10
            x = max(0, x - margin)
            y = max(0, y - margin)
            w = min(image.shape[1] - x, w + 2 * margin)
            h = min(image.shape[0] - y, h + 2 * margin)
            
            return (x, y, w, h)
            
        except Exception as e:
            print(f"检测石头边界失败: {e}")
            return None
    
    def detect_edges(self, image: np.ndarray, 
                    low_threshold: int = 50, 
                    high_threshold: int = 150) -> np.ndarray:
        """检测图像边缘"""
        try:
            # 转换为灰度图
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            # 应用高斯模糊
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # 边缘检测
            edges = cv2.Canny(blurred, low_threshold, high_threshold)
            
            return edges
            
        except Exception as e:
            print(f"检测边缘失败: {e}")
            return np.zeros_like(image)
    
    def detect_corners(self, image: np.ndarray, max_corners: int = 100) -> List[Tuple[int, int]]:
        """检测图像角点"""
        try:
            # 转换为灰度图
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            # 转换为float32
            gray_float = np.float32(gray)
            
            # 检测角点
            corners = cv2.goodFeaturesToTrack(gray_float, max_corners, 
                                            0.01, 10, None, 
                                            blockSize=3, 
                                            gradientSize=3)
            
            if corners is None:
                return []
            
            # 转换为整数坐标
            corner_points = []
            for corner in corners:
                x, y = corner.ravel()
                corner_points.append((int(x), int(y)))
            
            return corner_points
            
        except Exception as e:
            print(f"检测角点失败: {e}")
            return []
    
    def detect_lines(self, image: np.ndarray, 
                    min_line_length: int = 50, 
                    max_line_gap: int = 10) -> List[Dict[str, Any]]:
        """检测图像中的直线"""
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
            
            # 检测直线
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, 
                                   minLineLength=min_line_length, 
                                   maxLineGap=max_line_gap)
            
            if lines is None:
                return []
            
            # 处理直线
            line_list = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                
                # 计算长度和角度
                length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
                
                line_list.append({
                    "start": (x1, y1),
                    "end": (x2, y2),
                    "length": length,
                    "angle": angle,
                    "center": ((x1 + x2) // 2, (y1 + y2) // 2)
                })
            
            # 按长度排序
            line_list.sort(key=lambda line: line["length"], reverse=True)
            
            return line_list
            
        except Exception as e:
            print(f"检测直线失败: {e}")
            return []
    
    def detect_contours(self, image: np.ndarray, 
                       min_area: int = 100) -> List[np.ndarray]:
        """检测图像轮廓"""
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
            
            # 查找轮廓
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, 
                                         cv2.CHAIN_APPROX_SIMPLE)
            
            # 过滤小轮廓
            filtered_contours = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area >= min_area:
                    filtered_contours.append(contour)
            
            return filtered_contours
            
        except Exception as e:
            print(f"检测轮廓失败: {e}")
            return []