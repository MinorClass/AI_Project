import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os
from pathlib import Path
import time

ASSETS_PATH = os.path.abspath("./UI/assets/mock_interview")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class MockInterview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")

        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)

        # 배경 이미지
        self.bg_image = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(960, 540, image=self.bg_image)

        # 이미지
        self.image1 = PhotoImage(file=relative_to_assets("bimage_l.png"))
        canvas.create_image(225,210, image=self.image1, anchor="nw")

        self.image2 = PhotoImage(file=relative_to_assets("bimage_r.png"))
        canvas.create_image(955,210, image=self.image2, anchor="nw")
            #가상면접관 이미지 자리
        self.image3 = PhotoImage(file=relative_to_assets("image_v.png"))
        canvas.create_image(735,266, image=self.image3, anchor="nw")
            #질문창
        self.image4 = PhotoImage(file=relative_to_assets("image_q.png"))
        canvas.create_image(419,761, image=self.image4, anchor="nw")
            #feedback창
        self.image5 = PhotoImage(file=relative_to_assets("image_f.png"))
        canvas.create_image(1256,595, image=self.image5, anchor="nw")
            #면접자 cam있어야하는 자리
        self.image6 = PhotoImage(file=relative_to_assets("image_cam.png"))
        canvas.create_image(1310,266, image=self.image6, anchor="nw")

        self.image7 = PhotoImage(file=relative_to_assets("image_2.png"))
        canvas.create_image(230,147, image=self.image7, anchor="nw")


        # 질문 텍스트
        canvas.create_text(
            485,
            807,
            anchor="nw",
            text="질문을 내보내야하는 자리입니다",
            fill="#42364C",
            font=("Aldrich Regular", 32)
        )

        # feedback 텍스트
        canvas.create_text(
            1270,
            640,
            anchor="nw",
            text="feedback을 내보내야하는 자리입니다",
            fill="#353C92",
            font=("AnekGurmukhi Light", 24)
        )

        # 버튼 이미지
        #종료
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(self, image=self.button_image_1,
                          command=lambda: controller.quit(),
                          borderwidth=0, relief="flat")
        canvas.create_window(1548, 865, window=button_1, anchor="nw")
        #면접시작
        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(self, image=self.button_image_2,
                          command=lambda: controller.quit(),
                          borderwidth=0, relief="flat")
        canvas.create_window(455, 563, window=button_2, anchor="nw")

        # 진행시간
        canvas.create_text(
            447,
            452,
            anchor="nw",
            text="진행시간",
            fill="#000000",
            font=("AnekGurmukhi Light", 22)
        )

        # 진행시간 라벨 (타이머 표시용)
        canvas.create_text(
            447, 452, anchor="nw",
            text="진행시간", fill="#000000", font=("AnekGurmukhi Light", 22)
        )
        self.timer_label = tk.Label(self, text="60", font=("Arial", 24), bg="#FFFFFF")
        canvas.create_window(445, 500, window=self.timer_label, anchor="nw")

        # 버튼 이미지
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(self, image=self.button_image_1,
                          command=lambda: controller.show_frame("WaitGame"),
                          borderwidth=0, relief="flat")
        canvas.create_window(1548, 865, window=button_1, anchor="nw")

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(self, image=self.button_image_2,
                          command=self.start_timer,  # ✅ 타이머 시작
                          borderwidth=0, relief="flat")
        canvas.create_window(455, 563, window=button_2, anchor="nw")

    # 타이머 시작
    def start_timer(self):
        self.remaining_time = 6
        self.update_timer()

    # 타이머 업데이트
    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.config(text=str(self.remaining_time))
            self.remaining_time -= 1
            # 1초 후 다시 호출
            self.after(1000, self.update_timer)
        # else:
            # 타이머 끝나면 다음 화면으로 이동
            # self.controller.show_frame("WaitGame")  # 원하는 페이지 이름으로 변경

        




