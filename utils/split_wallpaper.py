from PIL import Image, ImageDraw
from screeninfo import get_monitors

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

def split_wallpaper(image, mode='default', screen_info=None):
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
        return draw_screen_divisions(image, screen_info)
    
    # 其他模式的實現將在後續添加
    # 目前僅返回整張圖片
    return [image.copy()]

def draw_screen_divisions(image, screen_info):
    """
    在圖片上繪製屏幕分割線。
    
    :param image: PIL Image 對象
    :param screen_info: 屏幕信息列表
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

        # 獲取圖片背景顏色
        background_color = image_copy.getpixel((int(current_x + screen_width / 2), int(screen_height / 2)))

        # 計算高對比顏色
        contrast_color = (
            (background_color[0] + 128) % 256,
            (background_color[1] + 128) % 256,
            (background_color[2] + 128) % 256
        )

        # 繪製虛線方框
        for y in range(0, int(screen_height), 10):
            draw.line([(current_x, y), (current_x + screen_width, y)], fill=contrast_color, width=3)
            y += 5
        for x in range(int(current_x), int(current_x + screen_width), 10):
            draw.line([(x, 0), (x, screen_height)], fill=contrast_color, width=3)
            x += 5

        current_x += screen_width

    return image_copy


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
