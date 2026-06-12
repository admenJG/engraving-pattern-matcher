# 电脑雕刻套图匹配系统 - AGENTS.md

## 项目信息
- **仓库**: [admenJG/engraving-pattern-matcher](https://github.com/admenJG/engraving-pattern-matcher)
- **本地路径**: `D:\软件\套图系统`
- **分支**: `main`
- **维护者**: admenJG (a19951641601@gmail.com)

## 技术栈
- **语言**: Python 3.12
- **Python 路径**: `D:\软件\开发环境工具依赖\Python\python.exe`
- **Pythonw 路径**: `D:\软件\开发环境工具依赖\Python\pythonw.exe`（无控制台窗口启动）
- **UI 框架**: PyQt5
- **图像处理**: OpenCV (cv2) + Pillow + NumPy
- **Git 路径**: `D:\软件\开发环境工具依赖\Git\cmd\git.exe`
- **Git 代理**: `socks5://127.0.0.1:7890`（GitHub 需要代理才能访问）

## 项目结构
```
main.py              # 主程序入口（~1900行，核心单文件应用）
start.bat            # 启动脚本（使用 pythonw.exe 无控制台）
requirements.txt     # 依赖列表
需求分析.md           # 需求文档
config/              # 配置模块
core/                # 核心逻辑（AppCore, HistoryManager, OverlayManager）
image_processing/    # 图像处理（背景移除, 检测, 加载, 变换）
ui/                  # UI 模块（主窗口, 画布, 工具栏, 面板）
utils/               # 工具函数
resources/           # 资源文件
tests/               # 测试
```

## 核心功能
1. **上传原材料图** → 从图案库选择图案叠加
2. **GrabCut 背景移除** → 自动识别前景/背景
3. **四角控制点拖拽缩放** → 等比缩放图案
4. **左键拖动** → 移动图案位置
5. **右键拖拽旋转** → 360° 自由旋转
6. **滚轮缩放** → 缩放选中图案
7. **镜像翻转** → 水平/垂直
8. **撤销/重做** → Ctrl+Z / Ctrl+Y / Ctrl+Shift+Z
9. **Delete 删除** / **Escape 取消选中**
10. **导出 PNG** → 合成后保存

## 运行方式
```bash
# 无控制台窗口启动
"D:\软件\开发环境工具依赖\Python\pythonw.exe" main.py

# 带控制台启动（调试用）
"D:\软件\开发环境工具依赖\Python\python.exe" main.py
```

## Git 操作指南
```bash
$env:PATH = "D:\软件\开发环境工具依赖\Git\cmd;$env:PATH"
cd "D:\软件\套图系统"
git config http.proxy socks5://127.0.0.1:7890
git config https.proxy socks5://127.0.0.1:7890
```

## GitHub 认证
- **方式**: Personal Access Token (ghp_...)
- **认证 API 示例**:
  ```python
  headers = {"Authorization": "token ghp_..."}
  ```
- **Git push 认证**: 代理走 `socks5://127.0.0.1:7890`，token 已配置在 git credential 中

## 开发注意事项
- `main.py` 是核心文件，所有主要功能都在此文件中
- `core/`、`ui/`、`image_processing/` 下是模块化骨架，尚未完全接入 main.py
- 修改 `main.py` 后用 `py_compile` 验证语法
- 启动时不能用 `python.exe`（会弹控制台黑窗），用 `pythonw.exe`
- `_draw_checkerboard()` 在 `_init_ui()` 中调用，此时部分 widget 还未创建，访问前需 `hasattr` 检查

## 主题色
- 背景色: `#1a1a2e`
- 主色调: `#533483` / `#7b2ff7`
- 强调色: `#e94560`
- 文字色: `#e6e6e6`