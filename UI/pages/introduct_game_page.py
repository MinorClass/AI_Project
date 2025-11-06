import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os
from pathlib import Path

# 에셋 경로 (Figma에서 생성된 이미지들이 들어있는 폴더)
ASSETS_PATH = os.path.abspath("./UI/assets/introduct_game")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class IntroGames(tk.Frame):
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

        self.image2 = PhotoImage(file=relative_to_assets("bimageb.png"))
        canvas.create_image(230,213, image=self.image2, anchor="nw")

        self.image3 = PhotoImage(file=relative_to_assets("bimages.png"))
        canvas.create_image(230,468, image=self.image3, anchor="nw")

        # 가위바위보 텍스트
        canvas.create_text(
            280,
            317,
            anchor="nw",
            text="가위바위보",
            fill="#42364C",
            font=("Aldrich Regular", 32)
        )

        # 숫자누르기 텍스트
        canvas.create_text(
            280,
            570,
            anchor="nw",
            text="숫자누르기",
            fill="#42364C",
            font=("Aldrich Regular", 32)
        )

        # 개수 비교하기 텍스트
        canvas.create_text(
            280,
            820,
            anchor="nw",
            text="개수비교하기",
            fill="#42364C",
            font=("Aldrich Regular", 32)
        )


        # 가위바위보 게임 설명 텍스트
        canvas.create_text(
            650.0,
            293.0,
            anchor="nw",
            text="       '나'또는 '상대'의 관점에서 가위바위보를 하는 게임으로,\n"
                 "'나'인 경우에는 이기고, '상대'인 경우에는 져야하는 게임입니다.",
            fill="#353C92",
            font=("AnekGurmukhi Light", 22)
        )

        # 숫자 누르기 게임 설명 텍스트
        canvas.create_text(
            700.0,
            557.0,
            anchor="nw",
            text="신호가 제시되면 주어진 규칙에 맞게 1부터 9까지 숫자 버튼을\n"
                 "       최대한 빠르고 정확하게 누르면 되는 게임입니다.",
            fill="#353C92",
            font=("AnekGurmukhi Light", 22)
        )

        # 개수비교하기 게임 설명 텍스트
        canvas.create_text(
            700.0,
            785.0,
            anchor="nw",
            text="    화면 왼쪽과 오른쪽에 단어가 여러 개 제시됩니다.\n"
                 "두 단어 중 어떤 단어의 개수가 더 많았는지 선택해 주세요.",
            fill="#353C92",
            font=("AnekGurmukhi Light", 22)
        )

        

        # 버튼 이미지
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_1 = Button(self, image=self.button_image_1,
                          command=lambda: controller.quit(),
                          borderwidth=0, relief="flat")
        canvas.create_window(1545, 916, window=button_1, anchor="nw")

