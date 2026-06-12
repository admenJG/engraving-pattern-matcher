"""
历史记录管理模块
实现撤销/重做功能
"""

from typing import Any, Callable, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class HistoryEntry:
    """历史记录条目"""
    action: str
    data: Any
    timestamp: datetime
    description: str = ""


class HistoryManager:
    """历史记录管理器"""
    
    def __init__(self, max_size: int = 30):
        """初始化管理器"""
        self._undo_stack: List[HistoryEntry] = []
        self._redo_stack: List[HistoryEntry] = []
        self._max_size = max_size
        self._listeners = []
        
    @property
    def can_undo(self) -> bool:
        """是否可以撤销"""
        return len(self._undo_stack) > 0
    
    @property
    def can_redo(self) -> bool:
        """是否可以重做"""
        return len(self._redo_stack) > 0
    
    @property
    def undo_count(self) -> int:
        """可撤销的操作数量"""
        return len(self._undo_stack)
    
    @property
    def redo_count(self) -> int:
        """可重做的操作数量"""
        return len(self._redo_stack)
    
    def add_listener(self, listener: Callable):
        """添加监听器"""
        self._listeners.append(listener)
    
    def remove_listener(self, listener: Callable):
        """移除监听器"""
        if listener in self._listeners:
            self._listeners.remove(listener)
    
    def _notify_listeners(self, event_type: str, data: Any = None):
        """通知监听器"""
        for listener in self._listeners:
            try:
                listener(event_type, data)
            except Exception as e:
                print(f"通知监听器失败: {e}")
    
    def push(self, action: str, data: Any, description: str = ""):
        """添加历史记录"""
        entry = HistoryEntry(
            action=action,
            data=data,
            timestamp=datetime.now(),
            description=description
        )
        
        # 添加到撤销栈
        self._undo_stack.append(entry)
        
        # 清空重做栈（新操作后不能重做之前的操作）
        self._redo_stack.clear()
        
        # 限制栈大小
        if len(self._undo_stack) > self._max_size:
            self._undo_stack.pop(0)
        
        self._notify_listeners("history_pushed", entry)
    
    def undo(self) -> Optional[HistoryEntry]:
        """撤销最后一个操作"""
        if not self.can_undo:
            return None
        
        # 从撤销栈弹出
        entry = self._undo_stack.pop()
        
        # 添加到重做栈
        self._redo_stack.append(entry)
        
        self._notify_listeners("history_undone", entry)
        return entry
    
    def redo(self) -> Optional[HistoryEntry]:
        """重做最后一个撤销的操作"""
        if not self.can_redo:
            return None
        
        # 从重做栈弹出
        entry = self._redo_stack.pop()
        
        # 添加到撤销栈
        self._undo_stack.append(entry)
        
        self._notify_listeners("history_redone", entry)
        return entry
    
    def clear(self):
        """清空历史记录"""
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._notify_listeners("history_cleared")
    
    def get_undo_description(self) -> Optional[str]:
        """获取下一个可撤销操作的描述"""
        if self.can_undo:
            return self._undo_stack[-1].description
        return None
    
    def get_redo_description(self) -> Optional[str]:
        """获取下一个可重做操作的描述"""
        if self.can_redo:
            return self._redo_stack[-1].description
        return None
    
    def get_history_list(self) -> List[dict]:
        """获取历史记录列表（用于显示）"""
        history = []
        
        # 添加撤销栈（倒序）
        for entry in reversed(self._undo_stack):
            history.append({
                "type": "undo",
                "action": entry.action,
                "description": entry.description,
                "timestamp": entry.timestamp
            })
        
        # 添加重做栈
        for entry in self._redo_stack:
            history.append({
                "type": "redo",
                "action": entry.action,
                "description": entry.description,
                "timestamp": entry.timestamp
            })
        
        return history
    
    def save_state(self) -> dict:
        """保存当前状态（用于持久化）"""
        return {
            "undo_stack": [
                {
                    "action": entry.action,
                    "data": entry.data,
                    "timestamp": entry.timestamp.isoformat(),
                    "description": entry.description
                }
                for entry in self._undo_stack
            ],
            "redo_stack": [
                {
                    "action": entry.action,
                    "data": entry.data,
                    "timestamp": entry.timestamp.isoformat(),
                    "description": entry.description
                }
                for entry in self._redo_stack
            ]
        }
    
    def load_state(self, state: dict):
        """加载状态（用于恢复）"""
        try:
            # 清空当前栈
            self._undo_stack.clear()
            self._redo_stack.clear()
            
            # 加载撤销栈
            for item in state.get("undo_stack", []):
                entry = HistoryEntry(
                    action=item["action"],
                    data=item["data"],
                    timestamp=datetime.fromisoformat(item["timestamp"]),
                    description=item.get("description", "")
                )
                self._undo_stack.append(entry)
            
            # 加载重做栈
            for item in state.get("redo_stack", []):
                entry = HistoryEntry(
                    action=item["action"],
                    data=item["data"],
                    timestamp=datetime.fromisoformat(item["timestamp"]),
                    description=item.get("description", "")
                )
                self._redo_stack.append(entry)
            
            self._notify_listeners("history_loaded")
            
        except Exception as e:
            print(f"加载历史状态失败: {e}")