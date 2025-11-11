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
WIN_RULE: Dict[str, str] = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock",
    "blank": "blank"
}
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

        self.correct_count = 0        # 맞춘 수
        self.total_tries = 0         # 전체 시도 수 (한 클릭당 +1)
        self.img_card_pick = None    # 현재 라운드에 '보여진' 카드 값 (rock/paper/scissors)
        self.computer_is_actor = None  # True -> 상대(왼쪽)가 보여짐; False -> 나(오른쪽)가 보여짐

        # 이미지 캐시
        self.choice_images: Dict[str, ImageTk.PhotoImage] = {}
        self.load_images()

        # UI 세팅
        self.setup_ui()

        # 첫 라운드 준비 (게임 시작 전에 화면에 한쪽 카드가 보이게)
        # start_game() 호출하면 타이머 시작 및 라운드 반복
        self.start_game()

    # 이미지 로드
    def load_images(self):
        for choice in CHOICES + ["blank"]:
            path = relative_to_assets(f"card_{choice}.png")
            self.choice_images[choice] = ImageTk.PhotoImage(Image.open(path))
        # 버튼 이미지 (같은 이미지로 사용)
        self.btn_img = ImageTk.PhotoImage(Image.open(relative_to_assets("btn_pupple.png")))
        # vs, background, win 이미지 (선택적)
        self.vs_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_vs.png")))
        self.bg_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_background.png")))
        # win image may exist; if not, ignore errors externally

    # UI 구성 — canvas와 요소들을 인스턴스 ID로 저장
    def setup_ui(self):
        self.canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        self.canvas.pack(fill="both", expand=True)

        # 배경
        self.canvas.create_image(960, 540, image=self.bg_image)

        # 타이틀 / 레이블
        self.canvas.create_text(400, 162, anchor="center", text="가위바위보",
                                fill="#FFFFFF", font=("Malgun Gothic", 25))
        self.canvas.create_text(WIDTH_CENTER-320, HEIGHT_CENTER-280, anchor="center",
                                text="상대방", font=("Aldrich Bold", 30), fill="#000000")
        self.canvas.create_text(WIDTH_CENTER+320, HEIGHT_CENTER-280, anchor="center",
                                text="나", font=("Aldrich Bold", 30), fill="#000000")

        # 카드 이미지 자리(초기엔 blank로 설정)
        self.opponent_image_id = self.canvas.create_image(WIDTH_CENTER-320, HEIGHT_CENTER-50,
                                                          image=self.choice_images["blank"])
        self.my_image_id = self.canvas.create_image(WIDTH_CENTER+320, HEIGHT_CENTER-50,
                                                    image=self.choice_images["blank"])

        # VS 이미지
        self.canvas.create_image(WIDTH_CENTER, HEIGHT_CENTER-50, image=self.vs_image)

        # 점수/타이머 텍스트 (ID 저장)
        self.score_text_id = self.canvas.create_text(WIDTH_CENTER, HEIGHT_CENTER-270, anchor="center",
                                                     text="0 / 0", font=("Aldrich Bold", 30), fill="#000000")
        self.timer_text_id = self.canvas.create_text(WIDTH_CENTER, HEIGHT_CENTER-210, anchor="center",
                                                     text="남은 시간: 30초", font=("Aldrich Bold", 20), fill="#000000")

        # 설명 텍스트
        self.canvas.create_text(WIDTH_CENTER, HEIGHT_CENTER+200, anchor="center",
                                text="화면에 보이는 쪽을 보고 정답을 선택하세요", font=("Aldrich Bold", 20), fill="#000000")

        # 버튼들: 클릭 시 play_click(choice) 호출
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

    # UI 갱신: 점수, 타이머, 카드 이미지 갱신
    def update_ui(self):
        # 점수 텍스트: correct / total
        self.canvas.itemconfig(self.score_text_id, text=f"{self.correct_count} / {self.total_tries}")
        # 타이머 텍스트
        self.canvas.itemconfig(self.timer_text_id, text=f"남은 시간: {self.remaining_time}초")
        # 카드 이미지 (현재 라운드의 '보여진' 상태를 반영)
        # opponent_choice, my_choice는 항상 존재 (이미지 객체)
        self.canvas.itemconfig(self.opponent_image_id, image=self.opponent_choice)
        self.canvas.itemconfig(self.my_image_id, image=self.my_choice)

    # 게임 시작: 타이머 시작 후 첫 라운드 준비
    def start_game(self):
        self.is_game_running = True
        self.correct_count = 0
        self.total_tries = 0
        self.start_time = time.time()
        self.remaining_time = self.duration_time
        # 즉시 한 라운드를 준비해 화면에 보여줌
        self.prepare_new_round()
        # 타이머 갱신 시작
        self.update_timer()

    # 타이머 갱신 (after 기반으로 UI 멈춤 없음)
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

    # 라운드 준비: 누가 카드를 보일지 랜덤으로 정하고 '보여진' 카드 셋업
    def prepare_new_round(self):
        # 랜덤으로 어느 쪽에 문제가 보일지 결정
        self.computer_is_actor = random.choice([True, False])
        # 보여지는 카드 결정
        self.img_card_pick = random.choice(CHOICES)
        # 셋업: 보여진 쪽에는 카드, 반대쪽은 blank
        if self.computer_is_actor:
            # 상대(왼쪽)가 보여짐, 오른쪽은 blank
            self.opponent_choice = self.choice_images[self.img_card_pick]
            self.my_choice = self.choice_images["blank"]
        else:
            # 나(오른쪽)가 보여짐, 왼쪽은 blank
            self.opponent_choice = self.choice_images["blank"]
            self.my_choice = self.choice_images[self.img_card_pick]
        # 화면 반영
        self.update_ui()

    # 사용자가 버튼을 눌렀을 때 처리
    # 클릭한 choice는 '사용자가 선택한 카드' 역할을 상황에 따라 다르게 해석
    def play_click(self, clicked_choice: str):
        if not self.is_game_running:
            return

        # 한 번의 클릭이 하나의 라운드 시도
        self.total_tries += 1

        # 상황 해석:
        # - 만약 상대가 보여진 상태(computer_is_actor == True):
        #     상대가 img_card_pick을 보여주고 있으므로 사용자의 클릭은 '내가 낸 카드'로 해석
        #     -> my_card = clicked_choice, opponent_card = img_card_pick
        # - 만약 내가 보여진 상태(computer_is_actor == False):
        #     내가 img_card_pick을 보여주고 있으므로 사용자의 클릭은 '상대가 낸 카드'로 해석
        #     -> my_card = img_card_pick, opponent_card = clicked_choice
        if self.computer_is_actor:
            opponent_card = self.img_card_pick
            my_card = clicked_choice
            # 화면: 보여진 상대 카드(왼쪽)와 사용자가 낸 카드(오른쪽) 모두 표시
            self.opponent_choice = self.choice_images[opponent_card]
            self.my_choice = self.choice_images[my_card]
        else:
            my_card = self.img_card_pick
            opponent_card = clicked_choice
            # 화면: 보여진 내 카드(오른쪽)와 사용자가(=상대역) 선택한 카드(왼쪽) 모두 표시
            self.opponent_choice = self.choice_images[opponent_card]
            self.my_choice = self.choice_images[my_card]

        # 정답 판단: 항상 '내가 이겨야 정답' 기준
        if WIN_RULE[my_card] == opponent_card:
            self.correct_count += 1

        # UI 즉시 갱신해서 선택 결과를 보여줌
        self.update_ui()

        # 잠깐 결과를 보여준 뒤 다음 라운드로 (0.5초)
        self.after(500, self.prepare_new_round)

    # 게임 종료: 점수 저장
    def end_game(self):
        self.is_game_running = False
        # 컨트롤러에 correct/total 저장
        self.controller.scores["rsp"] = {
            "correct": self.correct_count,
            "total": self.total_tries
        }
        print(f"가위바위보 종료: {self.correct_count}승 / {self.total_tries}판")
        # 다음 화면 이동은 외부에서 결정하도록 남겨둠
