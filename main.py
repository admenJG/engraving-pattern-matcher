#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电脑雕刻套图匹配系统 - Computer Engraving Pattern Matching System
主程序入口
"""

import sys
import os

def _configure_qt_plugin_paths():
    """Set Qt plugin paths before QApplication is created."""
    if sys.platform.startswith("win"):
        os.environ["QT_QPA_PLATFORM"] = "windows"

    try:
        import PyQt5
        candidates = [
            os.path.join(os.path.dirname(PyQt5.__file__), "Qt5", "plugins"),
            r"D:\软件\开发环境工具依赖\Python\Lib\site-packages\PyQt5\Qt5\plugins",
        ]
    except Exception:
        candidates = [
            r"D:\软件\开发环境工具依赖\Python\Lib\site-packages\PyQt5\Qt5\plugins",
        ]

    for plugins_dir in candidates:
        platform_path = os.path.join(plugins_dir, "platforms")
        if os.path.exists(platform_path):
            os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platform_path
            os.environ["QT_PLUGIN_PATH"] = plugins_dir
            return


_configure_qt_plugin_paths()

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QSlider, QFileDialog, QMessageBox, QSplitter, QFrame,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QGraphicsItemGroup, QGraphicsItem,
    QSpinBox, QComboBox, QSizePolicy, QScrollArea, QStyle
)
from PyQt5.QtCore import Qt, QSize, QTimer, QMimeData, QPoint, QRectF, QPointF, QThread, pyqtSignal
from PyQt5.QtGui import (
    QPixmap, QImage, QColor, QPainter, QBrush, QPen, QFont,
    QDrag, QPalette, QIcon, QTransform, QPainterPath
)
from PyQt5.QtWidgets import QAbstractItemView

class CleanPixmapItem(QGraphicsPixmapItem):
    """QGraphicsPixmapItem subclass that renders cleanly without selection borders or artifacts."""

    def __init__(self, pixmap, parent=None):
        super().__init__(pixmap, parent)
        # Explicitly disable selection to prevent Qt drawing selection rectangles
        self.setFlag(QGraphicsPixmapItem.ItemIsSelectable, False)
        # Use MaskShape so the item shape follows the alpha mask,
        # preventing rectangular bounding-box artifacts
        self.setShapeMode(QGraphicsPixmapItem.MaskShape)

    def paint(self, painter, option, widget=None):
        """Clean paint - no extra borders, no selection indicators."""
        from PyQt5.QtWidgets import QStyle
        from PyQt5.QtCore import QRect
        # Create a clean option without selection state
        opt = type(option)(option) if option else option
        if opt:
            # Clear selection state flags
            opt.state = opt.state & ~QStyle.State_Selected
            opt.state = opt.state & ~QStyle.State_HasFocus
        # Call parent paint
        super().paint(painter, opt, widget)





# ============================================================================
#  深色主题样式表
# ============================================================================
DARK_THEME = """
QMainWindow, QWidget {
    background-color: #1a1a2e;
    color: #e0e0e0;
    font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
    font-size: 13px;
}

/* 按钮通用样式 */
QPushButton {
    background-color: #16213e;
    color: #e0e0e0;
    border: 1px solid #0f3460;
    border-radius: 6px;
    padding: 6px 14px;
    min-height: 28px;
    font-size: 12px;
}
QPushButton:hover {
    background-color: #0f3460;
    border-color: #7b2ff7;
}
QPushButton:pressed {
    background-color: #7b2ff7;
}
QPushButton:disabled {
    background-color: #0d1117;
    color: #555;
    border-color: #222;
}

/* 工具栏按钮 - 紧凑 */
QToolBar QPushButton {
    padding: 5px 10px;
    min-height: 26px;
    font-size: 12px;
}

/* 强调按钮(紫色) */
QPushButton#accentBtn {
    background-color: #7b2ff7;
    color: #ffffff;
    border: none;
    font-weight: bold;
}
QPushButton#accentBtn:hover {
    background-color: #9b4dff;
}
QPushButton#accentBtn:pressed {
    background-color: #5a1fcc;
}

/* 文本输入框 */
QLineEdit {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 5px;
    padding: 5px 8px;
    color: #e0e0e0;
    selection-background-color: #7b2ff7;
}
QLineEdit:focus {
    border-color: #7b2ff7;
}

/* SpinBox / DoubleSpinBox */
QSpinBox, QDoubleSpinBox {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 4px;
    padding: 3px 6px;
    color: #e0e0e0;
    min-width: 60px;
}

/* 下拉框 */
QComboBox {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 5px;
    padding: 5px 10px;
    color: #e0e0e0;
    min-width: 70px;
}
QComboBox:hover {
    border-color: #7b2ff7;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox QAbstractItemView {
    background-color: #16213e;
    border: 1px solid #0f3460;
    color: #e0e0e0;
    selection-background-color: #7b2ff7;
}

/* 滚动条 */
QScrollBar:vertical {
    background: #1a1a2e;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #0f3460;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #7b2ff7;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background: #1a1a2e;
    height: 8px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: #0f3460;
    border-radius: 4px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background: #7b2ff7;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Slider */
QSlider::groove:horizontal {
    border: none;
    height: 6px;
    background: #0f3460;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #7b2ff7;
    border: none;
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}
QSlider::handle:horizontal:hover {
    background: #9b4dff;
}
QSlider::sub-page:horizontal {
    background: #533483;
    border-radius: 3px;
}

/* ListWidget */
QListWidget {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    padding: 4px;
    outline: none;
}
QListWidget::item {
    border-radius: 6px;
    padding: 4px;
    margin: 2px 0;
}
QListWidget::item:selected {
    background-color: #0f3460;
    border: 1px solid #7b2ff7;
}
QListWidget::item:hover {
    background-color: #1f2b47;
}

/* Frame / 分隔线 */
QFrame#separatorV {
    background-color: #0f3460;
    max-width: 1px;
}
QFrame#separatorH {
    background-color: #0f3460;
    max-height: 1px;
}

/* 标签 */
QLabel#sectionTitle {
    color: #7b2ff7;
    font-weight: bold;
    font-size: 13px;
    padding: 4px 0;
}
QLabel#statusLabel {
    color: #888;
    font-size: 12px;
}
QLabel#sliderLabel {
    color: #aaa;
    font-size: 12px;
}

/* 图案库缩略图项 */
QWidget#patternItem {
    background-color: #1f2b47;
    border: 1px solid #0f3460;
    border-radius: 6px;
}
QWidget#patternItem:hover {
    border-color: #7b2ff7;
}

/* 工具栏容器 */
QWidget#toolbarWidget {
    background-color: #16213e;
    border-bottom: 1px solid #0f3460;
}

/* 底部控制栏 */
QWidget#bottomBar {
    background-color: #16213e;
    border-top: 1px solid #0f3460;
}
"""



# ============================================================================
#  后台目录扫描线程（不阻塞UI）
# ============================================================================
class DirectoryScanThread(QThread):
    """后台线程：扫描目录中的图片文件"""
    finished = pyqtSignal(list)  # 扫描完成，发送文件列表
    progress = pyqtSignal(str)   # 扫描进度

    def __init__(self, dirs, extensions, parent=None):
        super().__init__(parent)
        self.dirs = dirs
        self.extensions = extensions

    def run(self):
        files = []
        for d in self.dirs:
            if not os.path.isdir(d):
                continue
            self.progress.emit(f"正在扫描: {os.path.basename(d)}...")
            for root, dirs_list, file_list in os.walk(d):
                for f in file_list:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in self.extensions:
                        full = os.path.join(root, f)
                        if full not in files:
                            files.append(full)
        self.progress.emit(f"扫描完成，共 {len(files)} 个图案")
        self.finished.emit(files)


# ============================================================================
#  后台去背景线程（不阻塞UI）
# ============================================================================
class BackgroundRemovalThread(QThread):
    """后台线程：极速移除背景"""
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path

    def run(self):
        try:
            import cv2
            import numpy as np
            from PyQt5.QtGui import QImage, QPixmap as QPix

            # 读取原图
            raw = np.fromfile(self.file_path, dtype=np.uint8)
            img = cv2.imdecode(raw, cv2.IMREAD_UNCHANGED)
            if img is None:
                self.error.emit("无法加载图片")
                return

            h, w = img.shape[:2]
            has_alpha = len(img.shape) == 3 and img.shape[2] == 4
            bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) if has_alpha else img.copy()

            # === 极速：缩小到400px处理 ===
            max_dim = max(h, w)
            if max_dim > 400:
                ratio = 400.0 / max_dim
                small = cv2.resize(bgr, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_AREA)
            else:
                small = bgr
                ratio = 1.0
            sh, sw = small.shape[:2]

            # 采样四角颜色（RGB均值）
            m = max(2, min(5, sh // 10, sw // 10))
            corners = [
                small[:m, :m].reshape(-1, 3).mean(0),
                small[:m, sw-m:].reshape(-1, 3).mean(0),
                small[sh-m:, :m].reshape(-1, 3).mean(0),
                small[sh-m:, sw-m:].reshape(-1, 3).mean(0),
            ]
            bg_color = np.mean(corners, axis=0)  # BGR

            # 计算每个像素与背景色的距离
            diff = np.abs(small.astype(np.float32) - bg_color)
            dist = np.max(diff, axis=2)  # 取通道最大差异

            # 阈值分割：距离<35视为背景
            bg_mask = dist < 35

            # === 放回原图尺寸 ===
            if ratio < 1.0:
                bg_mask_full = cv2.resize(bg_mask.astype(np.uint8), (w, h), interpolation=cv2.INTER_NEAREST).astype(bool)
            else:
                bg_mask_full = bg_mask

            # 生成alpha：背景=0，前景=255
            alpha = np.where(bg_mask_full, 0, 255).astype(np.uint8)

            # === 极速边缘处理：只对缩小后的alpha做一次模糊 ===
            if ratio < 1.0:
                small_alpha = cv2.resize(alpha, (sw, sh), interpolation=cv2.INTER_NEAREST)
                blur_k = max(3, sh // 20)
                if blur_k % 2 == 0: blur_k += 1
                small_blur = cv2.GaussianBlur(small_alpha.astype(np.float32), (blur_k, blur_k), 0)
                alpha_f = cv2.resize(small_blur, (w, h), interpolation=cv2.INTER_LINEAR)
            else:
                alpha_f = alpha.astype(np.float32)

            alpha_result = np.clip(alpha_f, 0, 255).astype(np.uint8)

            # 直接复用原图像素数据
            if has_alpha:
                rgba = img.copy()
            else:
                rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
            rgba[:, :, 3] = alpha_result

            # 转QPixmap
            qimg = QImage(rgba.data, w, h, 4 * w, QImage.Format_RGBA8888)
            new_pixmap = QPix.fromImage(qimg.copy())  # copy()防止数据被回收

            if not new_pixmap.isNull():
                self.finished.emit(new_pixmap)
            else:
                self.error.emit("处理失败")

        except Exception as e:
            self.error.emit(str(e))


# ============================================================================
#  后台去背景线程 - 处理 QPixmap（用于已添加到画布的图案）
# ============================================================================
class PixmapBackgroundRemovalThread(QThread):
    """后台线程：使用OpenCV GrabCut移除QPixmap的背景"""
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.pixmap = pixmap

    def run(self):
        try:
            import cv2
            import numpy as np
            from PyQt5.QtGui import QImage, QPixmap as QPix

            qimg = self.pixmap.toImage().convertToFormat(QImage.Format_RGBA8888)
            w, h = qimg.width(), qimg.height()
            ptr = qimg.bits()
            ptr.setsize(qimg.sizeInBytes())
            img_array = np.frombuffer(ptr, dtype=np.uint8).reshape(h, qimg.bytesPerLine())[:, :w*4].reshape(h, w, 4)

            bgr = cv2.cvtColor(img_array[:, :, :3], cv2.COLOR_RGB2BGR)

            max_dim = max(h, w)
            scale = 1.0
            if max_dim > 500:
                scale = 500.0 / max_dim
                small = cv2.resize(bgr, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            else:
                small = bgr
            sh, sw = small.shape[:2]

            mask = np.zeros((sh, sw), np.uint8)
            bgd_model = np.zeros((1, 65), np.float64)
            fgd_model = np.zeros((1, 65), np.float64)

            border = max(2, min(5, sh // 15, sw // 15))
            inner = max(2, min(8, sh // 10, sw // 10))

            mask[:border, :] = cv2.GC_BGD
            mask[-border:, :] = cv2.GC_BGD
            mask[:, :border] = cv2.GC_BGD
            mask[:, -border:] = cv2.GC_BGD
            mask[border:border+inner, :] = cv2.GC_PR_BGD
            mask[-(border+inner):-border, :] = cv2.GC_PR_BGD
            mask[:, border:border+inner] = cv2.GC_PR_BGD
            mask[:, -(border+inner):-border] = cv2.GC_PR_BGD
            mask[border+inner:-border-inner, border+inner:-border-inner] = cv2.GC_PR_FGD

            rect = (border, border, sw - 2*border, sh - 2*border)
            cv2.grabCut(small, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_MASK)

            fg_mask = ((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD)).astype(np.uint8) * 255

            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

            d = cv2.dilate(fg_mask, kernel, 1)
            e = cv2.erode(fg_mask, kernel, 1)
            edge = (d.astype(np.int16) - e.astype(np.int16)) > 0

            blur_sz = max(3, min(sw, sh) // 30)
            if blur_sz % 2 == 0:
                blur_sz += 1
            fg_blur = cv2.GaussianBlur(fg_mask.astype(np.float64), (blur_sz, blur_sz), 0)

            alpha_f = fg_mask.astype(np.float64)
            alpha_f[edge] = np.clip(fg_blur[edge], 0, 255)

            if scale < 1.0:
                alpha_f = cv2.resize(alpha_f, (w, h), interpolation=cv2.INTER_LINEAR)

            alpha_result = np.clip(alpha_f, 0, 255).astype(np.uint8)

            rgba = img_array.copy()
            rgba[:, :, 3] = alpha_result

            data = rgba.tobytes()
            qimg_out = QImage(data, w, h, 4 * w, QImage.Format_RGBA8888)
            new_pixmap = QPix.fromImage(qimg_out.copy())

            if not new_pixmap.isNull():
                self.finished.emit(new_pixmap)
            else:
                self.error.emit("处理失败")

        except Exception as e:
            self.error.emit(str(e))


# ============================================================================
#  自定义画布视图(支持滚轮缩放叠加图案)
# ============================================================================
class CanvasView(QGraphicsView):
    """Custom QGraphicsView with wheel-to-scale, corner-handle resize, and drag-move."""

    HANDLE_SIZE = 10
    HANDLE_HIT = 14

    def __init__(self, scene, main_window=None):
        super().__init__(scene)
        self.main_window = main_window
        self._scale_factor = 1.1
        self._rotating = False
        self._rotate_overlay = None
        self._rotate_center = None
        self._rotate_start_angle = None
        self._resizing = False
        self._resize_item = None
        self._resize_corner = None
        self._resize_start_scene = None
        self._resize_start_scale = 1.0
        self._resize_start_pos = None

    def _get_handles(self, item):
        r = item.mapToScene(item.boundingRect()).boundingRect()
        return {
            'tl': r.topLeft(),
            'tr': r.topRight(),
            'bl': r.bottomLeft(),
            'br': r.bottomRight(),
        }

    def _hit_handle(self, scene_pos, item):
        handles = self._get_handles(item)
        for name, pt in handles.items():
            dx = scene_pos.x() - pt.x()
            dy = scene_pos.y() - pt.y()
            if (dx*dx + dy*dy) < self.HANDLE_HIT * self.HANDLE_HIT:
                return name
        return None

    def _item_at(self, pos):
        if not self.main_window:
            return None, -1
        items = self.items(pos)
        for it in items:
            if isinstance(it, QGraphicsPixmapItem) and it.zValue() > 0:
                for i, ov in enumerate(self.main_window.overlay_items):
                    if ov is it:
                        return it, i
        return None, -1

    def wheelEvent(self, event):
        if self.main_window and self.main_window.selected_overlay_idx >= 0:
            idx = self.main_window.selected_overlay_idx
            if idx < len(self.main_window.overlay_items):
                item = self.main_window.overlay_items[idx]
                delta = event.angleDelta().y()
                factor = self._scale_factor if delta > 0 else 1.0 / self._scale_factor
                self.main_window._save_undo_state()
                item.setTransform(item.transform().scale(factor, factor))
                self.scene().update()
                return
        super().wheelEvent(event)

    def mousePressEvent(self, event):
        scene_pos = self.mapToScene(event.pos())

        if event.button() == Qt.RightButton and self.main_window:
            item, idx = self._item_at(event.pos())
            if item is not None:
                self.main_window._save_undo_state()
                self.main_window._select_overlay(idx)
                self._rotating = True
                self._rotate_overlay = item
                self._rotate_center = item.mapToScene(item.boundingRect().center())
                self._rotate_start_angle = event.pos()
                event.accept()
                return

        if event.button() == Qt.LeftButton and self.main_window:
            item, idx = self._item_at(event.pos())
            if item is not None:
                corner = self._hit_handle(scene_pos, item)
                if corner:
                    self.main_window._save_undo_state()
                    self.main_window._select_overlay(idx)
                    self._resizing = True
                    self._resize_item = item
                    self._resize_corner = corner
                    self._resize_start_scene = scene_pos
                    self._resize_start_scale = item.scale()
                    self._resize_start_pos = item.pos()
                    self.setCursor(Qt.ClosedHandCursor)
                    event.accept()
                    return
                else:
                    self.main_window._save_undo_state()
                    self.main_window._select_overlay(idx)
                    super().mousePressEvent(event)
                    return
            else:
                self.main_window._select_overlay(-1)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        scene_pos = self.mapToScene(event.pos())

        if self._resizing and self._resize_item and self._resize_start_scene:
            import math
            item = self._resize_item
            center = item.mapToScene(item.boundingRect().center())
            orig_corner = self._resize_start_scene
            d_orig = math.hypot(orig_corner.x() - center.x(), orig_corner.y() - center.y())
            d_now = math.hypot(scene_pos.x() - center.x(), scene_pos.y() - center.y())
            if d_orig > 1:
                ratio = d_now / d_orig
                new_scale = self._resize_start_scale * ratio
                new_scale = max(0.05, min(10.0, new_scale))
                item.setScale(new_scale)
            if self.main_window:
                self.main_window.scene.update()
            event.accept()
            return

        if self._rotating and self._rotate_overlay:
            import math
            current_pos = event.pos()
            center = self.mapFromScene(self._rotate_center)
            start_vec = self._rotate_start_angle - center
            curr_vec = current_pos - center
            angle_start = math.atan2(start_vec.y(), start_vec.x())
            angle_curr = math.atan2(curr_vec.y(), curr_vec.x())
            delta_angle = math.degrees(angle_curr - angle_start)
            transform = self._rotate_overlay.transform()
            c = self._rotate_overlay.boundingRect().center()
            transform.translate(c.x(), c.y())
            transform.rotate(delta_angle)
            transform.translate(-c.x(), -c.y())
            self._rotate_overlay.setTransform(transform)
            if self.main_window:
                t = self._rotate_overlay.transform()
                rot_approx = int(math.degrees(math.atan2(t.dy(), t.dx())))
                rot_approx = rot_approx % 360
                if rot_approx > 180:
                    rot_approx -= 360
                self.main_window.slider_rotate.blockSignals(True)
                self.main_window.slider_rotate.setValue(rot_approx)
                self.main_window.slider_rotate.blockSignals(False)
                self.main_window.label_rotate.setText(f"{rot_approx}°")
                self.main_window.scene.update()
            self._rotate_start_angle = current_pos
            event.accept()
            return

        if self.main_window and self.main_window.selected_overlay_idx >= 0:
            idx = self.main_window.selected_overlay_idx
            if idx < len(self.main_window.overlay_items):
                item = self.main_window.overlay_items[idx]
                corner = self._hit_handle(scene_pos, item)
                if corner:
                    if corner in ('tl', 'br'):
                        self.setCursor(Qt.SizeFDiagCursor)
                    else:
                        self.setCursor(Qt.SizeBDiagCursor)
                    return
                items = self.items(event.pos())
                for it in items:
                    if it is item:
                        self.setCursor(Qt.SizeAllCursor)
                        return
        self.setCursor(Qt.ArrowCursor)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._resizing:
            self._resizing = False
            self._resize_item = None
            self._resize_corner = None
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        if self._rotating:
            self._rotating = False
            self._rotate_overlay = None
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def drawForeground(self, painter, rect):
        if not self.main_window:
            return
        idx = self.main_window.selected_overlay_idx
        if idx < 0 or idx >= len(self.main_window.overlay_items):
            return
        item = self.main_window.overlay_items[idx]
        if item is None or item.scene() is None:
            return
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, False)
        scene_rect = item.mapToScene(item.boundingRect()).boundingRect()
        handle_size = self.HANDLE_SIZE
        half = handle_size / 2.0
        pen = QPen(QColor("#ffffff"), 2)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor("#e94560")))
        for pt in [scene_rect.topLeft(), scene_rect.topRight(),
                   scene_rect.bottomLeft(), scene_rect.bottomRight()]:
            painter.drawRect(QRectF(pt.x()-half, pt.y()-half, handle_size, handle_size))
        dash_pen = QPen(QColor("#e94560"), 1, Qt.DashLine)
        painter.setPen(dash_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(scene_rect)
        painter.restore()



# ============================================================================
#  自定义缩略图 Widget
# ============================================================================
class PatternThumbnailWidget(QWidget):
    """图案库中每个图案的缩略图展示Widget（延迟加载）"""

    def __init__(self, image_path: str, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.setFixedHeight(90)
        self.setMinimumWidth(120)
        self.setObjectName("patternItem")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(8)

        # 缩略图 - 先显示占位符
        self.thumb_label = QLabel()
        self.thumb_label.setFixedSize(70, 70)
        self.thumb_label.setAlignment(Qt.AlignCenter)
        self.thumb_label.setStyleSheet(
            "background-color: #0d1117; border-radius: 4px; border: 1px solid #0f3460;"
        )
        self.thumb_label.setText("⏳")

        # 文件名
        name = os.path.splitext(os.path.basename(image_path))[0]
        if len(name) > 12:
            name = name[:10] + "..."
        self.name_label = QLabel(name)
        self.name_label.setStyleSheet("color: #ccc; font-size: 11px;")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)

        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(4)
        v_layout.addWidget(self.thumb_label)
        v_layout.addWidget(self.name_label)

        layout.addLayout(v_layout)
        
        self._loaded = False

    def load_thumbnail(self):
        """延迟加载缩略图"""
        if self._loaded:
            return
        self._loaded = True
        pixmap = EngravingMatchApp._load_pixmap_safe(self.image_path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(66, 66, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.thumb_label.setPixmap(scaled)
        else:
            self.thumb_label.setText("📷")


# ============================================================================
#  主窗口
# ============================================================================
class EngravingMatchApp(QMainWindow):
    """电脑雕刻套图匹配系统 主窗口"""

    SUPPORTED_EXT = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif'}

    def __init__(self):
        super().__init__()
        self.setWindowTitle("电脑雕刻套图匹配系统 v1.0")
        self.setMinimumSize(1200, 750)
        self.resize(1440, 900)

        # 状态数据
        self.base_image_path: str | None = None
        self.base_pixmap: QPixmap | None = None
        self.overlay_paths: list[str] = []
        self.overlay_items: list[QGraphicsPixmapItem] = []
        self.selected_overlay_idx: int = -1
        self.material_dirs: list[str] = []
        self.pattern_files: list[str] = []
        self.undo_stack: list = []
        self.redo_stack: list = []

        # 初始化 UI
        self._init_ui()

        # Load the default material directory after the window is shown.
        # Scanning a large pattern library during __init__ keeps the window hidden.
        QTimer.singleShot(500, self._load_default_material_dir)

    def _load_default_material_dir(self):
        default_dir = r'E:\常用图(禁止删除)'
        if os.path.isdir(default_dir) and default_dir not in self.material_dirs:
            self.material_dirs.append(default_dir)
            self.dir_list_widget.addItem(default_dir)
            self.pattern_count_label.setText("默认图库已添加，点击刷新加载图案")
    @staticmethod
    def _load_pixmap_safe(file_path: str) -> QPixmap:
        """Load QPixmap with Chinese path support using Pillow."""
        # Keep reference alive - QImage only references the buffer,
        # does NOT copy it. If `data` is garbage-collected the pixels vanish.
        _img_data = None
        try:
            from PIL import Image
            from PyQt5.QtGui import QImage, QPixmap as QPix
            # Load with Pillow (handles all formats + Chinese paths)
            img = Image.open(file_path)
            # Handle RGBA (with alpha/transparency)
            if img.mode == 'RGBA':
                _img_data = img.tobytes()
                w, h = img.size
                qimg = QImage(_img_data, w, h, 4 * w, QImage.Format_RGBA8888)
            elif img.mode == 'RGB':
                _img_data = img.tobytes()
                w, h = img.size
                qimg = QImage(_img_data, w, h, 3 * w, QImage.Format_RGB888)
            else:
                img = img.convert('RGB')
                _img_data = img.tobytes()
                w, h = img.size
                qimg = QImage(_img_data, w, h, 3 * w, QImage.Format_RGB888)
            pixmap = QPix.fromImage(qimg)
            if pixmap.isNull():
                print(f'QPixmap is null for: {file_path}')
            return pixmap
        except Exception as e:
            print(f'Pillow load failed for {file_path}: {e}')
            # Fallback: let Qt try directly (works for local ASCII paths)
            return QPixmap(file_path)

    @staticmethod
    def _crop_transparent(pixmap):
        """裁剪掉透明边框，返回 (裁剪后pixmap, 原始偏移x, 原始偏移y)"""
        import numpy as np
        from PyQt5.QtGui import QImage
        qimg = pixmap.toImage().convertToFormat(QImage.Format_RGBA8888)
        w, h = qimg.width(), qimg.height()
        ptr = qimg.bits()
        ptr.setsize(qimg.sizeInBytes())
        arr = np.frombuffer(ptr, dtype=np.uint8).reshape(h, qimg.bytesPerLine())[:, :w*4].reshape(h, w, 4)
        alpha = arr[:, :, 3]
        rows = np.any(alpha > 0, axis=1)
        cols = np.any(alpha > 0, axis=0)
        if not np.any(rows) or not np.any(cols):
            return pixmap, 0, 0
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        cropped = pixmap.copy(cmin, rmin, cmax - cmin + 1, rmax - rmin + 1)
        return cropped, cmin, rmin

    @staticmethod
    def _prepare_overlay_pixmap(file_path: str) -> QPixmap:
        """Load overlay image with alpha transparency.

        Uses OpenCV GrabCut for foreground/background separation.
        Border pixels are marked as sure-background, center area is
        probable foreground. GrabCut iteratively refines the boundary,
        producing clean edges without eating foreground details.
        """
        try:
            import cv2
            import numpy as np
            from PIL import Image
            from PyQt5.QtGui import QImage, QPixmap as QPix

            img_pil = Image.open(file_path).convert("RGBA")
            img_array = np.array(img_pil)
            h, w = img_array.shape[:2]
            bgr = cv2.cvtColor(img_array[:, :, :3], cv2.COLOR_RGB2BGR)

            # ---- GrabCut initialization ----
            mask = np.zeros((h, w), np.uint8)
            bgd_model = np.zeros((1, 13 * 5), np.float64)
            fgd_model = np.zeros((1, 13 * 5), np.float64)

            # Border pixels → sure background
            border = 3
            mask[:border, :] = cv2.GC_BGD
            mask[-border:, :] = cv2.GC_BGD
            mask[:, :border] = cv2.GC_BGD
            mask[:, -border:] = cv2.GC_BGD

            # Inner border → probable background
            inner = 5
            mask[border:border+inner, :] = cv2.GC_PR_BGD
            mask[-(border+inner):-border, :] = cv2.GC_PR_BGD
            mask[:, border:border+inner] = cv2.GC_PR_BGD
            mask[:, -(border+inner):-border] = cv2.GC_PR_BGD

            # Center → probable foreground
            mask[border+inner:-border-inner, border+inner:-border-inner] = cv2.GC_PR_FGD

            rect = (border, border, w - 2*border, h - 2*border)
            cv2.grabCut(bgr, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_MASK)

            # Foreground mask
            fg_mask = ((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD)).astype(np.uint8) * 255

            # Morphological close: fill small holes at edges
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

            # Edge anti-aliasing
            d = cv2.dilate(fg_mask, kernel, 1)
            e = cv2.erode(fg_mask, kernel, 1)
            edge = (d.astype(np.int16) - e.astype(np.int16)) > 0

            blur_sz = max(3, min(w, h) // 80)
            if blur_sz % 2 == 0:
                blur_sz += 1
            fg_blur = cv2.GaussianBlur(fg_mask.astype(np.float64), (blur_sz, blur_sz), 0)

            alpha_f = fg_mask.astype(np.float64)
            alpha_f[edge] = np.clip(fg_blur[edge], 0, 255)
            alpha_result = np.clip(alpha_f, 0, 255).astype(np.uint8)

            img_array[:, :, 3] = alpha_result
            data = img_array.tobytes()
            qimg = QImage(data, w, h, 4 * w, QImage.Format_RGBA8888)
            pixmap = QPix.fromImage(qimg)
            if not pixmap.isNull():
                return pixmap

        except Exception as e:
            print(f'[WARN] Overlay preprocessing failed for {file_path}: {e}')

        # Fallback: load original unchanged
        from PIL import Image
        from PyQt5.QtGui import QImage, QPixmap as QPix
        pil_img = Image.open(file_path)
        if pil_img.mode != 'RGBA':
            pil_img = pil_img.convert('RGBA')
        data = pil_img.tobytes('raw', 'RGBA')
        qimg = QImage(data, pil_img.width, pil_img.height, QImage.Format_RGBA8888)
        return QPix.fromImage(qimg)

    @staticmethod
    def _detect_stone_bounds(pixmap, file_path=None) -> tuple:
        """检测料子区域 - 基于料子轮廓线和边缘
        
        Returns (x, y, w, h) of the detected stone region, or None.
        """
        try:
            import cv2
            import numpy as np

            # 读原文件
            if file_path and os.path.isfile(file_path):
                bgr = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            else:
                from PyQt5.QtGui import QImage
                qimg = pixmap.toImage().convertToFormat(QImage.Format_RGB888)
                w, h = qimg.width(), qimg.height()
                ptr = qimg.bits()
                ptr.setsize(qimg.sizeInBytes())
                bgr = np.frombuffer(ptr, dtype=np.uint8).reshape(h, qimg.bytesPerLine(), 3)[:, :w*3].reshape(h, w, 3)
                bgr = cv2.cvtColor(bgr, cv2.COLOR_RGB2BGR)
            
            if bgr is None:
                return None

            orig_h, orig_w = bgr.shape[:2]
            gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            
            # 缩小加速
            scale = 1.0
            max_dim = max(orig_h, orig_w)
            if max_dim > 800:
                scale = 800.0 / max_dim
                gray = cv2.resize(gray, None, fx=scale, fy=scale)
            
            h, w = gray.shape[:2]
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Canny 边缘检测
            edges = cv2.Canny(blur, 30, 100)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            edges = cv2.dilate(edges, kernel, iterations=2)
            edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
            
            # 关键：遮掉图片边缘区域（忽略边框干扰）
            border_mask = np.zeros_like(edges)
            bm = max(5, min(h, w) // 20)  # 遮掉边缘5%
            border_mask[bm:h-bm, bm:w-bm] = 255
            edges = cv2.bitwise_and(edges, border_mask)
            
            # 找轮廓
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            best_rect = None
            best_score = 0
            img_area = w * h
            
            for cnt in contours:
                area = cv2.contourArea(cnt)
                # 料子面积：占图片5%~55%
                if area < 0.05 * img_area or area > 0.55 * img_area:
                    continue
                
                x, y, bw, bh = cv2.boundingRect(cnt)
                
                # 料子不应碰触图片最外层边缘
                if x < 2 or y < 2 or x + bw > w - 2 or y + bh > h - 2:
                    continue
                
                # 料子不应跨越图片95%以上（排除手指+背景的大轮廓）
                if bw > 0.95 * w or bh > 0.95 * h:
                    continue
                
                ratio = min(bw, bh) / max(bw, bh) if max(bw, bh) > 0 else 0
                if ratio < 0.15:
                    continue
                
                # 多边形近似检查矩形度
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                rect_score = max(0, 1.0 - abs(len(approx) - 4) * 0.15)
                
                # 居中度
                cx, cy = x + bw/2, y + bh/2
                center_dist = ((cx - w/2)**2 + (cy - h/2)**2) ** 0.5
                max_dist = (w**2 + h**2) ** 0.5 / 2
                center_score = 1.0 - center_dist / max_dist if max_dist > 0 else 0
                
                score = area * (0.3 + 0.2 * ratio + 0.2 * center_score + 0.3 * rect_score)
                if score > best_score:
                    best_score = score
                    best_rect = (x, y, bw, bh)
            
            # 备选：自适应阈值（找料子上的轮廓线）
            if best_rect is None:
                _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                # 遮掉边缘
                thresh[:bm, :] = 0
                thresh[h-bm:, :] = 0
                thresh[:, :bm] = 0
                thresh[:, w-bm:] = 0
                # 膨胀连接轮廓线
                thresh = cv2.dilate(thresh, kernel, iterations=3)
                thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
                
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in sorted(contours, key=cv2.contourArea, reverse=True)[:10]:
                    area = cv2.contourArea(cnt)
                    if area < 0.05 * img_area or area > 0.55 * img_area:
                        continue
                    x, y, bw, bh = cv2.boundingRect(cnt)
                    if x < 2 or y < 2 or x + bw > w - 2 or y + bh > h - 2:
                        continue
                    if bw > 0.95 * w or bh > 0.95 * h:
                        continue
                    ratio = min(bw, bh) / max(bw, bh) if max(bw, bh) > 0 else 0
                    if ratio < 0.15:
                        continue
                    best_rect = (x, y, bw, bh)
                    break

            if best_rect:
                x, y, bw, bh = best_rect
                # 还原原图坐标
                if scale < 1.0:
                    x = int(x / scale)
                    y = int(y / scale)
                    bw = int(bw / scale)
                    bh = int(bh / scale)
                # 内收缩
                pad = max(3, min(bw, bh) // 25)
                x += pad
                y += pad
                bw -= 2 * pad
                bh -= 2 * pad
                return (x, y, bw, bh)

            return None

        except Exception as e:
            print(f'[WARN] Stone detection failed: {e}')
            return None

    # ------------------------------------------------------------------
    #  构建 UI
    # ------------------------------------------------------------------
    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === 顶部工具栏 ===
        main_layout.addWidget(self._build_toolbar())

        # === 中间区域:左侧栏 + 主画布 ===
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background-color: #0f3460; width: 2px; }")

        left_widget = self._build_left_panel()
        left_widget.setMinimumWidth(220)
        left_widget.setMaximumWidth(350)
        splitter.addWidget(left_widget)

        canvas_widget = self._build_canvas_area()
        splitter.addWidget(canvas_widget)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        main_layout.addWidget(splitter, 1)

        # === 底部控制栏 ===
        main_layout.addWidget(self._build_bottom_bar())

    # ---- 工具栏 ----
    def _build_toolbar(self) -> QWidget:
        container = QWidget()
        container.setObjectName("toolbarWidget")
        container.setFixedHeight(52)
        h = QHBoxLayout(container)
        h.setContentsMargins(10, 6, 10, 6)
        h.setSpacing(8)

        btn_open = QPushButton("📂 打开原料")
        btn_open.setObjectName("accentBtn")
        btn_open.clicked.connect(self._open_material)

        btn_undo = QPushButton("↩ 撤销")
        btn_undo.clicked.connect(self._undo)


        btn_redo = QPushButton("↪ 重做")
        btn_redo.clicked.connect(self._redo)

        btn_clear = QPushButton("🗑 清空图案")
        btn_clear.clicked.connect(self._clear_overlays)

        btn_flip_h = QPushButton("↔ 水平")
        btn_flip_h.clicked.connect(lambda: self._flip_overlay("h"))

        btn_flip_v = QPushButton("↕ 垂直")
        btn_flip_v.clicked.connect(lambda: self._flip_overlay("v"))

        btn_export = QPushButton("💾 导出PNG")
        btn_export.clicked.connect(self._export_png)

        btn_remove_bg = QPushButton("🎨 去背景")
        btn_remove_bg.clicked.connect(self._remove_background)

        btn_correct = QPushButton("🔧 矫正")
        btn_correct.clicked.connect(self._correct_image)

        for b in [btn_open, btn_undo, btn_redo, btn_clear, btn_flip_h, btn_flip_v,
                  btn_export, btn_remove_bg, btn_correct]:
            h.addWidget(b)

        h.addSpacing(20)

        # 布局选择
        h.addWidget(QLabel("布局:"))
        self.combo_layout = QComboBox()
        self.combo_layout.addItems(["方块", "自由", "居中", "等距"])
        self.combo_layout.setFixedWidth(80)
        h.addWidget(self.combo_layout)

        h.addSpacing(10)

        # 尺寸输入
        h.addWidget(QLabel("尺寸:"))
        self.spin_width = QSpinBox()
        self.spin_width.setRange(1, 9999)
        self.spin_width.setValue(50)
        self.spin_width.setSuffix(" cm")
        self.spin_width.setFixedWidth(90)
        h.addWidget(self.spin_width)

        self.spin_height = QSpinBox()
        self.spin_height.setRange(1, 9999)
        self.spin_height.setSuffix(" cm")
        self.spin_height.setFixedWidth(90)
        h.addWidget(self.spin_height)

        h.addStretch()
        return container

    # ---- 左侧面板 ----
    def _build_left_panel(self) -> QWidget:
        widget = QWidget()
        v = QVBoxLayout(widget)
        v.setContentsMargins(8, 8, 8, 8)
        v.setSpacing(6)

        # 路径管理
        title_path = QLabel("📁 路径管理")
        title_path.setObjectName("sectionTitle")
        v.addWidget(title_path)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("输入素材目录路径...")
        v.addWidget(self.path_input)

        path_btns = QHBoxLayout()
        path_btns.setSpacing(6)
        btn_add = QPushButton("+ 添加")
        btn_add.clicked.connect(self._add_material_dir)
        btn_batch = QPushButton("批量")
        btn_batch.clicked.connect(self._batch_add_dirs)
        btn_clear_dirs = QPushButton("清空")
        btn_clear_dirs.clicked.connect(self._clear_dirs)
        btn_refresh = QPushButton("刷新")
        btn_refresh.clicked.connect(self._refresh_patterns)
        for b in [btn_add, btn_batch, btn_clear_dirs, btn_refresh]:
            path_btns.addWidget(b)
        v.addLayout(path_btns)

        # 已添加的目录列表
        self.dir_list_widget = QListWidget()
        self.dir_list_widget.setMaximumHeight(80)
        self.dir_list_widget.setStyleSheet(
            "QListWidget { background-color: #0d1117; font-size: 11px; }"
        )
        v.addWidget(self.dir_list_widget)

        # 分隔线
        sep = QFrame()
        sep.setObjectName("separatorH")
        sep.setFrameShape(QFrame.HLine)
        v.addWidget(sep)

        # 图案库
        title_pat = QLabel("🎨 图案库")
        title_pat.setObjectName("sectionTitle")
        v.addWidget(title_pat)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索图案名称...")
        self.search_input.textChanged.connect(self._filter_patterns)
        v.addWidget(self.search_input)

        self.pattern_count_label = QLabel("共 0 个图案")
        self.pattern_count_label.setObjectName("statusLabel")
        v.addWidget(self.pattern_count_label)

        self.pattern_list = QListWidget()
        self.pattern_list.setIconSize(QSize(70, 70))
        self.pattern_list.setSpacing(2)
        self.pattern_list.setMovement(QListWidget.Static)
        self.pattern_list.setFlow(QListWidget.TopToBottom)
        self.pattern_list.itemClicked.connect(self._add_pattern_to_canvas)
        v.addWidget(self.pattern_list, 1)

        return widget

    # ---- 主画布区域 ----
    def _build_canvas_area(self) -> QWidget:
        widget = QWidget()
        v = QVBoxLayout(widget)
        v.setContentsMargins(4, 4, 4, 4)

        # Create scene first
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(QColor("#0d1117")))

        # 画布
        self.canvas = CanvasView(self.scene, self)
        self.canvas.setRenderHint(QPainter.Antialiasing, True)
        self.canvas.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.canvas.setDragMode(QGraphicsView.NoDrag)
        self.canvas.setAcceptDrops(True)
        self.canvas.setStyleSheet(
            "QGraphicsView { background-color: #0d1117; border: none; border-radius: 4px; }"
        )
        self.canvas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.canvas.setScene(self.scene)

        # 棋盘格背景提示
        self._draw_checkerboard()

        v.addWidget(self.canvas, 1)

        # 画布中央提示
        self.canvas_hint = QLabel("📷 拖拽或点击「打开原料」加载原材料图片\n双击图案库中的图案添加到画布")
        self.canvas_hint.setAlignment(Qt.AlignCenter)
        self.canvas_hint.setStyleSheet(
            "color: #555; font-size: 14px; background: transparent;"
        )
        self.canvas_scene_stack = QVBoxLayout()
        self.canvas_scene_stack.setContentsMargins(0, 0, 0, 0)
        # hint 放在画布上方覆盖显示(使用 overlay 方式)
        # 简化:hint 作为画布下方的说明文字

        return widget

    def _draw_checkerboard(self):
        """在场景上画一个棋盘格作为空状态提示"""
        self.scene.clear()
        self.base_pixmap = None
        self.base_image_path = None
        self.overlay_items.clear()
        self.overlay_paths.clear()
        self.selected_overlay_idx = -1
        self.undo_stack.clear()
        self.redo_stack.clear()
        if hasattr(self, 'label_pattern_count') and self.label_pattern_count:
            self.label_pattern_count.setText("0 个图案")

        # 棋盘格
        checker_size = 20
        w, h = 600, 500
        checker_img = QImage(w, h, QImage.Format_RGB32)
        painter = QPainter(checker_img)
        for y in range(0, h, checker_size):
            for x in range(0, w, checker_size):
                c = QColor("#1a1a2e") if ((x // checker_size) + (y // checker_size)) % 2 == 0 else QColor("#16213e")
                painter.fillRect(x, y, checker_size, checker_size, c)
        painter.end()
        self.scene.addPixmap(QPixmap.fromImage(checker_img))

        # 中心提示文字
        text_item = self.scene.addText("📷 点击「打开原料」加载图片\n\n🎨 双击图案库中的图案叠加",
                           QFont("Microsoft YaHei", 14))
        text_item.setDefaultTextColor(QColor("#555"))

        self.scene.setSceneRect(0, 0, w, h)
        self.canvas.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    # ---- 底部控制栏 ----
    def _build_bottom_bar(self) -> QWidget:
        container = QWidget()
        container.setObjectName("bottomBar")
        container.setFixedHeight(70)
        h = QHBoxLayout(container)
        h.setContentsMargins(16, 8, 16, 8)
        h.setSpacing(16)

        # 缩放
        h.addWidget(QLabel("缩放:"))
        self.slider_zoom = QSlider(Qt.Horizontal)
        self.slider_zoom.setRange(10, 300)
        self.slider_zoom.setValue(100)
        self.slider_zoom.setTickInterval(10)
        self.slider_zoom.valueChanged.connect(self._on_zoom_changed)
        h.addWidget(self.slider_zoom, 2)
        self.label_zoom = QLabel("100%")
        self.label_zoom.setObjectName("sliderLabel")
        self.label_zoom.setFixedWidth(45)
        self.label_zoom.setAlignment(Qt.AlignCenter)
        h.addWidget(self.label_zoom)

        h.addSpacing(20)

        # 旋转
        h.addWidget(QLabel("旋转:"))
        self.slider_rotate = QSlider(Qt.Horizontal)
        self.slider_rotate.setRange(-180, 180)
        self.slider_rotate.setValue(0)
        self.slider_rotate.valueChanged.connect(self._on_rotate_changed)
        h.addWidget(self.slider_rotate, 2)
        self.label_rotate = QLabel("0°")
        self.label_rotate.setObjectName("sliderLabel")
        self.label_rotate.setFixedWidth(40)
        self.label_rotate.setAlignment(Qt.AlignCenter)
        h.addWidget(self.label_rotate)

        h.addSpacing(20)

        # 透明度
        h.addWidget(QLabel("透明:"))
        self.slider_opacity = QSlider(Qt.Horizontal)
        self.slider_opacity.setRange(0, 100)
        self.slider_opacity.setValue(85)
        self.slider_opacity.valueChanged.connect(self._on_opacity_changed)
        h.addWidget(self.slider_opacity, 2)
        self.label_opacity = QLabel("85%")
        self.label_opacity.setObjectName("sliderLabel")
        self.label_opacity.setFixedWidth(45)
        self.label_opacity.setAlignment(Qt.AlignCenter)
        h.addWidget(self.label_opacity)

        h.addSpacing(30)

        # 图案计数
        self.label_pattern_count = QLabel("0 个图案")
        self.label_pattern_count.setObjectName("statusLabel")
        h.addWidget(self.label_pattern_count)

        return container

    # ==================================================================
    #  功能实现
    # ==================================================================

    # ---- 路径管理 ----
    def _add_material_dir(self):
        path = self.path_input.text().strip()
        if not path:
            path = QFileDialog.getExistingDirectory(self, "选择素材目录")
            if not path:
                return
        if path and os.path.isdir(path) and path not in self.material_dirs:
            self.material_dirs.append(path)
            self.dir_list_widget.addItem(path)
            self.path_input.clear()
            self._refresh_patterns()

    def _batch_add_dirs(self):
        path = QFileDialog.getExistingDirectory(self, "选择素材目录(可多选后重复操作)")
        if path and path not in self.material_dirs:
            self.material_dirs.append(path)
            self.dir_list_widget.addItem(path)
            self._refresh_patterns()

    def _clear_dirs(self):
        self.material_dirs.clear()
        self.dir_list_widget.clear()
        self.pattern_files.clear()
        self.pattern_list.clear()
        self.pattern_count_label.setText("共 0 个图案")
        self.label_pattern_count.setText("0 个图案")

    def _refresh_patterns(self):
        """后台线程扫描目录，不阻塞UI"""
        if not self.material_dirs:
            return
        
        # 如果正在扫描，不重复启动
        if hasattr(self, '_scan_thread') and self._scan_thread and self._scan_thread.isRunning():
            return
        
        self.pattern_count_label.setText("正在扫描...")
        self.pattern_list.clear()
        
        # 启动后台扫描线程
        self._scan_thread = DirectoryScanThread(self.material_dirs, self.SUPPORTED_EXT, self)
        self._scan_thread.progress.connect(lambda msg: self.pattern_count_label.setText(msg))
        self._scan_thread.finished.connect(self._on_scan_finished)
        self._scan_thread.start()

    def _on_scan_finished(self, files):
        """扫描完成回调"""
        self.pattern_files = files
        self._populate_pattern_list(files)

    def _populate_pattern_list(self, files: list[str]):
        """填充图案列表（先创建占位符，再分批加载缩略图）"""
        self.pattern_list.clear()
        self._thumbnail_widgets = []  # 保存引用以便延迟加载
        
        for fp in files:
            item = QListWidgetItem()
            widget = PatternThumbnailWidget(fp)
            item.setSizeHint(widget.sizeHint())
            item.setData(Qt.UserRole, fp)
            self.pattern_list.addItem(item)
            self.pattern_list.setItemWidget(item, widget)
            self._thumbnail_widgets.append(widget)

        count = len(files)
        self.pattern_count_label.setText(f"共 {count} 个图案")
        self.label_pattern_count.setText(f"{count} 个图案")
        
        # 分批延迟加载缩略图（每批20个，间隔50ms）
        self._thumb_load_index = 0
        self._thumb_load_timer = QTimer(self)
        self._thumb_load_timer.timeout.connect(self._load_next_thumbnail_batch)
        self._thumb_load_timer.start(50)

    def _load_next_thumbnail_batch(self):
        """分批加载缩略图"""
        batch_size = 20
        end = min(self._thumb_load_index + batch_size, len(self._thumbnail_widgets))
        
        for i in range(self._thumb_load_index, end):
            self._thumbnail_widgets[i].load_thumbnail()
        
        self._thumb_load_index = end
        
        if self._thumb_load_index >= len(self._thumbnail_widgets):
            self._thumb_load_timer.stop()

    def _filter_patterns(self, text: str):
        text = text.lower().strip()
        if not text:
            self._populate_pattern_list(self.pattern_files)
            return
        filtered = [f for f in self.pattern_files if text in os.path.splitext(os.path.basename(f))[0].lower()]
        self._populate_pattern_list(filtered)

    # ---- 打开原料 ----
    def _open_material(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开原料图片", "",
            "图片文件 (*.jpg *.jpeg *.png *.webp *.bmp *.tiff *.tif);;所有文件 (*)"
        )
        if file_path:
            self._load_material(file_path)

    def _load_material(self, file_path: str):
        pixmap = EngravingMatchApp._load_pixmap_safe(file_path)
        if pixmap.isNull():
            QMessageBox.warning(self, "错误", f"无法加载图片:\n{file_path}")
            return

        self.base_image_path = file_path
        self.base_pixmap = pixmap

        # 清空场景
        self.scene.clear()
        self.overlay_items.clear()
        self.overlay_paths.clear()
        self.selected_overlay_idx = -1
        self.undo_stack.clear()
        self.redo_stack.clear()

        # 绘制棋盘格背景
        checker_size = 20
        pw, ph = pixmap.width(), pixmap.height()
        checker_img = QImage(pw, ph, QImage.Format_RGB32)
        painter = QPainter(checker_img)
        for y in range(0, ph, checker_size):
            for x in range(0, pw, checker_size):
                c = QColor("#222233") if ((x // checker_size) + (y // checker_size)) % 2 == 0 else QColor("#1a1a2e")
                painter.fillRect(x, y, checker_size, checker_size, c)
        painter.end()
        self.scene.addPixmap(QPixmap.fromImage(checker_img))

        # 原材料图片
        self.base_item = self.scene.addPixmap(pixmap)
        self.base_item.setZValue(0)

        self.scene.setSceneRect(0, 0, pw, ph)
        self.canvas.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        self.canvas_hint.hide() if hasattr(self, 'canvas_hint') and self.canvas_hint.isVisible() else None

    # ---- 双击图案库添加到画布 ----
    def _add_pattern_to_canvas(self, item: QListWidgetItem):
        fp = item.data(Qt.UserRole)
        if not fp or not self.base_pixmap:
            if not self.base_pixmap:
                QMessageBox.information(self, "提示", "请先打开原料图片")
            return

        pixmap = EngravingMatchApp._prepare_overlay_pixmap(fp)
        if pixmap.isNull():
            return

        # 裁剪透明边框
        cropped_pixmap, crop_ox, crop_oy = EngravingMatchApp._crop_transparent(pixmap)

        # 保存撤销状态
        self._save_undo_state()

        # 检测料子区域
        base_w = self.base_pixmap.width()
        base_h = self.base_pixmap.height()
        stone = EngravingMatchApp._detect_stone_bounds(self.base_pixmap, self.base_image_path)
        if stone:
            sx, sy, sw, sh = stone
        else:
            sx, sy, sw, sh = 0, 0, base_w, base_h

        # 用裁剪后的图案尺寸来计算缩放
        pat_w = cropped_pixmap.width()
        pat_h = cropped_pixmap.height()
        scale = min(sw * 0.90 / pat_w, sh * 0.90 / pat_h, 1.0)
        new_w = int(pat_w * scale)
        new_h = int(pat_h * scale)
        scaled = cropped_pixmap.scaled(new_w, new_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # 创建可拖拽的 pixmap item
        overlay = CleanPixmapItem(scaled)
        self.scene.addItem(overlay)
        overlay.setFlag(QGraphicsPixmapItem.ItemIsMovable, True)
        overlay.setFlag(QGraphicsPixmapItem.ItemSendsGeometryChanges, True)
        overlay.setZValue(1)

        # 居中放置在料子区域内
        x = sx + (sw - new_w) / 2
        y = sy + (sh - new_h) / 2
        overlay.setPos(x, y)

        # 设置透明度
        opacity = self.slider_opacity.value() / 100.0
        overlay.setOpacity(opacity)

        self.overlay_items.append(overlay)
        self.overlay_paths.append(fp)
        self.selected_overlay_idx = len(self.overlay_items) - 1

        # 选中最新添加的
        self._select_overlay(self.selected_overlay_idx)

    # ---- 选择叠加图案 ----
    def _select_overlay(self, idx: int):
        """选择叠加图案 - 同步滑块和属性面板"""
        self.selected_overlay_idx = idx

        if idx >= 0 and idx < len(self.overlay_items):
            item = self.overlay_items[idx]
            self.slider_rotate.blockSignals(True)
            self.slider_rotate.setValue(int(item.rotation()))
            self.slider_rotate.blockSignals(False)
            self.label_rotate.setText(f"{int(item.rotation())}°")

            self.slider_opacity.blockSignals(True)
            self.slider_opacity.setValue(int(item.opacity() * 100))
            self.slider_opacity.blockSignals(False)
            self.label_opacity.setText(f"{int(item.opacity() * 100)}%")

        count = len(self.overlay_items)
        sel_text = f"  (已选中 #{idx + 1})" if idx >= 0 else ""
        self.label_pattern_count.setText(f"{count} 个图案{sel_text}")

        if hasattr(self, 'scene') and self.scene:
            self.scene.update()

    # ---- 画布点击选择 ----
    def mousePressEventOnCanvas(self, event):
        """如果需要画布鼠标事件可以在此扩展"""
        pass

    # ---- 撤销 ----
    def _save_undo_state(self):
        state = {
            'selected_idx': self.selected_overlay_idx,
            'overlays': [
                {
                    'path': self.overlay_paths[i] if i < len(self.overlay_paths) else None,
                    'pixmap': item.pixmap().copy(),
                    'pos': QPointF(item.pos()),
                    'transform': QTransform(item.transform()),
                    'rotation': item.rotation(),
                    'scale': item.scale(),
                    'opacity': item.opacity(),
                    'z': item.zValue(),
                }
                for i, item in enumerate(self.overlay_items)
            ],
        }
        self.undo_stack.append(state)
        self.redo_stack.clear()
        if len(self.undo_stack) > 30:
            self.undo_stack.pop(0)

    def _capture_current_state(self) -> dict:
        """捕获当前画布状态"""
        return {
            'selected_idx': self.selected_overlay_idx,
            'overlays': [
                {
                    'path': self.overlay_paths[i] if i < len(self.overlay_paths) else None,
                    'pixmap': item.pixmap().copy(),
                    'pos': QPointF(item.pos()),
                    'transform': QTransform(item.transform()),
                    'rotation': item.rotation(),
                    'scale': item.scale(),
                    'opacity': item.opacity(),
                    'z': item.zValue(),
                }
                for i, item in enumerate(self.overlay_items)
            ],
        }

    def _restore_state(self, state: dict):
        """恢复画布到指定状态"""
        for item in self.overlay_items:
            self.scene.removeItem(item)
        self.overlay_items.clear()
        self.overlay_paths.clear()
        self.selected_overlay_idx = -1

        for overlay_state in state.get('overlays', []):
            pixmap = overlay_state['pixmap']
            if pixmap.isNull():
                continue
            overlay = CleanPixmapItem(pixmap.copy())
            self.scene.addItem(overlay)
            overlay.setFlag(QGraphicsPixmapItem.ItemIsMovable, True)
            overlay.setFlag(QGraphicsPixmapItem.ItemSendsGeometryChanges, True)
            overlay.setZValue(overlay_state.get('z', 1))
            overlay.setPos(overlay_state['pos'])
            overlay.setTransform(overlay_state['transform'])
            overlay.setRotation(overlay_state.get('rotation', 0))
            overlay.setScale(overlay_state.get('scale', 1))
            overlay.setOpacity(overlay_state.get('opacity', 1.0))
            self.overlay_items.append(overlay)
            self.overlay_paths.append(overlay_state.get('path'))

        if self.overlay_items:
            restored_idx = state.get('selected_idx', 0)
            if restored_idx < 0 or restored_idx >= len(self.overlay_items):
                restored_idx = 0
            self._select_overlay(restored_idx)
        else:
            self._select_overlay(-1)
        count = len(self.overlay_items)
        self.label_pattern_count.setText(f"{count} 个图案")

    def _undo(self):
        if not self.undo_stack:
            QMessageBox.information(self, "提示", "没有可撤销的操作")
            return
        current_state = self._capture_current_state()
        self.redo_stack.append(current_state)
        state = self.undo_stack.pop()
        self._restore_state(state)

    def _redo(self):
        if not self.redo_stack:
            QMessageBox.information(self, "提示", "没有可重做的操作")
            return
        current_state = self._capture_current_state()
        self.undo_stack.append(current_state)
        state = self.redo_stack.pop()
        self._restore_state(state)

    # ---- 清空图案 ----
    def _clear_overlays(self):
        if not self.overlay_items:
            return
        self._save_undo_state()
        for item in self.overlay_items:
            self.scene.removeItem(item)
        self.overlay_items.clear()
        self.overlay_paths.clear()
        self.selected_overlay_idx = -1
        self.label_pattern_count.setText("0 个图案")

    # ---- 旋转 ----
    def _rotate_overlay(self, degrees: float):
        """旋转选中的叠加图案(固定角度,备用)"""
        if self.selected_overlay_idx < 0 or self.selected_overlay_idx >= len(self.overlay_items):
            return

        self._save_undo_state()
        item = self.overlay_items[self.selected_overlay_idx]

        rect = item.boundingRect()
        center = rect.center()

        transform = item.transform()
        transform.translate(center.x(), center.y())
        transform.rotate(degrees)
        transform.translate(-center.x(), -center.y())
        item.setTransform(transform)

    # ---- 翻转 ----
    def _flip_overlay(self, direction: str):
        if self.selected_overlay_idx < 0 or self.selected_overlay_idx >= len(self.overlay_items):
            QMessageBox.information(self, "提示", "请先选择一个叠加图案")
            return

        self._save_undo_state()
        item = self.overlay_items[self.selected_overlay_idx]
        pixmap_item = item

        # Flip the CURRENT pixmap each time (allows infinite flips)
        current = pixmap_item.pixmap()
        transform = QTransform()
        if direction == "h":
            transform.scale(-1, 1)
        else:
            transform.scale(1, -1)
        flipped = current.transformed(transform, Qt.SmoothTransformation)
        pixmap_item.setPixmap(flipped)

    # ---- 导出PNG ----
    def _export_png(self):
        if not self.base_pixmap:
            QMessageBox.information(self, "提示", "请先打开原料图片")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出PNG", "", "PNG文件 (*.png);;所有文件 (*)"
        )
        if not file_path:
            return

        # 创建导出图像
        pw, ph = self.base_pixmap.width(), self.base_pixmap.height()
        export_img = QImage(pw, ph, QImage.Format_ARGB32)
        export_img.fill(QColor(0, 0, 0, 0))

        painter = QPainter(export_img)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        # 绘制原料
        painter.drawPixmap(0, 0, self.base_pixmap)

        # 绘制叠加图案，保留画布上的缩放、旋转、翻转和透明度
        for item in self.overlay_items:
            if not item.isVisible():
                continue
            painter.save()
            painter.setOpacity(item.opacity())
            painter.setWorldTransform(item.sceneTransform(), True)
            painter.drawPixmap(0, 0, item.pixmap())
            painter.restore()

        painter.end()

        if export_img.save(file_path, "PNG"):
            QMessageBox.information(self, "成功", f"已导出到:\n{file_path}")
        else:
            QMessageBox.warning(self, "错误", "导出失败")

    # ---- 去背景(一键智能移除) ----
    def _remove_background(self):
        """一键智能移除背景 - 使用OpenCV GrabCut"""
        if self.selected_overlay_idx < 0 or self.selected_overlay_idx >= len(self.overlay_items):
            QMessageBox.information(self, "去背景", "请先选择一个叠加图案")
            return

        self._save_undo_state()
        
        item = self.overlay_items[self.selected_overlay_idx]
        current_pixmap = item.pixmap()
        
        self._bg_thread = PixmapBackgroundRemovalThread(current_pixmap, self)
        self._bg_thread.finished.connect(self._on_bg_removal_done)
        self._bg_thread.error.connect(self._on_bg_removal_error)
        self._bg_thread.start()

    def _on_bg_removal_done(self, new_pixmap):
        """去背景完成回调"""
        if self.selected_overlay_idx < 0 or self.selected_overlay_idx >= len(self.overlay_items):
            return
        
        item = self.overlay_items[self.selected_overlay_idx]
        old_pos = item.pos()
        old_transform = item.transform()
        old_opacity = item.opacity()

        self.scene.removeItem(item)

        new_item = CleanPixmapItem(new_pixmap)
        self.scene.addItem(new_item)
        new_item.setFlag(QGraphicsPixmapItem.ItemIsMovable, True)
        new_item.setFlag(QGraphicsPixmapItem.ItemSendsGeometryChanges, True)
        new_item.setZValue(1)
        new_item.setPos(old_pos)
        new_item.setOpacity(old_opacity)
        new_item.setTransform(old_transform)

        self.overlay_items[self.selected_overlay_idx] = new_item

    def _on_bg_removal_error(self, msg):
        """去背景失败回调"""
        QMessageBox.warning(self, "去背景", f"错误: {msg}")

    def _correct_image(self):
        if not self.base_pixmap:
            QMessageBox.information(self, "提示", "请先打开原料图片")
            return
        QMessageBox.information(self, "矫正", "图像矫正功能将在后续版本中实现\n将支持透视矫正和自动校准")

    # ---- 滑块事件 ----
    def _on_zoom_changed(self, value: int):
        self.label_zoom.setText(f"{value}%")
        factor = value / 100.0
        self.canvas.resetTransform()
        self.canvas.scale(factor, factor)

    def _on_rotate_changed(self, value: int):
        self.label_rotate.setText(f"{value}°")
        if self.selected_overlay_idx >= 0 and self.selected_overlay_idx < len(self.overlay_items):
            item = self.overlay_items[self.selected_overlay_idx]
            item.setRotation(value)
            if hasattr(self, 'scene') and self.scene:
                self.scene.update()

    def _on_opacity_changed(self, value: int):
        self.label_opacity.setText(f"{value}%")
        opacity = value / 100.0
        if self.selected_overlay_idx >= 0 and self.selected_overlay_idx < len(self.overlay_items):
            self.overlay_items[self.selected_overlay_idx].setOpacity(opacity)
            if hasattr(self, 'scene') and self.scene:
                self.scene.update()

    # ---- 快捷键 ----
    def keyPressEvent(self, event):
        """键盘快捷键"""
        if event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier:
            if event.modifiers() & Qt.ShiftModifier:
                self._redo()
            else:
                self._undo()
        elif event.key() == Qt.Key_Y and event.modifiers() & Qt.ControlModifier:
            self._redo()
        elif event.key() == Qt.Key_Delete:
            if self.selected_overlay_idx >= 0 and self.selected_overlay_idx < len(self.overlay_items):
                self._save_undo_state()
                item = self.overlay_items[self.selected_overlay_idx]
                self.scene.removeItem(item)
                self.overlay_items.pop(self.selected_overlay_idx)
                self.overlay_paths.pop(self.selected_overlay_idx)
                self.selected_overlay_idx = min(self.selected_overlay_idx, len(self.overlay_items) - 1)
                self.label_pattern_count.setText(f"{len(self.overlay_items)} 个图案")
                if self.selected_overlay_idx >= 0:
                    self._select_overlay(self.selected_overlay_idx)
        elif event.key() == Qt.Key_Escape:
            self._select_overlay(-1)
        else:
            super().keyPressEvent(event)

    # ---- 拖拽支持 ----
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            ext = os.path.splitext(path)[1].lower()
            if ext in self.SUPPORTED_EXT:
                if self.base_pixmap:
                    # 作为 overlay 添加
                    pixmap = EngravingMatchApp._prepare_overlay_pixmap(path)
                    if not pixmap.isNull():
                        self._save_undo_state()
                        base_w = self.base_pixmap.width()
                        base_h = self.base_pixmap.height()
                        stone = EngravingMatchApp._detect_stone_bounds(self.base_pixmap, self.base_image_path)
                        if stone:
                            sx, sy, sw, sh = stone
                            scale = min(sw * 0.95 / pixmap.width(), sh * 0.95 / pixmap.height(), 1.0)
                        else:
                            scale = min(base_w * 0.9 / pixmap.width(), base_h * 0.9 / pixmap.height(), 1.0)
                            sx, sy = 0, 0
                            sw, sh = base_w, base_h
                        scaled = pixmap.scaled(
                            int(pixmap.width() * scale), int(pixmap.height() * scale),
                            Qt.KeepAspectRatio, Qt.SmoothTransformation
                        )
                        overlay = CleanPixmapItem(scaled)
                        self.scene.addItem(overlay)
                        overlay.setFlag(QGraphicsPixmapItem.ItemIsMovable, True)
                        overlay.setFlag(QGraphicsPixmapItem.ItemSendsGeometryChanges, True)
                        overlay.setZValue(1)
                        x = sx + (sw - scaled.width()) / 2
                        y = sy + (sh - scaled.height()) / 2
                        overlay.setPos(x, y)
                        overlay.setOpacity(self.slider_opacity.value() / 100.0)
                        self.overlay_items.append(overlay)
                        self.overlay_paths.append(path)
                else:
                    # 作为原材料打开
                    self._load_material(path)


# ============================================================================
#  启动入口
# ============================================================================
def main():
    # 隐藏控制台窗口（Windows）
    if sys.platform == 'win32':
        try:
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 0)
        except Exception:
            pass

    # 高DPI支持
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # 全局字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)

    # 应用深色主题
    app.setStyleSheet(DARK_THEME)

    window = EngravingMatchApp()
    window.show()
    window.raise_()
    window.activateWindow()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
