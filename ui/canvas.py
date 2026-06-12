"""
画布模块
中央画布视图 - 支持图案交互操作
"""

import math
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QRectF, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPen, QColor, QTransform, QCursor


class CanvasView(QGraphicsView):
    """画布视图类 - 支持图案交互操作"""
    
    # 信号
    zoom_changed = pyqtSignal(float)
    position_changed = pyqtSignal(QPointF)
    pattern_selected = pyqtSignal(QGraphicsPixmapItem)
    
    def __init__(self, parent=None):
        """初始化画布视图"""
        super().__init__(parent)
        
        # 创建场景
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        
        # 设置视图属性
        self._setup_view()
        
        # 状态变量
        self._zoom = 1.0
        self._pan_start = None
        self._is_panning = False
        self._is_rotating = False
        self._rotation_start = None
        
        # 画布项
        self._background_item = None
        self._pattern_items = []
        self._selected_item = None
        
        # 控制点
        self._control_points = []
        self._resize_handle = None
        self._resize_start_pos = None
        self._resize_start_rect = None
        
        # 设置定时器用于更新
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._update_scene)
        self._update_timer.start(16)  # 约60fps
    
    def _setup_view(self):
        """设置视图属性"""
        # 设置渲染提示
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # 设置拖拽模式
        self.setDragMode(QGraphicsView.NoDrag)
        
        # 设置滚动条策略
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 设置背景颜色
        self.setBackgroundBrush(QBrush(QColor(40, 40, 60)))
        
        # 设置视图更新模式
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        
        # 设置对齐方式
        self.setAlignment(Qt.AlignCenter)
        
        # 启用鼠标跟踪
        self.setMouseTracking(True)
    
    def set_background(self, pixmap: QPixmap):
        """设置背景图像"""
        # 移除旧的背景
        if self._background_item:
            self._scene.removeItem(self._background_item)
        
        # 创建新的背景项
        self._background_item = QGraphicsPixmapItem(pixmap)
        self._background_item.setZValue(-1)  # 放在最底层
        self._scene.addItem(self._background_item)
        
        # 调整视图以适应背景
        self.fit_in_view()
    
    def add_pattern(self, pixmap: QPixmap, position: QPointF = QPointF(0, 0)):
        """添加图案到画布"""
        # 创建图案项
        pattern_item = QGraphicsPixmapItem(pixmap)
        pattern_item.setPos(position)
        pattern_item.setFlag(QGraphicsPixmapItem.ItemIsMovable)
        pattern_item.setFlag(QGraphicsPixmapItem.ItemIsSelectable)
        pattern_item.setFlag(QGraphicsPixmapItem.ItemSendsGeometryChanges)
        
        # 设置Z值（图案在背景上面）
        pattern_item.setZValue(0)
        
        # 添加到场景
        self._scene.addItem(pattern_item)
        self._pattern_items.append(pattern_item)
        
        # 选中这个图案
        self._select_item(pattern_item)
        
        return pattern_item
    
    def remove_pattern(self, item):
        """从画布移除图案"""
        if item in self._pattern_items:
            self._scene.removeItem(item)
            self._pattern_items.remove(item)
            
            # 如果移除的是选中的项，清空选中
            if self._selected_item == item:
                self._selected_item = None
    
    def clear_patterns(self):
        """清空所有图案"""
        for item in self._pattern_items:
            self._scene.removeItem(item)
        self._pattern_items.clear()
        self._selected_item = None
    
    def _select_item(self, item):
        """选中图案项"""
        # 取消之前选中的项
        if self._selected_item:
            self._selected_item.setSelected(False)
        
        # 选中新项
        self._selected_item = item
        if item:
            item.setSelected(True)
            self.pattern_selected.emit(item)
    
    def fit_in_view(self):
        """调整视图以适应内容"""
        if self._background_item:
            self.fitInView(self._background_item, Qt.KeepAspectRatio)
            self._zoom = self.transform().m11()
            self.zoom_changed.emit(self._zoom)
    
    def wheelEvent(self, event):
        """鼠标滚轮事件（缩放）"""
        # 获取缩放因子
        factor = 1.1
        if event.angleDelta().y() > 0:
            # 放大
            self._zoom *= factor
        else:
            # 缩小
            self._zoom /= factor
        
        # 限制缩放范围
        self._zoom = max(0.1, min(5.0, self._zoom))
        
        # 应用缩放
        self.setTransform(self.transform().scale(factor, factor))
        
        # 发送信号
        self.zoom_changed.emit(self._zoom)
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        scene_pos = self.mapToScene(event.pos())
        
        if event.button() == Qt.LeftButton:
            # 左键：选择或拖动
            item = self.itemAt(event.pos())
            
            if item and item in self._pattern_items:
                # 点击了图案
                self._select_item(item)
                
                # 检查是否点击了控制点
                self._check_resize_handle(scene_pos)
                
                if not self._resize_handle:
                    # 没有点击控制点，开始拖动
                    self.setDragMode(QGraphicsView.ScrollHandDrag)
                    super().mousePressEvent(event)
            else:
                # 点击了空白区域
                self._select_item(None)
                self.setDragMode(QGraphicsView.NoDrag)
                
        elif event.button() == Qt.MiddleButton:
            # 中键：平移
            self._is_panning = True
            self._pan_start = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            
        elif event.button() == Qt.RightButton:
            # 右键：旋转
            if self._selected_item:
                self._is_rotating = True
                self._rotation_start = scene_pos
                self.setCursor(Qt.ClosedHandCursor)
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        scene_pos = self.mapToScene(event.pos())
        
        # 发送位置变化信号
        self.position_changed.emit(scene_pos)
        
        if self._is_panning and self._pan_start is not None:
            # 平移视图
            delta = event.pos() - self._pan_start
            self._pan_start = event.pos()
            
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )
            
        elif self._is_rotating and self._rotation_start is not None and self._selected_item:
            # 旋转图案
            # 计算旋转角度
            item_center = self._selected_item.boundingRect().center()
            item_scene_pos = self._selected_item.mapToScene(item_center)
            
            # 计算角度变化
            start_angle = self._calculate_angle(item_scene_pos, self._rotation_start)
            current_angle = self._calculate_angle(item_scene_pos, scene_pos)
            angle_delta = current_angle - start_angle
            
            # 应用旋转
            current_rotation = self._selected_item.rotation()
            self._selected_item.setRotation(current_rotation + angle_delta)
            
            self._rotation_start = scene_pos
            
        elif self._resize_handle and self._selected_item:
            # 调整大小
            self._resize_pattern(scene_pos)
        
        else:
            # 更新鼠标光标
            self._update_cursor(scene_pos)
            
            # 调用父类方法
            super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.MiddleButton:
            self._is_panning = False
            self._pan_start = None
            self.setCursor(Qt.ArrowCursor)
            
        elif event.button() == Qt.RightButton:
            self._is_rotating = False
            self._rotation_start = None
            self.setCursor(Qt.ArrowCursor)
            
        elif event.button() == Qt.LeftButton:
            self._resize_handle = None
            self.setDragMode(QGraphicsView.NoDrag)
        
        super().mouseReleaseEvent(event)
    
    def keyPressEvent(self, event):
        """键盘按下事件"""
        if event.key() == Qt.Key_F:
            # F键适应视图
            self.fit_in_view()
        elif event.key() == Qt.Key_Delete:
            # 删除键移除选中的图案
            if self._selected_item:
                self.remove_pattern(self._selected_item)
        elif event.key() == Qt.Key_Escape:
            # ESC键取消选择
            self._select_item(None)
        elif event.key() == Qt.Key_H:
            # H键水平镜像
            if self._selected_item:
                self.mirror_pattern(self._selected_item, horizontal=True)
        elif event.key() == Qt.Key_V:
            # V键垂直镜像
            if self._selected_item:
                self.mirror_pattern(self._selected_item, vertical=True)
        elif event.key() == Qt.Key_L:
            # L键左旋
            if self._selected_item:
                self.rotate_pattern(self._selected_item, -15)
        elif event.key() == Qt.Key_R:
            # R键右旋
            if self._selected_item:
                self.rotate_pattern(self._selected_item, 15)
        else:
            super().keyPressEvent(event)
    
    def _calculate_angle(self, center, point):
        """计算两点之间的角度"""
        dx = point.x() - center.x()
        dy = point.y() - center.y()
        angle = math.degrees(math.atan2(dy, dx))
        return angle
    
    def _check_resize_handle(self, pos):
        """检查是否点击了调整大小的控制点"""
        if not self._selected_item:
            return False
        
        # 获取图案边界
        rect = self._selected_item.boundingRect()
        item_pos = self._selected_item.pos()
        
        # 转换为场景坐标
        scene_rect = QRectF(
            item_pos.x() + rect.x(),
            item_pos.y() + rect.y(),
            rect.width(),
            rect.height()
        )
        
        # 检查四个角
        handle_size = 10
        corners = [
            (scene_rect.topLeft(), "top_left"),
            (scene_rect.topRight(), "top_right"),
            (scene_rect.bottomLeft(), "bottom_left"),
            (scene_rect.bottomRight(), "bottom_right")
        ]
        
        for corner_pos, handle_name in corners:
            distance = math.sqrt((pos.x() - corner_pos.x())**2 + 
                               (pos.y() - corner_pos.y())**2)
            if distance < handle_size:
                self._resize_handle = handle_name
                self._resize_start_pos = pos
                self._resize_start_rect = scene_rect
                return True
        
        return False
    
    def _resize_pattern(self, current_pos):
        """调整图案大小"""
        if not self._selected_item or not self._resize_handle:
            return
        
        # 计算缩放比例
        start_rect = self._resize_start_rect
        delta = current_pos - self._resize_start_pos
        
        # 根据控制点计算新的尺寸
        new_rect = QRectF(start_rect)
        
        if "right" in self._resize_handle:
            new_rect.setRight(start_rect.right() + delta.x())
        if "left" in self._resize_handle:
            new_rect.setLeft(start_rect.left() + delta.x())
        if "bottom" in self._resize_handle:
            new_rect.setBottom(start_rect.bottom() + delta.y())
        if "top" in self._resize_handle:
            new_rect.setTop(start_rect.top() + delta.y())
        
        # 保持比例
        if new_rect.width() > 0 and new_rect.height() > 0:
            # 计算缩放比例
            scale_x = new_rect.width() / start_rect.width()
            scale_y = new_rect.height() / start_rect.height()
            scale = min(scale_x, scale_y)
            
            # 应用缩放
            self._selected_item.setScale(scale)
    
    def _update_cursor(self, pos):
        """更新鼠标光标"""
        if self._selected_item:
            # 检查是否在控制点附近
            if self._check_resize_handle(pos):
                # 根据控制点设置光标
                if "top_left" in self._resize_handle or "bottom_right" in self._resize_handle:
                    self.setCursor(Qt.SizeFDiagCursor)
                else:
                    self.setCursor(Qt.SizeBDiagCursor)
                return
        
        self.setCursor(Qt.ArrowCursor)
    
    def _update_scene(self):
        """更新场景"""
        # 这里可以添加场景更新逻辑
        pass
    
    def mirror_pattern(self, item, horizontal=False, vertical=False):
        """镜像图案"""
        if item:
            transform = QTransform()
            if horizontal:
                transform.scale(-1, 1)
            if vertical:
                transform.scale(1, -1)
            
            # 应用变换
            item.setTransform(transform, True)
    
    def rotate_pattern(self, item, angle):
        """旋转图案"""
        if item:
            current_rotation = item.rotation()
            item.setRotation(current_rotation + angle)
    
    def resize_pattern(self, item, width, height):
        """调整图案大小"""
        if item:
            # 计算缩放比例
            current_rect = item.boundingRect()
            if current_rect.width() > 0 and current_rect.height() > 0:
                scale_x = width / current_rect.width()
                scale_y = height / current_rect.height()
                item.setScale(min(scale_x, scale_y))
    
    def move_pattern(self, item, position):
        """移动图案"""
        if item:
            item.setPos(position)
    
    def update_pattern(self, item, pixmap):
        """更新图案图像"""
        if item:
            item.setPixmap(pixmap)
    
    def get_composite_image(self):
        """获取合成后的图像"""
        # 创建一个与背景相同大小的图像
        if not self._background_item:
            return None
        
        background_pixmap = self._background_item.pixmap()
        result = QPixmap(background_pixmap.size())
        result.fill(Qt.transparent)
        
        # 绘制背景
        painter = QPainter(result)
        painter.drawPixmap(0, 0, background_pixmap)
        
        # 绘制所有图案
        for item in self._pattern_items:
            if item.isVisible():
                # 获取图案位置和大小
                pos = item.pos()
                pixmap = item.pixmap()
                
                # 应用变换
                transform = item.transform()
                transformed_pixmap = pixmap.transformed(transform)
                
                # 绘制图案
                painter.drawPixmap(int(pos.x()), int(pos.y()), transformed_pixmap)
        
        painter.end()
        
        return result
    
    def get_zoom(self):
        """获取当前缩放比例"""
        return self._zoom
    
    def set_zoom(self, zoom: float):
        """设置缩放比例"""
        # 计算缩放因子
        factor = zoom / self._zoom
        self._zoom = zoom
        
        # 应用缩放
        self.setTransform(self.transform().scale(factor, factor))
        
        # 发送信号
        self.zoom_changed.emit(self._zoom)
    
    def get_pattern_items(self):
        """获取所有图案项"""
        return self._pattern_items
    
    def get_selected_item(self):
        """获取选中的图案项"""
        return self._selected_item