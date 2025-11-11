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

        # --- 상태 변수 ---
        self.total_questions = 0
        self.score = 0
        self.time_left = 30
        self.game_running = False
        self.current_sequence = []
        self.player_progress = []

        # 버튼 위치 (고정)
        self.positions = [
            (788, 524), (910, 524), (1032, 524),
            (788, 642), (911, 642), (1032, 642),
            (788, 760), (911, 760), (1032, 760)
        ]

        # 캔버스 생성 (먼저)
        self.canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        self.canvas.pack(fill="both", expand=True)

        # 배경 이미지 로드 (파일 없으면 예외 날 수 있으니 try)
        try:
            self.bg_image1 = PhotoImage(file=relative_to_assets("image_1.png"))
            self.canvas.create_image(960, 540, image=self.bg_image1)
            self.bg_image2 = PhotoImage(file=relative_to_assets("image_2.png"))
            self.canvas.create_image(959, 563, image=self.bg_image2)
        except Exception:
            pass

        # 텍스트: 타이머 / 점수 / total (총문제수)
        self.timer_text = self.canvas.create_text(
            884, 365, anchor="nw", text="00:30",
            fill="#07E597", font=("MonomaniacOne Regular", 32)
        )
        # score와 total은 같은 라인으로 보여주도록 변경
        self.score_text = self.canvas.create_text(
            1250, 266, anchor="nw", text="score : 0 / 0",
            fill="#FF5D00", font=("Baloo2 Regular", 28)
        )

        # 상태 라벨
        self.status_label = Label(self, text="1~9까지 순서대로 누르세요.",
                                  font=("Arial", 24), fg="black")
        self.canvas.create_window(960, 475, window=self.status_label, anchor="center")

        # 버튼 생성: 실제 Button 객체들을 미리 만들어 self.buttons 저장
        self.buttons = []
        for idx in range(1, 10):
            btn = Button(self, text=str(idx),
                         width=10, height=4,
                         bg="#703BA2", fg="white",
                         font=("Arial", 20),
                         command=lambda n=idx: self.button_click(n))
            self.buttons.append(btn)

        # 현재 버튼 윈도우 ID들을 보관 (shuffle 시 기존 윈도우를 삭제/재배치하기 위해)
        self.button_window_ids = [None] * 9

        # 우측 상단 / 중앙 시작 버튼 (이미지 로드 예외 처리)
        try:
            self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
            button_1 = Button(self, image=self.button_image_1,
                              borderwidth=0, relief="flat",
                              command=lambda: controller.show_frame("IntroClickGame"))
            self.canvas.create_window(1451, 140, window=button_1, anchor="nw")
        except Exception:
            pass

        try:
            self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
            button_2 = Button(self, image=self.button_image_2,
                              borderwidth=0, relief="flat",
                              command=self.start_game)
            self.canvas.create_window(910, 273, window=button_2, anchor="nw")
        except Exception:
            # 대체: 텍스트 버튼
            button_2 = Button(self, text="Start", command=self.start_game)
            self.canvas.create_window(910, 273, window=button_2, anchor="nw")

    # 조건 설명
    def sequence_description(self, seq):
        counts = {}
        for num in seq:
            counts[num] = counts.get(num, 0) + 1
        desc_list = [f"숫자 {num}는 {counts[num]}번 누르세요."
                    for num in range(1, 10) if num in counts and counts[num] > 1]
        base = " ".join(desc_list) if desc_list else "1~9까지 순서대로 누르세요."

        # 20자 단위로 강제 줄바꿈
        max_len = 46
        lines = [base[i:i+max_len] for i in range(0, len(base), max_len)]
        return "\n".join(lines)

    # 시퀀스 생성
    def generate_sequence(self):
        seq = []
        for num in range(1, 10):
            repeat = 1
            if random.random() < 0.3:
                repeat = random.randint(2, 4)
            seq.extend([num] * repeat)
        return seq

    # 버튼 섞기: 기존 create_window 누적 문제 해결
    def shuffle_buttons(self):
        # 기존에 생성된 버튼 윈도우가 있다면 삭제 (중복 방지)
        for i, win_id in enumerate(self.button_window_ids):
            if win_id is not None:
                try:
                    self.canvas.delete(win_id)
                except Exception:
                    pass
                self.button_window_ids[i] = None

        shuffled = self.positions[:]
        random.shuffle(shuffled)
        for idx, (btn, (x, y)) in enumerate(zip(self.buttons, shuffled)):
            # create_window 반환값 저장
            win_id = self.canvas.create_window(x, y, window=btn, anchor="nw", width=100, height=100)
            self.button_window_ids[idx] = win_id

    # 게임 시작
    def start_game(self):
        self.score = 0
        self.total_questions = 0
        self.time_left = 30
        self.game_running = True
        self.current_sequence = self.generate_sequence()
        self.player_progress = []
        # score_text shows "score : correct / total"
        self.canvas.itemconfig(self.score_text, text="score : 0 / 0")
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
                # 점수 저장
                self.controller.scores["clicknum"] = {
                    "correct": self.score,
                    "total": self.total_questions
                }
                # 타이머 끝나면 결과 페이지로 이동 (원하면 바꿔)
                self.controller.show_frame("IntroCompareGame")

    # 버튼 클릭 처리
    def button_click(self, num):
        if not self.game_running:
            return

        # 플레이어 입력 추가
        self.player_progress.append(num)

        # 올바른 접두사인지 확인
        if self.player_progress == self.current_sequence[:len(self.player_progress)]:
            # 시퀀스 완주
            if len(self.player_progress) == len(self.current_sequence):
                self.score += 1
                self.total_questions += 1
                # score 텍스트는 "score : correct / total"
                self.canvas.itemconfig(self.score_text, text=f"score : {self.score} / {self.total_questions}")
                # 다음 문제로
                self.current_sequence = self.generate_sequence()
                self.player_progress = []
                self.status_label.config(text=self.sequence_description(self.current_sequence))
                self.shuffle_buttons()
        else:
            # 틀린 경우: 한 문제로 카운트하고 다음 문제로
            self.total_questions += 1
            # 업데이트된 score/total 표시
            self.canvas.itemconfig(self.score_text, text=f"score : {self.score} / {self.total_questions}")
            self.player_progress = []
            self.current_sequence = self.generate_sequence()
            self.status_label.config(text=self.sequence_description(self.current_sequence))
            self.shuffle_buttons()

