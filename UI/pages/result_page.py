import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os
from pathlib import Path
from .mock_interview_page import MockInterview
# 에셋 경로 (Figma에서 생성된 이미지들이 들어있는 폴더)
ASSETS_PATH = os.path.abspath("./UI/assets/result")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class Result(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")
        self.controller = controller
        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)

        # 배경 이미지
        self.bg_image = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(960, 540, image=self.bg_image)

        # 이미지
        self.image1 = PhotoImage(file=relative_to_assets("image_2.png"))
        canvas.create_image(230,147, image=self.image1, anchor="nw")

            #결과 이미지1
        self.image2 = PhotoImage(file=relative_to_assets("image_r.png"))
        canvas.create_image(267,275, image=self.image2, anchor="nw")
            #결과 이미지2
        self.image3 = PhotoImage(file=relative_to_assets("image_r.png"))
        canvas.create_image(991,275, image=self.image3, anchor="nw")        

        # 버튼 이미지
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(self, image=self.button_image_1,
                          command=lambda: self.quitpage(),
                          borderwidth=0, relief="flat")
        canvas.create_window(822, 829, window=button_1, anchor="nw")

    def quitpage(self):
        print(MockInterview.get_parameter)
        self.controller.quit()