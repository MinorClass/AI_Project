from tkinter import Canvas, Button, PhotoImage, Tk, font, Frame
from PIL import Image, ImageTk

import os
from pathlib import Path

# 에셋 경로 (Figma에서 생성된 이미지들이 들어있는 폴더)
ASSETS_PATH = os.path.abspath("./UI/assets")
WEIGHT_CENTER = 1920 //2
HEIGHT_CENTER = 1080 // 2
MAINCOLOR = "#703BA2"
# SUBCOLOR = 

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class FirstPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")

        self.controller = controller
        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)

        # 배경 이미지
        self.bg_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_background.png")))
        canvas.create_image(WEIGHT_CENTER, 540, image=self.bg_image)
        self.win_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_win.png")))
        canvas.create_image(WEIGHT_CENTER, 550.0, image=self.win_image)

        # 상단 타이틀
        canvas.create_text(
            WEIGHT_CENTER,
            160,
            justify="center",
            anchor="center",
            text="AI 면접 훈련도구",
            fill='#FFFFFF',
            font=("Malgun Gothic", 30)
        )


        # 상단 텍스트
        canvas.create_text(
            WEIGHT_CENTER,
            370.0,
            justify= "center",
            anchor="center",
            text="부족한 면접 경험을 AI와 함께\n채워 나가보세요",
            fill="#42364C",
            font=("Aldrich Regular", 32)
        )


        # 설명 텍스트
        canvas.create_text(
            WEIGHT_CENTER,
            680.0,
            anchor="center",
            text="AI가 내 면접을 분석하고 판단하여 도움을 줘요\n"
                 "영상 면접 환경과 실제 면접의 훈련을 할 수 있어요\n"
                 "마지막 피드백을 통해 고쳐야 할 점을 알 수 있어요",
            fill="#353C92",
            font=("AnekGurmukhi Light", 24)
        )

        # 시간 안내 영역
        self.TimeInfo = ImageTk.PhotoImage(Image.open(relative_to_assets("btn_white.png")))
        canvas.create_image(822,500, image=self.TimeInfo, anchor="nw")
        canvas.create_text(
            WEIGHT_CENTER,
            540,
            anchor="center",
            text="총 시간 | 5분",
            fill=MAINCOLOR,
            font=("AnekGurmukhi Medium", 20)
        )



        # 시작버튼
        self.btn_area = ImageTk.PhotoImage(Image.open(relative_to_assets("btn_pupple.png")))
        btn_start = Button(self, 
                        image=self.btn_area,
                        text="시작하기",
                        font=("AnekGurmukhi Bold", 24),
                        fg="#FFFFFF",
                        bg = None,
                        compound="center",
                        command=lambda: controller.show_frame("CheckCam"),
                        borderwidth=0, 
                        relief='ridge'
                        )
        canvas.create_window(WEIGHT_CENTER, 829, window=btn_start, anchor="center")
        
