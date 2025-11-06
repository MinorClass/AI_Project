# from pathlib import Path
# from tkinter import Tk, Canvas, Button, PhotoImage, Label
# import random
# import os

# ASSETS_PATH = os.path.abspath("./UI/assets/click_num_game")

# def relative_to_assets(path: str) -> Path:
#     return Path(ASSETS_PATH) / Path(path)

# window = Tk()
# window.geometry("1920x1080")
# window.configure(bg="#FFFFFF")

# canvas = Canvas(
#     window,
#     bg="#FFFFFF",
#     height=1080,
#     width=1920,
#     bd=0,
#     highlightthickness=0,
#     relief="ridge"
# )
# canvas.place(x=0, y=0)

# # 배경 이미지
# image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
# canvas.create_image(960.0, 540.0, image=image_image_1)

# image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
# canvas.create_image(959.0, 563.0, image=image_image_2)

# # 텍스트
# timer_text = canvas.create_text(884.0, 365.0, anchor="nw", text="00:30", fill="#07E597", font=("MonomaniacOne Regular", 32))
# score_text = canvas.create_text(1146.0, 266.0, anchor="nw", text="score : 0", fill="#FF5D00", font=("Baloo2 Regular", 28))

# # 상태 라벨



# status_label = Label(window, text="1~9까지 순서대로 누르세요.", font=("Arial", 24), fg="black", bg="white", anchor="center", justify="center")
# status_label.place(x=960, y=475, anchor="center")

# # 게임 상태 변수
# score = 0
# time_left = 30
# game_running = False
# current_sequence = []
# player_progress = []

# # 조건 설명 생성 함수
# def sequence_description(seq):
#     counts = {}
#     for num in seq:
#         counts[num] = counts.get(num, 0) + 1
    
#     desc_list = []
#     for num in range(1, 10):
#         if num in counts and counts[num] > 1:
#             desc_list.append(f"숫자 {num}는 {counts[num]}번 누르세요.")
#     if not desc_list:
#         return "1~9까지 순서대로 누르세요."
#     return " ".join(desc_list)

# # 조건 시퀀스 생성
# def generate_sequence():
#     seq = []
#     for num in range(1, 10):
#         repeat = 1
#         if random.random() < 0.3:
#             repeat = random.randint(2, 4)
#         seq.extend([num] * repeat)
#     return seq



# # 버튼 좌표 리스트
# positions = [
#     (788, 524), (910, 524), (1032, 524),
#     (788, 642), (911, 642), (1032, 642),
#     (788, 760), (911, 760), (1032, 760)
# ]

# # 버튼 객체 리스트
# buttons = []

# # 버튼 생성 + 기본 순서 배치
# for idx, (x, y) in enumerate(positions, start=1):
#     btn = Button(window,
#                  text=str(idx),
#                  width=10,
#                  height=4,
#                  bg="#703BA2",
#                  fg="white",
#                  font=("Arial", 20),
#                  command=lambda n=idx: button_click(n))
#     btn.place(x=x, y=y, width=100, height=100)  # 기본 위치에 배치
#     buttons.append(btn)


# # 버튼 생성만 먼저 (좌표는 나중에 배치)
# for idx in range(1, 10):
#     btn = Button(window,
#                  text=str(idx),
#                  width=10,
#                  height=4,
#                  bg="#703BA2",
#                  fg="white",
#                  font=("Arial", 20),
#                  command=lambda n=idx: button_click(n))
#     buttons.append(btn)

# # 버튼 좌표 리스트
# positions = [
#     (788, 524), (910, 524), (1032, 524),
#     (788, 642), (911, 642), (1032, 642),
#     (788, 760), (911, 760), (1032, 760)
# ]


# # 버튼 랜덤 배치 함수
# def shuffle_buttons():
#     shuffled_positions = positions[:]
#     random.shuffle(shuffled_positions)
#     for btn, (x, y) in zip(buttons, shuffled_positions):
#         btn.place(x=x, y=y, width=100, height=100)

# # 게임 시작
# def start_game():
#     global score, time_left, game_running, current_sequence, player_progress
#     score = 0
#     time_left = 30
#     game_running = True
#     current_sequence = generate_sequence()
#     player_progress = []
#     canvas.itemconfig(score_text, text="score : 0")
#     canvas.itemconfig(timer_text, text="00:30")
#     status_label.config(text=sequence_description(current_sequence))
#     shuffle_buttons()   # 버튼 랜덤 배치
#     update_timer()

# # 타이머
# def update_timer():
#     global time_left, game_running
#     if game_running:
#         if time_left > 0:
#             canvas.itemconfig(timer_text, text=f"00:{time_left:02d}")
#             time_left -= 1
#             window.after(1000, update_timer)
#         else:
#             game_running = False
#             status_label.config(text="조건 테스트에서 종료했습니다")

# # 버튼 클릭 처리
# def button_click(num):
#     global player_progress, current_sequence, score
#     if not game_running:
#         return
#     player_progress.append(num)
#     if player_progress == current_sequence[:len(player_progress)]:
#         if len(player_progress) == len(current_sequence):
#             score += 1
#             canvas.itemconfig(score_text, text=f"score : {score}")
#             current_sequence = generate_sequence()
#             player_progress = []
#             status_label.config(text=sequence_description(current_sequence))
#             shuffle_buttons()   # 새로운 문제 때도 버튼 다시 섞기
#     else:
#         # 틀렸을 때도 새로운 문제 출제
#         player_progress = []
#         current_sequence = generate_sequence()
#         status_label.config(text=sequence_description(current_sequence))
#         shuffle_buttons()

# # 우측 상단 버튼 (연결 페이지용)
# button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
# button_1 = Button(
#     image=button_image_1,
#     borderwidth=0,
#     highlightthickness=0,
#     command=lambda: print("button_1 clicked"),
#     relief="flat"
# )
# button_1.place(x=1451.0, y=140.0, width=277.0, height=84.0)

# # 중앙 버튼 = 시작 버튼
# button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
# button_2 = Button(
#     image=button_image_2,
#     borderwidth=0,
#     highlightthickness=0,
#     command=start_game,
#     relief="flat"
# )
# button_2.place(x=821.0, y=273.0, width=277.0, height=84.0)

# window.resizable(False, False)
# window.mainloop()

import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, Label
import random, os
from pathlib import Path

ASSETS_PATH = os.path.abspath("./UI/assets/click_num_game")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class ClickGame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")
        self.controller = controller

        self.canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        self.canvas.pack(fill="both", expand=True)

        # 배경 이미지
        self.bg_image1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(960, 540, image=self.bg_image1)

        self.bg_image2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(959, 563, image=self.bg_image2)

        # 텍스트
        self.timer_text = self.canvas.create_text(
            884, 365, anchor="nw", text="00:30",
            fill="#07E597", font=("MonomaniacOne Regular", 32)
        )
        self.score_text = self.canvas.create_text(
            1250, 266, anchor="nw", text="score : 0",
            fill="#FF5D00", font=("Baloo2 Regular", 28)
        )

        # 상태 라벨
        self.status_label = Label(self, text="1~9까지 순서대로 누르세요.",
                                  font=("Arial", 24), fg="black")
        self.canvas.create_window(960, 475, window=self.status_label, anchor="center")

        # 게임 상태 변수
        self.score = 0
        self.time_left = 30
        self.game_running = False
        self.current_sequence = []
        self.player_progress = []

        # 버튼 좌표
        self.positions = [
            (788, 524), (910, 524), (1032, 524),
            (788, 642), (911, 642), (1032, 642),
            (788, 760), (911, 760), (1032, 760)
        ]

        # 버튼 생성
        self.buttons = []
        for idx in range(1, 10):
            btn = Button(self, text=str(idx),
                         width=10, height=4,
                         bg="#703BA2", fg="white",
                         font=("Arial", 20),
                         command=lambda n=idx: self.button_click(n))
            self.buttons.append(btn)

        # 우측 상단 버튼 (다음 화면 이동 예시)
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(self, image=self.button_image_1,
                          borderwidth=0, relief="flat",
                          command=lambda: controller.show_frame("IntroClickGame"))
        self.canvas.create_window(1451, 140, window=button_1, anchor="nw")

        # 중앙 시작 버튼
        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(self, image=self.button_image_2,
                          borderwidth=0, relief="flat",
                          command=self.start_game)
        self.canvas.create_window(910, 273, window=button_2, anchor="nw")

    # 조건 설명
    def sequence_description(self, seq):
        counts = {}
        for num in seq:
            counts[num] = counts.get(num, 0) + 1
        desc_list = [f"숫자 {num}는 {counts[num]}번 누르세요."
                     for num in range(1, 10) if num in counts and counts[num] > 1]
        return " ".join(desc_list) if desc_list else "1~9까지 순서대로 누르세요."

    # 시퀀스 생성
    def generate_sequence(self):
        seq = []
        for num in range(1, 10):
            repeat = 1
            if random.random() < 0.3:
                repeat = random.randint(2, 4)
            seq.extend([num] * repeat)
        return seq

    # 버튼 섞기
    def shuffle_buttons(self):
        shuffled = self.positions[:]
        random.shuffle(shuffled)
        for btn, (x, y) in zip(self.buttons, shuffled):
            self.canvas.create_window(x, y, window=btn, anchor="nw", width=100, height=100)

    # 게임 시작
    def start_game(self):
        self.score = 0
        self.time_left = 30
        self.game_running = True
        self.current_sequence = self.generate_sequence()
        self.player_progress = []
        self.canvas.itemconfig(self.score_text, text="score : 0")
        self.canvas.itemconfig(self.timer_text, text="00:30")
        self.status_label.config(text=self.sequence_description(self.current_sequence))
        self.shuffle_buttons()
        self.update_timer()

    # 타이머
    def update_timer(self):
        if self.game_running:
            if self.time_left > 0:
                self.canvas.itemconfig(self.timer_text, text=f"00:{self.time_left:02d}")
                self.time_left -= 1
                self.after(1000, self.update_timer)
            else:
                self.game_running = False
                self.status_label.config(text="조건 테스트에서 종료했습니다")
                # 타이머 끝나면 결과 페이지로 이동
                self.controller.show_frame("ResultPage")

    # 버튼 클릭 처리
    def button_click(self, num):
        if not self.game_running:
            return
        self.player_progress.append(num)
        if self.player_progress == self.current_sequence[:len(self.player_progress)]:
            if len(self.player_progress) == len(self.current_sequence):
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"score : {self.score}")
                self.current_sequence = self.generate_sequence()
                self.player_progress = []
                self.status_label.config(text=self.sequence_description(self.current_sequence))
                self.shuffle_buttons()
        else:
            self.player_progress = []
            self.current_sequence = self.generate_sequence()
            self.status_label.config(text=self.sequence_description(self.current_sequence))
            self.shuffle_buttons()
