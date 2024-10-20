from PIL import Image, ImageDraw
from screeninfo import get_monitors

# Constants definition
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
    Split the wallpaper image according to the mode.
    """
    if screen_info is None:
        screen_info = get_screen_info()

    if mode == 'default':
        return [image.copy()], []
    elif mode == 'A':
        return draw_horizontal_screen_divisions(image, screen_info, height_adjustment_ratio)
    elif mode == 'B':
        return draw_vertical_screen_divisions(image, screen_info, width_adjustment_ratio)
    return [image.copy()], []

def draw_horizontal_screen_divisions(image, screen_info, height_adjustment_ratio=0):
    """
    Draw horizontal screen divisions on the image and return a list of sub-images.
    
    :param image: PIL Image object
    :param screen_info: List of screen information
    :param height_adjustment_ratio: Ratio parameter to adjust the frame height, range from -1 to 1, positive values move down, negative values move up
    :return: Image with division lines and list of sub-images
    """
    image_copy = image.copy()
    draw = ImageDraw.Draw(image_copy)

    img_width, img_height = image_copy.size

    aspect_ratio_list = [screen['width'] / screen['height'] for screen in screen_info]
    total_aspect_ratio = sum(aspect_ratio_list)
    resize_ratio = img_width / total_aspect_ratio

    current_x = 0
    sub_images = []

    for i, aspect_ratio in enumerate(aspect_ratio_list):
        screen_width = resize_ratio * aspect_ratio
        screen_height = screen_width / aspect_ratio

        height_adjustment = int((img_height - screen_height) * height_adjustment_ratio)
        adjusted_top = max(0, height_adjustment)
        adjusted_bottom = min(img_height - 1, int(screen_height) + height_adjustment)

        # Cut sub-image
        sub_image = image.crop((int(current_x), adjusted_top, int(current_x + screen_width), adjusted_bottom))
        sub_images.append(sub_image)

        # Draw division lines
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

    return image_copy, sub_images

def draw_vertical_screen_divisions(image, screen_info, width_adjustment_ratio=0):
    """
    Draw vertical screen divisions on the image and return a list of sub-images.
    
    :param image: PIL Image object
    :param screen_info: List of screen information
    :param width_adjustment_ratio: Ratio parameter to adjust the frame width, range from -1 to 1, positive values move right, negative values move left
    :return: Image with division lines and list of sub-images
    """
    image_copy = image.copy()
    draw = ImageDraw.Draw(image_copy)

    img_width, img_height = image_copy.size

    aspect_ratio_list = [screen['width'] / screen['height'] for screen in screen_info]
    total_aspect_ratio = sum(aspect_ratio_list)
    resize_ratio = img_height / total_aspect_ratio

    current_y = 0
    sub_images = []

    for i, aspect_ratio in enumerate(aspect_ratio_list):
        screen_height = resize_ratio * aspect_ratio
        screen_width = screen_height * aspect_ratio

        width_adjustment = int((img_width - screen_width) * width_adjustment_ratio)
        adjusted_left = max(0, width_adjustment)
        adjusted_right = min(img_width - 1, int(screen_width) + width_adjustment)

        # Cut sub-image
        sub_image = image.crop((adjusted_left, int(current_y), adjusted_right, int(current_y + screen_height)))
        sub_images.append(sub_image)

        # Draw division lines
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

    return image_copy, sub_images

def save_split_images(images, base_filename):
    """
    Save the split images.
    
    :param images: List of images (PIL Image objects)
    :param base_filename: Base filename
    """
    for i, img in enumerate(images):
        filename = f"{base_filename}_{i+1}.png"
        img.save(filename)
