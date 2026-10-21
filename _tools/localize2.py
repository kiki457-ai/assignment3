# -*- coding: utf-8 -*-
"""Second pass: clear the remaining Chinese comments left after localize.py."""
import io, sys, re

PATH = "index.html"

REPLACEMENTS = [
    ("<!-- 使用稳定的 CDN -->", "<!-- Pinned CDN build of Three.js -->"),
    ("高级极简 UI 设计 (暗色调 Glassmorphism)", "Minimal glassmorphism UI, dark theme"),
    ("<!-- 3D 渲染层 -->", "<!-- 3D render layer -->"),
    ("// 恢复为你本地的 mp3 文件，并去掉了网络替代逻辑",
     "// Points at a local mp3 again; the network fallback was removed"),
    ("// 相机水平角度", "// horizontal camera angle"),
    ("// ── 预设镜头动画系统 ──────────────────────────────────────",
     "// ── Preset camera system ──"),
    ("// 俯瞰阶段帧数（~0.83s @60fps）", "// overview frames (~0.83s at 60fps)"),
    ("// 特写阶段帧数（~1.5s @60fps）", "// close-up frames (~1.5s at 60fps)"),
    ("// 无条件触发魔法粒子特效，无需在PlayMode下",
     "// particles fire anywhere, not only in play mode"),
    ("// 绘制魔法十字星星", "// draw the magic sparkles"),
    ("// 调试日志", "// debug log"),
    ("// 上下拖拽 = 俯仰（往上滑仰视=低，往下滑俯视=高）",
     "// drag up/down = raise or lower the camera"),
    ("// 往上滑仰视=低，往下滑俯视=高", "// drag up to raise, down to lower"),
    ("[API] Request failed，${waitTime}ms 后第 ${attempt + 1} 次重试...",
     "[API] request failed, retry ${attempt + 1} in ${waitTime}ms..."),
    ("if (errorMsg.includes('503') || errorMsg.includes('高需求') || errorMsg.includes('high demand')) {",
     "if (errorMsg.includes('503') || errorMsg.includes('high demand')) {"),
]


def main():
    with io.open(PATH, "r", encoding="utf-8") as f:
        src = f.read()

    missing = []
    for old, new in REPLACEMENTS:
        if old in src:
            src = src.replace(old, new)
        else:
            missing.append(old)

    with io.open(PATH, "w", encoding="utf-8") as f:
        f.write(src)

    left = sorted(set(re.findall(r"[一-鿿]", src)))
    sys.stdout.write("replaced=%d not_found=%d\n" % (len(REPLACEMENTS) - len(missing), len(missing)))
    for m in missing:
        sys.stdout.write("  NOT FOUND: %s\n" % m[:70])
    sys.stdout.write("chinese remaining: %s\n" % ("".join(left) if left else "none"))


main()
