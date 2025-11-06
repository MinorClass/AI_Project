import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os
from pathlib import Path

ASSETS_PATH = os.path.abspath("./UI/assets/camera_check")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class CheckCam(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")

        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)

        # 배경 이미지
        self.bg_image = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(960, 540, image=self.bg_image)

        # 이미지
        self.image1 = PhotoImage(file=relative_to_assets("image_2.png"))
        canvas.create_image(230,147, image=self.image1, anchor="nw")

        # 버튼 이미지
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(self, image=self.button_image_1,
                          command=lambda: controller.quit(),
                          borderwidth=0, relief="flat")
        canvas.create_window(809, 686, window=button_1, anchor="nw")

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(self, image=self.button_image_2,
                          command=lambda: controller.quit(),
                          borderwidth=0, relief="flat")
        canvas.create_window(1014, 686, window=button_2, anchor="nw")

        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        button_3 = Button(self, image=self.button_image_3,
                          command=lambda: controller.show_frame("MockInterview"),
                          borderwidth=0, relief="flat")
        canvas.create_window(893, 803, window=button_3, anchor="nw")


