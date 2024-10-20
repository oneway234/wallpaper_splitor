import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from utils.split_wallpaper import split_wallpaper, save_split_images, get_screen_info

class ImageViewerApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Viewer")
        master.geometry("800x650")

        self.screen_info = get_screen_info()
        
        self.image_label = tk.Label(master)
        self.image_label.pack(expand=True, fill=tk.BOTH)

        self.create_buttons()
        self.create_slider()

        self.current_image = None

    def create_buttons(self):
        button_frame = tk.Frame(self.master)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        buttons = [
            ("Load Image", self.load_image),
            ("Save Image", self.save_image),
            ("Horizontal Split", lambda: self.split_image('A')),
            ("Vertical Split", lambda: self.split_image('B'))
        ]

        for text, command in buttons:
            tk.Button(button_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)

    def create_slider(self):
        self.slider_frame = tk.Frame(self.master)
        self.slider_label = tk.Label(self.slider_frame, text="Adjust Ratio:")
        self.slider_label.pack(side=tk.LEFT, padx=5)

        self.adjustment_slider = tk.Scale(self.slider_frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200, command=self.apply_adjustment)
        self.adjustment_slider.pack(side=tk.LEFT, padx=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((800, 800))
            self.current_image = image
            self.update_image_display(image)

    def update_image_display(self, image):
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def save_image(self):
        if self.current_image:
            _, split_images = split_wallpaper(self.current_image, mode=self.current_mode, screen_info=self.screen_info,
                                           height_adjustment_ratio=self.adjustment_slider.get() if self.current_mode == 'A' else None,
                                           width_adjustment_ratio=self.adjustment_slider.get() if self.current_mode == 'B' else None)
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All Files", "*.*")])
            if file_path:
                base_filename = file_path.rsplit('.', 1)[0]
                save_split_images(split_images, base_filename)
                messagebox.showinfo("Save Successful", f"Successfully saved {len(split_images)} images.")  # Changed to English

    def split_image(self, mode):
        if self.current_image:
            self.current_mode = mode
            self.slider_frame.pack(side=tk.BOTTOM, pady=5)
            self.slider_label.config(text=f"Adjust {'Height' if mode == 'A' else 'Width'} Ratio:")  # Changed to English
            self.apply_adjustment(0)

    def apply_adjustment(self, value):
        if self.current_image:
            adjustment_ratio = float(value)
            draw_image, _ = split_wallpaper(self.current_image, mode=self.current_mode, screen_info=self.screen_info, 
                                           height_adjustment_ratio=adjustment_ratio if self.current_mode == 'A' else None,
                                           width_adjustment_ratio=adjustment_ratio if self.current_mode == 'B' else None)
            self.update_image_display(draw_image)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = ImageViewerApp(tk.Toplevel())
    root.mainloop()
