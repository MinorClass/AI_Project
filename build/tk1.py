import tkinter as tk
from PIL import Image, ImageTk
import os 

# 1. 현재 실행 중인 파일의 절대 경로를 얻습니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
# 2. BASE_DIR과 파일 이름을 결합하여 최종 경로를 정의합니다.
BACKGROUND_PATH = os.path.join(BASE_DIR, "background.jpg")
# ----------------------------------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI 면접 훈련 도구")
        self.geometry("1920x1080")
        self.resizable(False, False)

        # 배경 이미지 로드 (경로 문제 해결됨)
        try:
            self.bg_img = Image.open(BACKGROUND_PATH).resize((1920, 1080))
            self.bg_photo = ImageTk.PhotoImage(self.bg_img)
        except FileNotFoundError:
            # 파일을 찾지 못하면 오류 메시지 출력 후 흰색 배경으로 대체
            print(f"ERROR: 배경 이미지 파일 '{BACKGROUND_PATH}'를 찾을 수 없습니다.")
            self.bg_photo = None # 배경 이미지 로드 실패 처리

        # 컨테이너
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # 페이지 등록
        self.frames = {
            "MainPage": MainPage(self.container, self),
            "InterviewPage": InterviewPage(self.container, self)
        }

        # 첫 화면 표시
        self.current_frame = None
        self.show_frame("MainPage")

    def show_frame(self, name):
        # 이전 페이지 숨기기
        if self.current_frame:
            self.current_frame.place_forget()

        # 새 페이지 표시
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
        
        # 배경 이미지 로드에 성공했을 경우에만 이미지 배치
        if self.controller.bg_photo:
            self.canvas.create_image(0, 0, image=self.controller.bg_photo, anchor="nw")
        else:
             # 이미지 로드 실패 시 대체 배경색 사용
            self.canvas.configure(bg="#F0F0F0") 

        # 오버레이 프레임
        # 배경 이미지 대신 캔버스를 배경으로 사용하기 위해 canvas.create_window 사용
        self.overlay = tk.Frame(self.canvas, bg="", padx=16, pady=16)
        self.canvas.create_window(960, 540, window=self.overlay, anchor="center")


class MainPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        box = tk.Frame(self.overlay, bg="white", width=800, height=600, bd=2, relief="groove")
        box.pack(pady=50)

        header = tk.Label(box, text="AI 면접 훈련 도구",
                          bg="#4B0082", fg="white", font=("Arial", 28, "bold"), pady=15)
        header.pack(fill="x")

        msg = tk.Label(box, text="부족한 면접 경험을 AI와 함께 채워 나가보세요.",
                       bg="white", fg="#333333", font=("Arial", 18, "bold"), pady=40)
        msg.pack()

        start_btn = tk.Button(box, text="시작하기",
                              bg="#6A0DAD", fg="white", font=("Arial", 18, "bold"),
                              padx=30, pady=15,
                              activebackground="#8A2BE2", activeforeground="white",
                              bd=0, relief="flat",
                              command=lambda: controller.show_frame("InterviewPage"))
        start_btn.pack(pady=40)


class InterviewPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # 인터뷰 페이지의 메인 컨테이너 (중앙 정렬)
        main_content = tk.Frame(self.overlay, bg="white", bd=2, relief="groove", width=800, height=600)
        main_content.pack(pady=50)

        # 네비게이션/타이틀 프레임 (main_content 내부에 배치)
        nav = tk.Frame(main_content, bg="white")
        nav.pack(fill="x", pady=(10, 20))

        back_btn = tk.Button(nav, text="< 이전", 
                             font=("Arial", 12),
                             bd=0, relief="flat",
                             command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(side="left", padx=20)

        title = tk.Label(nav, text="가상 면접", font=("Arial", 22, "bold"), bg="white", fg="#4B0082")
        title.pack(side="left", padx=20, expand=True)

        # 카메라 화면 영역
        cam_frame = tk.Frame(main_content, bg="#DDDDDD", bd=5, relief="solid")
        cam_frame.pack(pady=20, padx=50)
        
        cam_label = tk.Label(cam_frame, text="카메라 화면 (300x300)\n\n웹캠 연결 대기 중...", 
                             bg="#1E1E1E", fg="white",
                             font=("Arial", 16),
                             width=30, height=15, anchor="center")
        cam_label.pack(padx=10, pady=10)

        # 버튼 프레임
        btn_frame = tk.Frame(main_content, bg="white")
        btn_frame.pack(pady=20)

        mic_btn = tk.Button(btn_frame, text="마이크 연결", width=15, font=("Arial", 14), bg="#C0C0C0")
        mic_btn.grid(row=0, column=0, padx=15, pady=10)

        cam_btn = tk.Button(btn_frame, text="카메라 연결", width=15, font=("Arial", 14), bg="#C0C0C0")
        cam_btn.grid(row=0, column=1, padx=15, pady=10)

        # 준비 완료 버튼
        ready_btn = tk.Button(main_content, text="준비 완료", 
                              bg="#008000", fg="white",
                              font=("Arial", 18, "bold"), padx=30, pady=15,
                              activebackground="#006400", activeforeground="white",
                              bd=0, relief="flat")
        ready_btn.pack(pady=30)


if __name__ == "__main__":
    app = App()
    app.mainloop()