"""
底部控制栏模块
缩放控制、状态信息
"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QSlider, 
                            QPushButton, QSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal


class BottomBar(QWidget):
    """底部控制栏类"""
    
    # 信号
    zoom_changed = pyqtSignal(float)
    zoom_fit_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        """初始化底部控制栏"""
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # 缩放控制
        zoom_layout = QHBoxLayout()
        zoom_layout.addWidget(QLabel("缩放:"))
        
        # 缩放滑块
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(10)  # 10%
        self.zoom_slider.setMaximum(500)  # 500%
        self.zoom_slider.setValue(100)  # 100%
        self.zoom_slider.setFixedWidth(150)
        self.zoom_slider.valueChanged.connect(self._on_zoom_slider_changed)
        zoom_layout.addWidget(self.zoom_slider)
        
        # 缩放百分比
        self.zoom_label = QLabel("100%")
        self.zoom_label.setFixedWidth(50)
        zoom_layout.addWidget(self.zoom_label)
        
        # 适应视图按钮
        self.btn_fit = QPushButton("适应视图")
        self.btn_fit.setFixedWidth(80)
        self.btn_fit.clicked.connect(self.zoom_fit_clicked.emit)
        zoom_layout.addWidget(self.btn_fit)
        
        layout.addLayout(zoom_layout)
        
        # 弹性空间
        layout.addStretch()
        
        # 位置信息
        position_layout = QHBoxLayout()
        position_layout.addWidget(QLabel("位置:"))
        
        self.pos_x_label = QLabel("X: 0")
        self.pos_x_label.setFixedWidth(60)
        position_layout.addWidget(self.pos_x_label)
        
        self.pos_y_label = QLabel("Y: 0")
        self.pos_y_label.setFixedWidth(60)
        position_layout.addWidget(self.pos_y_label)
        
        layout.addLayout(position_layout)
        
        # 尺寸信息
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("尺寸:"))
        
        self.width_label = QLabel("宽: 0")
        self.width_label.setFixedWidth(60)
        size_layout.addWidget(self.width_label)
        
        self.height_label = QLabel("高: 0")
        self.height_label.setFixedWidth(60)
        size_layout.addWidget(self.height_label)
        
        layout.addLayout(size_layout)
        
        # 图案数量
        pattern_layout = QHBoxLayout()
        pattern_layout.addWidget(QLabel("图案:"))
        
        self.pattern_count_label = QLabel("0")
        self.pattern_count_label.setFixedWidth(30)
        pattern_layout.addWidget(self.pattern_count_label)
        
        layout.addLayout(pattern_layout)
    
    def _on_zoom_slider_changed(self, value):
        """缩放滑块改变"""
        zoom = value / 100.0
        self.zoom_label.setText(f"{value}%")
        self.zoom_changed.emit(zoom)
    
    def set_zoom(self, zoom: float):
        """设置缩放显示"""
        percentage = int(zoom * 100)
        self.zoom_slider.setValue(percentage)
        self.zoom_label.setText(f"{percentage}%")
    
    def set_position(self, x: int, y: int):
        """设置位置显示"""
        self.pos_x_label.setText(f"X: {x}")
        self.pos_y_label.setText(f"Y: {y}")
    
    def set_size(self, width: int, height: int):
        """设置尺寸显示"""
        self.width_label.setText(f"宽: {width}")
        self.height_label.setText(f"高: {height}")
    
    def set_pattern_count(self, count: int):
        """设置图案数量"""
        self.pattern_count_label.setText(str(count))