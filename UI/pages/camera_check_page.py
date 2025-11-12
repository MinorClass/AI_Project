from tkinter import Canvas, Button, PhotoImage, Label, Frame
import os
from pathlib import Path
from .GazeTracking.example import AttentionMonitor
import cv2
from PIL import Image, ImageTk

ASSETS_PATH = os.path.abspath("./UI/assets")
WEIGHT_CENTER = 1920 //2
HEIGHT_CENTER = 1080 // 2
MAINCOLOR = "#703BA2"
# SUBCOLOR = 


def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class CheckCam(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")

        self.controller = controller
        # self.is_camera_on = False

            
        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)

        # 배경 이미지
        self.bg_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_background.png")))
        canvas.create_image(WEIGHT_CENTER, 540, image=self.bg_image)
        self.win_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_win.png")))
        canvas.create_image(WEIGHT_CENTER, 550.0, image=self.win_image)

        # 타이틀 - 가상면접
        canvas.create_text( 
            400,
            162,
            anchor="center",
            text="가상 면접",
            fill='#FFFFFF',
            font=("Malgun Gothic", 25)
        )

        # 상단 타이틀 - 이전 BUTTON
        self.btn_previous = ImageTk.PhotoImage(Image.open(relative_to_assets("button/btn_previous.png")))
        btn_previous = Button(self,
                            image=self.btn_previous,
                            borderwidth=0,
                            relief="flat",
                            command= controller.show_frame("FirstPage"))
        canvas.create_window(1600, 162, window=btn_previous, anchor="center")

        # 카메라 피드 표시 영역
        self.video_label = Label(self,bg="#000000")
        canvas.create_window(WEIGHT_CENTER, HEIGHT_CENTER-60, 
                             window=self.video_label, width=300, height=300) 

        # 마이크 ON 버튼
        btn_voiceON = Button(self, width=12, height=2, bg= "#DDDDDD",compound="center", text="마이크 연결",
                          command=lambda: controller.quit(),
                          relief="flat")
        canvas.create_window(WEIGHT_CENTER-87, 686, window=btn_voiceON, anchor="center")

        # 카메라 ON 버튼
        btn_camON = Button(self, width=12, height=2, bg= "#DDDDDD",compound="center", text="카메라 연결",
                          command= self.start_camera_feed,
                          relief="flat")
        canvas.create_window(WEIGHT_CENTER+87, 686, window=btn_camON, anchor="center")


        # 🔹 다음으로 (button_3.png)
        self.button_image_3 = ImageTk.PhotoImage(Image.open(relative_to_assets("button/btn_ready.png")))
        button_3 = Button(self, image=self.button_image_3,
                          command= self.next_page,
                          borderwidth=0, relief="flat")
        canvas.create_window(WEIGHT_CENTER, 803, window=button_3, anchor="center")

    def start_camera_feed(self):
        """카메라 시작"""
        self.monitor = cv2.VideoCapture(4)
        print(self.monitor.isOpened())
        if not self.monitor or not self.monitor.isOpened():
            print("카메라를 열 수 없습니다.")
            return
        # self.is_camera_on = True
        self.update_frame()

    def update_frame(self):
        """화면 갱신"""
        ret, frame = self.monitor.read()
        if frame is None:
            pass            
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            resize_img = img.resize((300,300))
            imgtk = ImageTk.PhotoImage(image=resize_img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            self.after(30, self.update_frame)

        # if self.is_camera_on and self.monitor:
        #     ret, frame = self.monitor.read()
        #     if ret:
        #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #         img = Image.fromarray(frame)
        #         resize_img = img.resize((300,300))
        #         imgtk = ImageTk.PhotoImage(image=resize_img)
        #         self.video_label.imgtk = imgtk
        #         self.video_label.configure(image=imgtk)
        #     self.after(30, self.update_frame)
    
    def next_page(self):
        if self.monitor.isOpened():
            self.monitor.release()
            # self.is_camera_on = False
            self.video_label.configure(image='')  # 비디오 라벨 초기화
        # print(self.monitor.isOpened())
        # if not self.monitor.release():
            # self.monitor.release()
        self.controller.show_frame("MockInterview")

