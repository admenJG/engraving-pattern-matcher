# 测试模块
import unittest
from config.settings import Settings
from config.constants import ImageConstants, UIConstants
from utils.file_utils import FileUtils
from utils.math_utils import MathUtils


class TestConfig(unittest.TestCase):
    """测试配置模块"""
    
    def test_settings_exists(self):
        """测试设置类是否存在"""
        self.assertTrue(hasattr(Settings, 'APP_NAME'))
        self.assertTrue(hasattr(Settings, 'APP_VERSION'))
    
    def test_constants_exist(self):
        """测试常量类是否存在"""
        self.assertTrue(hasattr(ImageConstants, 'GRAYSCALE_THRESHOLD'))
        self.assertTrue(hasattr(UIConstants, 'BUTTON_WIDTH'))


class TestUtils(unittest.TestCase):
    """测试工具模块"""
    
    def test_file_utils(self):
        """测试文件工具"""
        # 测试确保目录存在
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, "test_dir")
            self.assertTrue(FileUtils.ensure_dir(test_dir))
            self.assertTrue(os.path.exists(test_dir))
    
    def test_math_utils(self):
        """测试数学工具"""
        # 测试钳制函数
        self.assertEqual(MathUtils.clamp(5, 0, 10), 5)
        self.assertEqual(MathUtils.clamp(-5, 0, 10), 0)
        self.assertEqual(MathUtils.clamp(15, 0, 10), 10)
        
        # 测试线性插值
        self.assertEqual(MathUtils.lerp(0, 10, 0.5), 5)
        self.assertEqual(MathUtils.lerp(0, 10, 0), 0)
        self.assertEqual(MathUtils.lerp(0, 10, 1), 10)


if __name__ == '__main__':
    unittest.main()