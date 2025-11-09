from tkinter import Canvas, Button, PhotoImage, Tk, font, Frame, Label
from PIL import Image, ImageTk
import os
from pathlib import Path

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

        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)

        # 배경 이미지
        self.bg_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_background.png")))
        canvas.create_image(960, 540, image=self.bg_image)
        self.win_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_win.png")))
        canvas.create_image(960.0, 550.0, image=self.win_image)

        # 상단 타이틀
        canvas.create_text( 
            400,
            162,
            anchor="center",
            text="가상 면접",
            fill='#FFFFFF',
            font=("Malgun Gothic", 25)
        )

        # 상단 타이틀 - 이전 BUTTON
        self.btn_previous = ImageTk.PhotoImage(Image.open(relative_to_assets("btn_previous.png")))
        btn_previous = Button(self,
                            image=self.btn_previous,
                            borderwidth=0,
                            relief="flat",
                            command=lambda: controller.show_frame("FirstPage"))
        canvas.create_window(1600, 162, window=btn_previous, anchor="center")
        
        # 카메라 영역
        camArea = Frame(self, 
                        width=300, 
                        height=300, 
                        highlightbackground=MAINCOLOR,
                        highlightthickness=3,
                        # borderwidth=2,
                        # bordercolor="#3C0074",
                        # bd="#3C0074",
                        relief="solid")
        camArea.place(x=WEIGHT_CENTER, y=HEIGHT_CENTER-80, anchor="center")


        # 🔹 마이크 ON 버튼
        btn_camON = Button(self,
                           width=15,
                           height=2,
                           bg = "#DDDDDD",
                           compound="center",
                           text="마이크 연결", 
                           command=lambda: controller.quit(),
                          relief="flat")
        canvas.create_window(WEIGHT_CENTER - 95, 686, window=btn_camON, anchor="center")

        # 🔹 카메라 ON 버튼
        btn_camON = Button(self,
                           width=15,
                           height=2,
                           bg = "#DDDDDD",
                           compound="center",
                           text="카메라 연결", 
                           command=self.start_camera_feed,
                          relief="flat")
        canvas.create_window(WEIGHT_CENTER + 95, 686, window=btn_camON, anchor="center")

        # 🔹 다음으로 (MockInterview로 이동)
        self.btn_area = ImageTk.PhotoImage(Image.open(relative_to_assets("btn_pupple.png")))
        btn_next = Button(self, 
                        image=self.btn_area,
                        text="준비완료",
                        font=("AnekGurmukhi Bold", 24),
                        fg="#FFFFFF",
                        compound="center",
                        command=lambda: controller.show_frame("MockInterview"),
                        borderwidth=0, 
                        relief='ridge'
                        )
        canvas.create_window(WEIGHT_CENTER, 829, window=btn_next, anchor="center")



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
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
            self.after(30, self.update_frame)