"""
应用核心逻辑模块
管理应用状态和业务逻辑
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from enum import Enum


class AppState(Enum):
    """应用状态枚举"""
    IDLE = "idle"
    LOADING = "loading"
    EDITING = "editing"
    PROCESSING = "processing"
    ERROR = "error"


class AppCore:
    """应用核心逻辑类"""
    
    def __init__(self):
        """初始化应用核心"""
        self._state = AppState.IDLE
        self._current_material = None
        self._current_patterns = []
        self._selected_pattern = None
        self._listeners = []
        
        # 配置
        self._material_dir = None
        self._temp_dir = None
        
    @property
    def state(self) -> AppState:
        """获取当前状态"""
        return self._state
    
    @state.setter
    def state(self, new_state: AppState):
        """设置状态并通知监听器"""
        old_state = self._state
        self._state = new_state
        self._notify_listeners("state_changed", {
            "old_state": old_state,
            "new_state": new_state
        })
    
    @property
    def current_material(self):
        """获取当前原料"""
        return self._current_material
    
    @property
    def current_patterns(self) -> List:
        """获取当前图案列表"""
        return self._current_patterns
    
    @property
    def selected_pattern(self):
        """获取选中的图案"""
        return self._selected_pattern
    
    def add_listener(self, listener):
        """添加状态监听器"""
        self._listeners.append(listener)
    
    def remove_listener(self, listener):
        """移除状态监听器"""
        if listener in self._listeners:
            self._listeners.remove(listener)
    
    def _notify_listeners(self, event_type: str, data: Dict[str, Any] = None):
        """通知所有监听器"""
        for listener in self._listeners:
            if callable(listener):
                try:
                    listener(event_type, data)
                except Exception as e:
                    print(f"通知监听器失败: {e}")
    
    def set_material_dir(self, dir_path: str):
        """设置材料目录"""
        if os.path.exists(dir_path):
            self._material_dir = dir_path
            self._notify_listeners("material_dir_changed", {"path": dir_path})
            return True
        return False
    
    def set_temp_dir(self, dir_path: str):
        """设置临时目录"""
        if os.path.exists(dir_path):
            self._temp_dir = dir_path
            return True
        return False
    
    def load_material(self, file_path: str) -> bool:
        """加载原料"""
        try:
            self.state = AppState.LOADING
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            # 检查文件格式
            ext = os.path.splitext(file_path)[1].lower()
            supported_formats = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif'}
            if ext not in supported_formats:
                raise ValueError(f"不支持的文件格式: {ext}")
            
            # 加载原料（实际图像加载由UI层处理）
            self._current_material = {
                "path": file_path,
                "name": os.path.basename(file_path),
                "extension": ext
            }
            
            self.state = AppState.EDITING
            self._notify_listeners("material_loaded", self._current_material)
            
            return True
            
        except Exception as e:
            self.state = AppState.ERROR
            self._notify_listeners("error", {"message": str(e)})
            return False
    
    def add_pattern(self, pattern_info: Dict[str, Any]) -> bool:
        """添加图案"""
        try:
            # 生成图案ID
            pattern_id = len(self._current_patterns) + 1
            
            # 设置默认属性
            pattern = {
                "id": pattern_id,
                "path": pattern_info.get("path", ""),
                "name": pattern_info.get("name", f"图案{pattern_id}"),
                "x": pattern_info.get("x", 0),
                "y": pattern_info.get("y", 0),
                "width": pattern_info.get("width", 100),
                "height": pattern_info.get("height", 100),
                "rotation": pattern_info.get("rotation", 0),
                "opacity": pattern_info.get("opacity", 1.0),
                "flip_h": pattern_info.get("flip_h", False),
                "flip_v": pattern_info.get("flip_v", False),
                "visible": pattern_info.get("visible", True),
                "locked": pattern_info.get("locked", False)
            }
            
            self._current_patterns.append(pattern)
            self._selected_pattern = pattern
            
            self._notify_listeners("pattern_added", pattern)
            return True
            
        except Exception as e:
            self._notify_listeners("error", {"message": str(e)})
            return False
    
    def remove_pattern(self, pattern_id: int) -> bool:
        """移除图案"""
        try:
            for i, pattern in enumerate(self._current_patterns):
                if pattern["id"] == pattern_id:
                    removed_pattern = self._current_patterns.pop(i)
                    
                    # 如果移除的是选中的图案，清空选中
                    if self._selected_pattern and self._selected_pattern["id"] == pattern_id:
                        self._selected_pattern = None
                    
                    self._notify_listeners("pattern_removed", removed_pattern)
                    return True
            
            return False
            
        except Exception as e:
            self._notify_listeners("error", {"message": str(e)})
            return False
    
    def update_pattern(self, pattern_id: int, updates: Dict[str, Any]) -> bool:
        """更新图案属性"""
        try:
            for pattern in self._current_patterns:
                if pattern["id"] == pattern_id:
                    # 更新属性
                    for key, value in updates.items():
                        if key in pattern:
                            pattern[key] = value
                    
                    # 如果更新的是选中的图案
                    if self._selected_pattern and self._selected_pattern["id"] == pattern_id:
                        self._selected_pattern = pattern
                    
                    self._notify_listeners("pattern_updated", pattern)
                    return True
            
            return False
            
        except Exception as e:
            self._notify_listeners("error", {"message": str(e)})
            return False
    
    def select_pattern(self, pattern_id: int) -> bool:
        """选择图案"""
        try:
            for pattern in self._current_patterns:
                if pattern["id"] == pattern_id:
                    self._selected_pattern = pattern
                    self._notify_listeners("pattern_selected", pattern)
                    return True
            
            return False
            
        except Exception as e:
            self._notify_listeners("error", {"message": str(e)})
            return False
    
    def clear_patterns(self):
        """清空所有图案"""
        self._current_patterns.clear()
        self._selected_pattern = None
        self._notify_listeners("patterns_cleared")
    
    def get_pattern_by_id(self, pattern_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取图案"""
        for pattern in self._current_patterns:
            if pattern["id"] == pattern_id:
                return pattern
        return None
    
    def get_patterns_count(self) -> int:
        """获取图案数量"""
        return len(self._current_patterns)
    
    def reset(self):
        """重置应用状态"""
        self._state = AppState.IDLE
        self._current_material = None
        self._current_patterns.clear()
        self._selected_pattern = None
        self._notify_listeners("app_reset")