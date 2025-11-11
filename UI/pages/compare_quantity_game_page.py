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

        # 리소스 / 설정
        self.WORDS = ["준혁", "혜인", "승현", "준희"]
        self.TOTAL_QUESTIONS = 10
        self.LEFT_AREA = (336, 388, 836, 888)
        self.RIGHT_AREA = (1085, 388, 1585, 888)

        # 게임 상태 변수
        self.remaining = self.TOTAL_QUESTIONS
        self.score = 0
        self.total_answered = 0   # 추가: 푼 문제 수(정답+오답+타임아웃)
        self.game_running = False
        self.start_time = None
        self.answer_expected = None
        self.answer_allowed = False  # 정답 제출 허용 플래그

        self.current_left_word = None
        self.current_right_word = None
        self.count_left = 0
        self.count_right = 0

        # after 핸들러 id
        self.timer_after_id = None
        self.answer_after_id = None

        # 로드 및 UI 구성
        self.load_assets()
        self.setup_ui()
        self.bind_events()

    def load_assets(self):
        ASSETS_PATH = Path("./UI/assets/compare_quantity_game")
        self.relative_to_assets = lambda path: ASSETS_PATH / Path(path)

        # 이미지 로드 (필요 시 try/except로 감싸서 안전하게 처리 가능)
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

        # 배경/장식 이미지
        self.canvas.create_image(960, 540, image=self.bg1)
        self.canvas.create_image(959, 563, image=self.bg2)
        self.canvas.create_image(586, 638, image=self.left_img)
        self.canvas.create_image(1335, 638, image=self.right_img)
        self.canvas.create_image(959, 629, image=self.center_img)

        # 타이머 / 남은 문항 표시
        self.timer_text_id = self.canvas.create_text(320, 238, anchor="nw", text="진행시간\n00:00:00",
                                                     fill="#000000", font=("Inter Light", 18))
        self.remain_text_id = self.canvas.create_text(1411, 258, anchor="nw",
                                                      text=f"남은 문항 : {self.TOTAL_QUESTIONS}",
                                                      fill="#000000", font=("Inter Light", 18))

        # 추가: 실시간 점수 / 총 푼 문제 수 표시
        # 위치와 폰트는 필요에 따라 조정해
        self.score_status_id = self.canvas.create_text(1411, 222, anchor="nw",
                                                       text=f"맞춘 수 : 0    푼 문제 : 0",
                                                       fill="#000000", font=("Inter Light", 18))

        # 정보 라벨
        self.info_label = Label(self, text="", font=("Arial", 20), fg="red", bg=None, anchor="center")
        self.canvas.create_window(960, 940, window=self.info_label)

        # 상단 버튼들 (기능은 필요에 따라 수정)
        self.button_1 = Button(self, image=self.btn_img_1, borderwidth=0, highlightthickness=0,
                               command=lambda: print("button_1 clicked"), relief="flat")
        self.canvas.create_window(1501, 147, window=self.button_1, width=168, height=66)

        self.start_button = Button(self, image=self.btn_img_2, borderwidth=0, highlightthickness=0,
                                   command=self.start_game, relief="flat")
        self.canvas.create_window(830, 258, window=self.start_button, width=257, height=81)

    def bind_events(self):
        # 캔버스 클릭 핸들링
        self.canvas.bind("<Button-1>", self.handle_canvas_click)

    def handle_canvas_click(self, event):
        # 정답 제출 허용 상태에서만 클릭 처리
        if not self.game_running or not self.answer_allowed:
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
        # 이전 word 태그 삭제 및 안내 초기화
        self.canvas.delete("word")
        self.info_label.config(text="")

        # 랜덤 단어/카운트 선정 (같은 단어가 양쪽에 오지 않도록 처리)
        self.current_left_word = random.choice(self.WORDS)
        right_candidates = [w for w in self.WORDS if w != self.current_left_word]
        self.current_right_word = random.choice(right_candidates)

        # 각 영역의 개수 결정 (같지 않도록)
        self.count_left = random.randint(self.MIN_WORDS, self.MAX_WORDS)
        self.count_right = random.randint(self.MIN_WORDS, self.MAX_WORDS)
        while self.count_right == self.count_left:
            self.count_right = random.randint(self.MIN_WORDS, self.MAX_WORDS)

        # 정답은 개수가 더 많은 쪽의 단어
        self.answer_expected = self.current_left_word if self.count_left > self.count_right else self.current_right_word

        # 화면에 단어들 배치 (tag="word")
        self.place_word(self.LEFT_AREA, self.current_left_word, self.count_left, "word")
        self.place_word(self.RIGHT_AREA, self.current_right_word, self.count_right, "word")

        # 단어 노출 후 선택 가능하도록 ask_answer 호출 (2초 후)
        self.answer_allowed = False
        self.after(2000, self.ask_answer)

    def ask_answer(self):
        # 정답 제출 허용 및 안내 표시, 타임아웃 예약
        self.info_label.config(text="더 많은 단어를 클릭하세요 (3초 제한)")
        self.answer_allowed = True

        # 이전에 예약된 answer_after_id가 있으면 취소
        if self.answer_after_id:
            self.after_cancel(self.answer_after_id)
            self.answer_after_id = None

        # 3초 뒤 타임아웃 처리
        self.answer_after_id = self.after(3000, self.judge_and_next)

    def _update_score_status(self):
        # 실시간 점수 / 총 푼 문제 수 UI 갱신
        self.canvas.itemconfig(self.score_status_id, text=f"맞춘 수 : {self.score}    푼 문제 : {self.total_answered}")

    def judge_answer(self, selected_word):
        # 정답 제출 허용 상태에서만 처리
        if not self.game_running or not self.answer_allowed:
            return

        # 타임아웃 예약 취소
        if self.answer_after_id:
            self.after_cancel(self.answer_after_id)
            self.answer_after_id = None

        # 더 이상 정답 제출 허용하지 않음
        self.answer_allowed = False

        # 판정 및 안내
        if selected_word == self.answer_expected:
            self.score += 1
            self.info_label.config(text=f"정답! ({selected_word})")
        else:
            self.info_label.config(text=f"오답! 정답은 {self.answer_expected}")

        # 남은 문항 감소 및 총 푼 문제 수 증가, 표시 갱신
        self.remaining -= 1
        self.total_answered += 1
        self.canvas.itemconfig(self.remain_text_id, text=f"남은 문항 : {self.remaining}")
        self._update_score_status()

        # 다음 라운드 또는 종료: 정답/오답 모두 1초 대기 후 다음 라운드
        if self.remaining > 0:
            self.after(1000, self.show_words_once)
        else:
            self.canvas.delete("word")
            self.info_label.config(text=f"게임 종료! 최종 점수는 {self.score}점입니다.")
            self.after(1000, self.go_to_next_page)

    def judge_and_next(self):
        # 타임아웃 발생: 즉시 오답으로 처리하고 다음 라운드로 (지연 없이)
        if self.answer_after_id:
            self.after_cancel(self.answer_after_id)
            self.answer_after_id = None

        # 더 이상 정답 제출 허용하지 않음
        self.answer_allowed = False

        # 시간 초과는 오답으로 처리 (점수 증가 없음)
        self.info_label.config(text=f"시간 초과! 정답은 {self.answer_expected}")

        # 남은 문항 감소 및 총 푼 문제 수 증가, 표시 갱신
        self.remaining -= 1
        self.total_answered += 1
        self.canvas.itemconfig(self.remain_text_id, text=f"남은 문항 : {self.remaining}")
        self._update_score_status()

        # 즉시 다음 라운드 또는 종료 (지연 없이 진행)
        if self.remaining > 0:
            # 즉시 다음 라운드로 이동
            self.show_words_once()
        else:
            self.canvas.delete("word")
            self.info_label.config(text=f"게임 종료! 최종 점수는 {self.score}점입니다.")
            self.after(1000, self.go_to_next_page)

    def go_to_next_page(self):
        # 게임 종료 정리 후 결과 저장 및 페이지 이동
        self.end_game_cleanup()
        try:
            # controller.scores에 저장: 정답 수와 총문항(전체 문제 수)를 기록
            self.controller.scores["compare"] = {"correct": self.score, "total": self.TOTAL_QUESTIONS}
        except Exception:
            pass
        # 결과 화면으로 이동 (컨트롤러에 맞춰 페이지명 사용)
        self.controller.show_frame("WaitResult")

    def end_game_cleanup(self):
        # 타이머/예약 취소 및 상태 초기화
        self.game_running = False
        self.start_time = None
        self.answer_allowed = False

        if self.timer_after_id:
            try:
                self.after_cancel(self.timer_after_id)
            except Exception:
                pass
            self.timer_after_id = None

        if self.answer_after_id:
            try:
                self.after_cancel(self.answer_after_id)
            except Exception:
                pass
            self.answer_after_id = None

        # 화면 초기화: 단어 삭제
        try:
            self.canvas.delete("word")
        except Exception:
            pass

    def start_game(self):
        if self.game_running:
            return
        self.game_running = True
        self.start_time = time.time()
        self.remaining = self.TOTAL_QUESTIONS
        self.score = 0
        self.total_answered = 0
        self.canvas.itemconfig(self.remain_text_id, text=f"남은 문항 : {self.remaining}")
        self._update_score_status()
        self.update_timer()
        self.show_words_once()

    def place_word(self, area, word, count, tag):
        placed = []
        for _ in range(count):
            for _ in range(100):  # 시도 횟수 제한
                x = random.randint(area[0], area[2])
                y = random.randint(area[1], area[3])
                size = random.randint(self.FONT_SIZE_MIN, self.FONT_SIZE_MAX)

                # 충돌 회피
                if all((abs(x - px) > size + ps + 10 and abs(y - py) > size + ps + 10)
                       for px, py, ps in placed):
                    self.canvas.create_text(x, y, text=word, font=("Arial", size),
                                            fill="black", tags=tag)
                    placed.append((x, y, size))
                    break
