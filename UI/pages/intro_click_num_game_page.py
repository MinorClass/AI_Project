import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os
from pathlib import Path

# 에셋 경로 (Figma에서 생성된 이미지들이 들어있는 폴더)
ASSETS_PATH = os.path.abspath("./UI/assets/intro_click_num_game")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class IntroClickGame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")

        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)

        # 배경 이미지
        self.bg_image = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(960, 540, image=self.bg_image)

        # 이미지
        self.image0 = PhotoImage(file=relative_to_assets("image_b.png"))
        canvas.create_image(230,211, image=self.image0, anchor="nw")

        self.image1 = PhotoImage(file=relative_to_assets("image_2.png"))
        canvas.create_image(230,147, image=self.image1, anchor="nw")

        self.image2 = PhotoImage(file=relative_to_assets("image_s.png"))
        canvas.create_image(230,211, image=self.image2, anchor="nw")

        self.image3 = PhotoImage(file=relative_to_assets("image_br.png"))
        canvas.create_image(1079,211, image=self.image3, anchor="nw")

        self.image4 = PhotoImage(file=relative_to_assets("image_brb.png"))
        canvas.create_image(1079,641, image=self.image4, anchor="nw")

        self.image5 = PhotoImage(file=relative_to_assets("image_lv1.png"))
        canvas.create_image(240,221, image=self.image5, anchor="nw")

        self.image6 = PhotoImage(file=relative_to_assets("image_lv2.png"))
        canvas.create_image(240,620, image=self.image6, anchor="nw")


        # Lv1 설명 텍스트
        canvas.create_text(
            396,
            395,
            anchor="nw",
            text="제시된 숫자 하나를 빠르게 눌러야 한다.",
            fill="#42364C",
            font=("Aldrich Regular", 22)
        )

        # Lv2 설명 텍스트
        canvas.create_text(
            350,
            770,
            anchor="nw",
            text="조건에 따라 1~9의 숫자를 빠르게 눌러야 한다",
            fill="#42364C",
            font=("Aldrich Regular", 22)
        )

        # 목표 텍스트
        canvas.create_text(
            1300,
            341,
            anchor="nw",
            text="• 목표",
            fill="#353C92",
            font=("AnekGurmukhi Bold", 40)
        )

        # 목표 설명 텍스트
        canvas.create_text(
            1115.0,
            448,
            anchor="nw",
            text="이 게임은 무작위로 배열된 숫자를 \n주어진 규칙에 맞게 정확하고 빠르게 \n차례대로 눌러야하는 게임입니다.",
            fill="#353C92",
            font=("AnekGurmukhi Light", 22)
        )

        # 버튼 이미지
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(self, image=self.button_image_1,
                          command=lambda: controller.quit(),
                          borderwidth=0, relief="flat")
        canvas.create_window(1246, 768, window=button_1, anchor="nw")

