import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os
from pathlib import Path

# 에셋 경로 (Figma에서 생성된 이미지들이 들어있는 폴더)
ASSETS_PATH = os.path.abspath("./UI/assets/first")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")

        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)

        # 배경 이미지
        self.bg_image = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(960, 540, image=self.bg_image)

        # 상단 텍스트
        canvas.create_text(
            662.0,
            329.0,
            anchor="nw",
            text="부족한 면접 경험을 AI와 함께\n" "        채워 나가보세요.",
            fill="#42364C",
            font=("Aldrich Regular", 32)
        )

        # 설명 텍스트
        canvas.create_text(
            582.0,
            630.0,
            anchor="nw",
            text="AI가 내 면접을 분석하고 판단하여 도움을 줘요,\n"
                 "영상 면접 환경과 실제 면접의 훈련을 할 수 있어요.\n"
                 "마지막 피드백을 통해 고쳐야 할 점을 알 수 있어요.",
            fill="#353C92",
            font=("AnekGurmukhi Light", 24)
        )

        # 이미지
        self.image1 = PhotoImage(file=relative_to_assets("image_2.png"))
        canvas.create_image(230,147, image=self.image1, anchor="nw")

        self.image2 = PhotoImage(file=relative_to_assets("button_1.png"))
        canvas.create_image(822,517, image=self.image2, anchor="nw")

        # 버튼 이미지
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_1 = Button(self, image=self.button_image_1,
                          command=lambda: controller.show_frame("CheckCam"),
                          borderwidth=0, relief="flat")
        canvas.create_window(822, 829, window=button_1, anchor="nw")

