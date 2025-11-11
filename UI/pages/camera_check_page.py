import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, Label
import os
from pathlib import Path
from .GazeTracking.example import AttentionMonitor
import cv2
from PIL import Image, ImageTk

ASSETS_PATH = os.path.abspath("./UI/assets/camera_check")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class CheckCam(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")

        self.controller = controller
        # ... (생략) ...

        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)

        # 배경 이미지 (image_1.png)
        # 💡 PhotoImage -> ImageTk.PhotoImage 로 수정
        self.bg_image = ImageTk.PhotoImage(Image.open(relative_to_assets("image_1.png")))
        canvas.create_image(960, 540, image=self.bg_image)

        # 카메라 피드 표시 영역 (이전 요청에 따라 Label로 변경됨)
        self.video_label = Label(self, bg="#000000")
        # 이미지 크기가 300x300이 되도록 place 대신 create_window 사용 시 크기를 지정합니다.
        canvas.create_window(960, 480, window=self.video_label, width=300, height=300) 

        # 이미지 (image_2.png)
        # 💡 PhotoImage -> ImageTk.PhotoImage 로 수정
        self.image1 = ImageTk.PhotoImage(Image.open(relative_to_assets("image_2.png")))
        canvas.create_image(230,147, image=self.image1, anchor="nw")

        # 카메라 ON 버튼 (button_1.png)
        # 💡 PhotoImage -> ImageTk.PhotoImage 로 수정
        self.button_image_1 = ImageTk.PhotoImage(Image.open(relative_to_assets("button_1.png")))
        button_1 = Button(self, image=self.button_image_1,
                          command=lambda: controller.quit(),
                          borderwidth=0, relief="flat")
        canvas.create_window(809, 686, window=button_1, anchor="nw")

        # 🔹 앱 종료 버튼 (button_2.png)
        # 💡 PhotoImage -> ImageTk.PhotoImage 로 수정
        self.button_image_2 = ImageTk.PhotoImage(Image.open(relative_to_assets("button_2.png")))
        button_2 = Button(self, image=self.button_image_2,
                          command=self.start_camera_feed,
                          borderwidth=0, relief="flat")
        canvas.create_window(1014, 686, window=button_2, anchor="nw")

        # 🔹 다음으로 (button_3.png)
        # 💡 PhotoImage -> ImageTk.PhotoImage 로 수정
        self.button_image_3 = ImageTk.PhotoImage(Image.open(relative_to_assets("button_3.png")))
        button_3 = Button(self, image=self.button_image_3,
                          command=lambda: self.next_page(),
                          borderwidth=0, relief="flat")
        canvas.create_window(893, 803, window=button_3, anchor="nw")

    def start_camera_feed(self):
        """카메라 시작"""
        self.monitor = cv2.VideoCapture(4)
        if not self.monitor or not self.monitor.isOpened():
            print("카메라를 열 수 없습니다.")
            return
        self.is_camera_on = True
        self.update_frame()

    def update_frame(self):
        """화면 갱신"""
        if self.is_camera_on and self.monitor:
            ret, frame = self.monitor.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                resize_img = img.resize((300,300))
                imgtk = ImageTk.PhotoImage(image=resize_img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
            self.after(30, self.update_frame)
    def next_page(self):
        if not self.monitor.release():
            self.monitor.release()
        self.controller.show_frame("MockInterview")
