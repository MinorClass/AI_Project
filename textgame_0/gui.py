import random, time
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Entry, Label

class WordGameApp:
    MIN_WORDS = 9
    MAX_WORDS = 20
    FONT_SIZE_MIN = 11
    FONT_SIZE_MAX = 19

    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.configure(bg="#FFFFFF")
        self.canvas = Canvas(root, bg="#FFFFFF", height=1080, width=1920, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.WORDS = ["준혁", "혜인", "승현", "준희"]
        self.TOTAL_QUESTIONS = 40
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

        self.load_assets()
        self.setup_ui()
        self.bind_events()

        self.timer_after_id = None
        self.answer_after_id = None

    def load_assets(self):
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"/home/l/L_test/LL/Tkinter-Designer/build/assets/frame0")
        self.relative_to_assets = lambda path: ASSETS_PATH / Path(path)

        self.bg1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.bg2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.left_img = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.right_img = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.center_img = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.btn_img_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.btn_img_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))

    def setup_ui(self):
        self.canvas.create_image(960, 540, image=self.bg1)
        self.canvas.create_image(959, 563, image=self.bg2)
        self.canvas.create_image(586, 638, image=self.left_img)
        self.canvas.create_image(1335, 638, image=self.right_img)
        self.canvas.create_image(959, 629, image=self.center_img)

        self.timer_text_id = self.canvas.create_text(320, 238, anchor="nw", text="진행시간\n00:00:00",
                                                     fill="#000000", font=("Inter Light", 18))
        self.remain_text_id = self.canvas.create_text(1411, 258, anchor="nw", text="남은 문항 : 40",
                                                      fill="#000000", font=("Inter Light", 18))

        self.info_label = Label(self.root, text="", font=("Arial", 20), fg="red", bg=None, anchor="center")
        self.info_label.place(relx=0.5, y=940, anchor="center")

        self.answer_entry = Entry(self.root, font=("Arial", 20))
        self.answer_entry.place(x=760, y=860, width=400)

        self.button_1 = Button(image=self.btn_img_1, borderwidth=0, highlightthickness=0,
                               command=lambda: print("button_1 clicked"), relief="flat")
        self.button_1.place(x=1501, y=147, width=168, height=66)

        self.start_button = Button(image=self.btn_img_2, borderwidth=0, highlightthickness=0,
                                   command=self.start_game, relief="flat")
        self.start_button.place(x=830, y=258, width=257, height=81)

    def bind_events(self):
        self.answer_entry.bind("<Return>", self.judge_answer)

    def update_timer(self):
        if not self.game_running or self.start_time is None:
            return
        
        elapsed = int(time.time() - self.start_time)
        h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
        self.canvas.itemconfig(self.timer_text_id, text=f"진행시간\n{h:02d}:{m:02d}:{s:02d}")
        
        # 이전 예약 취소 (중복 방지)
        if self.timer_after_id:
            self.root.after_cancel(self.timer_after_id)
        
        # 새 예약 저장
        self.timer_after_id = self.root.after(1000, self.update_timer)

    def show_words_once(self):
        self.canvas.delete("word")
        self.info_label.config(text="")

        self.current_left_word = random.choice(self.WORDS)
        
        #우측 단어는 좌측과 다른 단어 선택
        right_candidates = [w for w in self.WORDS if w != self.current_left_word]
        self.current_right_word = random.choice(right_candidates)

        #서로 다른 값. (같은 갯수 방지)
        self.count_left = random.randint(self.MIN_WORDS, self.MAX_WORDS)
        self.count_right = random.randint(self.MIN_WORDS, self.MAX_WORDS)
        while self.count_right == self.count_left:
            self.count_right = random.randint(self.MIN_WORDS, self.MAX_WORDS)

        self.answer_expected = self.current_left_word if self.count_left > self.count_right else self.current_right_word

        # 영역을 겹치지 않기 위해 고르게
        self.place_word(self.LEFT_AREA, self.current_left_word, self.count_left, "word")
        self.place_word(self.RIGHT_AREA, self.current_right_word, self.count_right, "word")

        #2초후 입력 단계로 가게 만듦
        self.root.after(2000, self.ask_answer)

     

       

    def ask_answer(self):
        self.answer_entry.delete(0, "end")
        self.answer_entry.focus()
        self.info_label.config(text="정답을 입력하세요 : ex) 혜인 (5초 제한)")
        
        # 기존 예약 취소
        if self.answer_after_id:
            self.root.after_cancel(self.answer_after_id)
        
        #5초후 자동 판정 예약
        self.answer_after_id = self.root.after(5000, self.judge_and_next)

        
    def judge_answer(self, event=None):
        user_input = self.answer_entry.get().strip()
        self.answer_entry.delete(0, "end")

        #5초 타이머 취소

        if self.answer_after_id:
            self.root.after_cancel(self.answer_after_id)
            self.answer_after_id = None

        if user_input == self.answer_expected:
            self.score += 1
            self.remaining -= 1
            self.canvas.itemconfig(self.remain_text_id, text=f"남은 문항 : {self.remaining}")
            if self.remaining > 0:
                self.show_words_once()
            else:
                self.canvas.delete("word")
                self.info_label.config(text=f"게임 종료! 최종 점수는 {self.score}점입니다.")
                self.end_game_cleanup()

        else:
            self.info_label.config(text=f"오답! 정답은 {self.answer_expected}")
            # self.remaining -= 1
            # self.canvas.itemconfig(self.remain_text_id, text=f"남은 문항 : {self.remaining}")
            # if self.remaining > 0:
            #     self.root.after(1000, self.show_words_once)
            # else:
            #     self.canvas.delete("word")
            #     self.info_label.config(text=f"게임 종료! 최종 점수는 {self.score}점입니다.")

    def judge_and_next(self):

        #5초 타이머 예약 정리

        if self.answer_after_id:
            self.root.after_cancel(self.answer_after_id)
            self.answer_after_id = None


        user_input = self.answer_entry.get().strip()
        self.answer_entry.delete(0, "end")

        if user_input == self.answer_expected:
            self.score += 1
            self.info_label.config(text=f"정답! ({self.answer_expected})")
        else:
            self.info_label.config(text=f"오답! 정답은 {self.answer_expected}")

        self.remaining -= 1
        self.canvas.itemconfig(self.remain_text_id, text=f"남은 문항 : {self.remaining}")

        if self.remaining > 0:
            self.root.after(1000, self.show_words_once) # 1초 후 다음 문제

        else:
            self.canvas.delete("word")
            self.info_label.config(text=f"게임 종료! 최종 점수는 {self.score}점입니다.")
            self.end_game_cleanup()

    def end_game_cleanup(self):
        self.game_running = False
        self.start_time = None
        self.remaining = self.TOTAL_QUESTIONS

        if self.timer_after_id:
            self.root.after_cancel(self.timer_after_id)
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
        min_distance = 50 # 픽셀 기준거리
        for _ in range(count):
            for _ in range(100):  # 최대 100번 시도
                x = random.randint(area[0], area[2])
                y = random.randint(area[1], area[3])
                size = random.randint(self.FONT_SIZE_MIN, self.FONT_SIZE_MAX)

                # 기존 좌표와 거리 비교 (충돌 방지)
                if all((abs(x - px) > size + ps + 10 and abs(y - py) > size + ps + 10)
                        for px, py, ps in placed):
                    self.canvas.create_text(x, y, text=word, font=("Arial", size),
                                            fill="black", tags=tag)
                    placed.append((x, y, size))
                    break

if __name__ == "__main__":
    window = Tk()
    app = WordGameApp(window)
    window.resizable(False, False)
    window.mainloop()