#!/usr/bin/env python3
"""
一键安装所有依赖
使用清华镜像源，完全自动化
"""

import subprocess
import sys
import time


def install_package(package_name, mirror="https://pypi.tuna.tsinghua.edu.cn/simple"):
    """安装单个包"""
    print(f"正在安装 {package_name}...")
    
    cmd = [
        sys.executable, "-m", "pip", "install",
        "--index-url", mirror,
        "--upgrade",
        package_name
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {package_name} 安装成功")
            return True
        else:
            print(f"❌ {package_name} 安装失败")
            # 显示错误信息
            if result.stderr:
                lines = result.stderr.strip().split('\n')
                for line in lines[-3:]:
                    print(f"   {line}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {package_name} 安装超时")
        return False
    except Exception as e:
        print(f"❌ {package_name} 安装异常: {e}")
        return False


def main():
    print("=" * 60)
    print("🚀 套图系统 - 一键安装所有依赖")
    print("=" * 60)
    print("使用清华镜像源，完全自动化安装")
    print("=" * 60)
    
    # 需要安装的依赖
    dependencies = [
        "numpy",
        "Pillow",
        "opencv-python",
        "scipy",
        "PyQt5"
    ]
    
    # 使用清华镜像源
    mirror = "https://pypi.tuna.tsinghua.edu.cn/simple"
    print(f"\n使用镜像源: {mirror}")
    
    # 安装依赖
    print("\n" + "=" * 60)
    print("开始安装依赖:")
    print("=" * 60)
    
    success_count = 0
    failed_packages = []
    
    for package in dependencies:
        if install_package(package, mirror):
            success_count += 1
        else:
            failed_packages.append(package)
        
        # 短暂延迟，避免请求过快
        time.sleep(1)
    
    # 安装结果
    print("\n" + "=" * 60)
    print("安装结果:")
    print("=" * 60)
    print(f"总依赖数: {len(dependencies)}")
    print(f"安装成功: {success_count} 个")
    print(f"安装失败: {len(failed_packages)} 个")
    
    if failed_packages:
        print(f"\n❌ 失败的包: {', '.join(failed_packages)}")
        print("\n请手动安装失败的包:")
        for pkg in failed_packages:
            print(f"   pip install {pkg}")
    else:
        print("\n🎉 所有依赖安装成功！")
    
    # 验证安装
    print("\n" + "=" * 60)
    print("验证安装结果:")
    print("=" * 60)
    
    all_ok = True
    for package in dependencies:
        try:
            if package == "opencv-python":
                import cv2
                print(f"✅ {package}: {cv2.__version__}")
            elif package == "Pillow":
                import PIL
                print(f"✅ {package}: {PIL.__version__}")
            elif package == "numpy":
                import numpy
                print(f"✅ {package}: {numpy.__version__}")
            elif package == "scipy":
                import scipy
                print(f"✅ {package}: {scipy.__version__}")
            elif package == "PyQt5":
                import PyQt5
                print(f"✅ {package}: {PyQt5.QtCore.PYQT_VERSION_STR}")
            else:
                print(f"✅ {package}: 已安装")
        except ImportError:
            print(f"❌ {package}: 未安装")
            all_ok = False
    
    if all_ok:
        print("\n🎉 所有依赖验证通过！")
        print("\n🚀 准备运行项目...")
        
        # 运行主程序
        try:
            import os
            project_root = os.path.dirname(os.path.abspath(__file__))
            main_script = os.path.join(project_root, "main.py")
            
            if os.path.exists(main_script):
                print("正在启动应用程序...")
                subprocess.Popen([sys.executable, main_script])
                print("✅ 应用程序已启动")
                print("感谢使用套图系统！")
            else:
                print(f"❌ 找不到主程序: {main_script}")
                print("请手动运行: python main.py")
                
        except Exception as e:
            print(f"❌ 启动项目失败: {e}")
            print("请手动运行: python main.py")
    else:
        print("\n⚠️  部分依赖未安装，项目可能无法正常运行")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  安装被用户中断")
    except Exception as e:
        print(f"\n❌ 安装过程中发生错误: {e}")