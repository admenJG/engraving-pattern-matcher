"""
左侧面板模块
路径管理和图案库
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QListWidget, QListWidgetItem,
                            QFileDialog, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class LeftPanel(QWidget):
    """左侧面板类"""
    
    # 信号
    material_dir_changed = pyqtSignal(str)
    pattern_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """初始化左侧面板"""
        super().__init__(parent)
        self._current_dir = ""
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 路径管理组
        path_group = QGroupBox("路径管理")
        path_layout = QVBoxLayout(path_group)
        
        # 材料目录
        path_layout.addWidget(QLabel("材料目录:"))
        
        dir_layout = QHBoxLayout()
        self.dir_edit = QLineEdit()
        self.dir_edit.setPlaceholderText("选择材料目录...")
        self.dir_edit.setReadOnly(True)
        dir_layout.addWidget(self.dir_edit)
        
        self.btn_browse = QPushButton("浏览")
        self.btn_browse.setFixedWidth(60)
        self.btn_browse.clicked.connect(self._browse_directory)
        dir_layout.addWidget(self.btn_browse)
        
        path_layout.addLayout(dir_layout)
        layout.addWidget(path_group)
        
        # 图案库组
        pattern_group = QGroupBox("图案库")
        pattern_layout = QVBoxLayout(pattern_group)
        
        # 图案列表
        self.pattern_list = QListWidget()
        self.pattern_list.currentItemChanged.connect(self._on_pattern_selected)
        pattern_layout.addWidget(self.pattern_list)
        
        # 图案操作按钮
        btn_layout = QHBoxLayout()
        self.btn_add_library = QPushButton("添加图库")
        self.btn_add_library.clicked.connect(self._add_library)
        btn_layout.addWidget(self.btn_add_library)
        
        self.btn_remove_pattern = QPushButton("移除图案")
        self.btn_remove_pattern.clicked.connect(self._remove_pattern)
        btn_layout.addWidget(self.btn_remove_pattern)
        
        pattern_layout.addLayout(btn_layout)
        layout.addWidget(pattern_group)
        
        # 图案属性组
        property_group = QGroupBox("图案属性")
        property_layout = QVBoxLayout(property_group)
        
        # 位置
        pos_layout = QHBoxLayout()
        pos_layout.addWidget(QLabel("X:"))
        self.pos_x_edit = QLineEdit("0")
        self.pos_x_edit.setFixedWidth(60)
        pos_layout.addWidget(self.pos_x_edit)
        
        pos_layout.addWidget(QLabel("Y:"))
        self.pos_y_edit = QLineEdit("0")
        self.pos_y_edit.setFixedWidth(60)
        pos_layout.addWidget(self.pos_y_edit)
        
        property_layout.addLayout(pos_layout)
        
        # 尺寸
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("宽度:"))
        self.width_edit = QLineEdit("100")
        self.width_edit.setFixedWidth(60)
        size_layout.addWidget(self.width_edit)
        
        size_layout.addWidget(QLabel("高度:"))
        self.height_edit = QLineEdit("100")
        self.height_edit.setFixedWidth(60)
        size_layout.addWidget(self.height_edit)
        
        property_layout.addLayout(size_layout)
        
        # 旋转
        rotation_layout = QHBoxLayout()
        rotation_layout.addWidget(QLabel("旋转:"))
        self.rotation_edit = QLineEdit("0")
        self.rotation_edit.setFixedWidth(60)
        rotation_layout.addWidget(self.rotation_edit)
        rotation_layout.addWidget(QLabel("°"))
        rotation_layout.addStretch()
        
        property_layout.addLayout(rotation_layout)
        
        # 透明度
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("透明度:"))
        self.opacity_edit = QLineEdit("1.0")
        self.opacity_edit.setFixedWidth(60)
        opacity_layout.addWidget(self.opacity_edit)
        opacity_layout.addStretch()
        
        property_layout.addLayout(opacity_layout)
        
        # 应用按钮
        self.btn_apply = QPushButton("应用属性")
        self.btn_apply.clicked.connect(self._apply_properties)
        property_layout.addWidget(self.btn_apply)
        
        layout.addWidget(property_group)
        
        # 弹性空间
        layout.addStretch()
    
    def _browse_directory(self):
        """浏览目录"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择材料目录", self._current_dir
        )
        
        if dir_path:
            self._current_dir = dir_path
            self.dir_edit.setText(dir_path)
            self.material_dir_changed.emit(dir_path)
    
    def _on_pattern_selected(self, current, previous):
        """图案选择改变"""
        if current:
            self.pattern_selected.emit(current.data(0))
    
    def _add_pattern(self):
        """添加图案"""
        # 这里将由主窗口处理
        pass
    
    def _remove_pattern(self):
        """移除图案"""
        current_item = self.pattern_list.currentItem()
        if current_item:
            self.pattern_list.takeItem(self.pattern_list.row(current_item))
    
    def _apply_properties(self):
        """应用属性"""
        # 这里将由主窗口处理
        pass
    
    def add_pattern_item(self, name: str, file_path: str):
        """添加图案到列表"""
        item = QListWidgetItem(name)
        item.setData(0, file_path)
        self.pattern_list.addItem(item)
    
    def clear_patterns(self):
        """清空图案列表"""
        self.pattern_list.clear()
    
    def set_current_dir(self, dir_path: str):
        """设置当前目录"""
        self._current_dir = dir_path
        self.dir_edit.setText(dir_path)
    
    def _add_library(self):
        """添加图库目录"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择图库目录", self._current_dir
        )
        
        if dir_path:
            # 扫描目录中的图片文件
            import os
            image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif'}
            
            self.clear_patterns()
            
            for file_name in os.listdir(dir_path):
                file_ext = os.path.splitext(file_name)[1].lower()
                if file_ext in image_extensions:
                    file_path = os.path.join(dir_path, file_name)
                    self.add_pattern_item(file_name, file_path)
            
            # 更新当前目录
            self._current_dir = dir_path
            self.dir_edit.setText(dir_path)
            
            # 发送信号
            self.material_dir_changed.emit(dir_path)