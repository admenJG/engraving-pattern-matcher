"""
常量定义模块
避免在代码中使用魔术数字和硬编码值
"""

# 图像处理常量
class ImageConstants:
    """图像处理相关常量"""
    
    # 颜色阈值
    GRAYSCALE_THRESHOLD = 128
    ALPHA_THRESHOLD = 128
    
    # 边缘检测参数
    CANNY_LOW_THRESHOLD = 50
    CANNY_HIGH_THRESHOLD = 150
    
    # GrabCut参数
    GRABCUT_ITERATIONS = 5
    GRABCUT_RECT_MARGIN = 10
    
    # 缩放比例
    MIN_SCALE = 0.1
    MAX_SCALE = 5.0
    SCALE_STEP = 0.1
    
    # 旋转角度
    ROTATION_STEP = 15  # 度
    
    # 透明度
    MIN_OPACITY = 0.0
    MAX_OPACITY = 1.0
    OPACITY_STEP = 0.1


# UI常量
class UIConstants:
    """界面相关常量"""
    
    # 按钮尺寸
    BUTTON_WIDTH = 120
    BUTTON_HEIGHT = 35
    ICON_BUTTON_SIZE = 30
    
    # 间距
    SMALL_SPACING = 5
    MEDIUM_SPACING = 10
    LARGE_SPACING = 20
    
    # 边距
    SMALL_MARGIN = 5
    MEDIUM_MARGIN = 10
    LARGE_MARGIN = 20
    
    # 字体
    FONT_FAMILY = "Microsoft YaHei, SimHei, Arial"
    FONT_SIZE_SMALL = 10
    FONT_SIZE_NORMAL = 12
    FONT_SIZE_LARGE = 14
    
    # 动画
    ANIMATION_DURATION = 200  # 毫秒


# 文件常量
class FileConstants:
    """文件相关常量"""
    
    # 配置文件扩展名
    CONFIG_EXTENSIONS = {'.json', '.yaml', '.yml', '.ini', '.cfg'}
    
    # 备份文件后缀
    BACKUP_SUFFIX = ".bak"
    
    # 临时文件前缀
    TEMP_PREFIX = "temp_"
    
    # 日志文件
    LOG_FILE = "app.log"
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5


# 错误消息
class ErrorMessages:
    """错误消息常量"""
    
    # 文件错误
    FILE_NOT_FOUND = "文件不存在: {}"
    FILE_READ_ERROR = "读取文件失败: {}"
    FILE_WRITE_ERROR = "写入文件失败: {}"
    UNSUPPORTED_FORMAT = "不支持的文件格式: {}"
    
    # 图像错误
    IMAGE_LOAD_ERROR = "加载图像失败: {}"
    IMAGE_SAVE_ERROR = "保存图像失败: {}"
    IMAGE_PROCESS_ERROR = "图像处理失败: {}"
    
    # 配置错误
    CONFIG_NOT_FOUND = "配置文件不存在: {}"
    CONFIG_LOAD_ERROR = "加载配置失败: {}"
    
    # 通用错误
    UNKNOWN_ERROR = "未知错误: {}"
    OPERATION_FAILED = "操作失败: {}"