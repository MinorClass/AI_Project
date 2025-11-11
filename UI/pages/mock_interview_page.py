import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os
from pathlib import Path
import time
import cv2 
from PIL import Image, ImageTk 
from .GazeTracking.example import AttentionMonitor
import google.generativeai as genai 

API_KEY = "AIzaSyBSuHxEGpxivX39ZPjy_cuI1jvDq5MkdyM"  

try:
    genai.configure(api_key=API_KEY)
    MODEL = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    print(f"Gemini API 설정 실패: {e}. 질문 자동 생성 기능이 작동하지 않습니다.")
    MODEL = None


ASSETS_PATH = os.path.abspath("./UI/assets/mock_interview")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)


class MockInterview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")
        self.monitor = None
        self.controller = controller
        self.unfocustime = 0.0

        canvas = Canvas(self, bg="#FFFFFF", height=1080, width=1920)
        canvas.pack(fill="both", expand=True)

        self.bg_image = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(960, 540, image=self.bg_image)
          # 이미지
        self.image1 = PhotoImage(file=relative_to_assets("bimage_l.png"))
        canvas.create_image(225,210, image=self.image1, anchor="nw")

        self.image2 = PhotoImage(file=relative_to_assets("bimage_r.png"))
        canvas.create_image(955,210, image=self.image2, anchor="nw")
            #가상면접관 이미지 자리
        self.image3 = PhotoImage(file=relative_to_assets("image_v.png"))
        canvas.create_image(735,266, image=self.image3, anchor="nw")
            #질문창
        self.image4 = PhotoImage(file=relative_to_assets("image_q.png"))
        canvas.create_image(419,761, image=self.image4, anchor="nw")
            #feedback창
        self.image5 = PhotoImage(file=relative_to_assets("image_f.png"))
        canvas.create_image(1256,595, image=self.image5, anchor="nw")
            #면접자 cam있어야하는 자리
        self.image6 = PhotoImage(file=relative_to_assets("image_cam.png"))
        canvas.create_image(1310,266, image=self.image6, anchor="nw")

        self.image7 = PhotoImage(file=relative_to_assets("image_2.png"))
        canvas.create_image(230,147, image=self.image7, anchor="nw")
        
        # 6. 면접자 cam 자리 (1310, 266 - nw anchor)
        cam_x, cam_y = 1310, 266 
        
        # Tkinter Label을 생성하고 캔버스에 배치
        self.video_panel = tk.Label(self) 
        canvas.create_window(cam_x, cam_y, window=self.video_panel, anchor="nw")
        
        # 🌟 1. 질문 텍스트 변수 및 라벨 추가 (질문창 419, 761 - nw anchor 위치 활용)
        self.question_text = tk.StringVar(self)
        self.question_text.set("면접 시작 버튼을 눌러주세요.") 
        
        q_x, q_y = 440, 780 
        q_width = 480 
        
        self.question_label = tk.Label(self, textvariable=self.question_text, 
                                       font=("AnekGurmukhi Light", 18), fg="#353C92", bg="white", 
                                       justify=tk.LEFT, anchor="nw", wraplength=q_width) # 텍스트 줄바꿈 설정
        canvas.create_window(q_x, q_y, window=self.question_label, anchor="nw")
        
        # 🌟 2. 피드백 텍스트 레이블 추가
        self.feedback_text = tk.StringVar(self)
        self.feedback_text.set("")
        
        self.feedback_label = tk.Label(self, textvariable=self.feedback_text, 
                                       font=("AnekGurmukhi Light", 18), fg="#353C92", bg="white", 
                                       justify=tk.LEFT, anchor="nw")
        canvas.create_window(1270, 640, window=self.feedback_label, anchor="nw")
        

        # ... (종료 버튼, 시작 버튼, 진행시간 라벨 - 생략) ...
        # 종료 버튼
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(self, image=self.button_image_1,
                          command=self.stop_camera_and_quit, 
                          borderwidth=0, relief="flat")
        canvas.create_window(1548, 865, window=button_1, anchor="nw")

        # 면접시작 버튼
        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(self, image=self.button_image_2,
                          command=self.start_interview,  
                          borderwidth=0, relief="flat")
        canvas.create_window(455, 563, window=button_2, anchor="nw")
        
        # 진행시간 라벨
        canvas.create_text(447, 452, anchor="nw", text="진행시간", fill="#000000", font=("AnekGurmukhi Light", 22))
        self.timer_label = tk.Label(self, text="60", font=("Arial", 24), bg="#FFFFFF")
        canvas.create_window(445, 500, window=self.timer_label, anchor="nw")
        
        # 카메라 업데이트 루프를 위한 변수
        self.delay = 30 
        self.camera_update_id = None
        self.is_interview_running = False



    def _fetch_gemini_question(self):
        if not MODEL:
            return "Gemini API 설정에 문제가 있어 질문을 가져올 수 없습니다."
        
        try:
            question = "한국인 면접관으로 랜덤 질문 하나만 내봐 질문만 간결하게 답해줘"
            # 불필요한 공백/줄바꿈 제거 후 반환
            response = MODEL.generate_content(question)
            return response.text.strip()
            
        except Exception as e:
            return f"질문 생성 중 오류 발생: {e}"


    def start_interview(self):
        """면접 시작 시 질문을 가져오고 타이머 및 카메라 스트림을 시작합니다."""
        if not self.is_interview_running:
            self.is_interview_running = True
            
            #면접 시작 시 Gemini API를 호출하여 질문을 가져와서 업데이트
            question = self._fetch_gemini_question()
            self.question_text.set(question)
            
            self.start_timer()
            self.start_camera()
            self.update_camera() 

    def stop_camera_and_quit(self):
        """카메라를 해제하고 애플리케이션을 종료합니다."""
        if self.camera_update_id:
            self.after_cancel(self.camera_update_id) 
        if not self.monitor.__del__:
            self.monitor.__del__() 
        
        print(self.unfocustime)
        print("카메라 및 면접 모니터링이 중단되었습니다.")
        self.controller.show_frame("WaitGame")
        
    def start_timer(self):
        self.remaining_time = 60 #
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.config(text=str(self.remaining_time))
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
             self.is_interview_running = False
             self.monitor.__del__()
             self.question_text.set("면접 종료! 결과를 확인하세요.")

    def start_camera(self):
        self.monitor = AttentionMonitor(camera_index=4)

    def update_camera(self):
        ret, frame = self.monitor.get_frame()
        if ret:
            annotated_frame, results = self.monitor.process_frame()
            
            if annotated_frame is not None:
                cv2image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGBA)
                
                current_image = Image.fromarray(cv2image)
                
                cam_width, cam_height = 300, 300 
                resized_image = current_image.resize((cam_width, cam_height))
                self.photo = ImageTk.PhotoImage(image=resized_image)
                self.video_panel.config(image=self.photo)
                self.video_panel.image = self.photo 
                feedback, self.unfocustime = self._generate_feedback_text(results,self.unfocustime)
                self.feedback_text.set(feedback)
                
            
        self.camera_update_id = self.after(self.delay, self.update_camera)

    def _generate_feedback_text(self, results,unfocustime):
        feedback = []
        # 1. 시선 피드백
        gaze_text = results.get("gaze_text", "None")
        gaze_time = results.get("gaze_elapsed_time", 0.0)
        gaze_unfoucs = results.get("distraction_time")

        if "distraction" in gaze_text:
            feedback.append(f"시선 상태 : 눈을 맞추주십시오")
        elif "focus on right" in gaze_text or "focus on left" in gaze_text:
            feedback.append(f"시선 이탈 감지: 중앙을 벗어난 지 {gaze_time:.2f}초 경과.") 
        else:
            feedback.append(f"시선 상태: {gaze_text}")
        unfocustime = max(gaze_unfoucs,unfocustime)
        # 2. 떨림 피드백
        tremor_status = results.get("tremor_status", "(Stable)")
        
        if "Tremor" in tremor_status:
            feedback.append("신체 상태 : 불안정  ")
        elif "Stable" in tremor_status:
            feedback.append(f" 신체 상태: 안정적입니다.")
        else:
            feedback.append(f" 신체 상태: 감지 대기 중입니다.")
            
        return "\n".join(feedback),unfocustime

