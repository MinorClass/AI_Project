import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, Label
import os
from pathlib import Path
import cv2
from PIL import Image, ImageTk

ASSETS_PATH = os.path.abspath("./UI/assets/camera_check")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class CheckCam(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")
        self.controller = controller
        self.cap = None
        self.video_label = None
        self.is_camera_on = False

        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)

        self.bg_image = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(960, 540, image=self.bg_image)

        # 카메라 피드 표시 영역
        self.video_label = Label(self, bg="#000000")
        canvas.create_window(960, 540, window=self.video_label, width=300, height=300)

        # 🔹 카메라 ON 버튼
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(self, image=self.button_image_1,
                          command=self.start_camera_feed,
                          borderwidth=0, relief="flat")
        canvas.create_window(809, 686, window=button_1, anchor="nw")

        # 🔹 앱 종료 버튼
        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(self, image=self.button_image_2,
                          command=lambda: controller.quit(),
                          borderwidth=0, relief="flat")
        canvas.create_window(1014, 686, window=button_2, anchor="nw")

        # 🔹 다음으로 (MockInterview로 이동)
        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        button_3 = Button(self, image=self.button_image_3,
                          command=lambda: controller.show_frame("MockInterview"),
                          borderwidth=0, relief="flat")
        canvas.create_window(893, 803, window=button_3, anchor="nw")

    def start_camera_feed(self):
        """카메라 시작"""
        self.cap = self.controller.start_camera()
        if not self.cap or not self.cap.isOpened():
            print("카메라를 열 수 없습니다.")
            return
        self.is_camera_on = True
        self.update_frame()

    def update_frame(self):
        """화면 갱신"""
        if self.is_camera_on and self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
            self.after(30, self.update_frame)
