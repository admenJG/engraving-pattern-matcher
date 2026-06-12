"""
工具栏模块
顶部工具栏
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class Toolbar(QWidget):
    """工具栏类"""
    
    # 信号
    open_material_clicked = pyqtSignal()
    save_clicked = pyqtSignal()
    undo_clicked = pyqtSignal()
    redo_clicked = pyqtSignal()
    add_pattern_clicked = pyqtSignal()
    add_library_clicked = pyqtSignal()
    remove_bg_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        """初始化工具栏"""
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # 打开原料按钮
        self.btn_open = QPushButton("📂 打开原料")
        self.btn_open.setMinimumWidth(120)
        self.btn_open.clicked.connect(self.open_material_clicked.emit)
        layout.addWidget(self.btn_open)
        
        # 保存按钮
        self.btn_save = QPushButton("💾 保存")
        self.btn_save.setMinimumWidth(80)
        self.btn_save.clicked.connect(self.save_clicked.emit)
        layout.addWidget(self.btn_save)
        
        # 分隔符
        layout.addWidget(self._create_separator())
        
        # 撤销按钮
        self.btn_undo = QPushButton("↩ 撤销")
        self.btn_undo.setMinimumWidth(80)
        self.btn_undo.clicked.connect(self.undo_clicked.emit)
        layout.addWidget(self.btn_undo)
        
        # 重做按钮
        self.btn_redo = QPushButton("↪ 重做")
        self.btn_redo.setMinimumWidth(80)
        self.btn_redo.clicked.connect(self.redo_clicked.emit)
        layout.addWidget(self.btn_redo)
        
        # 分隔符
        layout.addWidget(self._create_separator())
        
        # 添加图库按钮
        self.btn_add_library = QPushButton("📁 添加图库")
        self.btn_add_library.setMinimumWidth(120)
        self.btn_add_library.clicked.connect(self.add_library_clicked.emit)
        layout.addWidget(self.btn_add_library)
        
        # 去背景按钮
        self.btn_remove_bg = QPushButton("🖼 去背景")
        self.btn_remove_bg.setMinimumWidth(100)
        self.btn_remove_bg.clicked.connect(self.remove_bg_clicked.emit)
        layout.addWidget(self.btn_remove_bg)
        
        # 弹性空间
        layout.addStretch()
        
        # 标题
        title_label = QLabel("电脑雕刻套图匹配系统")
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        title_label.setStyleSheet("color: #e94560;")
        layout.addWidget(title_label)
    
    def _create_separator(self):
        """创建分隔符"""
        separator = QLabel("|")
        separator.setStyleSheet("color: #533483; font-size: 16px;")
        return separator
    
    def set_undo_enabled(self, enabled: bool):
        """设置撤销按钮状态"""
        self.btn_undo.setEnabled(enabled)
    
    def set_redo_enabled(self, enabled: bool):
        """设置重做按钮状态"""
        self.btn_redo.setEnabled(enabled)