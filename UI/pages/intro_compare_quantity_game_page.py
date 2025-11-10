import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os
from pathlib import Path

# 에셋 경로 (Figma에서 생성된 이미지들이 들어있는 폴더)
ASSETS_PATH = os.path.abspath("./UI/assets/intro_click_num_game")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class IntroCompareGame(tk.Frame):
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

        self.image2 = PhotoImage(file=relative_to_assets("image_b.png"))
        canvas.create_image(230,211, image=self.image2, anchor="nw")

        self.image3 = PhotoImage(file=relative_to_assets("image_br.png"))
        canvas.create_image(1079,211, image=self.image3, anchor="nw")

        self.image4 = PhotoImage(file=relative_to_assets("image_brb.png"))
        canvas.create_image(1079,641, image=self.image4, anchor="nw")

        # 설명 텍스트
        canvas.create_text(
            260,
            340,
            anchor="nw",
            text="도형의 크기는 과제의 목표와는 무관하니 꼭 기억해 주세요.\n\n"  
                "                 도형이 나타나는 시간이 짧으니,\n\n" 
                "             제시 화면을 놓치지 않도록 해야 해요.\n\n"
                "  게임이 진행될수록 양쪽 단어의 수가 많아져서 어려워져요.\n\n"
                "       헷갈리더라도 직관적으로 선택하는 것이 중요해요!",
            fill="#42364C",
            font=("Aldrich Regular", 20)
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
            text="         개수가 더 많은 도형을 \n"
                 "         선택해야하는 게임입니다",
            fill="#353C92",
            font=("AnekGurmukhi Light", 22)
        )

        # 버튼 이미지
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(self, image=self.button_image_1,
                          command=lambda: controller.show_frame("CompareGame"),
                          borderwidth=0, relief="flat")
        canvas.create_window(1246, 768, window=button_1, anchor="nw")

