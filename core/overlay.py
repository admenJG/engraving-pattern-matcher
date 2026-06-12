"""
叠加图案管理模块
管理图案的叠加、变换、渲染
"""

import cv2
import numpy as np
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path


class OverlayManager:
    """叠加图案管理器"""
    
    def __init__(self):
        """初始化管理器"""
        self._overlays = []
        self._canvas_size = (800, 600)  # 默认画布尺寸
        
    def set_canvas_size(self, width: int, height: int):
        """设置画布尺寸"""
        self._canvas_size = (width, height)
    
    def add_overlay(self, image: np.ndarray, 
                   position: Tuple[int, int] = (0, 0),
                   size: Optional[Tuple[int, int]] = None,
                   rotation: float = 0,
                   opacity: float = 1.0,
                   flip_h: bool = False,
                   flip_v: bool = False) -> int:
        """添加叠加图案"""
        try:
            # 处理图像
            processed_image = self._process_image(
                image, size, rotation, opacity, flip_h, flip_v
            )
            
            # 创建叠加信息
            overlay = {
                "id": len(self._overlays) + 1,
                "image": processed_image,
                "original_image": image,
                "position": position,
                "size": size or (image.shape[1], image.shape[0]),
                "rotation": rotation,
                "opacity": opacity,
                "flip_h": flip_h,
                "flip_v": flip_v,
                "visible": True,
                "locked": False
            }
            
            self._overlays.append(overlay)
            return overlay["id"]
            
        except Exception as e:
            print(f"添加叠加图案失败: {e}")
            return -1
    
    def remove_overlay(self, overlay_id: int) -> bool:
        """移除叠加图案"""
        try:
            for i, overlay in enumerate(self._overlays):
                if overlay["id"] == overlay_id:
                    self._overlays.pop(i)
                    return True
            return False
        except Exception as e:
            print(f"移除叠加图案失败: {e}")
            return False
    
    def update_overlay(self, overlay_id: int, 
                      position: Optional[Tuple[int, int]] = None,
                      size: Optional[Tuple[int, int]] = None,
                      rotation: Optional[float] = None,
                      opacity: Optional[float] = None,
                      flip_h: Optional[bool] = None,
                      flip_v: Optional[bool] = None) -> bool:
        """更新叠加图案"""
        try:
            for overlay in self._overlays:
                if overlay["id"] == overlay_id:
                    # 更新属性
                    if position is not None:
                        overlay["position"] = position
                    if size is not None:
                        overlay["size"] = size
                    if rotation is not None:
                        overlay["rotation"] = rotation
                    if opacity is not None:
                        overlay["opacity"] = opacity
                    if flip_h is not None:
                        overlay["flip_h"] = flip_h
                    if flip_v is not None:
                        overlay["flip_v"] = flip_v
                    
                    # 重新处理图像
                    overlay["image"] = self._process_image(
                        overlay["original_image"],
                        overlay["size"],
                        overlay["rotation"],
                        overlay["opacity"],
                        overlay["flip_h"],
                        overlay["flip_v"]
                    )
                    
                    return True
            return False
        except Exception as e:
            print(f"更新叠加图案失败: {e}")
            return False
    
    def render_all(self, background: Optional[np.ndarray] = None) -> np.ndarray:
        """渲染所有叠加图案"""
        try:
            # 创建或使用背景
            if background is None:
                canvas = np.ones((self._canvas_size[1], self._canvas_size[0], 3), 
                               dtype=np.uint8) * 255  # 白色背景
            else:
                canvas = background.copy()
                # 调整背景尺寸
                if canvas.shape[:2] != (self._canvas_size[1], self._canvas_size[0]):
                    canvas = cv2.resize(canvas, self._canvas_size)
            
            # 渲染每个叠加图案
            for overlay in self._overlays:
                if not overlay["visible"]:
                    continue
                
                canvas = self._render_overlay(canvas, overlay)
            
            return canvas
            
        except Exception as e:
            print(f"渲染叠加图案失败: {e}")
            # 返回错误图像
            error_img = np.ones((self._canvas_size[1], self._canvas_size[0], 3), 
                              dtype=np.uint8) * 200
            cv2.putText(error_img, "Render Error", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return error_img
    
    def _process_image(self, image: np.ndarray,
                      size: Optional[Tuple[int, int]],
                      rotation: float,
                      opacity: float,
                      flip_h: bool,
                      flip_v: bool) -> np.ndarray:
        """处理图像（缩放、旋转、翻转、透明度）"""
        try:
            processed = image.copy()
            
            # 水平翻转
            if flip_h:
                processed = cv2.flip(processed, 1)
            
            # 垂直翻转
            if flip_v:
                processed = cv2.flip(processed, 0)
            
            # 缩放
            if size is not None:
                processed = cv2.resize(processed, size, interpolation=cv2.INTER_AREA)
            
            # 旋转
            if rotation != 0:
                processed = self._rotate_image(processed, rotation)
            
            # 调整透明度
            if opacity < 1.0:
                processed = self._adjust_opacity(processed, opacity)
            
            return processed
            
        except Exception as e:
            print(f"处理图像失败: {e}")
            return image
    
    def _rotate_image(self, image: np.ndarray, angle: float) -> np.ndarray:
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
    
    def _adjust_opacity(self, image: np.ndarray, opacity: float) -> np.ndarray:
        """调整图像透明度"""
        try:
            # 如果图像没有Alpha通道，添加一个
            if len(image.shape) == 3 and image.shape[2] == 3:
                # BGR转BGRA
                image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
            
            # 调整Alpha通道
            image[:, :, 3] = (image[:, :, 3] * opacity).astype(np.uint8)
            
            return image
        except Exception as e:
            print(f"调整透明度失败: {e}")
            return image
    
    def _render_overlay(self, canvas: np.ndarray, overlay: Dict[str, Any]) -> np.ndarray:
        """渲染单个叠加图案到画布"""
        try:
            image = overlay["image"]
            x, y = overlay["position"]
            h, w = image.shape[:2]
            
            # 确保坐标在画布范围内
            canvas_h, canvas_w = canvas.shape[:2]
            x = max(0, min(x, canvas_w - w))
            y = max(0, min(y, canvas_h - h))
            
            # 计算有效区域
            end_x = min(x + w, canvas_w)
            end_y = min(y + h, canvas_h)
            img_w = end_x - x
            img_h = end_y - y
            
            if img_w <= 0 or img_h <= 0:
                return canvas
            
            # 获取图像区域
            img_region = image[:img_h, :img_w]
            
            # 处理Alpha通道
            if len(img_region.shape) == 3 and img_region.shape[2] == 4:
                # 有Alpha通道
                alpha = img_region[:, :, 3:] / 255.0
                rgb = img_region[:, :, :3]
                
                # 混合图像
                for c in range(3):
                    canvas[y:end_y, x:end_x, c] = \
                        (rgb[:, :, c] * alpha[:, :, 0] + 
                         canvas[y:end_y, x:end_x, c] * (1 - alpha[:, :, 0]))
            else:
                # 没有Alpha通道，直接复制
                canvas[y:end_y, x:end_x] = img_region
            
            return canvas
            
        except Exception as e:
            print(f"渲染叠加图案失败: {e}")
            return canvas
    
    def clear_all(self):
        """清空所有叠加图案"""
        self._overlays.clear()
    
    def get_overlay_count(self) -> int:
        """获取叠加图案数量"""
        return len(self._overlays)
    
    def get_overlay_by_id(self, overlay_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取叠加图案"""
        for overlay in self._overlays:
            if overlay["id"] == overlay_id:
                return overlay
        return None