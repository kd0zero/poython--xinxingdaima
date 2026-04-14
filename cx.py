import tkinter as tk
import random
import math

# 主窗口
root = tk.Tk()
root.withdraw()

# 配置
WINDOWS = []          # 存储 (窗口, 标签) 元组
W = 220
H = 70
COUNT = 200          # 爱心弹窗数量
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

# 文案库
tips = [
    '多喝水哦~', '保持微笑呀', '每天都要元气满满', '记得吃水果',
    '保持好心情', '好好爱自己', '我想你了', '梦想成真',
    '期待下一次见面', '金榜题名', '顺顺利利', '早点休息',
    '愿所有烦恼都消失', '别熬夜', '今天过得开心嘛', '天冷了，多穿衣服',
    '记得想我~！', '永远爱你~', '每天都要开开心心哒~', '公主殿下~',
    '工作/学习再忙，也要记得休息', '快出来接收我的爱心光波！biu biu~',
    '拜托，你超酷的！', '今天也要全力以赴哦！', '风里雨里，我在这里等你',
    '你是我藏在云层里的月亮', '你笑起来真好看，像春天的花一样'
]

# 颜色库
colors = [
    '#FFB6C1', '#FFAACC', '#FFD1DC', '#F8C8DC', '#C9A0DC',
    '#9FE2BF', '#DFF2FD', '#FFE5B4', '#FFCCB6', '#FFABAB'
]


def make_win(x, y):
    """创建单个弹窗，返回 (窗口, 标签) 以便后续修改"""
    win = tk.Toplevel(root)
    win.geometry(f"{W}x{H}+{x}+{y}")
    win.title("❤️")
    win.resizable(0, 0)
    win.attributes('-topmost', True)
    bg_color = random.choice(colors)
    win.config(bg=bg_color)

    label = tk.Label(
        win, text=random.choice(tips), bg=bg_color,
        font=('微软雅黑', 13, 'bold'), wraplength=200
    )
    label.pack(expand=True, fill=tk.BOTH)

    return win, label


def heart_points():
    """生成爱心形状的坐标点（窗口左上角）"""
    pts = []
    cx = screen_w // 2 - W // 2
    cy = screen_h // 2 - H // 2
    scale = 28          # 爱心大小

    for i in range(COUNT):
        t = i / COUNT * math.pi * 2
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        px = int(cx + x * scale)
        py = int(cy - y * scale)
        pts.append((px, py))
    return pts


def draw_heart(idx=0):
    """逐步绘制爱心弹窗"""
    pts = heart_points()
    if idx < len(pts):
        x, y = pts[idx]
        win, label = make_win(x, y)
        WINDOWS.append((win, label))
        root.after(40, draw_heart, idx + 1)
    else:
        explode()


def generate_i_points(num_points):
    """生成字母 I 的点位（单列竖排），位置更靠左"""
    points = []
    x = screen_w // 8 - W // 2
    y_start = screen_h // 4
    y_end = screen_h * 3 // 4
    for i in range(num_points):
        y = y_start + (y_end - y_start) * i / (num_points - 1) if num_points > 1 else y_start
        points.append((x, int(y)))
    return points


def generate_heart_points_iu(num_points):
    """生成心形 ❤️ 的点位，居中"""
    points = []
    center_x = screen_w // 2
    center_y = screen_h // 2
    scale = 22
    for i in range(num_points):
        t = i / num_points * math.pi * 2
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        px = int(center_x + x * scale - W // 2)
        py = int(center_y - y * scale - H // 2)
        px = max(0, min(px, screen_w - W))
        py = max(0, min(py, screen_h - H))
        points.append((px, py))
    return points


def generate_u_points(num_points):
    """生成字母 U 的点位，开口缩小，位置更靠右"""
    points = []
    base_x = screen_w * 7 // 8
    gap = int(W * 1.2)          # 开口缩小
    left_x = base_x - gap
    right_x = base_x
    y_start = screen_h // 4
    y_end = screen_h * 3 // 4
    bottom_y = y_end

    per_side = max(1, num_points // 3)
    bottom_count = num_points - 2 * per_side
    if bottom_count < 1:
        bottom_count = 1
        per_side = (num_points - 1) // 2

    # 左竖线
    for i in range(per_side):
        y = y_start + (y_end - y_start) * i / (per_side - 1) if per_side > 1 else y_start
        points.append((left_x, int(y)))
    # 右竖线
    for i in range(per_side):
        y = y_start + (y_end - y_start) * i / (per_side - 1) if per_side > 1 else y_start
        points.append((right_x, int(y)))
    # 底部横线
    for i in range(bottom_count):
        x = left_x + (right_x - left_x) * i / (bottom_count - 1) if bottom_count > 1 else left_x
        points.append((int(x), bottom_y))
    return points


def rearrange_to_iu():
    """重新排列成 I❤️U 形状"""
    if not WINDOWS:
        return

    total = len(WINDOWS)
    i_count = min(15, total // 10)
    u_count = min(15, total // 10)
    heart_count = total - i_count - u_count
    if heart_count < 10:
        i_count = max(1, total // 3)
        u_count = max(1, total // 3)
        heart_count = total - i_count - u_count

    i_points = generate_i_points(i_count)
    heart_points_iu = generate_heart_points_iu(heart_count)
    u_points = generate_u_points(u_count)

    all_points = i_points + heart_points_iu + u_points
    while len(all_points) < total:
        all_points.append(all_points[-1])

    for idx, (win, _) in enumerate(WINDOWS):
        try:
            if win.winfo_exists():
                x, y = all_points[idx]
                win.geometry(f"{W}x{H}+{x}+{y}")
        except:
            continue


def change_to_iu():
    """将所有弹窗内容改为 I ❤️ U（带空格，间距匀称），标题也改为 I❤️U"""
    rearrange_to_iu()
    for win, label in WINDOWS:
        try:
            if win.winfo_exists():
                # 文字中间加空格，使三个字符间距匀称
                label.config(text="I ❤️U", font=('微软雅黑', 24, 'bold'), fg='red')
                win.config(bg='#FFEEEE')
                win.title("I❤️U")      # 窗口标题也改为 I❤️U
        except:
            continue


def explode():
    """炸开：随机移动所有弹窗，3秒后统一改为 I❤️U 并重新排列"""
    for win, _ in WINDOWS:
        try:
            if win.winfo_exists():
                rx = random.randint(0, screen_w - W)
                ry = random.randint(0, screen_h - H)
                win.geometry(f"{W}x{H}+{rx}+{ry}")
        except:
            continue
    root.after(3500, change_to_iu)


def print_heart():  #终端打印心形图案
    heart_ascii = """
      ❤️❤️❤️    ❤️❤️❤️
    ❤️❤️❤️❤️❤️❤️❤️❤️❤️
  ❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️
    ❤️❤️❤️❤️❤️❤️❤️❤️❤️
      ❤️❤️❤️❤️❤️❤️❤️
        ❤️❤️❤️❤️❤️
          ❤️❤️❤️
            ❤️
    """
    print(heart_ascii)


if __name__ == "__main__":
    print_heart()
    draw_heart()
    root.mainloop()
