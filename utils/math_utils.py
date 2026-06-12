"""
数学计算工具模块
提供常用的数学计算函数
"""

import math
from typing import Tuple, Union


class MathUtils:
    """数学计算工具类"""
    
    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """将值限制在最小值和最大值之间"""
        return max(min_val, min(max_val, value))
    
    @staticmethod
    def lerp(start: float, end: float, t: float) -> float:
        """线性插值"""
        return start + (end - start) * t
    
    @staticmethod
    def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """计算两点之间的距离"""
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    
    @staticmethod
    def angle_between(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """计算两点之间的角度（度）"""
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        return angle_deg
    
    @staticmethod
    def point_in_rect(point: Tuple[float, float], 
                      rect: Tuple[float, float, float, float]) -> bool:
        """判断点是否在矩形内"""
        x, y = point
        rx, ry, rw, rh = rect
        return rx <= x <= rx + rw and ry <= y <= ry + rh
    
    @staticmethod
    def rect_intersection(rect1: Tuple[float, float, float, float],
                         rect2: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
        """计算两个矩形的交集"""
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        
        # 计算交集矩形
        x_left = max(x1, x2)
        y_top = max(y1, y2)
        x_right = min(x1 + w1, x2 + w2)
        y_bottom = min(y1 + h1, y2 + h2)
        
        if x_left < x_right and y_top < y_bottom:
            return (x_left, y_top, x_right - x_left, y_bottom - y_top)
        else:
            return (0, 0, 0, 0)  # 没有交集
    
    @staticmethod
    def scale_rect(rect: Tuple[float, float, float, float], 
                   scale: float, 
                   center: Tuple[float, float] = None) -> Tuple[float, float, float, float]:
        """缩放矩形"""
        x, y, w, h = rect
        
        if center is None:
            center = (x + w / 2, y + h / 2)
        
        # 计算新尺寸
        new_w = w * scale
        new_h = h * scale
        
        # 计算新位置（保持中心点不变）
        new_x = center[0] - new_w / 2
        new_y = center[1] - new_h / 2
        
        return (new_x, new_y, new_w, new_h)
    
    @staticmethod
    def rotate_point(point: Tuple[float, float], 
                    angle: float, 
                    center: Tuple[float, float] = (0, 0)) -> Tuple[float, float]:
        """旋转点"""
        x, y = point
        cx, cy = center
        
        # 转换为弧度
        angle_rad = math.radians(angle)
        
        # 旋转公式
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        new_x = cx + (x - cx) * cos_a - (y - cy) * sin_a
        new_y = cy + (x - cx) * sin_a + (y - cy) * cos_a
        
        return (new_x, new_y)
    
    @staticmethod
    def normalize(value: float, min_val: float, max_val: float) -> float:
        """将值归一化到0-1范围"""
        if max_val == min_val:
            return 0.0
        return (value - min_val) / (max_val - min_val)
    
    @staticmethod
    def denormalize(value: float, min_val: float, max_val: float) -> float:
        """将0-1范围的值反归一化"""
        return min_val + value * (max_val - min_val)
    
    @staticmethod
    def smooth_step(edge0: float, edge1: float, x: float) -> float:
        """平滑阶梯函数"""
        t = MathUtils.clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
        return t * t * (3 - 2 * t)
    
    @staticmethod
    def ease_in_quad(t: float) -> float:
        """二次缓入"""
        return t * t
    
    @staticmethod
    def ease_out_quad(t: float) -> float:
        """二次缓出"""
        return t * (2 - t)
    
    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """二次缓入缓出"""
        if t < 0.5:
            return 2 * t * t
        else:
            return -1 + (4 - 2 * t) * t
    
    @staticmethod
    def round_to(value: float, decimals: int = 2) -> float:
        """四舍五入到指定小数位"""
        factor = 10 ** decimals
        return round(value * factor) / factor