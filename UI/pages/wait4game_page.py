import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os
from pathlib import Path

# 에셋 경로 (Figma에서 생성된 이미지들이 들어있는 폴더)
ASSETS_PATH = os.path.abspath("./UI/assets/wait4game")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class WaitGame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")

        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)

        # 배경 이미지
        self.bg_image = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(960, 540, image=self.bg_image)

        # 상단 텍스트
        canvas.create_text(
            758.0,
            447.0,
            anchor="nw",
            text="수고하셨습니다!\n\n"
            "     게임 시작 전\n"
            "잠시 쉬어가겠습니다.",
            fill="#42364C",
            font=("Aldrich Regular", 32)
        )


        # 이미지
        self.image1 = PhotoImage(file=relative_to_assets("image_2.png"))
        canvas.create_image(230,147, image=self.image1, anchor="nw")

        # 버튼 이미지
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(self, image=self.button_image_1,
                          command=lambda: controller.show_frame("IntroGames"),
                          borderwidth=0, relief="flat")
        canvas.create_window(822, 829, window=button_1, anchor="nw")

