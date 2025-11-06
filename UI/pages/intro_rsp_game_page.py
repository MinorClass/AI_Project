import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os
from pathlib import Path

# 에셋 경로 (Figma에서 생성된 이미지들이 들어있는 폴더)
ASSETS_PATH = os.path.abspath("./UI/assets/intro_rsp_game")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class IntroRSPGame(tk.Frame):
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

        self.image2 = PhotoImage(file=relative_to_assets("image_bt.png"))
        canvas.create_image(230,211, image=self.image2, anchor="nw")

        self.image3 = PhotoImage(file=relative_to_assets("image_bb.png"))
        canvas.create_image(230,466, image=self.image3, anchor="nw")

        self.image4 = PhotoImage(file=relative_to_assets("image_br.png"))
        canvas.create_image(1079,211, image=self.image4, anchor="nw")

        self.image5 = PhotoImage(file=relative_to_assets("image_brb.png"))
        canvas.create_image(1079,641, image=self.image5, anchor="nw")

        self.image6 = PhotoImage(file=relative_to_assets("image_lv1.png"))
        canvas.create_image(238,220, image=self.image6, anchor="nw")

        self.image7 = PhotoImage(file=relative_to_assets("image_lv2.png"))
        canvas.create_image(238,473, image=self.image7, anchor="nw")

        self.image8 = PhotoImage(file=relative_to_assets("image_lv3.png"))
        canvas.create_image(238,728, image=self.image8, anchor="nw")



        # Lv1 설명 텍스트
        canvas.create_text(
            362,
            290,
            anchor="nw",
            text="        '나'의 관점에서 진행한다.\n"
            "즉, '상대'를 보고 '나'가 이기게 선택해야한다.",
            fill="#42364C",
            font=("Aldrich Regular", 22)
        )

        # Lv2 설명 텍스트
        canvas.create_text(
            375,
            540,
            anchor="nw",
            text="        ‘상대’의 관점에서 진행한다.\n"
            "즉, ‘나’를 보고 ‘나’가 이기게 선택해야한다.",
            fill="#42364C",
            font=("Aldrich Regular", 22)
        )

        # Lv3 설명 텍스트
        canvas.create_text(
            410,
            800,
            anchor="nw",
            text="‘나’, ‘상대’ 관점이 랜덤으로 진행된다.\n"
            " 무조건 ‘나’가 이기게 선택해야한다.",
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
            text="이 게임은 가위, 바위, 보를 선택하여 \n    상대방을 이겨야하는 게임입니다.",
            fill="#353C92",
            font=("AnekGurmukhi Light", 22)
        )

        # 버튼 이미지
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(self, image=self.button_image_1,
                          command=lambda: controller.quit(),
                          borderwidth=0, relief="flat")
        canvas.create_window(1246, 768, window=button_1, anchor="nw")

