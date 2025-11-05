import tkinter as tk
from PIL import Image, ImageTk
import os 
import cv2 # 웹캠 기능을 위해 OpenCV 추가 (AttentionMonitor 내부에서 사용)
from example import  AttentionMonitor

# 1. 현재 실행 중인 파일의 절대 경로를 얻습니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
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
            # 캔버스 크기에 맞게 이미지 로드
            self.bg_img = Image.open(BACKGROUND_PATH).resize((1920, 1080), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_img)
        except FileNotFoundError:
            # 파일을 찾지 못하면 오류 메시지 출력 후 흰색 배경으로 대체
            print(f"ERROR: 배경 이미지 파일 '{BACKGROUND_PATH}'를 찾을 수 없습니다. 대체 배경색을 사용합니다.")
            self.bg_photo = None # 배경 이미지 로드 실패 처리
        # 컨테이너
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # 페이지 등록
        # App 클래스가 프레임 인스턴스를 직접 생성하여 관리
        self.frames = {}
        for F in (MainPage, InterviewPage):
            page_name = F.__name__
            frame = F(self.container, self)
            self.frames[page_name] = frame

        # 첫 화면 표시
        self.current_frame = None
        self.show_frame("MainPage")

    def show_frame(self, name):
        # 이전 페이지 숨기기 전에 on_hide 이벤트 실행 (카메라 해제 등)
        if self.current_frame:
            self.current_frame.on_hide()
            self.current_frame.place_forget()

        # 새 페이지 표시 및 on_show 이벤트 실행
        frame = self.frames[name]
        frame.on_show()
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
        # 캔버스 중앙에 오버레이 프레임 배치
        self.canvas.create_window(960, 540, window=self.overlay, anchor="center")

    def on_show(self):
        # 페이지가 표시될 때 실행되는 로직 (선택적)
        pass

    def on_hide(self):
        # 페이지가 숨겨질 때 실행되는 로직 (카메라 해제 등)
        pass


class MainPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # 메인 콘텐츠 박스
        box = tk.Frame(self.overlay, bg="white", width=800, height=600, bd=2, relief="groove")
        # Tkinter 프레임 크기 고정을 위해 pack_propagate(False) 사용
        box.pack_propagate(False) 
        box.pack(pady=50)

        # 제목
        header = tk.Label(box, text="AI 면접 훈련 도구",
                          bg="#4B0082", fg="white", font=("Arial", 28, "bold"), pady=15)
        header.pack(fill="x")

        # 메시지
        msg = tk.Label(box, text="부족한 면접 경험을 AI와 함께 채워 나가보세요.",
                       bg="white", fg="#333333", font=("Arial", 18, "bold"), pady=40)
        msg.pack()

        # 시작 버튼
        start_btn = tk.Button(box, text="시작하기",
                              bg="#6A0DAD", fg="white", font=("Arial", 18, "bold"),
                              padx=30, pady=15,
                              activebackground="#8A2BE2", activeforeground="white",
                              bd=0, relief="flat",
                              command=lambda: controller.show_frame("InterviewPage"))
        start_btn.pack(pady=40)


class InterviewPage(BasePage):
    DEFAULT_CAM_WIDTH = 300
    DEFAULT_CAM_HEIGHT = 300
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # 웹캠 관련 변수 초기화 
        self.monitor = None #
        self.is_streaming = False
        self.cam_label_width = self.DEFAULT_CAM_WIDTH
        self.cam_label_height = self.DEFAULT_CAM_HEIGHT
        self.current_photo = None #

        # 인터뷰 페이지의 메인 컨테이너 (중앙 정렬)
        main_content = tk.Frame(self.overlay, bg="white", bd=2, relief="groove", width=800, height=800)
        main_content.pack_propagate(False)
        main_content.pack(pady=50)

        # 네비게이션/타이틀 프레임 (main_content 내부에 배치)
        nav = tk.Frame(main_content, bg="white")
        nav.pack(fill="x", pady=(10, 20))

        back_btn = tk.Button(nav, text="< 이전", 
                             font=("Arial", 12),
                             bd=0, relief="flat",
                             # show_frame 호출 시 on_hide가 자동으로 호출됩니다.
                             command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(side="left", padx=20)

        title = tk.Label(nav, text="가상 면접", font=("Arial", 22, "bold"), bg="white", fg="#4B0082")
        title.pack(side="left", padx=20, expand=True)

        # 카메라 화면 영역
        # 프레임 크기를 레이블 기본 크기에 맞춥니다.
        cam_frame = tk.Frame(main_content, bg="#DDDDDD", bd=5, relief="solid", 
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

        # 버튼 프레임
        btn_frame = tk.Frame(main_content, bg="white")
        btn_frame.pack(pady=20)

        mic_btn = tk.Button(btn_frame, text="마이크 연결", width=15, font=("Arial", 14), bg="#C0C0C0")
        mic_btn.grid(row=0, column=0, padx=15, pady=10)

        # 카메라 연결 버튼: start_monitoring 메서드 연결로 변경
        cam_btn = tk.Button(btn_frame, text="카메라 연결", width=15, font=("Arial", 14), bg="#4CAF50", fg="white",
                            command=self.start_monitoring)
        cam_btn.grid(row=0, column=1, padx=15, pady=10)

        # 준비 완료 버튼
        ready_btn = tk.Button(main_content, text="준비 완료", 
                              bg="#008000", fg="white",
                              font=("Arial", 18, "bold"), padx=30, pady=15,
                              activebackground="#006400", activeforeground="white",
                              bd=0, relief="flat")
        ready_btn.pack(pady=30)
    
    # 웹캠 스트리밍 시작 -> 모니터링 시작으로 변경
    def start_monitoring(self):
        # AttentionMonitor 객체가 이미 존재하고 카메라가 열려있다면 중복 실행 방지
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
            
            # 5. Tkinter PhotoImage로 변환 및 참조 유지
            # Tkinter 레이블 크기에 맞게 이미지 크기를 조정할 수 있습니다.
            # 여기서는 기본 크기(300x300)에 맞춥니다.
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