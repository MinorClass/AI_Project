from tkinter import Canvas, Button, PhotoImage, Tk, font, Frame, Label
from PIL import Image, ImageTk
import os
from pathlib import Path
import time
import random
from typing import Dict, List

# 에셋 경로 (Figma에서 생성된 이미지들이 들어있는 폴더)
ASSETS_PATH = os.path.abspath("./UI/assets")
WIDTH_CENTER = 1920 //2
HEIGHT_CENTER = 1080 // 2
MAINCOLOR = "#703BA2"
# SUBCOLOR = 


def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

# 게임에서 이기는 경우 : 판단 딕셔너리 (key가 value를 이긴다)
WIN_RULE: Dict[str, str] = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock",
    "blank" : "blank"
}
CHOICES = list(WIN_RULE.keys())

# ========================================
# 가위바위보 게임 페이지
# ========================================

class RSPGame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")

        # --- 게임 상태 변수 초기화 ---
        self.is_game_running = False
        self.duration_time = 30                 # 총 게임 시간
        self.start_time = 0            
        self.remaining_time = 0
        self.correct_count = 0                  # 맞춘 개수 (승리 횟수)
        self.total_tries = 0                    # 총 시도한 개수
        self.opponent_choice = None             # 상대방이 낸 패 (랜덤)
        self.my_choice = None                   # 내가 낸 패 (랜덤)
        self.img_card_pick = None
        self.computer_is_actor = None

        # --- 이미지 로드 ---
        self.choice_images: Dict[str, ImageTk.PhotoImage] = {}
        self.load_imgaes()
        self.card_pick()


        # --- UI 구성 ---
        self.setup_ui()

        # --- 게임 시작 ---
        self.start_game()

       

    # 가위바위보 이미지 로드
    def load_imgaes(self):
        for choice in CHOICES:
            path = relative_to_assets(f"card_{choice}.png")
            img_card = ImageTk.PhotoImage(Image.open(path))
            self.choice_images[choice] = img_card

    # UI 구성
    def setup_ui(self):
        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)
   
        # 배경 이미지
        self.bg_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_background.png")))
        canvas.create_image(960, 540, image=self.bg_image)
        self.win_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_win.png")))
        canvas.create_image(960.0, 550.0, image=self.win_image)

        # 상단 타이틀
        canvas.create_text( 
            400,
            162,
            anchor="center",
            text="가위바위보",
            fill='#FFFFFF',
            font=("Malgun Gothic", 25)
        )

        # --- 카드 영역(computer) ---
        canvas.create_text(WIDTH_CENTER-320,HEIGHT_CENTER-280,
                           anchor="center", 
                           text="상대방", font=("Aldrich Bold", 30),
                           fill ="#000000"
                           )
        canvas.create_image(WIDTH_CENTER-320, HEIGHT_CENTER-50, image=self.opponent_choice)

        # --- 카드 영역(me) ---
        canvas.create_text(WIDTH_CENTER+320,HEIGHT_CENTER-280,
                           anchor="center", 
                           text="나", font=("Aldrich Bold", 30),
                           fill ="#000000"
                           )

        canvas.create_image(WIDTH_CENTER+320, HEIGHT_CENTER-50, image=self.my_choice)

        # vs 이미지
        self.vs_image = ImageTk.PhotoImage(Image.open(relative_to_assets("img_vs.png")))
        canvas.create_image(WIDTH_CENTER, HEIGHT_CENTER-50, image=self.vs_image)

        # --- 버튼 영역 ---
        self.btn_scissors= self.btn_rock= self.btn_paper = ImageTk.PhotoImage(Image.open(relative_to_assets("btn_pupple.png")))
        # 가위 버튼
        btn_scissors = Button(self, 
                              image=self.btn_scissors,
                              text="가위",
                              font=("AnekGurmukhi Bold", 30),
                              fg="#FFFFFF",
                              compound="center",
                              command= self.determine_winner('scissors', self.img_card_pick, self.computer_is_actor),
                              borderwidth=0,
                              relief="flat")
        canvas.create_window(WIDTH_CENTER-300, HEIGHT_CENTER+300, window=btn_scissors)
        # 바위 버튼
        btn_rock = Button(self, 
                              image=self.btn_rock,
                              text="바위",
                              font=("AnekGurmukhi Bold", 30),
                              fg="#FFFFFF",
                              compound="center",
                              command=self.determine_winner('rock', self.img_card_pick, self.computer_is_actor),
                              borderwidth=0,
                              relief="flat")
        canvas.create_window(WIDTH_CENTER, HEIGHT_CENTER+300, window=btn_rock)
        # 보 버튼
        btn_paper = Button(self, 
                              image=self.btn_paper,
                              text="보",
                              font=("AnekGurmukhi Bold", 30),
                              fg="#FFFFFF",
                              compound="center",
                              command=self.determine_winner('paper', self.img_card_pick, self.computer_is_actor),
                              borderwidth=0,
                              relief="flat")
        canvas.create_window(WIDTH_CENTER+300, HEIGHT_CENTER+300, window=btn_paper)

        # 게임 조건
        canvas.create_text(WIDTH_CENTER, HEIGHT_CENTER+200, anchor="center", 
                           text="내가 이겨야 합니다!", font=("Aldrich Bold", 24),
                           fill ="#000000"
                           )

        # 점수 텍스트
        canvas.create_text(WIDTH_CENTER,HEIGHT_CENTER-270, anchor="center", 
                           text=self.total_tries, font=("Aldrich Bold", 30),
                           fill ="#000000")
        # Timer 텍스트
        canvas.create_text(WIDTH_CENTER,HEIGHT_CENTER-210, anchor="center", 
                           text=self.remaining_time, font=("Aldrich Bold", 20),
                           fill ="#000000")

    # ========================================
    # 가위바위보 게임 함수
    # ========================================
    
    def start_game(self):
        """게임 시작 및 타이머 초기화"""
        self.is_game_running = True
        self.correct_count = 0
        self.total_tries = 1
        # self.update_timer()             # 타이머 시작
        

    def update_timer(self):
        """100ms마다 타이머를 업데이트하고 게임 종료를 확인"""
        self.start_time = time.time()
        while self.is_game_running:
            self.remaining_time = int(self.duration_time - (time.time()-self.start_time))

            if self.remaining_time <= 0:
                self.is_game_running = False
                break

            time.sleep(0.1)

    def determine_winner(self, choice_a :str, choice_b: str, computer_is_actor:bool) ->str:
        """
        랜덤 행위자 규칙에 따라 승패를 판단한다
        Args:
            choice_a: 사용자가 누른 카드 (rock/scissors/paper).
            choice_b: 컴퓨터가 랜덤으로 뽑은 카드.
            computer_is_actor: True면 컴퓨터가 카드를 뽑았고, False면 사용자가 카드를 뽑았습니다.
        """
        # 승리조건
        if computer_is_actor :
            # key가 valuse를 이긴다
            if choice_b == WIN_RULE.get(choice_a):
                self.correct_count += 1
        else:
            if choice_a == WIN_RULE.get(choice_b):
                self.correct_count += 1

        self.total_tries += 1

        self.card_pick()
                

    def card_pick(self) :
        """
        사용자가 버튼을 클릭할때마다 게임 로직 실행
        """
    
        # 1. 누가 무슨 카드를 뽑을지 선택
        self.computer_is_actor = random.choice([True, False])
        self.img_card_pick = random.choice(['rock', 'paper', 'scissors'])
        # 2. 카드 선택
        if self.computer_is_actor :
            self.opponent_choice = self.choice_images.get(self.img_card_pick)
            self.my_choice = self.choice_images.get('blank')
        else :
            self.opponent_choice = self.choice_images.get('blank')
            self.my_choice = self.choice_images.get(self.img_card_pick)


        
