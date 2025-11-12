from tkinter import Canvas, Button, PhotoImage, Frame 
from PIL import Image, ImageTk 
import os 
from pathlib import Path 
import time 
import random 
from typing import Dict 
# 에셋 경로 설정 
ASSETS_PATH = os.path.abspath("./UI/assets")
WIDTH_CENTER = 1920 // 2 
HEIGHT_CENTER = 1080 // 2 
def relative_to_assets(path: str) -> Path: 
    return Path(ASSETS_PATH) / Path(path) 
# 승리 규칙: key가 value를 이긴다 
WIN_RULE: Dict[str, str] = { "rock": "scissors", "scissors": "paper", "paper": "rock", "blank": "blank" } 
CHOICES = ["rock", "paper", "scissors"] 

class RSPGame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")
        self.controller = controller

        # --- 게임 상태 변수 ---
        self.is_game_running = False
        self.duration_time = 30
        self.start_time = 0
        self.remaining_time = 0

        self.correct_count = 0
        self.total_tries = 0
        self.img_card_pick = None
        self.computer_is_actor = None

        # 이미지 캐시
        self.choice_images: Dict[str, ImageTk.PhotoImage] = {}
        self.load_images()

        # UI 세팅
        self.setup_ui()

        # ❌ 게임 시작 제거 — 화면에 올라올 때 시작하도록 변경
        # self.start_game()

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        # ✅ 화면에 올라올 때만 게임 시작
        if not self.is_game_running:
            self.start_game()

    def load_images(self):
        for choice in CHOICES + ["blank"]:
            path = relative_to_assets(f"card_{choice}.png")
            self.choice_images[choice] = ImageTk.PhotoImage(Image.open(path))
        self.btn_img = ImageTk.PhotoImage(Image.open(relative_to_assets("btn_pupple.png")))
        self.vs_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_vs.png")))
        self.bg_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_background.png")))
        self.win_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_win.png")))

    def setup_ui(self):
        self.canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(960, 540, image=self.bg_image)
        self.canvas.create_image(960, 550, image=self.win_image)

        self.canvas.create_text(400, 162, anchor="center", text="가위바위보",
                                fill="#FFFFFF", font=("Malgun Gothic", 25))
        self.canvas.create_text(WIDTH_CENTER-320, HEIGHT_CENTER-280, anchor="center",
                                text="상대방", font=("Aldrich Bold", 30), fill="#000000")
        self.canvas.create_text(WIDTH_CENTER+320, HEIGHT_CENTER-280, anchor="center",
                                text="나", font=("Aldrich Bold", 30), fill="#000000")

        self.opponent_image_id = self.canvas.create_image(WIDTH_CENTER-320, HEIGHT_CENTER-50,
                                                          image=self.choice_images["blank"])
        self.my_image_id = self.canvas.create_image(WIDTH_CENTER+320, HEIGHT_CENTER-50,
                                                    image=self.choice_images["blank"])

        self.canvas.create_image(WIDTH_CENTER, HEIGHT_CENTER-50, image=self.vs_image)

        self.score_text_id = self.canvas.create_text(WIDTH_CENTER, HEIGHT_CENTER-270, anchor="center",
                                                     text="0 / 0", font=("Aldrich Bold", 30), fill="#000000")
        self.timer_text_id = self.canvas.create_text(WIDTH_CENTER, HEIGHT_CENTER-210, anchor="center",
                                                     text="남은 시간: 30초", font=("Aldrich Bold", 20), fill="#000000")

        self.canvas.create_text(WIDTH_CENTER, HEIGHT_CENTER+200, anchor="center",
                                text="화면에 보이는 쪽을 보고 정답을 선택하세요", font=("Aldrich Bold", 20), fill="#000000")

        btn_scissors = Button(self, image=self.btn_img, text="가위",
                              font=("AnekGurmukhi Bold", 30), fg="#FFFFFF",
                              compound="center", command=lambda: self.play_click('scissors'),
                              borderwidth=0, relief="flat")
        btn_rock = Button(self, image=self.btn_img, text="바위",
                          font=("AnekGurmukhi Bold", 30), fg="#FFFFFF",
                          compound="center", command=lambda: self.play_click('rock'),
                          borderwidth=0, relief="flat")
        btn_paper = Button(self, image=self.btn_img, text="보",
                           font=("AnekGurmukhi Bold", 30), fg="#FFFFFF",
                           compound="center", command=lambda: self.play_click('paper'),
                           borderwidth=0, relief="flat")

        self.canvas.create_window(WIDTH_CENTER-300, HEIGHT_CENTER+300, window=btn_scissors)
        self.canvas.create_window(WIDTH_CENTER,     HEIGHT_CENTER+300, window=btn_rock)
        self.canvas.create_window(WIDTH_CENTER+300, HEIGHT_CENTER+300, window=btn_paper)

    def update_ui(self):
        self.canvas.itemconfig(self.score_text_id, text=f"푼 문제 : {self.total_tries}")
        self.canvas.itemconfig(self.timer_text_id, text=f"남은 시간: {self.remaining_time}초")
        self.canvas.itemconfig(self.opponent_image_id, image=self.opponent_choice)
        self.canvas.itemconfig(self.my_image_id, image=self.my_choice)

    def start_game(self):
        self.is_game_running = True
        self.correct_count = 0
        self.total_tries = 0
        self.start_time = time.time()
        self.remaining_time = self.duration_time
        self.prepare_new_round()
        self.update_timer()

    def update_timer(self):
        if not self.is_game_running:
            return
        elapsed = int(time.time() - self.start_time)
        self.remaining_time = max(0, self.duration_time - elapsed)
        self.update_ui()
        if self.remaining_time <= 0:
            self.end_game()
            return
        self.after(100, self.update_timer)

    def prepare_new_round(self):
        self.computer_is_actor = random.choice([True, False])
        self.img_card_pick = random.choice(CHOICES)
        if self.computer_is_actor:
            self.opponent_choice = self.choice_images[self.img_card_pick]
            self.my_choice = self.choice_images["blank"]
        else:
            self.opponent_choice = self.choice_images["blank"]
            self.my_choice = self.choice_images[self.img_card_pick]
        self.update_ui()

    def play_click(self, clicked_choice: str):
        if not self.is_game_running:
            return

        self.total_tries += 1

        if self.computer_is_actor:
            opponent_card = self.img_card_pick
            my_card = clicked_choice
            self.opponent_choice = self.choice_images[opponent_card]
            self.my_choice = self.choice_images[my_card]
        else:
            my_card = self.img_card_pick
            opponent_card = clicked_choice
            self.opponent_choice = self.choice_images[opponent_card]
            self.my_choice = self.choice_images[my_card]

        if WIN_RULE[my_card] == opponent_card:
            self.correct_count += 1

        self.update_ui()
        self.after(200, self.prepare_new_round)

    def end_game(self):
        self.is_game_running = False
        self.controller.scores["rsp"] = {
            "correct": self.correct_count,
            "total": self.total_tries
        }
        self.controller.show_frame("IntroClickGame")
