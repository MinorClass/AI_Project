import tkinter as tk
from PIL import Image, ImageTk
import os
import time
import cv2 
from example import  AttentionMonitor

BACKGROUND_PATH = "background.jpg"
INTERVIEWER_IMG = "interviewer.jpg"  # 면접관 이미지 파일 (450x450 권장)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
BACKGROUND_PATH = os.path.join(BASE_DIR, "background.jpg")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI 면접 훈련 도구")
        self.geometry("1920x1080")
        self.resizable(False, False)

        # 배경 이미지
        self.bg_img = Image.open(BACKGROUND_PATH).resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(self.bg_img)

        # 컨테이너
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # 페이지 등록
        self.frames = {
            "MainPage": MainPage(self.container, self),
            "CheckPage": CheckPage(self.container, self),
            "InterviewPage1": InterviewPage1(self.container, self),
            "InterviewPage2": InterviewPage2(self.container, self),
            "InterviewPage3": InterviewPage3(self.container, self),
            "ExplainGamePage" : ExplainGamePage(self.container, self),
            "GameIntroPage" : GameIntroPage(self.container,self)

        }

        self.current_frame = None
        self.show_frame("MainPage")

    def show_frame(self, name):
        if self.current_frame:
            self.current_frame.place_forget()
        frame = self.frames[name]
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.current_frame = frame


class BasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # 캔버스 + 배경
        self.canvas = tk.Canvas(self, width=1920, height=1080, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.controller.bg_photo, anchor="nw")

        # 오버레이 프레임
        self.overlay = tk.Frame(self.canvas, bg="", padx=16, pady=16)
        self.canvas.create_window(960, 540, window=self.overlay, anchor="center")


class MainPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        box = tk.Frame(self.overlay, bg="white", width=800, height=600)
        box.pack()

        header = tk.Label(box, text="AI 면접 훈련 도구",
                          bg="#4B0082", fg="white", font=("Arial", 20, "bold"), pady=10)
        header.pack(fill="x")

        msg = tk.Label(box, text="부족한 면접 경험을 AI와 함께 채워 나가보세요.",
                       bg="white", fg="#333333", font=("Arial", 16, "bold"), pady=20)
        msg.pack()

        start_btn = tk.Button(box, text="시작하기",
                              bg="#6A0DAD", fg="white", font=("Arial", 14, "bold"),
                              padx=20, pady=10,
                              command=lambda: controller.show_frame("CheckPage"))
        start_btn.pack(pady=30)


class CheckPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        nav = tk.Frame(self.overlay, bg="white")
        nav.pack(fill="x", pady=10)

        back_btn = tk.Button(nav, text="< 이전", command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(side="left", padx=10)

        title = tk.Label(nav, text="카메라/마이크 확인", font=("Arial", 18, "bold"), bg="white")
        title.pack(side="left", padx=20)

        cam_frame = tk.Frame(self.overlay, bg="white", width=320, height=320)
        cam_frame.pack(pady=40)
        cam_label = tk.Label(cam_frame, text="카메라 화면 (300x300)", bg="black", fg="white",
                             width=40, height=15)
        cam_label.pack()

        btn_frame = tk.Frame(self.overlay, bg="white")
        btn_frame.pack(pady=20)

        mic_btn = tk.Button(btn_frame, text="마이크 연결", width=15)
        mic_btn.grid(row=0, column=0, padx=10)

        cam_btn = tk.Button(btn_frame, text="카메라 연결", width=15)
        cam_btn.grid(row=0, column=1, padx=10)

        ready_btn = tk.Button(self.overlay, text="준비완료", bg="#6A0DAD", fg="white",
                              font=("Arial", 14, "bold"), padx=20, pady=10,
                              command=lambda: controller.show_frame("InterviewPage1"))
        ready_btn.pack(pady=30)


class InterviewPage1(BasePage):
    def __init__(self, parent, controller, duration_sec=60):
        super().__init__(parent, controller)

        self.total_duration = duration_sec
        self.remaining = duration_sec
        self.timer_running = False

        # overlay를 grid 레이아웃으로
        self.overlay.grid_rowconfigure(1, weight=1)
        self.overlay.grid_columnconfigure(1, weight=1)

        # 상단 바
        top = tk.Frame(self.overlay, bg="#4B0082")
        top.grid(row=0, column=0, columnspan=3, sticky="ew")
        tk.Label(top, text="가상 면접", bg="#4B0082", fg="white",
                 font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=10)
        tk.Button(top, text="이전", command=lambda: controller.show_frame("CheckPage")
                  if controller else None).pack(side="right", padx=20)

        # 좌측: 타이머
        left = tk.Frame(self.overlay, bg="white")
        left.grid(row=1, column=0, sticky="n", padx=20, pady=20)

        tk.Label(left, text="진행시간", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
        self.lbl_timer = tk.Label(left, text="00:00:00",
                                  font=("Arial", 18, "bold"), bg="white", fg="black")
        self.lbl_timer.pack(anchor="w", pady=10)
        self.btn_start = tk.Button(left, text="면접시작", command=self.start_countdown)
        self.btn_start.pack(anchor="w")

        # 중앙: 면접관
        center = tk.Frame(self.overlay, bg="white")
        center.grid(row=1, column=1, padx=20, pady=20)

        try:
            img = Image.open(INTERVIEWER_IMG).resize((450, 450))
            self.interviewer_photo = ImageTk.PhotoImage(img)
            tk.Label(center, image=self.interviewer_photo, bg="white").pack()
        except Exception:
            tk.Label(center, text="Interviewer 450x450", bg="gray", width=60, height=25).pack()

        self.question_label = tk.Label(center,
                                       text="시작 버튼을 누르고 10초 뒤 시작하면 됩니다.",
                                       font=("Arial", 12), bg="white")
        self.question_label.pack(pady=20)

        # 우측: 사용자 카메라 + 피드백
        right = tk.Frame(self.overlay, bg="white")
        right.grid(row=1, column=2, sticky="n", padx=20, pady=20)

        tk.Label(right, text="모의 면접자 카메라", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        self.user_cam = tk.Label(right, text="Camera 300x300",
                                 bg="black", fg="white", width=40, height=15)
        self.user_cam.pack(pady=10)

        tk.Label(right, text="Feedback", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        self.feedback_label = tk.Label(right, text="분석 결과가 여기에 표시됩니다.",
                                       font=("Arial", 11), bg="white", fg="gray", justify="left")
        self.feedback_label.pack(fill="x")

        # 하단: 질문 박스 + 종료 버튼
        bottom = tk.Frame(self.overlay, bg="white")
        bottom.grid(row=2, column=0, columnspan=3, sticky="ew", padx=20, pady=20)

        self.question_box = tk.Label(bottom,
                                     text="시작 버튼을 누르고 10초 뒤 시작하면 됩니다.",
                                     font=("Arial", 12), bg="#F7F7F9", fg="black",
                                     anchor="w", justify="left", wraplength=1000)
        self.question_box.pack(side="left", fill="x", expand=True, padx=(0, 20))

        next_btn = tk.Button(bottom, text="다음", bg="red", fg="white",
                  command=lambda: controller.show_frame("InterviewPage2"))
        next_btn.pack(pady=30)

    # --- 타이머 ---
        # --- 타이머 ---
    def _fmt(self, sec: int) -> str:
        """초 단위를 시:분:초 문자열로 변환"""
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        return f"{h:02}:{m:02}:{s:02}"

    def start_countdown(self):
        """카운트다운 시작"""
        if not self.timer_running:
            self.timer_running = True
            self._tick()

    def _tick(self):
        """1초마다 호출되어 남은 시간을 갱신"""
        if not self.timer_running:
            return
        # 라벨에 현재 남은 시간 표시
        self.lbl_timer.config(text=self._fmt(self.remaining))
        if self.remaining <= 0:
            self.timer_running = False
            return
        self.remaining -= 1
        # 1초 후 다시 호출
        self.after(1000, self._tick)

class InterviewPage2(BasePage):
    def __init__(self, parent, controller, duration_sec=60):
        super().__init__(parent, controller)

        self.total_duration = duration_sec
        self.remaining = duration_sec
        self.timer_running = False

        # overlay를 grid 레이아웃으로
        self.overlay.grid_rowconfigure(1, weight=1)
        self.overlay.grid_columnconfigure(1, weight=1)

        # 상단 바
        top = tk.Frame(self.overlay, bg="#4B0082")
        top.grid(row=0, column=0, columnspan=3, sticky="ew")
        tk.Label(top, text="가상 면접", bg="#4B0082", fg="white",
                 font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=10)
        tk.Button(top, text="이전", command=lambda: controller.show_frame("CheckPage")
                  if controller else None).pack(side="right", padx=20)

        # 좌측: 타이머
        left = tk.Frame(self.overlay, bg="white")
        left.grid(row=1, column=0, sticky="n", padx=20, pady=20)

        tk.Label(left, text="진행시간", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
        self.lbl_timer = tk.Label(left, text="00:00:00",
                                  font=("Arial", 18, "bold"), bg="white", fg="black")
        self.lbl_timer.pack(anchor="w", pady=10)
        self.btn_start = tk.Button(left, text="면접시작", command=self.start_countdown)
        self.btn_start.pack(anchor="w")

        # 중앙: 면접관
        center = tk.Frame(self.overlay, bg="white")
        center.grid(row=1, column=1, padx=20, pady=20)

        try:
            img = Image.open(INTERVIEWER_IMG).resize((450, 450))
            self.interviewer_photo = ImageTk.PhotoImage(img)
            tk.Label(center, image=self.interviewer_photo, bg="white").pack()
        except Exception:
            tk.Label(center, text="Interviewer 450x450", bg="gray", width=60, height=25).pack()

        self.question_label = tk.Label(center,
                                       text="시작 버튼을 누르고 10초 뒤 시작하면 됩니다.",
                                       font=("Arial", 12), bg="white")
        self.question_label.pack(pady=20)

        # 우측: 사용자 카메라 + 피드백
        right = tk.Frame(self.overlay, bg="white")
        right.grid(row=1, column=2, sticky="n", padx=20, pady=20)

        tk.Label(right, text="모의 면접자 카메라", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        self.user_cam = tk.Label(right, text="Camera 300x300",
                                 bg="black", fg="white", width=40, height=15)
        self.user_cam.pack(pady=10)

        tk.Label(right, text="Feedback", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        self.feedback_label = tk.Label(right, text="분석 결과가 여기에 표시됩니다.",
                                       font=("Arial", 11), bg="white", fg="gray", justify="left")
        self.feedback_label.pack(fill="x")

        # 하단: 질문 박스 + 종료 버튼
        bottom = tk.Frame(self.overlay, bg="white")
        bottom.grid(row=2, column=0, columnspan=3, sticky="ew", padx=20, pady=20)

        self.question_box = tk.Label(bottom,
                                     text="시작 버튼을 누르고 10초 뒤 시작하면 됩니다.",
                                     font=("Arial", 12), bg="#F7F7F9", fg="black",
                                     anchor="w", justify="left", wraplength=1000)
        self.question_box.pack(side="left", fill="x", expand=True, padx=(0, 20))

        next_btn =tk.Button(bottom, text="다음", bg="red", fg="white",
                  command=lambda: controller.show_frame("InterviewPage3"))
        next_btn.pack(pady=30)

    # --- 타이머 ---
        # --- 타이머 ---
    def _fmt(self, sec: int) -> str:
        """초 단위를 시:분:초 문자열로 변환"""
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        return f"{h:02}:{m:02}:{s:02}"

    def start_countdown(self):
        """카운트다운 시작"""
        if not self.timer_running:
            self.timer_running = True
            self._tick()

    def _tick(self):
        """1초마다 호출되어 남은 시간을 갱신"""
        if not self.timer_running:
            return
        # 라벨에 현재 남은 시간 표시
        self.lbl_timer.config(text=self._fmt(self.remaining))
        if self.remaining <= 0:
            self.timer_running = False
            return
        self.remaining -= 1
        # 1초 후 다시 호출
        self.after(1000, self._tick)

class InterviewPage3(BasePage):

    DEFAULT_CAM_WIDTH = 300
    DEFAULT_CAM_HEIGHT = 300
    
    def __init__(self, parent, controller, duration_sec=60):
        super().__init__(parent, controller)

         # 웹캠 관련 변수 초기화 
        self.monitor = None #
        self.is_streaming = False
        self.cam_label_width = self.DEFAULT_CAM_WIDTH
        self.cam_label_height = self.DEFAULT_CAM_HEIGHT
        self.current_photo = None #

        self.total_duration = duration_sec
        self.remaining = duration_sec
        self.timer_running = False

        # overlay를 grid 레이아웃으로
        self.overlay.grid_rowconfigure(1, weight=1)
        self.overlay.grid_columnconfigure(1, weight=1)

        # 상단 바
        top = tk.Frame(self.overlay, bg="#4B0082")
        top.grid(row=0, column=0, columnspan=3, sticky="ew")
        tk.Label(top, text="가상 면접", bg="#4B0082", fg="white",
                 font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=10)
        tk.Button(top, text="이전", command=lambda: controller.show_frame("CheckPage")
                  if controller else None).pack(side="right", padx=20)

        # 좌측: 타이머
        left = tk.Frame(self.overlay, bg="white")
        left.grid(row=1, column=0, sticky="n", padx=20, pady=20)

        tk.Label(left, text="진행시간", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
        self.lbl_timer = tk.Label(left, text="00:00:00",
                                  font=("Arial", 18, "bold"), bg="white", fg="black")
        self.lbl_timer.pack(anchor="w", pady=10)
        self.btn_start = tk.Button(left, text="면접시작", command=self.start_countdown)
        self.btn_start.pack(anchor="w")

        # 중앙: 면접관
        center = tk.Frame(self.overlay, bg="white")
        center.grid(row=1, column=1, padx=20, pady=20)

        try:
            img = Image.open(INTERVIEWER_IMG).resize((450, 450))
            self.interviewer_photo = ImageTk.PhotoImage(img)
            tk.Label(center, image=self.interviewer_photo, bg="white").pack()
        except Exception:
            tk.Label(center, text="Interviewer 450x450", bg="gray", width=60, height=25).pack()

        self.question_label = tk.Label(center,
                                       text="시작 버튼을 누르고 10초 뒤 시작하면 됩니다.",
                                       font=("Arial", 12), bg="white")
        self.question_label.pack(pady=20)

        # 우측: 사용자 카메라 + 피드백
        right = tk.Frame(self.overlay, bg="white")
        right.grid(row=1, column=2, sticky="n", padx=20, pady=20)

        tk.Label(right, text="모의 면접자 카메라", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        self.user_cam = tk.Label(right, text="Camera 300x300",
                                 bg="black", fg="white", width=40, height=15)
        self.user_cam.pack(pady=10)

        tk.Label(right, text="Feedback", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        self.feedback_label = tk.Label(right, text="분석 결과가 여기에 표시됩니다.",
                                       font=("Arial", 11), bg="white", fg="gray", justify="left")
        self.feedback_label.pack(fill="x")

        # 하단: 질문 박스 + 종료 버튼
        bottom = tk.Frame(self.overlay, bg="white")
        bottom.grid(row=2, column=0, columnspan=3, sticky="ew", padx=20, pady=20)

        self.question_box = tk.Label(bottom,
                                     text="시작 버튼을 누르고 10초 뒤 시작하면 됩니다.",
                                     font=("Arial", 12), bg="#F7F7F9", fg="black",
                                     anchor="w", justify="left", wraplength=1000)
        self.question_box.pack(side="left", fill="x", expand=True, padx=(0, 20))

        next_btn = tk.Button(bottom, text="다음", bg="red", fg="white",
                  command=lambda: controller.show_frame("ExplainGamePage"))
        next_btn.pack(pady=30)

        # 카메라 화면 영역
        # 프레임 크기를 레이블 기본 크기에 맞춥니다.
        cam_frame = tk.Frame(right, bg="#DDDDDD", bd=5, relief="solid", 
                              width=self.cam_label_width + 20, height=self.cam_label_height + 20)
        cam_frame.pack_propagate(False) # 크기 고정
        cam_frame.pack(pady=20, padx=50)
        
        # 웹캠 프레임이 표시될 레이블
        self.cam_label = tk.Label(cam_frame, 
                                  text=f"카메라 화면 ({self.cam_label_width}x{self.cam_label_height})\n\n웹캠 연결 대기 중...", 
                                  bg="#1E1E1E", fg="white",
                                  font=("Arial", 16),
                                  width=self.cam_label_width, 
                                  height=self.cam_label_height, 
                                  anchor="center")
        self.cam_label.pack(fill="both", expand=True, padx=10, pady=10)
        

    # --- 타이머 ---
    def _fmt(self, sec: int) -> str:
        """초 단위를 시:분:초 문자열로 변환"""
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        return f"{h:02}:{m:02}:{s:02}"

    def start_countdown(self):
        """카운트다운 시작"""
        if not self.timer_running:
            self.timer_running = True
            self._tick()

    def _tick(self):
        """1초마다 호출되어 남은 시간을 갱신"""
        if not self.timer_running:
            return
        # 라벨에 현재 남은 시간 표시
        self.lbl_timer.config(text=self._fmt(self.remaining))
        if self.remaining <= 0:
            self.timer_running = False
            return
        self.remaining -= 1
        # 1초 후 다시 호출
        self.after(1000, self._tick)


class ExplainGamePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # overlay를 grid 레이아웃으로 설정
        self.overlay.grid_rowconfigure(1, weight=1)
        self.overlay.grid_columnconfigure(0, weight=1)

        # 상단 바
        top = tk.Frame(self.overlay, bg="white")
        top.grid(row=0, column=0, sticky="ew", pady=10, padx=10)

        back_btn = tk.Button(top, text="이전",
                             command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(side="right")

        # 중앙 선택 영역 (4개)
        center = tk.Frame(self.overlay, bg="white")
        center.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)

        self.option_frames = []
        for i in range(1, 5):
            frame = tk.Frame(center, bg="white", bd=1, relief="solid", height=100)
            frame.pack(fill="x", pady=10)
            lbl = tk.Label(frame, text=f"{i}. 선택", font=("Arial", 14), bg="white")
            lbl.pack(anchor="w", padx=10, pady=10)
            self.option_frames.append(frame)

        # 하단 바
        bottom = tk.Frame(self.overlay, bg="white")
        bottom.grid(row=2, column=0, sticky="ew", pady=10, padx=10)

        next_btn = tk.Button(bottom, text="다음", bg="red", fg="white",
                  command=lambda: controller.show_frame("GameIntroPage"))
        next_btn.pack(pady=30)


    
class GameIntroPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # overlay를 grid 레이아웃으로
        self.overlay.grid_rowconfigure(1, weight=1)
        self.overlay.grid_columnconfigure(0, weight=1)
        self.overlay.grid_columnconfigure(1, weight=2)

        # 상단 바
        top = tk.Frame(self.overlay, bg="white")
        top.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10, padx=10)

        title = tk.Label(top, text="가위, 바위, 보", font=("Arial", 18, "bold"), bg="white")
        title.pack(side="left", padx=10)

        back_btn = tk.Button(top, text="이전",
                             command=lambda: controller.show_frame("ExplainGamePage"))
        back_btn.pack(side="right")

        # 좌측 설명 박스들
        left = tk.Frame(self.overlay, bg="white")
        left.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        for text in ["가위", "바위", "보"]:
            frame = tk.Frame(left, bg="white", bd=1, relief="solid", height=100)
            frame.pack(fill="x", pady=10)
            tk.Label(frame, text=text, font=("Arial", 14), bg="white").pack(anchor="center", pady=20)

        # 우측 설명 영역
        right = tk.Frame(self.overlay, bg="white")
        right.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

        tk.Label(right, text="- 목표", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", pady=(0,10))
        tk.Label(right,
                 text="이 게임은 가위, 바위, 보를 선택하고\n상대방을 이겨야 하는 게임입니다.",
                 font=("Arial", 12), bg="white", justify="left").pack(anchor="w")

        # 하단 시작 버튼
        bottom = tk.Frame(self.overlay, bg="white")
        bottom.grid(row=2, column=0, columnspan=2, sticky="ew", pady=20, padx=20)

        start_btn = tk.Button(bottom, text="시작", bg="#6A0DAD", fg="white",
                              font=("Arial", 14, "bold"),
                              command=lambda: print("게임 시작"))
        start_btn.pack(side="right")

        next_btn = tk.Button(bottom, text="다음", bg="red", fg="white",
                  command=lambda: controller.show_frame("ExplainGamePage"))
        next_btn.pack(pady=30)


    # 웹캠 스트리밍 시작 -> 모니터링 시작으로 변경
    def start_monitoring(self):
        #  객체가 이미 존재하고 카메라가 열려있다면 중복 실행 방지
        if self.monitor and self.monitor.cap.isOpened():
            print("INFO: 이미 모니터링이 실행 중입니다.")
            return

        # 번 카메라 인덱스로 고정하여 시도합니다.
        CAMERA_INDEX = 4
        
        # 1. AttentionMonitor 인스턴스 초기화 (내부적으로 cv2.VideoCapture 시도)
        try:
            # 이전 시도에서 리소스 해제가 제대로 되지 않았을 경우를 대비해 정리
            if hasattr(self, 'monitor') and self.monitor is not None:
                del self.monitor
            
            self.monitor = AttentionMonitor(camera_index=CAMERA_INDEX)
        except Exception as e:
            # 초기화 오류 (MediaPipe 등) 처리
            self.cam_label.config(text=f"ERROR: 모니터 초기화 중 오류 발생: {e}", image=None)
            self.monitor = None
            return
        
        # 2. 카메라 연결 성공 여부 확인
        if not self.monitor.cap.isOpened():
            # 최종 실패
            self.cam_label.config(text=f"ERROR: {CAMERA_INDEX}번 웹캠을 열 수 없습니다.\n(장치 연결 및 권한 확인)", image=None)
            print(f"ERROR: {CAMERA_INDEX}번 웹캠을 찾거나 열 수 없습니다. 인덱스를 확인하세요.")
            # 실패 시 모니터 객체 정리
            del self.monitor
            self.monitor = None
            return

        self.is_streaming = True
        print("INFO: 웹캠 스트리밍 및 AI 분석을 시작합니다.")
        self.update_frame() # 스트리밍 시작

    # 프레임 업데이트 및 표시 
    def update_frame(self):
        # 모니터가 연결되지 않았거나 카메라가 닫혔다면 종료
        if not self.monitor or not self.monitor.cap.isOpened():
            return

        # 1. 모니터에서 프레임 가져오기
        ret, frame = self.monitor.get_frame()

        if ret:
            # 2. AttentionMonitor 클래스에서 프레임 처리 (Gaze, Tremor 분석 및 텍스트 추가)
            annotated_frame, metrics = self.monitor.process_frame()
            
            # 3. OpenCV의 BGR 색상 순서를 Tkinter 표시를 위한 RGB/RGBA 순서로 변경
            cv2image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGBA)
            
            # 4. PIL 이미지로 변환
            img = Image.fromarray(cv2image)
            
            resized_img = img.resize((self.DEFAULT_CAM_WIDTH, self.DEFAULT_CAM_HEIGHT), Image.LANCZOS)
            self.current_photo = ImageTk.PhotoImage(image=resized_img)
            
            # 6. 레이블 업데이트 (분석 결과가 포함된 프레임 표시)
            self.cam_label.config(image=self.current_photo, text="")
        else:
            # 프레임 읽기 실패 시 모니터링 중단
            self.cam_label.config(text="ERROR: 프레임 읽기 실패", image=None)
            self.stop_monitoring()
            return
            
        self.after_id = self.after(10, self.update_frame)

    def stop_monitoring(self):
        if self.is_streaming and self.monitor:
            if hasattr(self, 'after_id'):
                self.after_cancel(self.after_id)
            
            # AttentionMonitor의 리소스 정리 (__del__ 호출)
            # 웹캠 해제 및 MediaPipe 파이프라인 정리
            del self.monitor 
            self.monitor = None
            
            print("INFO: AI 모니터링을 중단하고 리소스를 해제합니다.")

        self.is_streaming = False
        self.current_photo = None 
        self.cam_label.config(text=f"카메라 화면 ({self.DEFAULT_CAM_WIDTH}x{self.DEFAULT_CAM_HEIGHT})\n\n웹캠 연결 대기 중...", image=None)

    def on_hide(self):
        # 페이지가 숨겨질 때 모니터링 중단 로직 실행
        self.stop_monitoring()

    def on_show(self):
        self.cam_label.config(text=f"카메라 화면 ({self.DEFAULT_CAM_WIDTH}x{self.DEFAULT_CAM_HEIGHT})\n\n웹캠 연결 대기 중...", image=None)


if __name__ == "__main__":
    app = App()
    app.mainloop()