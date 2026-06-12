"""
应用配置模块
所有配置集中管理，避免硬编码
"""

import os
from pathlib import Path


class Settings:
    """应用配置类"""
    
    # 应用基本信息
    APP_NAME = "电脑雕刻套图匹配系统"
    APP_VERSION = "2.0"
    APP_DESCRIPTION = "用于雕刻图案的叠加、编辑、去背景、导出"
    
    # 路径配置
    BASE_DIR = Path(__file__).parent.parent
    TEMP_DIR = BASE_DIR / "temp"
    RESOURCES_DIR = BASE_DIR / "resources"
    
    # 默认材料目录（可以从配置文件或环境变量读取）
    DEFAULT_MATERIAL_DIR = os.getenv(
        "MATERIAL_DIR",
        r"E:\常用图(禁止删除)"  # 默认值，但建议通过环境变量设置
    )
    
    # 支持的图像格式
    SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif'}
    
    # 图像处理参数
    MAX_IMAGE_SIZE = (4096, 4096)  # 最大图像尺寸
    DEFAULT_QUALITY = 95  # 默认保存质量
    THUMBNAIL_SIZE = (120, 120)  # 缩略图尺寸
    
    # 界面设置
    WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"
    WINDOW_MIN_SIZE = (1200, 750)
    WINDOW_DEFAULT_SIZE = (1440, 900)
    
    # 撤销/重做设置
    MAX_UNDO_STACK = 30
    
    # 主题设置
    THEMES = {
        "dark": {
            "name": "深色主题",
            "primary_color": "#533483",
            "secondary_color": "#0f3460",
            "background_color": "#1a1a2e",
            "text_color": "#e6e6e6",
            "accent_color": "#e94560"
        },
        "light": {
            "name": "浅色主题",
            "primary_color": "#3498db",
            "secondary_color": "#2ecc71",
            "background_color": "#ecf0f1",
            "text_color": "#2c3e50",
            "accent_color": "#e74c3c"
        }
    }
    
    # 默认主题
    DEFAULT_THEME = "dark"
    
    @classmethod
    def get_theme(cls, theme_name=None):
        """获取主题配置"""
        if theme_name is None:
            theme_name = cls.DEFAULT_THEME
        return cls.THEMES.get(theme_name, cls.THEMES[cls.DEFAULT_THEME])
    
    @classmethod
    def ensure_directories(cls):
        """确保必要的目录存在"""
        cls.TEMP_DIR.mkdir(exist_ok=True)
        (cls.RESOURCES_DIR / "styles").mkdir(exist_ok=True)
        (cls.RESOURCES_DIR / "icons").mkdir(exist_ok=True)