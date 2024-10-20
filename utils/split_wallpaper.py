from PIL import Image, ImageDraw
from screeninfo import get_monitors

# 常量定義
DASH_LENGTH = 10
GAP_LENGTH = 10
LINE_WIDTH = 3

def get_screen_info():
    screens = get_monitors()
    screen_info = []
    for screen in screens:
        screen_info.append({
            "width": screen.width,
            "height": screen.height,
            "x": screen.x,
            "y": screen.y
        })
    return screen_info

def split_wallpaper(image, mode='default', screen_info=None, height_adjustment_ratio=0, width_adjustment_ratio=0):
    """
    根據模式分割壁紙圖片。
    """
    if screen_info is None:
        screen_info = get_screen_info()

    if mode == 'default':
        return [image.copy()]
    elif mode == 'A':
        return draw_horizontal_screen_divisions(image, screen_info, height_adjustment_ratio)
    elif mode == 'B':
        return draw_vertical_screen_divisions(image, screen_info, width_adjustment_ratio)
    return [image.copy()]

def draw_horizontal_screen_divisions(image, screen_info, height_adjustment_ratio=0):
    """
    在圖片上繪製水平屏幕分割線。
    
    :param image: PIL Image 對象
    :param screen_info: 屏幕信息列表
    :param height_adjustment_ratio: 調整方框高度的比例參數，範圍為-1到1
    :return: 帶有分割線的圖片
    """
    return draw_screen_divisions(image, screen_info, height_adjustment_ratio, is_horizontal=True)

def draw_vertical_screen_divisions(image, screen_info, width_adjustment_ratio=0):
    """
    在圖片上繪製垂直屏幕分割線。
    
    :param image: PIL Image 對象
    :param screen_info: 屏幕信息列表
    :param width_adjustment_ratio: 調整方框寬度的比例參數，範圍為-1到1
    :return: 帶有分割線的圖片
    """
    return draw_screen_divisions(image, screen_info, width_adjustment_ratio, is_horizontal=False)

def draw_screen_divisions(image, screen_info, adjustment_ratio, is_horizontal):
    """
    在圖片上繪製屏幕分割線。
    
    :param image: PIL Image 對象
    :param screen_info: 屏幕信息列表
    :param adjustment_ratio: 調整方框的比例參數，範圍為-1到1
    :param is_horizontal: 是否為水平分割
    :return: 帶有分割線的圖片
    """
    image_copy = image.copy()
    draw = ImageDraw.Draw(image_copy)
    img_width, img_height = image_copy.size

    aspect_ratio_list = [screen['width'] / screen['height'] for screen in screen_info]
    total_aspect_ratio = sum(aspect_ratio_list)
    resize_ratio = img_width / total_aspect_ratio if is_horizontal else img_height / total_aspect_ratio

    current_pos = 0
    for aspect_ratio in aspect_ratio_list:
        if is_horizontal:
            screen_width = resize_ratio * aspect_ratio
            screen_height = screen_width / aspect_ratio
            adjustment = int((img_height - screen_height) * adjustment_ratio)
            adjusted_start = max(0, adjustment)
            adjusted_end = min(img_height - 1, int(screen_height) + adjustment)
        else:
            screen_height = resize_ratio * aspect_ratio
            screen_width = screen_height * aspect_ratio
            adjustment = int((img_width - screen_width) * adjustment_ratio)
            adjusted_start = max(0, adjustment)
            adjusted_end = min(img_width - 1, int(screen_width) + adjustment)

        draw_dashed_rectangle(draw, image_copy, current_pos, adjusted_start, 
                              current_pos + (screen_width if is_horizontal else screen_height), 
                              adjusted_end, is_horizontal)

        current_pos += screen_width if is_horizontal else screen_height

    return image_copy

def draw_dashed_rectangle(draw, image, x1, y1, x2, y2, is_horizontal):
    """繪製虛線矩形"""
    sides = [(x1, y1, x2, y1), (x1, y2, x2, y2), (x1, y1, x1, y2), (x2, y1, x2, y2)]
    for start_x, start_y, end_x, end_y in sides:
        draw_dashed_line(draw, image, start_x, start_y, end_x, end_y, is_horizontal)

def draw_dashed_line(draw, image, x1, y1, x2, y2, is_horizontal):
    """繪製虛線"""
    length = x2 - x1 if is_horizontal else y2 - y1
    for i in range(0, length, DASH_LENGTH + GAP_LENGTH):
        end = min(i + DASH_LENGTH, length)
        if is_horizontal:
            line_start = (x1 + i, y1)
            line_end = (x1 + end, y1)
        else:
            line_start = (x1, y1 + i)
            line_end = (x1, y1 + end)
        pixel_color = image.getpixel(line_start)
        contrast_color = tuple((c + 128) % 256 for c in pixel_color)
        draw.line([line_start, line_end], fill=contrast_color, width=LINE_WIDTH)

def save_split_images(images, base_filename):
    """
    保存分割後的圖片。
    
    :param images: 圖片列表（PIL Image 對象）
    :param base_filename: 基礎文件名
    """
    for i, img in enumerate(images):
        filename = f"{base_filename}_{i+1}.png"
        img.save(filename)
