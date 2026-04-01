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


def draw_outlined_text(draw, xy, text, font, fill, outline, thickness=5):
    x, y = xy
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx * dx + dy * dy <= thickness * thickness:
                draw.text((x + dx, y + dy), text, font=font, fill=outline)
    draw.text((x, y), text, font=font, fill=fill)


def draw_nelson(draw, cx, cy_head, R, t, skin, shirt, hat_col, black, white):
    """Draw a Nelson Muntz character. cy_head is the centre of the head."""

    GROUND_Y = cy_head + R + 230

    # --- Sky gradient (two rects) ---
    # (caller already filled background)

    # --- Legs ---
    torso_bot = cy_head + R + 145
    leg_top   = torso_bot
    lx = cx - 30
    rx = cx + 8
    draw.rectangle([lx,      leg_top, lx + 28, GROUND_Y], fill="#3333AA", outline=black, width=2)
    draw.rectangle([rx,      leg_top, rx + 28, GROUND_Y], fill="#3333AA", outline=black, width=2)
    # Shoes
    draw.ellipse([lx - 6, GROUND_Y - 12, lx + 34, GROUND_Y + 10], fill=black)
    draw.ellipse([rx - 6, GROUND_Y - 12, rx + 34, GROUND_Y + 10], fill=black)

    # --- Torso ---
    torso_top = cy_head + R + 18
    draw.rectangle([cx - 48, torso_top, cx + 48, torso_bot], fill=shirt, outline=black, width=2)
    # Collar detail
    draw.polygon([
        (cx - 10, torso_top), (cx, torso_top + 18), (cx + 10, torso_top)
    ], fill=white, outline=black)

    # --- Neck ---
    draw.rectangle([cx - 14, cy_head + R - 5, cx + 14, torso_top + 2], fill=skin)

    # --- Head ---
    draw.ellipse([cx - R, cy_head - R, cx + R, cy_head + R],
                 fill=skin, outline=black, width=3)

    # --- Hat (floppy peaked cap) ---
    hat_peak_y = cy_head - R - 55
    brim_y     = cy_head - R + 5
    # Crown (trapezoid — wider at brim, narrower at top)
    draw.polygon([
        (cx - 25, hat_peak_y),
        (cx + 20, hat_peak_y - 8),
        (cx + 52, brim_y),
        (cx - 52, brim_y),
    ], fill=hat_col, outline=black)
    # Brim
    draw.ellipse([cx - 60, brim_y - 8, cx + 60, brim_y + 10], fill=hat_col, outline=black)

    # --- Eyes: happy squint arcs ---
    ey = cy_head - 14
    squint = 2 + int(4 * abs(math.sin(t * math.pi * 2)))
    draw.arc([cx - 40, ey - squint, cx - 10, ey + squint * 2 + 4], 190, 350, fill=black, width=4)
    draw.arc([cx + 10, ey - squint, cx + 40, ey + squint * 2 + 4], 190, 350, fill=black, width=4)
    # Eyebrow raised in mock
    draw.arc([cx - 42, ey - squint - 12, cx - 8,  ey - squint + 2], 200, 340, fill=black, width=3)
    draw.arc([cx + 8,  ey - squint - 12, cx + 42, ey - squint + 2], 200, 340, fill=black, width=3)

    # --- Nose ---
    draw.ellipse([cx - 7, cy_head + 4, cx + 7, cy_head + 18],
                 fill="#FFBB44", outline=black, width=1)

    # --- Mouth: laughing wide open, height pulses ---
    mouth_y  = cy_head + 20
    mouth_h  = int(20 + 14 * abs(math.sin(t * math.pi * 4)))
    mouth_w  = 36
    draw.ellipse([cx - mouth_w, mouth_y,
                  cx + mouth_w, mouth_y + mouth_h], fill=black)
    # Teeth (top row)
    if mouth_h > 22:
        tooth_y = mouth_y + 3
        for tx in range(cx - mouth_w + 4, cx + mouth_w - 8, 14):
            draw.rectangle([tx, tooth_y, tx + 11, tooth_y + 10], fill=white)
    # Tongue
    if mouth_h > 28:
        draw.ellipse([cx - 16, mouth_y + mouth_h - 16,
                      cx + 16, mouth_y + mouth_h + 2], fill="#CC3333")

    # --- Pointing arm (left, toward viewer) ---
    arm_bob  = int(8 * math.sin(t * math.pi * 4))
    shoulder = (cx - 48, torso_top + 14)
    elbow    = (cx - 95, torso_top + 40 + arm_bob)
    tip      = (cx - 145, torso_top + 20 + arm_bob)
    draw.line([shoulder, elbow, tip], fill=skin, width=16, joint="curve")
    # Fist + pointing finger
    draw.ellipse([tip[0] - 16, tip[1] - 16, tip[0] + 16, tip[1] + 16],
                 fill=skin, outline=black, width=2)
    draw.rounded_rectangle([tip[0] - 8, tip[1] - 34, tip[0] + 8, tip[1] - 10],
                            radius=6, fill=skin, outline=black, width=2)

    # --- Relaxed right arm slightly raised ---
    r_shoulder = (cx + 48, torso_top + 14)
    r_elbow    = (cx + 88, torso_top + 55 - arm_bob // 2)
    draw.line([r_shoulder, r_elbow], fill=skin, width=16)
    draw.ellipse([r_elbow[0] - 14, r_elbow[1] - 14,
                  r_elbow[0] + 14, r_elbow[1] + 14], fill=skin, outline=black, width=2)

    # --- Laugh lines radiating from head ---
    line_count = 8
    base_len   = 18 + int(10 * abs(math.sin(t * math.pi * 2)))
    for k in range(line_count):
        angle = (k / line_count) * 2 * math.pi + t * math.pi * 0.5
        # Only draw lines in upper arc so they don't overlap body
        if math.sin(angle) > 0.1:
            continue
        x0 = cx + int((R + 8)  * math.cos(angle))
        y0 = cy_head + int((R + 8)  * math.sin(angle))
        x1 = cx + int((R + 8 + base_len) * math.cos(angle))
        y1 = cy_head + int((R + 8 + base_len) * math.sin(angle))
        draw.line([x0, y0, x1, y1], fill=black, width=3)


def create_haha_gif(output_path="haha.gif"):
    W, H     = 900, 640
    FRAMES   = 24
    FRAME_MS = 65

    SKY   = "#6BB8E8"
    GRASS = "#4A9B3A"
    GRASS_DARK = "#3A7A2A"
    SKIN  = "#FFD700"
    SHIRT = "#DD1111"
    HAT   = "#7B3F00"
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    HA_YELLOW = "#FFE500"
    HA_SHADOW = "#B8860B"

    font_ha   = try_fonts(130)
    font_sub  = try_fonts(36)

    frames = []
    cx, cy_head = 580, 300
    R = 80

    for i in range(FRAMES):
        t = i / FRAMES

        img  = Image.new("RGB", (W, H), SKY)
        draw = ImageDraw.Draw(img)

        # Sky: simple two-tone
        draw.rectangle([0, H // 2, W, H], fill="#87CEEB")

        # Grass with a darker strip at the edge
        ground_y = cy_head + R + 230
        draw.rectangle([0, ground_y - 4, W, H], fill=GRASS)
        draw.rectangle([0, ground_y - 4, W, ground_y + 12], fill=GRASS_DARK)

        # Some simple clouds
        for cx_c, cy_c, cr in [(160, 90, 45), (310, 60, 35), (720, 100, 50), (820, 70, 30)]:
            draw.ellipse([cx_c - cr, cy_c - cr // 2,
                          cx_c + cr, cy_c + cr // 2], fill=WHITE)
            draw.ellipse([cx_c - cr * 2 // 3, cy_c - cr,
                          cx_c + cr * 2 // 3, cy_c], fill=WHITE)

        # Nelson
        draw_nelson(draw, cx, cy_head, R, t, SKIN, SHIRT, HAT, BLACK, WHITE)

        # ---- "HA HA!" text ----
        bounce    = int(10 * abs(math.sin(t * math.pi * 2)))
        scale_pop = 1.0 + 0.04 * abs(math.sin(t * math.pi * 4))  # subtle pulse

        # Shadow layer
        text      = "HA HA!"
        tx        = 28
        ty        = 22 - bounce

        draw_outlined_text(draw, (tx + 5, ty + 6), text, font_ha,
                           fill=HA_SHADOW, outline=BLACK, thickness=2)
        # Main text
        draw_outlined_text(draw, (tx, ty), text, font_ha,
                           fill=HA_YELLOW, outline=BLACK, thickness=6)

        # Subtitle
        draw_outlined_text(draw, (42, ty + 150), "— Nelson Muntz", font_sub,
                           fill=WHITE, outline=BLACK, thickness=3)

        frames.append(img)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=FRAME_MS,
        optimize=False,
    )
    print(f"Saved {output_path}  ({W}x{H}, {FRAMES} frames @ {FRAME_MS}ms = "
          f"{FRAMES * FRAME_MS / 1000:.2f}s per loop)")


if __name__ == "__main__":
    create_haha_gif()
