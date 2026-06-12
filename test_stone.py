"""调试料子检测"""
import sys
import os
sys.path.insert(0, '.')
import cv2
import numpy as np

file_path = r"C:\Users\Administrator\Desktop\微信图片_20260526091614_50_17.jpg"
bgr = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
orig_h, orig_w = bgr.shape[:2]
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

scale = 800.0 / max(orig_h, orig_w)
gray = cv2.resize(gray, None, fx=scale, fy=scale)
h, w = gray.shape[:2]
blur = cv2.GaussianBlur(gray, (5, 5), 0)

edges = cv2.Canny(blur, 30, 100)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
edges = cv2.dilate(edges, kernel, iterations=2)
edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)

bm = max(5, min(h, w) // 20)
print(f"图片: {w}x{h}, 边缘遮罩: {bm}px")

border_mask = np.zeros_like(edges)
border_mask[bm:h-bm, bm:w-bm] = 255
edges = cv2.bitwise_and(edges, border_mask)

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_area = w * h
print(f"\n共 {len(contours)} 个轮廓:")

for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    x, y, bw, bh = cv2.boundingRect(cnt)
    ratio = min(bw, bh) / max(bw, bh) if max(bw, bh) > 0 else 0
    
    touches_border = x <= bm or y <= bm or x + bw >= w - bm or y + bh >= h - bm
    too_small = area < 0.05 * img_area
    too_big = area > 0.70 * img_area
    bad_ratio = ratio < 0.15
    
    status = []
    if too_small: status.append("太小")
    if too_big: status.append("太大")
    if touches_border: status.append("碰边")
    if bad_ratio: status.append("比例差")
    if not status: status.append("✅通过!")
    
    print(f"  #{i}: pos=({x},{y}) size={bw}x{bh} area={area:.0f}({area/img_area*100:.1f}%) ratio={ratio:.2f} | {', '.join(status)}")

# 也测试阈值
print("\n--- 自适应阈值 ---")
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
thresh[:bm, :] = 0
thresh[h-bm:, :] = 0
thresh[:, :bm] = 0
thresh[:, w-bm:] = 0
thresh = cv2.dilate(thresh, kernel, iterations=3)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"共 {len(contours)} 个轮廓:")

for i, cnt in enumerate(sorted(contours, key=cv2.contourArea, reverse=True)[:15]):
    area = cv2.contourArea(cnt)
    x, y, bw, bh = cv2.boundingRect(cnt)
    ratio = min(bw, bh) / max(bw, bh) if max(bw, bh) > 0 else 0
    
    touches_border = x <= bm or y <= bm or x + bw >= w - bm or y + bh >= h - bm
    too_small = area < 0.05 * img_area
    too_big = area > 0.70 * img_area
    bad_ratio = ratio < 0.15
    
    status = []
    if too_small: status.append("太小")
    if too_big: status.append("太大")
    if touches_border: status.append("碰边")
    if bad_ratio: status.append("比例差")
    if not status: status.append("✅通过!")
    
    print(f"  #{i}: pos=({x},{y}) size={bw}x{bh} area={area:.0f}({area/img_area*100:.1f}%) ratio={ratio:.2f} | {', '.join(status)}")
