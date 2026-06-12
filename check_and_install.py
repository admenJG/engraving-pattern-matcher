#!/usr/bin/env python3
"""
智能依赖检测和安装脚本
在安装前先检查电脑上是否已经安装了依赖
"""

import subprocess
import sys
import importlib
from typing import List, Tuple, Dict


def check_package_installed(package_name: str) -> Tuple[bool, str]:
    """检查包是否已安装"""
    try:
        # 尝试导入包
        if package_name == 'opencv-python':
            # OpenCV的导入名是cv2
            import cv2
            version = cv2.__version__
            return True, f"已安装 (版本: {version})"
        elif package_name == 'Pillow':
            # Pillow的导入名是PIL
            import PIL
            version = PIL.__version__
            return True, f"已安装 (版本: {version})"
        elif package_name == 'numpy':
            import numpy
            version = numpy.__version__
            return True, f"已安装 (版本: {version})"
        elif package_name == 'scipy':
            import scipy
            version = scipy.__version__
            return True, f"已安装 (版本: {version})"
        elif package_name == 'PyQt5':
            import PyQt5
            version = PyQt5.QtCore.PYQT_VERSION_STR
            return True, f"已安装 (版本: {version})"
        else:
            # 通用检查方法
            # 将包名转换为导入名（处理连字符）
            import_name = package_name.replace('-', '_').lower()
            importlib.import_module(import_name)
            return True, "已安装"
            
    except ImportError:
        return False, "未安装"
    except Exception as e:
        return False, f"检查失败: {e}"


def get_installed_version(package_name: str) -> str:
    """获取已安装包的版本"""
    try:
        # 使用pip list获取版本信息
        cmd = [sys.executable, "-m", "pip", "list"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # 解析pip list输出
            for line in result.stdout.split('\n'):
                if package_name.lower() in line.lower():
                    # 提取版本号（通常是第二列）
                    parts = line.split()
                    if len(parts) >= 2:
                        return parts[1]
            
            # 特殊处理OpenCV
            if package_name == 'opencv-python':
                for line in result.stdout.split('\n'):
                    if 'opencv' in line.lower():
                        parts = line.split()
                        if len(parts) >= 2:
                            return parts[1]
        
        return "未知版本"
        
    except Exception:
        return "未知版本"


def install_package(package_name: str) -> bool:
    """安装单个包"""
    try:
        print(f"正在安装 {package_name}...")
        # 使用当前Python解释器的pip
        cmd = [sys.executable, "-m", "pip", "install", package_name]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {package_name} 安装成功")
            return True
        else:
            print(f"❌ {package_name} 安装失败:")
            print(f"   错误信息: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {package_name} 安装超时")
        return False
    except Exception as e:
        print(f"❌ {package_name} 安装异常: {e}")
        return False


def parse_requirements(requirements_file: str) -> List[str]:
    """解析requirements.txt文件"""
    packages = []
    try:
        with open(requirements_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue
                # 移除版本号（简单处理）
                if '>=' in line:
                    package = line.split('>=')[0]
                elif '<=' in line:
                    package = line.split('<=')[0]
                elif '==' in line:
                    package = line.split('==')[0]
                else:
                    package = line
                packages.append(package.strip())
    except Exception as e:
        print(f"读取requirements.txt失败: {e}")
    return packages


def main():
    """主函数"""
    print("=" * 60)
    print("🔍 智能依赖检测和安装工具")
    print("=" * 60)
    
    # 项目依赖文件路径
    requirements_file = "requirements.txt"
    
    # 检查requirements.txt是否存在
    import os
    if not os.path.exists(requirements_file):
        print(f"❌ 找不到 {requirements_file} 文件")
        return
    
    # 解析依赖
    packages = parse_requirements(requirements_file)
    if not packages:
        print("❌ 没有找到任何依赖")
        return
    
    print(f"\n📋 共找到 {len(packages)} 个依赖:")
    for i, pkg in enumerate(packages, 1):
        print(f"   {i}. {pkg}")
    
    # 检查每个依赖
    print("\n" + "=" * 60)
    print("🔍 检查依赖安装状态:")
    print("=" * 60)
    
    installed_packages = []
    missing_packages = []
    
    for package in packages:
        is_installed, status = check_package_installed(package)
        version = get_installed_version(package) if is_installed else ""
        
        if is_installed:
            print(f"✅ {package}: {status} (版本: {version})")
            installed_packages.append(package)
        else:
            print(f"❌ {package}: {status}")
            missing_packages.append(package)
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 依赖检查结果:")
    print("=" * 60)
    print(f"已安装: {len(installed_packages)} 个")
    print(f"未安装: {len(missing_packages)} 个")
    
    if not missing_packages:
        print("\n🎉 所有依赖都已安装！可以运行项目了。")
        print("运行命令: python main.py")
        return
    
    # 询问是否安装缺失的依赖
    print(f"\n⚠️  以下依赖需要安装:")
    for pkg in missing_packages:
        print(f"   - {pkg}")
    
    # 自动安装缺失的依赖
    print("\n" + "=" * 60)
    print("🚀 开始安装缺失的依赖:")
    print("=" * 60)
    
    success_count = 0
    failed_packages = []
    
    for package in missing_packages:
        if install_package(package):
            success_count += 1
        else:
            failed_packages.append(package)
    
    # 安装结果
    print("\n" + "=" * 60)
    print("📊 安装结果:")
    print("=" * 60)
    print(f"成功安装: {success_count} 个")
    print(f"安装失败: {len(failed_packages)} 个")
    
    if failed_packages:
        print("\n❌ 以下包安装失败:")
        for pkg in failed_packages:
            print(f"   - {pkg}")
        print("\n请手动安装这些包:")
        print(f"   pip install {' '.join(failed_packages)}")
    else:
        print("\n🎉 所有依赖安装成功！")
        print("现在可以运行项目了: python main.py")
    
    # 验证安装
    print("\n" + "=" * 60)
    print("🔍 验证安装结果:")
    print("=" * 60)
    
    all_ok = True
    for package in packages:
        is_installed, status = check_package_installed(package)
        if is_installed:
            version = get_installed_version(package)
            print(f"✅ {package}: {version}")
        else:
            print(f"❌ {package}: {status}")
            all_ok = False
    
    if all_ok:
        print("\n🎉 所有依赖验证通过！可以运行项目了。")
    else:
        print("\n⚠️  部分依赖验证失败，请检查安装。")


if __name__ == "__main__":
    main()