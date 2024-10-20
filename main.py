import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from utils.split_wallpaper import split_wallpaper, save_split_images, get_screen_info

class ImageViewerApp:
    def __init__(self, master):
        self.master = master
        master.title("圖片預覽器")
        master.geometry("800x600")
        master.resizable(True, True)

        # 獲取屏幕信息
        self.screen_info = get_screen_info()
        
        # 創建圖片顯示區域
        self.image_label = tk.Label(master)
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # 創建底部按鈕框架
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side=tk.BOTTOM, pady=10)

        # 創建載入按鈕
        self.load_button = tk.Button(self.button_frame, text="載入圖片", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=5)

        # 創建保存按鈕
        self.save_button = tk.Button(self.button_frame, text="保存圖片", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # 創建 A, B, C 按鈕
        self.button_a = tk.Button(self.button_frame, text="水平切割", command=self.button_a_action)
        self.button_a.pack(side=tk.LEFT, padx=5)

        self.button_b = tk.Button(self.button_frame, text="B", command=self.button_b_action)
        self.button_b.pack(side=tk.LEFT, padx=5)

        self.button_c = tk.Button(self.button_frame, text="C", command=self.button_c_action)
        self.button_c.pack(side=tk.LEFT, padx=5)

        self.current_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("圖片文件", "*.png *.jpg *.jpeg *.gif *.bmp")])
        
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((800, 800))  # 調整圖片大小，保持比例
            
            self.current_image = image
            self.update_image_display(image)

    def update_image_display(self, image):
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # 保持對圖片的引用

    def save_image(self):
        if self.current_image:
            split_images = split_wallpaper(self.current_image, mode='default')
            
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All Files", "*.*")])
            if file_path:
                base_filename = file_path.rsplit('.', 1)[0]
                save_split_images(split_images, base_filename)

    def button_a_action(self):
        print("水平模式")
        # 創建滑動條框架
        self.slider_frame = tk.Frame(self.master)
        self.slider_frame.pack(side=tk.BOTTOM, pady=5)

        # 創建滑動條標籤
        self.slider_label = tk.Label(self.slider_frame, text="調整高度比例:")
        self.slider_label.pack(side=tk.LEFT, padx=5)

        # 創建滑動條
        self.height_adjustment_slider = tk.Scale(self.slider_frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200, command=self.apply_height_adjustment)
        self.height_adjustment_slider.set(0)  # 設置初始值為0
        self.height_adjustment_slider.pack(side=tk.LEFT, padx=5)

        # 隱藏滑動條框架（初始狀態）
        self.slider_frame.pack_forget()

        # 顯示滑動條框架
        self.slider_frame.pack(side=tk.BOTTOM, pady=5)
        if self.current_image:
            height_adjustment_ratio = self.height_adjustment_slider.get()
            split_images = split_wallpaper(self.current_image, mode='A', screen_info=self.screen_info, height_adjustment_ratio=height_adjustment_ratio)
            self.update_image_display(split_images)  # 顯示第一張圖片

    def apply_height_adjustment(self, value):
        if self.current_image:
            height_adjustment_ratio = float(value)
            split_images = split_wallpaper(self.current_image, mode='A', screen_info=self.screen_info, height_adjustment_ratio=height_adjustment_ratio)
            self.update_image_display(split_images)  # 顯示第一張圖片

    def button_b_action(self):
        print("按鈕 B 被點擊")
        if self.current_image:
            split_images = split_wallpaper(self.current_image, mode='B', screen_info=self.screen_info)
            self.update_image_display(split_images)

    def button_c_action(self):
        print("按鈕 C 被點擊")

# 創建主窗口
root = tk.Tk()
app = ImageViewerApp(root)
root.mainloop()
