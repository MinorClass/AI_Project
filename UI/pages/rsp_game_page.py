from tkinter import Canvas, Button, PhotoImage, Tk, font, Frame, Label
from PIL import Image, ImageTk
import os
from pathlib import Path
import time
import random

# 에셋 경로 (Figma에서 생성된 이미지들이 들어있는 폴더)
ASSETS_PATH = os.path.abspath("./UI/assets")
WIDTH_CENTER = 1920 //2
HEIGHT_CENTER = 1080 // 2
MAINCOLOR = "#703BA2"
# SUBCOLOR = 


def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

# 게임에서 이기는 경우 : 판단 딕셔너리 (key가 value를 이긴다)
WIN_RULE = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock"
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
        self.start_time = 30            # 총 게임 시간
        self.start_time = 0
        self.correct_count = 0          # 맞춘 개수 (승리 횟수)
        self.total_tries = 0            # 총 시도한 개수
        self.opponent_choice = None     # 상대방이 낸 패 (랜덤)
        self.my_choice = None           # 내가 낸 패 (랜덤)

        # --- 이미지 로드 ---
        self.images = {}
        self.load_imgaes()

        # --- UI 구성 ---
        self.setup_ui()

        # --- 게임 시작 ---
        self.start_game()


    # 가위바위보 이미지 로드
    def load_imgaes(self):
        self.images = {
            "rock": ImageTk.PhotoImage(Image.open(relative_to_assets("card_rock.png"))),
            "paper": ImageTk.PhotoImage(Image.open(relative_to_assets("card_paper.png"))),
            "scissors": ImageTk.PhotoImage(Image.open(relative_to_assets("card_scissors.png"))),
            "unknown": ImageTk.PhotoImage(Image.open(relative_to_assets("card_blank.png")))
        }

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

        # self.card_area = Frame(self, bg="#FFFFFF", padx=10, pady=10)
        # self.card_area.pack(fill="both", expand=True)
        
        # Label(self.card_area, text="상대방", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)
        # Label(self.card_area, text="나", font=("Arial", 16, "bold")).grid(row=0, column=2, pady=10)
        
        # self.opponent_card_label = Label(self.card_area, image=self.images.get("unknown"), relief="solid", bd=2)
        # self.opponent_card_label.grid(row=1, column=0, padx=50, pady=20)
        
        # Label(self.card_area, text="VS", font=("Arial", 40, "bold")).grid(row=1, column=1)
        
        # self.my_card_label = Label(self.card_area, image=self.images.get("unknown"), relief="solid", bd=2)
        # self.my_card_label.grid(row=1, column=2, padx=50, pady=20)
        
        # self.card_area.grid_columnconfigure((0, 2), weight=1)


        # --- 카드 영역(computer) ---
        canvas.create_text(WIDTH_CENTER-320,HEIGHT_CENTER-280,
                           anchor="center", 
                           text="상대방", font=("Aldrich Bold", 30),
                           fill ="#000000"
                           )
        canvas.create_image(WIDTH_CENTER-320, HEIGHT_CENTER-50, image=self.images.get("unknown"))

        # --- 카드 영역(me) ---
        canvas.create_text(WIDTH_CENTER+320,HEIGHT_CENTER-280,
                           anchor="center", 
                           text="나", font=("Aldrich Bold", 30),
                           fill ="#000000"
                           )
        canvas.create_image(WIDTH_CENTER+320, HEIGHT_CENTER-50, image=self.images.get("unknown"))

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
                              command=lambda: print("scissors"),
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
                              command=lambda: print('rock'),
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
                              command=lambda: print("paper"),
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
                           text="00/00", font=("Aldrich Bold", 30),
                           fill ="#000000")
        # Timer 텍스트
        canvas.create_text(WIDTH_CENTER,HEIGHT_CENTER-210, anchor="center", 
                           text="00:00:00", font=("Aldrich Bold", 20),
                           fill ="#000000")

    # ========================================
    # 가위바위보 게임 함수
    # ========================================
    
    def start_game(self):
        """게임 시작 및 타이머 초기화"""
        self.is_game_running = True
        self.start_time = time.time()
        self.correct_count = 0
        self.total_tries = 0
        # self.update_timer()             # 타이머 시작
        # self.next_round()               # 첫 문제 출제

    def update_timer(self):
        """100ms마다 타이머를 업데이트하고 게임 종료를 확인"""
        # if not self.is_game_running:
        #     self.opponent_choice
    
        # for i, 

        # for i, choice in enumerate(CHOICES):
        #     btn = Button(
        #         self.button_frame,
        #         image=None, #self.images.get("button_bg"), # 버튼 배경 이미지 (없으면 None)
        #         text=choice.upper(),
        #         compound="center", # 텍스트를 이미지 중앙에 배치
        #         font=("Arial", 18, "bold"),
        #         fg="white",
        #         command=lambda c=choice: self.check_answer(c)
        #     )
        #     btn.grid(row=0, column=i, padx=20, pady=10, sticky="ew")
        #     self.button_frame.grid_columnconfigure(i, weight=1)

    # def start_game(self):
    #     """게임 시작 및 타이머 초기화"""
    #     self.is_game_running = True
    #     self.start_time = time.time()
    #     self.correct_count = 0
    #     self.total_tries = 0
    #     self.update_timer()
    #     self.next_round()

    # def update_timer(self):
    #     """100ms마다 타이머를 업데이트하고 게임 종료를 확인"""
    #     if not self.is_game_running:
    #         return

    #     elapsed_time = time.time() - self.start_time
    #     remaining_time = self.total_time - elapsed_time
        
    #     if remaining_time <= 0:
    #         self.is_game_running = False
    #         self.timer_label.config(text="진행시간\n00:00:00")
    #         print("게임 종료! 최종 점수:", self.score_label.cget("text"))
    #         return

    #     # 시간 표시 형식 포맷 (MM:SS:ms)
    #     minutes = int(elapsed_time // 60)
    #     seconds = int(elapsed_time % 60)
    #     ms = int((elapsed_time - int(elapsed_time)) * 100)
    #     time_str = f"진행시간\n{minutes:02}:{seconds:02}:{ms:02}"
    #     self.timer_label.config(text=time_str)

    #     # 100ms 후 다시 호출
    #     self.window.after(100, self.update_timer)

    # def next_round(self):
    #     """새로운 문제를 출제"""
    #     if not self.is_game_running:
    #         return
        
    #     # 1. 상대방의 선택을 랜덤으로 결정
    #     self.opponent_choice = random.choice(CHOICES)
        
    #     # 2. 상대방 카드 UI 업데이트
    #     # 상대방 카드는 '?' 이미지로 다시 설정하거나, 이번 라운드의 선택을 바로 표시할 수 있습니다.
    #     # 여기서는 바로 상대방의 선택을 보여주고, '내가 이기는' 패를 고르게 합니다.
    #     self.opponent_label.config(image=self.images[self.opponent_choice])
        
    #     # 3. 내 카드 UI 초기화
    #     self.my_label.config(image=self.images["unknown"])

    # def check_answer(self, user_choice):
    #     """사용자 버튼 클릭 시 정답 확인"""
    #     if not self.is_game_running or not self.opponent_choice:
    #         return
        
    #     self.total_tries += 1
        
    #     # 1. 사용자의 선택을 '내 카드' 영역에 표시
    #     self.my_label.config(image=self.images[user_choice])
        
    #     # 2. 승리 로직 확인: 상대방의 패(opponent_choice)를 이기는 패가 user_choice인지 확인
    #     # ex: 상대가 'rock'이면, 이기는 패는 'paper'입니다.
        
    #     # 상대방의 패를 이기는 패를 찾음
    #     winning_hand = next(k for k, v in WIN_RULES.items() if v == self.opponent_choice)
        
    #     if user_choice == winning_hand:
    #         # 정답 (승리)
    #         self.correct_count += 1
    #         print(f"✅ 정답! 상대({self.opponent_choice}) vs 나({user_choice})")
    #     elif user_choice == self.opponent_choice:
    #         # 무승부
    #         print(f"🤝 무승부! 상대({self.opponent_choice}) vs 나({user_choice})")
    #     else:
    #         # 패배 (오답)
    #         print(f"❌ 오답! 상대({self.opponent_choice}) vs 나({user_choice})")
        
    #     # 3. 스코어 업데이트
    #     self.score_label.config(text=f"맞춘 개수\n{self.correct_count}/{self.total_tries}")
        
    #     # 4. 잠시 후 다음 라운드 시작
    #     self.window.after(1000, self.next_round)

# if __name__ == "__main__":
#     app_window = tk.Tk()
#     # 💡 주의: 이 코드는 반드시 'assets' 폴더에 'rock.png', 'scissors.png', 'paper.png', 'question_mark.png' 
#     # (선택적으로 'button_bg.png') 파일이 있어야 정상 실행됩니다.
#     game_app = RPS_GUI(app_window)
#     app_window.mainloop()


        # ## computer vs player
        # img_blank = ImageTk.PhotoImage(Image.open(relative_to_assets("card_blank.png")))
        # #computer 영역
        # self.computer_label = Label(self, bg ="#FFFFFF")
        # computerArea = Frame(self,image = img_blank)
        # canvas.create_window(960, 480, window=self.video_label, width=300, height=300)
        # computerArea.place(x=WEIGHT_CENTER - 300, y=HEIGHT_CENTER - 100, anchor="center")
        #player 영역
        # playerArea = Frame(self, image = img_blank)
        # playerArea.place(x=WEIGHT_CENTER + 300, y=HEIGHT_CENTER - 100, anchor="center")







        #     #상대방 이미지 창 박스 크기는 w361 h375
        # self.image2 = PhotoImage(file=relative_to_assets("image_blank.png"))
        # canvas.create_image(377,316, image=self.image2, anchor="nw")
        #     #나 이미지 창
        # self.image3 = PhotoImage(file=relative_to_assets("image_blank.png"))
        # canvas.create_image(1183,316, image=self.image3, anchor="nw")

        # self.image4 = PhotoImage(file=relative_to_assets("image_vs.png"))
        # canvas.create_image(769,419, image=self.image4, anchor="nw")


        # # 텍스트
        # canvas.create_text(
        #     385,
        #     253,
        #     anchor="nw",
        #     text="상대방",
        #     fill="#000000",
        #     font=("Aldrich Bold", 24)
        # )

        # canvas.create_text(
        #     1185,
        #     253,
        #     anchor="nw",
        #     text="나",
        #     fill="#000000",
        #     font=("Aldrich Bold", 24)
        # )


        # # 버튼 이미지
        # #가위
        # self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        # button_1 = Button(self, image=self.button_image_1,
        #                   command=lambda: controller.quit(),
        #                   borderwidth=0, relief="flat")
        # canvas.create_window(372, 726, window=button_1, anchor="nw")

        # #바위
        # self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        # button_2 = Button(self, image=self.button_image_2,
        #                   command=lambda: controller.quit(),
        #                   borderwidth=0, relief="flat")
        # canvas.create_window(774, 726, window=button_2, anchor="nw")

        # #보
        # self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        # button_3 = Button(self, image=self.button_image_3,
        #                   command=lambda: controller.show_frame("IntroClickGame"),
        #                   borderwidth=0, relief="flat")
        # canvas.create_window(1178, 726, window=button_3, anchor="nw")



# ========================================
# 게임용 함수들
# ========================================
class RPS_Game: 
    def __init__(self):
        # --- 게임 상태 변수 ---
        self.is_game_running = False
        self.total_time = 30  # 지속시간
        self.start_time = None
        self.end_time = None
        self.correct_count = 0
        self.total_tries = 0
        # 상대방이 낸 패는 랜덤
        self.choice = None
        self.who = ['computer', 'you']

        self.score_rsp = 0

    def load_img(self, choice):
        """선택지에 따른 이미지 로드"""
        if choice == 'rock':
            img_path = relative_to_assets("card_rock.png")
        elif choice == 'paper':
            img_path = relative_to_assets("card_paper.png")
        elif choice == 'scissors':
            img_path = relative_to_assets("card_scissors.png")
        else:
            img_path = relative_to_assets("card_blank.png")
        return ImageTk.PhotoImage(Image.open(img_path))

    def runGame(self, gameId=None, duration = 30): #게임 실행
        import random

        while self.is_game_running:
            blank_pick = random.choice(self.choices)
            who_pick = random.choice(self.who)

            print('\n----------------------------------------------')
            print('내가 이겨야합니다(30초 경과 시 자동 종료)')
            print('\n----------------------------------------------')

            # --- 가위바위보 게임 로직 시작 ---
            if who_pick == 'computer':
                print (f'Computer: {blank_pick}')
                player_pick = input('rock scissors paper <-- One choice   ').upper()
                if  (blank_pick == 'rock' and player_pick == 'paper') or \
                    (blank_pick == 'scissors' and player_pick == 'rock') or \
                    (blank_pick == 'paper' and player_pick == 'scissors'):
                    self.correct_count += 1
            elif who_pick =='you':
                print (f'You: {blank_pick}')
                computer_pick = input('rock scissors paper <-- One choice   ').upper()
                if  (blank_pick == 'paper' and computer_pick == 'rock') or \
                    (blank_pick == 'rock' and computer_pick == 'scissors') or \
                    (blank_pick == 'scissors' and computer_pick == 'paper'):
                    self.correct_count += 1
            
            self.solved_count += 1
        
        # --- 최종점수 출력 ---
        self.score_rsp = (self.correct_count / self.solved_count) *100
        print(f'Score: {self.score_rsp}점')