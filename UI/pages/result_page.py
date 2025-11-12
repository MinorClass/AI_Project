import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os
from pathlib import Path
# from .mock_interview_page import MockInterview # 이 페이지에서 직접 사용되지 않으므로 주석 처리 (선택 사항)
import google.generativeai as genai 

API_KEY = "AIzaSyBSuHxEGpxivX39ZPjy_cuI1jvDq5MkdyM"  
try:
    genai.configure(api_key=API_KEY)
    MODEL = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    print(f"Gemini API 설정 실패: {e}. 질문 자동 생성 기능이 작동하지 않습니다.")
    MODEL = None

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
        
        # --- UI 요소 로드 및 배치 ---
        
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

        # 왼쪽 결과 박스 이미지
        try:
            self.image_r_left = PhotoImage(file=relative_to_assets("image_r.png"))
            self.canvas.create_image(267, 275, image=self.image_r_left, anchor="nw")
        except Exception:
            self.image_r_left = None

        # 🌟 1. 왼쪽 심리 분석 텍스트 라벨 추가
        self.analysis_text = tk.StringVar(self)
        self.analysis_text.set("결과 분석을 시작합니다...") 
        
        # 텍스트가 표시될 라벨 생성 (좌표는 이미지 박스 내부에 맞게 조정)
        analysis_x, analysis_y = 280, 300 
        analysis_width = 400  # 텍스트 줄바꿈 너비
        
        self.analysis_label = tk.Label(self, textvariable=self.analysis_text, 
                                       font=("Arial", 14), fg="#353C92", bg="white", 
                                       justify=tk.LEFT, anchor="nw", wraplength=analysis_width)
        self.canvas.create_window(analysis_x, analysis_y, window=self.analysis_label, anchor="nw")


        # 오른쪽 기존 image_r 제거하고 여기서 게임별 점수 텍스트를 표시
        # 텍스트 위치와 스타일
        self.score_text_x = 991 + 100   # 적절한 x 좌표 조정 (원하는 위치로 변경 가능)
        self.score_text_y = 300         # 시작 y 좌표
        
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
        """컨트롤러의 점수 딕셔너리를 화면에 표시할 텍스트로 변환합니다."""
        # 안전한 기본값 처리
        rsp = scores_dict.get("rsp", {"correct": 0, "total": 0})
        click = scores_dict.get("clicknum", {"correct": 0, "total": 0})
        compare = scores_dict.get("compare", {"correct": 0, "total": 0})
        unfocus = scores_dict.get("unfocus", {"time": 0.0})
        tremor = scores_dict.get("tremor", {"time": 0.0})

        lines = [
            f"가위바위보    : {rsp['correct']} / {rsp['total']}",
            f"숫자 누르기   : {click['correct']} / {click['total']}",
            f"개수 비교하기 : {compare['correct']} / {compare['total']}",
            f"집중 안한시간 : {unfocus['time']:.2f}초", # 소수점 포맷 추가
            f"떨어버린 시간 : {tremor['time']:.2f}초"
        ]
        return "\n".join(lines)

    def update_score_display(self):
        scores = getattr(self.controller, "scores", {}) or {}
        self.text = self._build_score_text(scores)
        self.canvas.itemconfig(self.score_text_id, text=self.text)

    def _fetch_and_display_analysis(self):
        """Gemini API를 호출하여 분석 결과를 가져오고 UI에 표시합니다."""
        
        if not self.controller.last:
            self.analysis_text.set("면접이 아직 완료되지 않았습니다.")
            return

        if not MODEL:
            self.analysis_text.set("Gemini API 설정 문제로 분석 기능을 사용할 수 없습니다.")
            return
            
        prompt = "가위,바위,보 게임은 나또는 상대의 관점에서 가위바위보를 하는 게임으로, " \
        "나인 경우에는 이기고, 상대인 경우에는 져야하는 게임이다. 숫자 누르기 게임은 신호가 제시되면 주어진 규칙에 맞게 1부터 9까지 숫자 버튼을 최대한 빠르고 정확하게 누르면 되는 게임입니다. " \
        "개수 비교하기 게임은 화면 왼쪽과 오른쪽에 단어가 여러 개 제시됩니다. 두 단어 중 어떤 단어의 개수가 더 많았는지 선택하는 게임야. 이 게임들의 점수를 가지고 각 게임들에게 필요한 요소, 능력, 역량, 요구사항, 기술 등을 키워드로 삼아 개선점이나 보완해야 할 역량들을 서술해줘. " \
        "100자 이내로그리고 집중 안 한시간, 떨어버린 시간이 있는데 그것은 면접 중 집중 안 한 시간은 시선 처리, 떨어버린 시간은 몸의 떨림을 통해 도출해낸 점수야. " \
        "이것을 통해 어땠는지 그리고 다음 향후 방안이나 개선점을 통합점으로 설명해줘. " \
        "100자 이내로 그리고 마지막으로 이 모든 것을 통합하여 심리 상태에 대해 분석하고, 개선 방안을 포괄적으로 만들어줘 200자 이내로" 
        + self.text

        try:
            self.analysis_text.set("AI 심리 분석 중입니다... 잠시만 기다려 주세요.")
            response = MODEL.generate_content(prompt)
            
            analysis_result = response.text.strip()
            self.analysis_text.set(analysis_result)
            
        except Exception as e:
            # 4. 오류 처리
            self.analysis_text.set(f"심리 분석 중 오류 발생. 인터넷 연결 및 API 키를 확인하세요.")
            print(f"Gemini API 호출 오류: {e}")

    def tkraise(self, aboveThis=None):
        # 1. 프레임을 보이기 직전에 최신 점수로 갱신
        self.update_score_display()
        super().tkraise(aboveThis)
        
        # 2. 🌟 프레임이 뜬 후 AI 분석 시작
        # self.after(100, ...)를 사용하여 UI가 먼저 뜬 후에 네트워크 요청을 시작합니다.
        self.after(100, self._fetch_and_display_analysis)
