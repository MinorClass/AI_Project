import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os
from pathlib import Path

# 에셋 경로 (Figma에서 생성된 이미지들이 들어있는 폴더)
ASSETS_PATH = os.path.abspath("./UI/assets/rsp_game")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class RSPGame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")

        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)

        # 배경 이미지
        self.bg_image = PhotoImage(file=relative_to_assets("image1.png"))
        canvas.create_image(960, 540, image=self.bg_image)

        # 이미지
        self.image1 = PhotoImage(file=relative_to_assets("image2.png"))
        canvas.create_image(230,147, image=self.image1, anchor="nw")

            #상대방 이미지 창 박스 크기는 w361 h375
        self.image2 = PhotoImage(file=relative_to_assets("image_blank.png"))
        canvas.create_image(377,316, image=self.image2, anchor="nw")
            #나 이미지 창
        self.image3 = PhotoImage(file=relative_to_assets("image_blank.png"))
        canvas.create_image(1183,316, image=self.image3, anchor="nw")

        self.image4 = PhotoImage(file=relative_to_assets("image_vs.png"))
        canvas.create_image(769,419, image=self.image4, anchor="nw")


        # 텍스트
        canvas.create_text(
            385,
            253,
            anchor="nw",
            text="상대방",
            fill="#000000",
            font=("Aldrich Bold", 24)
        )

        canvas.create_text(
            1185,
            253,
            anchor="nw",
            text="나",
            fill="#000000",
            font=("Aldrich Bold", 24)
        )


        # 버튼 이미지
        #가위
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(self, image=self.button_image_1,
                          command=lambda: controller.quit(),
                          borderwidth=0, relief="flat")
        canvas.create_window(372, 726, window=button_1, anchor="nw")

        #바위
        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(self, image=self.button_image_2,
                          command=lambda: controller.quit(),
                          borderwidth=0, relief="flat")
        canvas.create_window(774, 726, window=button_2, anchor="nw")

        #보
        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        button_3 = Button(self, image=self.button_image_3,
                          command=lambda: controller.show_frame("IntroClickGame"),
                          borderwidth=0, relief="flat")
        canvas.create_window(1178, 726, window=button_3, anchor="nw")

