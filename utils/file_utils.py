"""
文件操作工具模块
提供安全的文件操作函数
"""

import os
import shutil
from pathlib import Path
from typing import Optional, List, Union


class FileUtils:
    """文件操作工具类"""
    
    @staticmethod
    def ensure_dir(dir_path: Union[str, Path]) -> bool:
        """确保目录存在，不存在则创建"""
        try:
            path = Path(dir_path)
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"创建目录失败: {e}")
            return False
    
    @staticmethod
    def safe_delete(file_path: Union[str, Path]) -> bool:
        """安全删除文件（移到回收站或删除）"""
        try:
            path = Path(file_path)
            if path.exists():
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)
                return True
            return False
        except Exception as e:
            print(f"删除文件失败: {e}")
            return False
    
    @staticmethod
    def backup_file(file_path: Union[str, Path], backup_suffix: str = ".bak") -> Optional[Path]:
        """备份文件"""
        try:
            path = Path(file_path)
            if path.exists():
                backup_path = path.with_suffix(path.suffix + backup_suffix)
                shutil.copy2(path, backup_path)
                return backup_path
            return None
        except Exception as e:
            print(f"备份文件失败: {e}")
            return None
    
    @staticmethod
    def get_file_size(file_path: Union[str, Path]) -> int:
        """获取文件大小（字节）"""
        try:
            path = Path(file_path)
            if path.exists():
                return path.stat().st_size
            return 0
        except Exception:
            return 0
    
    @staticmethod
    def get_file_extension(file_path: Union[str, Path]) -> str:
        """获取文件扩展名（小写）"""
        try:
            path = Path(file_path)
            return path.suffix.lower()
        except Exception:
            return ""
    
    @staticmethod
    def is_image_file(file_path: Union[str, Path], supported_formats: set = None) -> bool:
        """判断是否为支持的图像文件"""
        if supported_formats is None:
            supported_formats = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif'}
        
        extension = FileUtils.get_file_extension(file_path)
        return extension in supported_formats
    
    @staticmethod
    def list_files(dir_path: Union[str, Path], 
                   extensions: Optional[set] = None,
                   recursive: bool = False) -> List[Path]:
        """列出目录中的文件"""
        try:
            path = Path(dir_path)
            if not path.exists():
                return []
            
            files = []
            if recursive:
                for item in path.rglob("*"):
                    if item.is_file():
                        if extensions is None or item.suffix.lower() in extensions:
                            files.append(item)
            else:
                for item in path.iterdir():
                    if item.is_file():
                        if extensions is None or item.suffix.lower() in extensions:
                            files.append(item)
            
            return sorted(files)
        except Exception as e:
            print(f"列出文件失败: {e}")
            return []
    
    @staticmethod
    def copy_file(src: Union[str, Path], dst: Union[str, Path]) -> bool:
        """复制文件"""
        try:
            src_path = Path(src)
            dst_path = Path(dst)
            
            # 确保目标目录存在
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(src_path, dst_path)
            return True
        except Exception as e:
            print(f"复制文件失败: {e}")
            return False
    
    @staticmethod
    def move_file(src: Union[str, Path], dst: Union[str, Path]) -> bool:
        """移动文件"""
        try:
            src_path = Path(src)
            dst_path = Path(dst)
            
            # 确保目标目录存在
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(src_path, dst_path)
            return True
        except Exception as e:
            print(f"移动文件失败: {e}")
            return False
    
    @staticmethod
    def read_text_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> Optional[str]:
        """读取文本文件"""
        try:
            path = Path(file_path)
            if path.exists():
                with open(path, 'r', encoding=encoding) as f:
                    return f.read()
            return None
        except Exception as e:
            print(f"读取文件失败: {e}")
            return None
    
    @staticmethod
    def write_text_file(file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> bool:
        """写入文本文件"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"写入文件失败: {e}")
            return False