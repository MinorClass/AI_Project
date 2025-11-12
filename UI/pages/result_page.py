import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os
from pathlib import Path
from .mock_interview_page import MockInterview
# 에셋 경로 (Figma에서 생성된 이미지들이 들어있는 폴더)
ASSETS_PATH = os.path.abspath("./UI/assets/result")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

class Result(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")
        self.controller = controller

        # 캔버스 생성
        self.canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        self.canvas.pack(fill="both", expand=True)
        

        # 배경 이미지 (안전 로드)
        try:
            self.bg_image = PhotoImage(file=relative_to_assets("image_1.png"))
            self.canvas.create_image(960, 540, image=self.bg_image)
        except Exception:
            self.bg_image = None

        # 좌측 상단 이미지 (기존 이미지1)
        try:
            self.image1 = PhotoImage(file=relative_to_assets("image_2.png"))
            self.canvas.create_image(230, 147, image=self.image1, anchor="nw")
        except Exception:
            self.image1 = None

        # (기존) 결과 이미지1 위치는 유지하되 image_r는 사용하지 않음
        # 기존에 사용하던 image_r 왼쪽 복제는 제거하고, 오른쪽 영역에 점수 텍스트를 표시함.

        # 왼쪽 결과 박스 이미지(기존 이미지_r 자리) — 유지하려면 아래 주석 해제
        try:
            self.image_r_left = PhotoImage(file=relative_to_assets("image_r.png"))
            # 기존 좌측 결과 이미지는 그대로 둡니다 (원하면 제거 가능)
            self.canvas.create_image(267, 275, image=self.image_r_left, anchor="nw")
        except Exception:
            self.image_r_left = None

        # 오른쪽 기존 image_r 제거하고 여기서 게임별 점수 텍스트를 표시
        # 텍스트 위치와 스타일
        self.score_text_x = 991 + 100   # 적절한 x 좌표 조정 (원하는 위치로 변경 가능)
        self.score_text_y = 300         # 시작 y 좌표
        self.line_height = 40           # 각 게임 줄 간격

        # 초기 표시 (빈 값 또는 0/0)
        self.score_text_id = self.canvas.create_text(
            self.score_text_x, self.score_text_y,
            anchor="nw",
            text=self._build_score_text({}),
            fill="#000000",
            font=("Arial", 20)
        )

        # 버튼 이미지 (종료 버튼)
        try:
            self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
            button_1 = Button(self, image=self.button_image_1,
                              command=lambda: controller.quit(),
                              borderwidth=0, relief="flat")
            self.canvas.create_window(822, 829, window=button_1, anchor="nw")
        except Exception:
            # 대체 텍스트 버튼
            button_1 = Button(self, text="종료", command=lambda: controller.quit())
            self.canvas.create_window(822, 829, window=button_1, anchor="nw")

    def _build_score_text(self, scores_dict):
        """
        scores_dict expected format:
        {
          "rsp": {"correct": int, "total": int},
          "clicknum": {"correct": int, "total": int},
          "compare": {"correct": int, "total": int}
        }
        Returns a multiline string where each game is one line.
        """
        # 안전한 기본값 처리
        rsp = scores_dict.get("rsp", {"correct": 0, "total": 0})
        click = scores_dict.get("clicknum", {"correct": 0, "total": 0})
        compare = scores_dict.get("compare", {"correct": 0, "total": 0})

        lines = [
            f"가위바위보    : {rsp['correct']} / {rsp['total']}",
            f"숫자 누르기   : {click['correct']} / {click['total']}",
            f"개수 비교하기 : {compare['correct']} / {compare['total']}"
        ]
        return "\n".join(lines)

    def update_score_display(self):
        # controller.scores를 읽어 화면에 갱신
        scores = getattr(self.controller, "scores", {}) or {}
        text = self._build_score_text(scores)
        # 캔버스 텍스트 갱신
        self.canvas.itemconfig(self.score_text_id, text=text)

    def tkraise(self, aboveThis=None):
        # 프레임을 보이기 직전에 최신 점수로 갱신
        self.update_score_display()
        super().tkraise(aboveThis)
        # # 버튼 이미지
        # self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        # button_1 = Button(self, image=self.button_image_1,
        #                   command=lambda: self.quitpage(),
        #                   borderwidth=0, relief="flat")
        # self.canvas.create_window(822, 829, window=button_1, anchor="nw")

    # def quitpage(self):
    #     print(MockInterview.get_parameter)
    #     self.controller.quit()
