#!/usr/bin/env python3
"""
全自动依赖安装脚本
使用国内镜像源，完全自动化，无需用户交互
"""

import subprocess
import sys
import os
import time
import importlib
from typing import List, Dict, Tuple


class AutoInstaller:
    """自动安装器"""
    
    def __init__(self):
        """初始化安装器"""
        # 国内镜像源（按速度排序）
        self.mirrors = [
            "https://pypi.tuna.tsinghua.edu.cn/simple",  # 清华大学
            "https://mirrors.aliyun.com/pypi/simple",     # 阿里云
            "https://pypi.doubanio.com/simple",           # 豆瓣
            "https://mirrors.huaweicloud.com/pypi/simple", # 华为云
        ]
        
        # 项目依赖
        self.dependencies = [
            {"name": "numpy", "import_name": "numpy", "version_attr": "__version__"},
            {"name": "Pillow", "import_name": "PIL", "version_attr": "__version__"},
            {"name": "opencv-python", "import_name": "cv2", "version_attr": "__version__"},
            {"name": "scipy", "import_name": "scipy", "version_attr": "__version__"},
            {"name": "PyQt5", "import_name": "PyQt5", "version_attr": "QtCore.PYQT_VERSION_STR"},
        ]
        
        # 安装状态
        self.installed = []
        self.failed = []
        self.current_mirror = 0
    
    def print_header(self):
        """打印标题"""
        print("=" * 70)
        print("🚀 套图系统 - 全自动依赖安装器")
        print("=" * 70)
        print("使用国内镜像源，完全自动化安装")
        print("无需任何手动操作，安装完成后自动运行项目")
        print("=" * 70)
    
    def check_package(self, dep: Dict) -> Tuple[bool, str]:
        """检查包是否已安装"""
        try:
            module = importlib.import_module(dep["import_name"])
            
            # 获取版本
            version_parts = dep["version_attr"].split(".")
            obj = module
            for part in version_parts:
                obj = getattr(obj, part)
            
            version = str(obj)
            return True, version
            
        except ImportError:
            return False, "未安装"
        except Exception as e:
            return False, f"检查失败: {e}"
    
    def get_best_mirror(self) -> str:
        """测试并选择最快的镜像源"""
        print("\n🔍 测试镜像源速度...")
        
        # 简单测试：尝试安装一个很小的包
        test_package = "pip"  # pip肯定已安装，只是测试连接
        
        for i, mirror in enumerate(self.mirrors):
            try:
                print(f"   测试 {mirror.split('//')[1].split('/')[0]}...", end=" ")
                
                cmd = [
                    sys.executable, "-m", "pip", "install",
                    "--index-url", mirror,
                    "--no-deps", "--dry-run",
                    test_package
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print("✅ 可用")
                    return mirror
                else:
                    print("❌ 失败")
                    
            except subprocess.TimeoutExpired:
                print("⏰ 超时")
            except Exception as e:
                print(f"❌ 错误: {e}")
        
        # 如果都失败，使用默认源
        print("\n⚠️  所有镜像源测试失败，使用默认源")
        return "https://pypi.org/simple"
    
    def install_package(self, dep: Dict, mirror: str) -> bool:
        """安装单个包"""
        package_name = dep["name"]
        
        print(f"\n📦 安装 {package_name}...")
        
        # 构建安装命令
        cmd = [
            sys.executable, "-m", "pip", "install",
            "--index-url", mirror,
            "--upgrade",
            "--no-warn-script-location",
            package_name
        ]
        
        try:
            # 执行安装
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # 实时显示输出
            output_lines = []
            for line in process.stdout:
                line = line.strip()
                if line:
                    output_lines.append(line)
                    # 只显示重要信息
                    if any(keyword in line.lower() for keyword in ['installing', 'successfully', 'error', 'failed', 'downloading']):
                        print(f"   {line}")
            
            # 等待进程完成
            process.wait()
            
            if process.returncode == 0:
                print(f"   ✅ {package_name} 安装成功")
                return True
            else:
                print(f"   ❌ {package_name} 安装失败")
                # 显示最后几行错误信息
                for line in output_lines[-3:]:
                    print(f"   错误: {line}")
                return False
                
        except Exception as e:
            print(f"   ❌ {package_name} 安装异常: {e}")
            return False
    
    def install_all(self):
        """安装所有依赖"""
        self.print_header()
        
        # 第一步：检查当前状态
        print("\n📊 第一步：检查当前安装状态")
        print("-" * 50)
        
        missing = []
        for dep in self.dependencies:
            is_installed, version = self.check_package(dep)
            if is_installed:
                print(f"✅ {dep['name']}: {version}")
                self.installed.append(dep['name'])
            else:
                print(f"❌ {dep['name']}: {version}")
                missing.append(dep)
        
        print(f"\n总结: {len(self.installed)} 个已安装, {len(missing)} 个需要安装")
        
        if not missing:
            print("\n🎉 所有依赖都已安装！")
            self.run_project()
            return
        
        # 第二步：选择最快的镜像源
        print("\n📊 第二步：选择最快的镜像源")
        print("-" * 50)
        
        mirror = self.get_best_mirror()
        print(f"\n使用镜像源: {mirror}")
        
        # 第三步：安装缺失的依赖
        print("\n📊 第三步：安装缺失的依赖")
        print("-" * 50)
        
        success_count = 0
        for dep in missing:
            if self.install_package(dep, mirror):
                success_count += 1
                self.installed.append(dep['name'])
            else:
                self.failed.append(dep['name'])
            
            # 短暂延迟，避免请求过快
            time.sleep(1)
        
        # 第四步：验证安装
        print("\n📊 第四步：验证安装结果")
        print("-" * 50)
        
        all_ok = True
        for dep in self.dependencies:
            is_installed, version = self.check_package(dep)
            if is_installed:
                print(f"✅ {dep['name']}: {version}")
            else:
                print(f"❌ {dep['name']}: 未安装")
                all_ok = False
        
        # 最终总结
        print("\n" + "=" * 70)
        print("📊 安装完成总结")
        print("=" * 70)
        print(f"总依赖数: {len(self.dependencies)}")
        print(f"安装成功: {success_count} 个")
        print(f"安装失败: {len(self.failed)} 个")
        
        if self.failed:
            print(f"\n❌ 失败的包: {', '.join(self.failed)}")
            print("\n请手动安装失败的包:")
            for pkg in self.failed:
                print(f"   pip install {pkg}")
        else:
            print("\n🎉 所有依赖安装成功！")
        
        if all_ok:
            print("\n🚀 所有依赖验证通过，准备运行项目...")
            self.run_project()
        else:
            print("\n⚠️  部分依赖安装失败，项目可能无法正常运行")
    
    def run_project(self):
        """运行项目"""
        print("\n" + "=" * 70)
        print("🚀 启动套图系统")
        print("=" * 70)
        
        try:
            # 获取项目根目录
            project_root = os.path.dirname(os.path.abspath(__file__))
            main_script = os.path.join(project_root, "main.py")
            
            if not os.path.exists(main_script):
                print(f"❌ 找不到主程序: {main_script}")
                return
            
            print("正在启动应用程序...")
            print("如果程序没有自动打开，请检查任务栏")
            
            # 启动项目
            subprocess.Popen([sys.executable, main_script])
            
            print("✅ 应用程序已启动")
            print("感谢使用套图系统！")
            
        except Exception as e:
            print(f"❌ 启动项目失败: {e}")
            print("请手动运行: python main.py")


def main():
    """主函数"""
    installer = AutoInstaller()
    
    try:
        installer.install_all()
    except KeyboardInterrupt:
        print("\n\n⚠️  安装被用户中断")
    except Exception as e:
        print(f"\n❌ 安装过程中发生错误: {e}")
        print("请检查网络连接或手动安装依赖")


if __name__ == "__main__":
    main()