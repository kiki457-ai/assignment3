# -*- coding: utf-8 -*-
"""One-shot helper: replace the Chinese UI strings in index.html with English.
Run once during development; kept in the repo so the history shows the decision.
"""
import io, sys, re

PATH = "index.html"

# Order matters: longer keys first so 故事大王 is replaced before 故事.
REPLACEMENTS = [
    # ---------- page + titles ----------
    ("<title>Storypad - 任务小英雄</title>", "<title>Storypad - Whimsy Island</title>"),

    # ---------- place names (data, must match across all maps) ----------
    ("绿洲公园", "Oasis Park"),
    ("知识学院", "Knowledge Academy"),
    ("静谧街道", "Quiet Street"),
    ("暖阳社区", "Sunny Community"),

    # ---------- character names ----------
    ("故事大王", "Storyteller"),
    ("派对大王", "Party Host"),
    ("小厨师", "Little Chef"),
    ("探险家", "Explorer"),
    ("园艺师", "Gardener"),

    # ---------- NFC / placement toasts ----------
    ("已在游戏垫上", "is already on the island"),
    ("已离开游戏垫", "left the island"),
    ("已降落在", "landed at"),
    ("已收回", "is heading home"),
    ("放置失败", "could not be placed"),
    ("区域\"${zoneName}\"无效，${charName} 随机降落在${zone.name}",
     "Unknown location \"${zoneName}\" — ${charName} landed at ${zone.name}"),
    ("[NFC] 收到数据:", "[NFC] data received:"),
    ("[NFC] 轮询错误:", "[NFC] poll error:"),
    ("[NFC] 放置 ${data.name}，区域: ${zoneName}", "[NFC] placing ${data.name} at ${zoneName}"),
    ("NFC zoneName 无效: \"${zoneName}\"，已随机分配到: ${zone.name}",
     "[NFC] unknown zone \"${zoneName}\", assigned ${zone.name}"),
    ("'NFC 已连接'", "'NFC connected'"),
    ("'NFC 等待中'", "'NFC idle'"),
    ("'NFC 连接中...'", "'Looking for the NFC reader...'"),

    # ---------- story modal copy ----------
    ("📡 任务失联：当前区域没有英雄在场。请先把角色拖放到任务地点！",
     "📡 No hero on the island yet — drag a character onto a location first, then try again."),
    ("⚡ 正在接收求助信号，马上开始行动...",
     "⚡ Picking up the call for help..."),

    # ---------- role identities used to build the prompt ----------
    ("擅长照顾植物、种花弄草，小帮手", "cares for plants, flowers and gardens"),
    ("爱冒险、善于观察和发现新事物", "brave and curious, good at spotting new things"),
    ("对做饭和美食充满热情，喜欢动手实践", "loves cooking and making food with their own hands"),
    ("社交达人，善于组织活动、照顾朋友", "a natural host who organises things and looks after friends"),
    ("想象力丰富，擅长讲故事和编剧情", "imaginative, good at telling stories and inventing plots"),
    ("乐于助人的小朋友", "a helpful young friend"),
    ("小朋友", "the young hero"),

    # ---------- error copy ----------
    ("⚠️ 信号塔繁忙：Gemini 服务器当前负载过高，已自动重试但仍失败，请稍后再试（错误 503）",
     "⚠️ The story tower is busy — the Gemini server is overloaded right now. Please try again in a moment. (Error 503)"),
    ("⚠️ 绘图信号塔繁忙：服务器负载过高，已自动重试但仍失败，请稍后再试（错误 503）",
     "⚠️ The drawing tower is busy — the server is overloaded right now. Please try again in a moment. (Error 503)"),
    ("🔑 密钥失效：API 密钥无效或已过期，请在设置中重新输入",
     "🔑 That API key is invalid or expired. Open Settings and paste a new one."),
    ("⏱️ 次数耗尽：API 配额已用完，请稍后重试或更换密钥",
     "⏱️ The API quota is used up. Try again later or use a different key."),
    ("API 密钥无效或已过期，请在设置中重新输入", "API key is invalid or expired — open Settings and paste a new one."),
    ("API 配额已用完，请稍后重试或更换密钥", "API quota used up — try again later or use a different key."),
    ("API 返回了空内容", "the API returned an empty response"),
    ("未能生成图片数据", "no image data came back"),
    ("生成图片失败", "Image generation failed"),
    ("请求失败", "Request failed"),
    ("未知错误", "Unknown error"),
    ("🎨 正在绘制任务绘本，请稍候...", "🎨 Painting the mission picture, one moment..."),
    ("绘图魔法失败了", "The drawing magic failed"),
    ("▶️ 继续聆听", "▶️ Keep listening"),
    ("🔊 故事播放中...", "🔊 Playing the story..."),
    ("🔊 准备音频中...", "🔊 Preparing the audio..."),
    ("🎵 重新聆听 (异常)", "🎵 Listen again (error)"),
    ("🎵 重新聆听", "🎵 Listen again"),
    ("用温柔的语气说：", "Read this aloud in a warm, gentle voice: "),
    ("TTS失败", "TTS failed"),
    ("背景音乐可能由于浏览器自动播放限制无法启动",
     "Background music was blocked by the browser autoplay policy"),
    ("未能加载本地BGM，请确保音频文件与html在同一目录。",
     "Could not load the local background music — check the audio file sits next to index.html."),

    # ---------- AI prompt + system instruction ----------
    ('text: "你是一位擅长写儿童生活故事的作家，语言朴实自然，故事有对话有细节，像小学生真实会经历的事情。不要写成童话或散文，要有情节起伏。故事里所有角色的名字必须使用题目中给出的角色原名（如园艺师、探险家、小厨师、派对大王、故事大王），严禁替换成小明、小红、小华等任何其他名字。"',
     'text: "You write everyday stories for young children. Keep the language plain and natural, with dialogue and small concrete details, the kind of thing a primary school child could really experience. Do not write a fairy tale or an essay - there must be a problem and a turning point. You must refer to every character by the exact name you were given (for example Gardener, Explorer, Little Chef, Party Host, Storyteller) and never swap them for other names."'),

    # ---------- key section comments ----------
    ("/* 使用稳定的 CDN */", "/* Pinned CDN build of Three.js */"),
    ("/* 确保控制面板可以点击 */", "/* keep the control panel clickable */"),
    ("// 立即执行以避免提前点击报错", "// runs immediately so an early click cannot throw"),
    ("// ================= 1. 全局状态变量 =================", "// ===== 1. Global state ====="),
    ("// NFC特写时跳过轨道计算", "// skip orbit maths while the NFC close-up plays"),
    ("// 游戏垫目标旋转角度", "// target Y rotation of the island"),
    ("// 镜头动画状态机：'idle' | 'overview' | 'closeup'", "// camera state machine: 'idle' | 'overview' | 'closeup'"),
    ("// 当前阶段已过帧数", "// frames elapsed in the current phase"),
    ("// ================= 2. 音效函数 (固定音量) =================", "// ===== 2. Sound effects (fixed volume) ====="),
    ("// 固定音量", "// fixed volume"),
    ("// ================= 2.5 2D 粒子系统 (紫色流体拖尾 + 魔法星尘 + 爆裂) =================",
     "// ===== 2.5 2D particle system (trail + stardust + burst) ====="),
    ("// 无条件触发魔法粒子特效，无需在PlayMode中", "// particles fire anywhere, not just in play mode"),
    ("// 绘制拖尾", "// draw the cursor trail"),
    ("// 绘制全局漂浮星尘", "// draw the floating stardust"),
    ("// 绘制魔法十字星芒", "// draw the magic sparkles"),
    ("// 绘制火花粒子", "// draw the spark particles"),
    ("// 绘制震荡波", "// draw the shockwaves"),
    ("// ================= 3. Three.js 场景初始化 =================", "// ===== 3. Three.js scene setup ====="),
    ("// ================= 4. 建筑与地形生成 =================", "// ===== 4. Terrain and buildings ====="),
    ("// ================= 5. Voxel 角色生成器 =================", "// ===== 5. Voxel character builder ====="),
    ("// ================= 6. UI & NFC 逻辑 =================", "// ===== 6. UI and NFC logic ====="),
    ("// ── 触发预设镜头动画 ──────────────────────────────────────", "// ── Trigger the preset camera move ──"),
    ("// 直接在函数内部定义预设，避免重复声明问题，且确保THREE已加载",
     "// presets live inside the function so THREE is definitely loaded"),
    ("// 没有预设也给一个通用特写", "// no preset for this zone: fall back to a generic close-up"),
    ("// 第一阶段目标：区域俯瞰", "// phase 1: look down at the zone"),
    ("// 第二阶段目标：角色特写（基于角色世界坐标 + 偏移）",
     "// phase 2: close-up on the character (world position + offset)"),
    ("// 根据 zoneName 查找区域，找不到就随机选一个", "// look up the zone; fall back to a random one"),
    ("// 直接使用Arduino传来的zone，找不到才随机", "// trust the zone sent by Arduino, fall back to random"),
    ("// ✅ 预设镜头动画：先俯瞰区域，再推近特写角色",
     "// Preset camera move: overview of the zone, then push in on the character"),
    ("// ✅ 预设镜头动画", "// Preset camera move"),
    ("// ✅ 定格特写：同步 cameraDist，保持缩放可用",
     "// Lock the close-up: sync cameraDist so zoom still works"),
    ("// 锁定状态：相机停在当前位置，不更新", "// locked: the camera stays where it is"),
    ("// 相机环绕游戏垫（水平旋转 + 高度控制）", "// orbit the island (horizontal angle + height)"),
    ("// 首页游戏垫自动缓慢旋转", "// the island keeps turning slowly on the home screen"),
    ("// 游戏垫水平旋转（插值平滑），动画播放期间冻结",
     "// smooth the island rotation; freeze it while the camera move plays"),
    ("// ================= 7. 动画主循环 =================", "// ===== 7. Animation loop ====="),
    ("// ── 预设镜头状态机 ────────────────────────────────────", "// ── Camera state machine ──"),
    ("// 平滑推向俯瞰机位", "// ease towards the overview position"),
    ("// 平滑推向特写机位", "// ease towards the close-up position"),
    ("// ================= 8. 操控事件绑定 =================", "// ===== 8. Camera controls ====="),
    ("// 左右拖拽 = 旋转游戏垫", "// drag left/right = rotate the island"),
    ("// 上下拖拽 = 俯仰（往下滑仰角=低，往下滑俯角=高）", "// drag up/down = raise or lower the camera"),
    ("// 定格状态：滚轮直接推拉镜头距离", "// locked: the wheel pushes the camera in and out"),
    ("// ================= 9. 拖拽降落逻辑 =================", "// ===== 9. Drag and drop ====="),
    ("// ================= 10. UI & API 对接逻辑 =================", "// ===== 10. UI and API wiring ====="),
    ("// 相机高度", "// camera height"),
    ("// 相机距离", "// camera distance"),
    ("// 水平角度重置", "// reset the horizontal angle"),
    ("// 播放背景音乐并处理浏览器自动播放拦截",
     "// start the background music and survive the autoplay policy"),
    ("// ================= API 重试机制 =================", "// ===== API retry helper ====="),
    ("[API] 开始请求:", "[API] requesting:"),
    ("[API] 请求完成，状态码:", "[API] response status:"),
    ("// 如果是 503 错误且还有重试次数，继续重试", "// retry on 503 while attempts remain"),
    ("// 指数退避：1s, 2s, 4s", "// exponential backoff: 1s, 2s, 4s"),
    ("[API] 遇到 503 错误，第 ${attempt + 1} 次重试，${waitTime}ms 后重试...",
     "[API] got 503, retry ${attempt + 1} in ${waitTime}ms..."),
    ("// 如果是网络错误或 503，且还有重试次数", "// retry on network errors or 503 while attempts remain"),
    ("[API] 请求失败，${waitTime}ms 后第 ${attempt + 1} 次重试...",
     "[API] request failed, retry ${attempt + 1} in ${waitTime}ms..."),
    ("// 角色身份设定", "// Character personalities"),
    ("// 区域名称简化映射", "// Short location names for the prompt"),
    ("// 构建角色身份描述，使用简化后的区域名",
     "// Build the cast description using the short location names"),
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
    sys.stdout.write("chinese chars still present: %s\n" % ("".join(left) if left else "none"))


main()
