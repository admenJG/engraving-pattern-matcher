"""
主窗口模块
电脑雕刻套图匹配系统 - 主窗口
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QSplitter, QFileDialog, QMessageBox, QLabel,
                            QGroupBox, QGridLayout, QPushButton, QListWidget,
                            QListWidgetItem, QMenu, QAction, QToolBar)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QPointF, QRectF
from PyQt5.QtGui import QPixmap, QIcon, QCursor, QTransform

from config.settings import Settings
from ui.toolbar import Toolbar
from ui.left_panel import LeftPanel
from ui.canvas import CanvasView
from ui.bottom_bar import BottomBar


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        
        # 设置窗口属性
        self.setWindowTitle(Settings.WINDOW_TITLE)
        self.setMinimumSize(*Settings.WINDOW_MIN_SIZE)
        self.resize(*Settings.WINDOW_DEFAULT_SIZE)
        
        # 状态变量
        self._material_pixmap = None  # 材料图
        self._pattern_pixmap = None   # 图案图
        self._pattern_item = None     # 图案项
        
        # 设置窗口样式
        self._setup_style()
        
        # 初始化UI
        self._init_ui()
        
        # 连接信号
        self._connect_signals()
    
    def _setup_style(self):
        """设置窗口样式"""
        # 设置深色主题
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a2e;
            }
            QWidget {
                background-color: #1a1a2e;
                color: #e6e6e6;
                font-family: 'Microsoft YaHei', 'SimHei', Arial;
                font-size: 12px;
            }
            QPushButton {
                background-color: #533483;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #6a4c93;
            }
            QPushButton:pressed {
                background-color: #4a2d7a;
            }
            QLineEdit, QSpinBox, QComboBox {
                background-color: #0f3460;
                color: #e6e6e6;
                border: 1px solid #533483;
                border-radius: 3px;
                padding: 5px;
            }
            QListWidget {
                background-color: #0f3460;
                color: #e6e6e6;
                border: 1px solid #533483;
                border-radius: 3px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #533483;
            }
            QListWidget::item:selected {
                background-color: #533483;
            }
            QListWidget::item:hover {
                background-color: #6a4c93;
            }
            QToolBar {
                background-color: #0f3460;
                border-bottom: 1px solid #533483;
                spacing: 5px;
                padding: 5px;
            }
            QStatusBar {
                background-color: #0f3460;
                color: #e6e6e6;
            }
            QGroupBox {
                border: 1px solid #533483;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
    
    def _init_ui(self):
        """初始化UI"""
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 添加工具栏
        self.toolbar = Toolbar()
        main_layout.addWidget(self.toolbar)
        
        # 创建内容区域（使用分割器）
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setSpacing(5)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧面板 - 图案库
        self.left_panel = LeftPanel()
        self.left_panel.setMinimumWidth(200)
        self.left_panel.setMaximumWidth(300)
        
        splitter.addWidget(self.left_panel)
        
        # 中央画布区域
        self.canvas = CanvasView()
        splitter.addWidget(self.canvas)
        
        # 右侧面板 - 属性面板
        right_panel = QWidget()
        right_panel.setMinimumWidth(200)
        right_panel.setMaximumWidth(300)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 5, 5, 5)
        
        # 属性面板标题
        properties_title = QLabel("属性面板")
        properties_title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        right_layout.addWidget(properties_title)
        
        # 材料信息组
        material_group = QGroupBox("材料信息")
        material_layout = QGridLayout(material_group)
        
        material_layout.addWidget(QLabel("尺寸:"), 0, 0)
        self.material_size_label = QLabel("未加载")
        material_layout.addWidget(self.material_size_label, 0, 1)
        
        material_layout.addWidget(QLabel("文件:"), 1, 0)
        self.material_file_label = QLabel("未加载")
        material_layout.addWidget(self.material_file_label, 1, 1)
        
        right_layout.addWidget(material_group)
        
        # 图案属性组
        pattern_group = QGroupBox("图案属性")
        pattern_layout = QGridLayout(pattern_group)
        
        # 位置
        pattern_layout.addWidget(QLabel("X:"), 0, 0)
        self.pos_x_label = QLabel("0")
        pattern_layout.addWidget(self.pos_x_label, 0, 1)
        
        pattern_layout.addWidget(QLabel("Y:"), 0, 2)
        self.pos_y_label = QLabel("0")
        pattern_layout.addWidget(self.pos_y_label, 0, 3)
        
        # 尺寸
        pattern_layout.addWidget(QLabel("宽度:"), 1, 0)
        self.width_label = QLabel("0")
        pattern_layout.addWidget(self.width_label, 1, 1)
        
        pattern_layout.addWidget(QLabel("高度:"), 1, 2)
        self.height_label = QLabel("0")
        pattern_layout.addWidget(self.height_label, 1, 3)
        
        # 旋转
        pattern_layout.addWidget(QLabel("旋转:"), 2, 0)
        self.rotation_label = QLabel("0°")
        pattern_layout.addWidget(self.rotation_label, 2, 1)
        
        # 透明度
        pattern_layout.addWidget(QLabel("透明度:"), 2, 2)
        self.opacity_label = QLabel("100%")
        pattern_layout.addWidget(self.opacity_label, 2, 3)
        
        right_layout.addWidget(pattern_group)
        
        # 操作按钮组
        operation_group = QGroupBox("操作")
        operation_layout = QVBoxLayout(operation_group)
        
        # 镜像按钮
        mirror_layout = QHBoxLayout()
        self.btn_mirror_h = QPushButton("水平镜像")
        self.btn_mirror_h.clicked.connect(self._mirror_horizontal)
        mirror_layout.addWidget(self.btn_mirror_h)
        
        self.btn_mirror_v = QPushButton("垂直镜像")
        self.btn_mirror_v.clicked.connect(self._mirror_vertical)
        mirror_layout.addWidget(self.btn_mirror_v)
        
        operation_layout.addLayout(mirror_layout)
        
        # 旋转按钮
        rotation_layout = QHBoxLayout()
        self.btn_rotate_left = QPushButton("左旋90°")
        self.btn_rotate_left.clicked.connect(self._rotate_left)
        rotation_layout.addWidget(self.btn_rotate_left)
        
        self.btn_rotate_right = QPushButton("右旋90°")
        self.btn_rotate_right.clicked.connect(self._rotate_right)
        rotation_layout.addWidget(self.btn_rotate_right)
        
        operation_layout.addLayout(rotation_layout)
        
        # 适应按钮
        self.btn_fit_to_material = QPushButton("适应材料")
        self.btn_fit_to_material.clicked.connect(self._fit_to_material)
        operation_layout.addWidget(self.btn_fit_to_material)
        
        # 重置按钮
        self.btn_reset_pattern = QPushButton("重置图案")
        self.btn_reset_pattern.clicked.connect(self._reset_pattern)
        operation_layout.addWidget(self.btn_reset_pattern)
        
        right_layout.addWidget(operation_group)
        
        # 弹性空间
        right_layout.addStretch()
        
        splitter.addWidget(right_panel)
        
        # 设置分割器比例
        splitter.setSizes([200, 800, 200])
        
        content_layout.addWidget(splitter)
        main_layout.addWidget(content_widget, 1)
        
        # 添加底部控制栏
        self.bottom_bar = BottomBar()
        main_layout.addWidget(self.bottom_bar)
        
        # 设置状态栏
        self.statusBar().showMessage("就绪")
    
    def _connect_signals(self):
        """连接信号"""
        # 工具栏信号
        self.toolbar.open_material_clicked.connect(self._open_material)
        self.toolbar.save_clicked.connect(self._save_file)
        self.toolbar.undo_clicked.connect(self._undo)
        self.toolbar.redo_clicked.connect(self._redo)
        self.toolbar.add_library_clicked.connect(self._add_pattern_library)
        self.toolbar.remove_bg_clicked.connect(self._remove_background)
        
        # 左侧面板信号
        self.left_panel.pattern_selected.connect(self._on_pattern_selected_from_library)
        
        # 画布信号
        self.canvas.zoom_changed.connect(self.bottom_bar.set_zoom)
        self.canvas.position_changed.connect(self._update_position)
        self.canvas.pattern_selected.connect(self._update_pattern_properties)
        
        # 底部控制栏信号
        self.bottom_bar.zoom_fit_clicked.connect(self.canvas.fit_in_view)
    
    def _open_material(self):
        """打开材料图"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开材料图片", "",
            "图像文件 (*.jpg *.jpeg *.png *.webp *.bmp *.tiff *.tif);;所有文件 (*)"
        )
        
        if file_path:
            # 加载图片
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self._material_pixmap = pixmap
                
                # 设置画布背景
                self.canvas.set_background(pixmap)
                
                # 更新材料信息
                self.material_size_label.setText(f"{pixmap.width()} x {pixmap.height()}")
                self.material_file_label.setText(file_path.split('/')[-1].split('\\')[-1])
                
                # 更新状态栏
                self.statusBar().showMessage(f"已加载材料: {file_path}")
                
                # 如果有图案，重新适应材料
                if self._pattern_item:
                    self._fit_to_material()
            else:
                QMessageBox.warning(self, "错误", "无法加载图片文件")
    
    def _add_pattern_library(self):
        """添加图库目录"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择图库目录", "",
            "图像目录"
        )
        
        if dir_path:
            # 扫描目录中的图片文件
            import os
            image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif'}
            
            # 清空当前图案库
            self.left_panel.clear_patterns()
            
            # 扫描并添加图片
            count = 0
            for file_name in os.listdir(dir_path):
                file_ext = os.path.splitext(file_name)[1].lower()
                if file_ext in image_extensions:
                    file_path = os.path.join(dir_path, file_name)
                    self.left_panel.add_pattern_item(file_name, file_path)
                    count += 1
            
            # 更新状态栏
            self.statusBar().showMessage(f"已加载图库: {dir_path} ({count}张图片)")
            
            # 更新图案库标题
            # 这里可以更新左侧面板的标题显示目录名
    
    def _add_pattern(self):
        """添加图案"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图案文件", "",
            "图像文件 (*.jpg *.jpeg *.png *.webp *.bmp *.tiff *.tif);;所有文件 (*)"
        )
        
        if file_path:
            import os
            name = os.path.basename(file_path)
            self.left_panel.add_pattern_item(name, file_path)
            self.statusBar().showMessage(f"已添加图案: {name}")
    
    def _remove_pattern(self):
        """移除图案"""
        if self._pattern_item:
            self.canvas.remove_pattern(self._pattern_item)
            self._pattern_item = None
            
            # 从列表中移除
            current_item = self.left_panel.pattern_list.currentItem()
            if current_item:
                self.left_panel.pattern_list.takeItem(self.left_panel.pattern_list.row(current_item))
            
            # 更新状态栏
            self.statusBar().showMessage("已移除图案")
            
            # 更新图案数量
            pattern_count = len(self.canvas.get_pattern_items())
            self.bottom_bar.set_pattern_count(pattern_count)
    
    def _remove_background(self):
        """移除图案背景"""
        if self._pattern_item and self._pattern_pixmap:
            # 这里调用背景移除算法
            # 暂时使用简单的白色背景移除
            from PIL import Image
            import numpy as np
            from PyQt5.QtGui import QImage
            
            # 转换为PIL图像
            qimage = self._pattern_pixmap.toImage()
            buffer = qimage.bits().asstring(qimage.byteCount())
            pil_image = Image.frombuffer('RGBA', (qimage.width(), qimage.height()), buffer, 'raw', 'BGRA', 0, 1)
            
            # 转换为numpy数组
            img_array = np.array(pil_image)
            
            # 移除白色背景（简单阈值）
            threshold = 240
            mask = (img_array[:,:,0] > threshold) & (img_array[:,:,1] > threshold) & (img_array[:,:,2] > threshold)
            img_array[mask, 3] = 0  # 设置Alpha为0
            
            # 转换回PIL图像
            result_image = Image.fromarray(img_array)
            
            # 转换回QPixmap（使用正确的方法）
            data = result_image.tobytes("raw", "RGBA")
            qimage = QImage(data, result_image.size[0], result_image.size[1], QImage.Format_RGBA8888)
            result_pixmap = QPixmap.fromImage(qimage)
            
            # 更新图案
            self._pattern_pixmap = result_pixmap
            self.canvas.update_pattern(self._pattern_item, result_pixmap)
            
            self.statusBar().showMessage("已移除图案背景")
    
    def _save_file(self):
        """保存文件"""
        if self._material_pixmap:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存结果图片", "",
                "PNG文件 (*.png);;JPEG文件 (*.jpg);;所有文件 (*)"
            )
            
            if file_path:
                # 获取合成后的图像
                result_pixmap = self.canvas.get_composite_image()
                if result_pixmap:
                    result_pixmap.save(file_path)
                    self.statusBar().showMessage(f"已保存到: {file_path}")
                else:
                    QMessageBox.warning(self, "错误", "无法保存图片")
        else:
            QMessageBox.warning(self, "错误", "请先加载材料图片")
    
    def _undo(self):
        """撤销"""
        self.statusBar().showMessage("撤销功能开发中...")
    
    def _redo(self):
        """重做"""
        self.statusBar().showMessage("重做功能开发中...")
    
    def _mirror_horizontal(self):
        """水平镜像"""
        if self._pattern_item:
            self.canvas.mirror_pattern(self._pattern_item, horizontal=True)
            self.statusBar().showMessage("已水平镜像图案")
    
    def _mirror_vertical(self):
        """垂直镜像"""
        if self._pattern_item:
            self.canvas.mirror_pattern(self._pattern_item, vertical=True)
            self.statusBar().showMessage("已垂直镜像图案")
    
    def _rotate_left(self):
        """左旋90度"""
        if self._pattern_item:
            self.canvas.rotate_pattern(self._pattern_item, -90)
            self.statusBar().showMessage("已左旋图案90度")
    
    def _rotate_right(self):
        """右旋90度"""
        if self._pattern_item:
            self.canvas.rotate_pattern(self._pattern_item, 90)
            self.statusBar().showMessage("已右旋图案90度")
    
    def _fit_to_material(self):
        """适应材料大小"""
        if self._pattern_item and self._material_pixmap:
            # 计算适应大小
            pattern_size = self._pattern_pixmap.size()
            material_size = self._material_pixmap.size()
            
            # 计算缩放比例
            scale_x = material_size.width() / pattern_size.width()
            scale_y = material_size.height() / pattern_size.height()
            scale = min(scale_x, scale_y) * 0.8  # 留一些边距
            
            # 调整图案大小
            new_width = int(pattern_size.width() * scale)
            new_height = int(pattern_size.height() * scale)
            
            # 居中放置
            x = (material_size.width() - new_width) // 2
            y = (material_size.height() - new_height) // 2
            
            # 更新图案属性
            self.canvas.resize_pattern(self._pattern_item, new_width, new_height)
            self.canvas.move_pattern(self._pattern_item, QPointF(x, y))
            
            self.statusBar().showMessage("图案已适应材料大小")
    
    def _reset_pattern(self):
        """重置图案"""
        if self._pattern_item and self._pattern_pixmap:
            # 重置为原始大小和位置
            self.canvas.resize_pattern(self._pattern_item, 
                                      self._pattern_pixmap.width(), 
                                      self._pattern_pixmap.height())
            self.canvas.move_pattern(self._pattern_item, QPointF(0, 0))
            self.canvas.rotate_pattern(self._pattern_item, -self._pattern_item.rotation())
            
            self.statusBar().showMessage("图案已重置")
    
    def _update_position(self, pos):
        """更新位置显示"""
        self.bottom_bar.set_position(int(pos.x()), int(pos.y()))
        
        # 更新图案属性面板
        if self._pattern_item:
            item_pos = self._pattern_item.pos()
            self.pos_x_label.setText(str(int(item_pos.x())))
            self.pos_y_label.setText(str(int(item_pos.y())))
    
    def _update_pattern_properties(self, item):
        """更新图案属性显示"""
        if item:
            # 更新位置
            pos = item.pos()
            self.pos_x_label.setText(str(int(pos.x())))
            self.pos_y_label.setText(str(int(pos.y())))
            
            # 更新尺寸
            self.width_label.setText(str(int(item.boundingRect().width())))
            self.height_label.setText(str(int(item.boundingRect().height())))
            
            # 更新旋转
            self.rotation_label.setText(f"{int(item.rotation())}°")
            
            # 更新透明度
            opacity = int(item.opacity() * 100)
            self.opacity_label.setText(f"{opacity}%")
    
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        # 可以在这里处理画布自适应大小
    
    def _on_pattern_selected_from_library(self, file_path):
        """从图案库选择图案"""
        if file_path:
            # 加载图案
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self._pattern_pixmap = pixmap
                
                # 如果已经有图案，先移除
                if self._pattern_item:
                    self.canvas.remove_pattern(self._pattern_item)
                
                # 添加到画布
                self._pattern_item = self.canvas.add_pattern(pixmap, QPointF(0, 0))
                
                # 自动适应材料
                if self._material_pixmap:
                    self._fit_to_material()
                
                # 更新状态栏
                import os
                pattern_name = os.path.basename(file_path)
                self.statusBar().showMessage(f"已添加图案: {pattern_name}")
                
                # 更新图案数量
                pattern_count = len(self.canvas.get_pattern_items())
                self.bottom_bar.set_pattern_count(pattern_count)
            else:
                QMessageBox.warning(self, "错误", "无法加载图案文件")