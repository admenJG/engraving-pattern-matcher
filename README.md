# 电脑雕刻套图匹配系统

**Computer Engraving Pattern Matching System**

A Qt6-based desktop application for CNC engraving pattern matching and management. Designed for the 精雕 (JingDiao) CNC engraving workflow.

## Features

### Pattern Library Management
- Scan directories for engraving pattern images
- Automatic thumbnail generation and caching
- Pattern search by name
- Batch path management

### Image Processing
- Background removal (去背景)
- Edge detection (边缘检测)
- Brightness enhancement (标准提亮)
- Shadow/contrast adjustment (强阴影/弱阴影/高对比)
- Image straightening (摆正)
- Horizontal/vertical flip (水平/垂直翻转)
- Drag-to-rotate (拖拽调整角度)

### Pattern Matching
- Auto-match patterns to raw material images
- Real-time preview with thumbnails
- Right-click drag rotation for precise placement

### Export
- Export matched patterns for CNC processing
- Compatible with 精雕 (JingDiao) software format

## Technical Stack

- **Backend**: Go (HTTP server on localhost)
- **Frontend**: Web UI via Edge browser (app mode)
- **Database**: SQLite for pattern caching
- **Image Processing**: Qt6-based image algorithms
- **Platform**: Windows 10/11

## Architecture

`
main.go       - Application entry point
scanner.go    - Directory scanner for pattern files
server.go     - HTTP API server
desktop.go    - Edge browser integration
`

## Data Structure

`
data/
  config.json       - Scan paths configuration
  _lib_cache.db     - SQLite pattern cache
  _thumbs/          - Thumbnail cache
  tutugo.log        - Application logs
`

## Configuration

The data/config.json file stores scan paths:

`json
{
  "scan_paths": [
    "E:\\patterns",
    "D:\\engraving-library"
  ]
}
`

## Usage

1. Launch 电脑雕刻套图匹配系统.exe
2. The application starts an HTTP server and opens in Edge browser
3. Add scan paths to load pattern libraries
4. Open a raw material image
5. Select patterns from the library
6. Match and adjust patterns on the material
7. Export for CNC processing

## Pattern Categories

The system supports various engraving pattern categories:

- **Religious**: 佛像, 观音, 菩萨, 罗汉
- **Animals**: 龙, 凤, 虎, 鹰, 马, 鱼, 鸟, 麒麟, 貔貅
- **Plants**: 梅花, 兰花, 牡丹, 荷花, 竹子, 菊花
- **Symbols**: 福, 禄, 寿, 喜, 如意, 招财
- **Architecture**: 桥, 亭, 楼, 松
- **Patterns**: 回纹, 云纹, 水纹, 万花, 菱格
- **Calligraphy**: 书法, 印章, 诗词

## License

Proprietary - All rights reserved.