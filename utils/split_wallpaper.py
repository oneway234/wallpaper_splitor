from PIL import Image, ImageDraw
from screeninfo import get_monitors

# 常量定義
DASH_LENGTH, GAP_LENGTH, LINE_WIDTH = 10, 10, 3

def get_screen_info():
    return [{"width": s.width, "height": s.height, "x": s.x, "y": s.y} for s in get_monitors()]

def split_wallpaper(image, mode='default', screen_info=None, height_adjustment_ratio=0, width_adjustment_ratio=0):
    """
    根據不同模式分割壁紙圖片。
    
    :param image: PIL Image 對象
    :param mode: 分割模式，可以是 'default', 'A', 'B', 或 'C'
    :param screen_info: 屏幕信息列表
    :return: 分割後的圖片列表
    """
    if screen_info is None:
        screen_info = get_screen_info()

    if mode == 'default':
        # 預設模式：返回整張圖片
        return [image.copy()]
    elif mode == 'A':
        return draw_screen_divisions(image, screen_info, height_adjustment_ratio, is_horizontal=True)
    elif mode == 'B':
        return draw_screen_divisions(image, screen_info, width_adjustment_ratio, is_horizontal=False)
    # 其他模式的實現將在後續添加
    # 目前僅返回整張圖片
    return [image.copy()]

def draw_screen_divisions(image, screen_info, adjustment_ratio, is_horizontal):
    """
    在圖片上繪製屏幕分割線。
    
    :param image: PIL Image 對象
    :param screen_info: 屏幕信息列表
    :param adjustment_ratio: 調整方框的比例參數，範圍為-1到1，正值向下移動，負值向上移動
    :param is_horizontal: 是否為水平分割
    :return: 帶有分割線的圖片
    """
    image_copy = image.copy()
    draw = ImageDraw.Draw(image_copy)
    img_width, img_height = image_copy.size

    aspect_ratios = [screen['width'] / screen['height'] for screen in screen_info]
    total_aspect_ratio = sum(aspect_ratios)
    resize_ratio = (img_width if is_horizontal else img_height) / total_aspect_ratio

    current_pos = 0
    for aspect_ratio in aspect_ratios:
        if is_horizontal:
            screen_width = resize_ratio * aspect_ratio
            screen_height = screen_width / aspect_ratio
            adjustment = int((img_height - screen_height) * adjustment_ratio)
            top, bottom = max(0, adjustment), min(img_height - 1, int(screen_height) + adjustment)
            left, right = int(current_pos), int(current_pos + screen_width)
        else:
            screen_height = resize_ratio * aspect_ratio
            screen_width = screen_height * aspect_ratio
            adjustment = int((img_width - screen_width) * adjustment_ratio)
            left, right = max(0, adjustment), min(img_width - 1, int(screen_width) + adjustment)
            top, bottom = int(current_pos), int(current_pos + screen_height)

        draw_dashed_rectangle(draw, image_copy, left, top, right, bottom)
        current_pos += (screen_width if is_horizontal else screen_height)

    return image_copy

def draw_dashed_rectangle(draw, image, left, top, right, bottom):
    """
    在圖片上繪製帶有分割線的方框。
    
    :param draw: ImageDraw 對象
    :param image: PIL Image 對象
    :param left: 左邊界
    :param top: 上邊界
    :param right: 右邊界
    :param bottom: 下邊界
    """
    for side in ['top', 'bottom', 'left', 'right']:
        start = left if side in ['top', 'bottom'] else top
        end = right if side in ['top', 'bottom'] else bottom
        for pos in range(start, end, DASH_LENGTH + GAP_LENGTH):
            if side in ['top', 'bottom']:
                x, y = pos, top if side == 'top' else bottom
                line = [(x, y), (min(x + DASH_LENGTH, end), y)]
            else:
                x, y = left if side == 'left' else right, pos
                line = [(x, y), (x, min(y + DASH_LENGTH, end))]
            pixel_color = image.getpixel((x, y))
            contrast_color = tuple((c + 128) % 256 for c in pixel_color)
            draw.line(line, fill=contrast_color, width=LINE_WIDTH)

def save_split_images(images, base_filename):
    """
    保存分割後的圖片。
    
    :param images: 圖片列表（PIL Image 對象）
    :param base_filename: 基礎文件名
    """
    for i, img in enumerate(images):
        img.save(f"{base_filename}_{i+1}.png")
