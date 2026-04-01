"""
Generates haha.gif - a Nelson Muntz "HA HA!" animation.
Run this once before building the exe.
"""
import math
from PIL import Image, ImageDraw, ImageFont


def try_fonts(size):
    candidates = [
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/ariblk.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def draw_outlined_text(draw, xy, text, font, fill, outline, thickness=3):
    x, y = xy
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx * dx + dy * dy <= thickness * thickness:
                draw.text((x + dx, y + dy), text, font=font, fill=outline)
    draw.text((x, y), text, font=font, fill=fill)


def create_haha_gif(output_path="haha.gif"):
    W, H = 520, 380
    FRAMES = 16
    FRAME_MS = 80

    SKY = "#87CEEB"
    GRASS = "#5DBB63"
    SKIN = "#FFD700"
    SHIRT_RED = "#CC2200"
    HAT_BROWN = "#8B4513"
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    HA_YELLOW = "#FFE000"

    font_big = try_fonts(80)
    font_small = try_fonts(26)

    frames = []

    for i in range(FRAMES):
        t = i / FRAMES

        img = Image.new("RGB", (W, H), SKY)
        draw = ImageDraw.Draw(img)

        # Ground strip
        draw.rectangle([0, H - 80, W, H], fill=GRASS)

        # --- Nelson body ---
        cx, cy = W // 2 + 30, H // 2 + 40

        # Legs
        draw.rectangle([cx - 18, cy + 60, cx - 5, cy + 110], fill="#4444AA", outline=BLACK, width=1)
        draw.rectangle([cx + 5, cy + 60, cx + 18, cy + 110], fill="#4444AA", outline=BLACK, width=1)

        # Torso (red shirt)
        draw.rectangle([cx - 28, cy, cx + 28, cy + 65], fill=SHIRT_RED, outline=BLACK, width=2)

        # Neck
        draw.rectangle([cx - 8, cy - 12, cx + 8, cy + 5], fill=SKIN)

        # Head
        draw.ellipse([cx - 42, cy - 58, cx + 42, cy + 12], fill=SKIN, outline=BLACK, width=2)

        # Hat
        draw.rectangle([cx - 38, cy - 78, cx + 38, cy - 52], fill=HAT_BROWN, outline=BLACK, width=2)
        draw.rectangle([cx - 44, cy - 52, cx + 44, cy - 44], fill=HAT_BROWN, outline=BLACK, width=2)

        # Eyes - squinted laugh lines
        ey = cy - 32
        squint = 1 + int(2 * abs(math.sin(t * math.pi * 2)))
        draw.arc([cx - 34, ey - squint, cx - 14, ey + squint * 2], 180, 360, fill=BLACK, width=3)
        draw.arc([cx + 14, ey - squint, cx + 34, ey + squint * 2], 180, 360, fill=BLACK, width=3)

        # Nose
        draw.ellipse([cx - 5, cy - 15, cx + 5, cy - 5], fill="#FFBB55", outline=BLACK, width=1)

        # Laughing mouth - opens and closes
        mouth_h = int(12 + 8 * abs(math.sin(t * math.pi * 4)))
        mouth_y = cy - 2
        draw.ellipse([cx - 20, mouth_y, cx + 20, mouth_y + mouth_h], fill=BLACK)
        # Teeth
        if mouth_h > 14:
            draw.rectangle([cx - 14, mouth_y + 1, cx - 2, mouth_y + 7], fill=WHITE)
            draw.rectangle([cx + 2, mouth_y + 1, cx + 14, mouth_y + 7], fill=WHITE)

        # Pointing arm (left arm pointing toward viewer/left)
        arm_y_offset = int(4 * math.sin(t * math.pi * 4))
        arm_tip_x = cx - 100
        arm_tip_y = cy + 20 + arm_y_offset
        draw.line([cx - 28, cy + 20, arm_tip_x, arm_tip_y], fill=SKIN, width=10)
        # Hand / pointing finger
        draw.ellipse([arm_tip_x - 10, arm_tip_y - 10, arm_tip_x + 10, arm_tip_y + 10],
                     fill=SKIN, outline=BLACK, width=2)
        draw.rectangle([arm_tip_x - 4, arm_tip_y - 22, arm_tip_x + 4, arm_tip_y - 8],
                       fill=SKIN, outline=BLACK, width=1)

        # Right arm down
        draw.line([cx + 28, cy + 20, cx + 70, cy + 70], fill=SKIN, width=10)

        # --- HA HA! text - bounces slightly ---
        bounce = int(6 * abs(math.sin(t * math.pi * 2)))
        text_x = W // 2 - 140
        text_y = 18 - bounce

        draw_outlined_text(draw, (text_x, text_y), "HA HA!", font_big,
                           fill=HA_YELLOW, outline=BLACK, thickness=4)

        # Small subtitle
        sub_x = W // 2 - 60
        sub_y = 108
        draw_outlined_text(draw, (sub_x, sub_y), "- Nelson Muntz", font_small,
                           fill=WHITE, outline=BLACK, thickness=2)

        frames.append(img)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        loop=0,          # 0 = loop forever (window closes it after one pass)
        duration=FRAME_MS,
        optimize=False,
    )
    print(f"Saved {output_path}  ({FRAMES} frames @ {FRAME_MS}ms each = "
          f"{FRAMES * FRAME_MS / 1000:.1f}s per loop)")


if __name__ == "__main__":
    create_haha_gif()
