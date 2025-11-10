import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, Label
import random, time
from pathlib import Path

class CompareGame(tk.Frame):
    MIN_WORDS = 9
    MAX_WORDS = 20
    FONT_SIZE_MIN = 11
    FONT_SIZE_MAX = 19

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")
        self.controller = controller

        self.WORDS = ["준혁", "혜인", "승현", "준희"]
        self.TOTAL_QUESTIONS = 10
        self.LEFT_AREA = (336, 388, 836, 888)
        self.RIGHT_AREA = (1085, 388, 1585, 888)

        self.remaining = self.TOTAL_QUESTIONS
        self.score = 0
        self.game_running = False
        self.start_time = None
        self.answer_expected = None

        self.current_left_word = None
        self.current_right_word = None
        self.count_left = 0
        self.count_right = 0

        self.timer_after_id = None
        self.answer_after_id = None

        self.load_assets()
        self.setup_ui()
        self.bind_events()

    def load_assets(self):
        ASSETS_PATH = Path("./UI/assets/compare_quantity_game")
        self.relative_to_assets = lambda path: ASSETS_PATH / Path(path)

        self.bg1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.bg2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.left_img = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.right_img = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.center_img = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.btn_img_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.btn_img_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))

    def setup_ui(self):
        self.canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(960, 540, image=self.bg1)
        self.canvas.create_image(959, 563, image=self.bg2)
        self.canvas.create_image(586, 638, image=self.left_img)
        self.canvas.create_image(1335, 638, image=self.right_img)
        self.canvas.create_image(959, 629, image=self.center_img)

        self.timer_text_id = self.canvas.create_text(320, 238, anchor="nw", text="진행시간\n00:00:00",
                                                     fill="#000000", font=("Inter Light", 18))
        self.remain_text_id = self.canvas.create_text(1411, 258, anchor="nw", text="남은 문항 : 10",
                                                      fill="#000000", font=("Inter Light", 18))

        self.info_label = Label(self, text="", font=("Arial", 20), fg="red", bg=None, anchor="center")
        self.canvas.create_window(960, 940, window=self.info_label)

        self.button_1 = Button(self, image=self.btn_img_1, borderwidth=0, highlightthickness=0,
                               command=lambda: print("button_1 clicked"), relief="flat")
        self.canvas.create_window(1501, 147, window=self.button_1, width=168, height=66)

        self.start_button = Button(self, image=self.btn_img_2, borderwidth=0, highlightthickness=0,
                                   command=self.start_game, relief="flat")
        self.canvas.create_window(830, 258, window=self.start_button, width=257, height=81)

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.handle_canvas_click)

    def handle_canvas_click(self, event):
        if not self.game_running or self.answer_expected is None:
            return

        x, y = event.x, event.y
        if self.LEFT_AREA[0] <= x <= self.LEFT_AREA[2] and self.LEFT_AREA[1] <= y <= self.LEFT_AREA[3]:
            self.judge_answer(self.current_left_word)
        elif self.RIGHT_AREA[0] <= x <= self.RIGHT_AREA[2] and self.RIGHT_AREA[1] <= y <= self.RIGHT_AREA[3]:
            self.judge_answer(self.current_right_word)

    def update_timer(self):
        if not self.game_running or self.start_time is None:
            return

        elapsed = int(time.time() - self.start_time)
        h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
        self.canvas.itemconfig(self.timer_text_id, text=f"진행시간\n{h:02d}:{m:02d}:{s:02d}")

        if self.timer_after_id:
            self.after_cancel(self.timer_after_id)

        self.timer_after_id = self.after(1000, self.update_timer)

    def show_words_once(self):
        self.canvas.delete("word")
        self.info_label.config(text="")

        self.current_left_word = random.choice(self.WORDS)
        right_candidates = [w for w in self.WORDS if w != self.current_left_word]
        self.current_right_word = random.choice(right_candidates)

        self.count_left = random.randint(self.MIN_WORDS, self.MAX_WORDS)
        self.count_right = random.randint(self.MIN_WORDS, self.MAX_WORDS)
        while self.count_right == self.count_left:
            self.count_right = random.randint(self.MIN_WORDS, self.MAX_WORDS)

        self.answer_expected = self.current_left_word if self.count_left > self.count_right else self.current_right_word

        self.place_word(self.LEFT_AREA, self.current_left_word, self.count_left, "word")
        self.place_word(self.RIGHT_AREA, self.current_right_word, self.count_right, "word")

        self.after(2000, self.ask_answer)

    def ask_answer(self):
        self.info_label.config(text="더 많은 단어를 클릭하세요 (3초 제한)")

        if self.answer_after_id:
            self.after_cancel(self.answer_after_id)

        self.answer_after_id = self.after(3000, self.judge_and_next)

    def judge_answer(self, selected_word):
        if not self.game_running:
            return

        if self.answer_after_id:
            self.after_cancel(self.answer_after_id)
            self.answer_after_id = None

        if selected_word == self.answer_expected:
            self.score += 1
            self.info_label.config(text=f"정답! ({selected_word})")
        else:
            self.info_label.config(text=f"오답! 정답은 {self.answer_expected}")

        self.remaining -= 1
        self.canvas.itemconfig(self.remain_text_id, text=f"남은 문항 : {self.remaining}")

        if self.remaining > 0:
            self.after(1000, self.show_words_once)
        else:
            self.canvas.delete("word")
            self.info_label.config(text=f"게임 종료! 최종 점수는 {self.score}점입니다.")
            self.after(1000, self.go_to_next_page)

    def judge_and_next(self):
        if self.answer_after_id:
            self.after_cancel(self.answer_after_id)
            self.answer_after_id = None

        self.info_label.config(text=f"시간 초과! 정답은 {self.answer_expected}")
        self.remaining -= 1
        self.canvas.itemconfig(self.remain_text_id, text=f"남은 문항 : {self.remaining}")

        if self.remaining > 0:
            self.after(1000, self.show_words_once)
        else:
            self.canvas.delete("word")
            self.info_label.config(text=f"게임 종료! 최종 점수는 {self.score}점입니다.")
            self.after(1000, self.go_to_next_page)

    def go_to_next_page(self):
        self.end_game_cleanup()
        self.controller.show_frame("WaitResult")

    def end_game_cleanup(self):
        self.game_running = False
        self.start_time = None
        self.remaining = self.TOTAL_QUESTIONS

        if self.timer_after_id:
            self.after_cancel(self.timer_after_id)
            self.timer_after_id = None

    def start_game(self):
        if self.game_running:
            return
        self.game_running = True
        self.start_time = time.time()
        self.remaining = self.TOTAL_QUESTIONS
        self.score = 0
        self.canvas.itemconfig(self.remain_text_id, text=f"남은 문항 : {self.remaining}")
        self.update_timer()
        self.show_words_once()

    def place_word(self, area, word, count, tag):
        placed = []
        for _ in range(count):
            for _ in range(100):
                x = random.randint(area[0], area[2])
                y = random.randint(area[1], area[3])
                size = random.randint(self.FONT_SIZE_MIN, self.FONT_SIZE_MAX)

                # 기존 좌표들과 충돌하지 않도록 거리 확인
                if all((abs(x - px) > size + ps + 10 and abs(y - py) > size + ps + 10)
                       for px, py, ps in placed):
                    self.canvas.create_text(x, y, text=word, font=("Arial", size),
                                            fill="black", tags=tag)
                    placed.append((x, y, size))
                    break
