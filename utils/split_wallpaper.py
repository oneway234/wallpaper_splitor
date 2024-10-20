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
    在圖片上繪製屏幕分割線。
    
    :param image: PIL Image 對象
    :param screen_info: 屏幕信息列表
    :param height_adjustment_ratio: 調整方框高度的比例參數，範圍為-1到1，正值向下移動，負值向上移動
    :return: 帶有分割線的圖片
    """
    image_copy = image.copy()
    draw = ImageDraw.Draw(image_copy)

    img_width, img_height = image_copy.size

    aspect_ratio_list = [screen['width'] / screen['height'] for screen in screen_info]
    total_aspect_ratio = sum(aspect_ratio_list)
    resize_ratio = img_width / total_aspect_ratio

    current_x = 0
    for i, aspect_ratio in enumerate(aspect_ratio_list):
        screen_width = resize_ratio * aspect_ratio
        screen_height = screen_width / aspect_ratio

        height_adjustment = int((img_height - screen_height) * height_adjustment_ratio)
        adjusted_top = max(0, height_adjustment)
        adjusted_bottom = min(img_height - 1, int(screen_height) + height_adjustment)

        for side in ['top', 'bottom', 'left', 'right']:
            if side in ['top', 'bottom']:
                start = int(current_x)
                end = int(current_x + screen_width)
                y = adjusted_top if side == 'top' else adjusted_bottom
                for x in range(start, end, DASH_LENGTH + GAP_LENGTH):
                    pixel_color = image_copy.getpixel((x, y))
                    contrast_color = tuple((c + 128) % 256 for c in pixel_color)
                    draw.line([(x, y), (min(x + DASH_LENGTH, end), y)], fill=contrast_color, width=LINE_WIDTH)
            else:
                start = adjusted_top
                end = adjusted_bottom
                x = int(current_x) if side == 'left' else int(current_x + screen_width) - 1
                for y in range(start, end, DASH_LENGTH + GAP_LENGTH):
                    pixel_color = image_copy.getpixel((x, y))
                    contrast_color = tuple((c + 128) % 256 for c in pixel_color)
                    draw.line([(x, y), (x, min(y + DASH_LENGTH, end))], fill=contrast_color, width=LINE_WIDTH)

        current_x += screen_width

    return image_copy

def draw_vertical_screen_divisions(image, screen_info, width_adjustment_ratio=0):
    """
    在圖片上繪製垂直屏幕分割線。
    
    :param image: PIL Image 對象
    :param screen_info: 屏幕信息列表
    :param width_adjustment_ratio: 調整方框寬度的比例參數，範圍為-1到1，正值向右移動，負值向左移動
    :return: 帶有分割線的圖片
    """
    image_copy = image.copy()
    draw = ImageDraw.Draw(image_copy)

    img_width, img_height = image_copy.size

    aspect_ratio_list = [screen['width'] / screen['height'] for screen in screen_info]
    total_aspect_ratio = sum(aspect_ratio_list)
    resize_ratio = img_height / total_aspect_ratio

    current_y = 0
    for i, aspect_ratio in enumerate(aspect_ratio_list):
        screen_height = resize_ratio * aspect_ratio
        screen_width = screen_height * aspect_ratio

        width_adjustment = int((img_width - screen_width) * width_adjustment_ratio)
        adjusted_left = max(0, width_adjustment)
        adjusted_right = min(img_width - 1, int(screen_width) + width_adjustment)

        for side in ['top', 'bottom', 'left', 'right']:
            if side in ['left', 'right']:
                start = int(current_y)
                end = int(current_y + screen_height)
                x = adjusted_left if side == 'left' else adjusted_right
                for y in range(start, end, DASH_LENGTH + GAP_LENGTH):
                    pixel_color = image_copy.getpixel((x, y))
                    contrast_color = tuple((c + 128) % 256 for c in pixel_color)
                    draw.line([(x, y), (x, min(y + DASH_LENGTH, end))], fill=contrast_color, width=LINE_WIDTH)
            else:
                start = adjusted_left
                end = adjusted_right
                y = int(current_y) if side == 'top' else int(current_y + screen_height) - 1
                for x in range(start, end, DASH_LENGTH + GAP_LENGTH):
                    pixel_color = image_copy.getpixel((x, y))
                    contrast_color = tuple((c + 128) % 256 for c in pixel_color)
                    draw.line([(x, y), (min(x + DASH_LENGTH, end), y)], fill=contrast_color, width=LINE_WIDTH)

        current_y += screen_height

    return image_copy

def save_split_images(images, base_filename):
    """
    保存分割後的圖片。
    
    :param images: 圖片列表（PIL Image 對象）
    :param base_filename: 基礎文件名
    """
    for i, img in enumerate(images):
        filename = f"{base_filename}_{i+1}.png"
        img.save(filename)
