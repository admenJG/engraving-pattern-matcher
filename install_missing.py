#!/usr/bin/env python3
"""
安装缺失的依赖
先检查，再安装
"""

import subprocess
import sys
import importlib


def check_package(package_name):
    """检查包是否已安装"""
    try:
        if package_name == 'opencv-python':
            import cv2
            return True
        elif package_name == 'Pillow':
            import PIL
            return True
        elif package_name == 'numpy':
            import numpy
            return True
        elif package_name == 'scipy':
            import scipy
            return True
        elif package_name == 'PyQt5':
            import PyQt5
            return True
        else:
            import_name = package_name.replace('-', '_').lower()
            importlib.import_module(import_name)
            return True
    except ImportError:
        return False


def install_package(package_name):
    """安装包"""
    print(f"正在安装 {package_name}...")
    try:
        cmd = [sys.executable, "-m", "pip", "install", package_name]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {package_name} 安装成功")
            return True
        else:
            print(f"❌ {package_name} 安装失败")
            return False
    except Exception as e:
        print(f"❌ {package_name} 安装异常: {e}")
        return False


def main():
    print("=" * 60)
    print("📦 智能依赖安装工具")
    print("=" * 60)
    
    # 需要安装的依赖
    dependencies = [
        "PyQt5",
        "Pillow", 
        "numpy",
        "opencv-python",
        "scipy"
    ]
    
    print("\n🔍 检查依赖状态:")
    missing = []
    installed = []
    
    for pkg in dependencies:
        if check_package(pkg):
            print(f"✅ {pkg}: 已安装")
            installed.append(pkg)
        else:
            print(f"❌ {pkg}: 未安装")
            missing.append(pkg)
    
    print(f"\n📊 检查结果:")
    print(f"已安装: {len(installed)} 个")
    print(f"未安装: {len(missing)} 个")
    
    if not missing:
        print("\n🎉 所有依赖都已安装！")
        print("可以运行项目: python main.py")
        return
    
    print(f"\n⚠️  需要安装以下依赖:")
    for pkg in missing:
        print(f"   - {pkg}")
    
    # 安装缺失的依赖
    print("\n" + "=" * 60)
    print("🚀 开始安装缺失的依赖:")
    print("=" * 60)
    
    success = 0
    failed = []
    
    for pkg in missing:
        if install_package(pkg):
            success += 1
        else:
            failed.append(pkg)
    
    print(f"\n📊 安装完成:")
    print(f"成功安装: {success} 个")
    print(f"安装失败: {len(failed)} 个")
    
    if failed:
        print("\n❌ 以下包安装失败:")
        for pkg in failed:
            print(f"   - {pkg}")
        print("\n请手动安装:")
        print(f"   pip install {' '.join(failed)}")
    else:
        print("\n🎉 所有依赖安装成功！")
    
    # 最终验证
    print("\n" + "=" * 60)
    print("🔍 最终验证:")
    print("=" * 60)
    
    all_ok = True
    for pkg in dependencies:
        if check_package(pkg):
            print(f"✅ {pkg}: 已安装")
        else:
            print(f"❌ {pkg}: 未安装")
            all_ok = False
    
    if all_ok:
        print("\n🎉 所有依赖验证通过！")
        print("现在可以运行项目: python main.py")
    else:
        print("\n⚠️  部分依赖验证失败")


if __name__ == "__main__":
    main()