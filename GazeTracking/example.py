import cv2
import mediapipe as mp
from gaze_tracking import GazeTracking
import time
import math
import numpy as np # ✨ NumPy 라이브러리 추가

# ====================================================================
# 설정 상수 (개선)
# ====================================================================

# 떨림 감지 설정
FFT_WINDOW_SIZE = 64  # 주파수 분석을 위해 추적할 프레임 수 (2의 거듭제곱)
FPS = 30 # 비디오 캡처 FPS (실제 환경에 맞게 조정 필요)
TREMOR_FREQUENCY_RANGE = (3.0, 15.0) # 떨림으로 간주할 주파수 대역 (Hz)
TREMOR_AMPLITUDE_THRESHOLD = 0.05  # 떨림 판단 기준 (정규화된 진폭)

# 시선 경고 설정 (기존과 동일)
ALERT_THRESHOLD = 3.0 # 초 (중앙을 벗어난 시선 지속 시간)

# MediaPipe 떨림 계산 및 추적을 위한 랜드마크 인덱스
LEFT_EAR_INDEX = mp.solutions.pose.PoseLandmark.LEFT_EAR.value
RIGHT_EAR_INDEX = mp.solutions.pose.PoseLandmark.RIGHT_EAR.value
NOSE_INDEX = mp.solutions.pose.PoseLandmark.NOSE.value


def calculate_tremor_parameters(x_history, y_history, scale_factor, fps):
    """
    떨림의 진폭 및 주파수를 계산합니다.
    """
    history_len = len(x_history)
    
    if history_len < FFT_WINDOW_SIZE or scale_factor == 0 or fps == 0:
        return 0.0, 0.0 # 진폭, 주파수

    # 1. 진폭(Amplitude) 계산 

    # 평균 계산
    mean_x = np.mean(x_history)
    mean_y = np.mean(y_history)
    
    # 분산 합의 제곱근
    variance_x = np.mean([(x - mean_x) ** 2 for x in x_history])
    variance_y = np.mean([(y - mean_y) ** 2 for y in y_history]) 
    
    # 정규화된 진폭
    tremor_amplitude = math.sqrt(variance_x + variance_y) / scale_factor
    
    # 2. 주파수(Frequency) 계산 (FFT 적용)
    
    # 코 랜드마크의 2차원 변위 벡터
    displacement_signal = np.array(x_history) + 1j * np.array(y_history) # 복소수 신호로 결합

    # FFT 계산
    fft_values = np.fft.fft(displacement_signal)
    fft_power = np.abs(fft_values)
    
    # 주파수 축 생성
    frequencies = np.fft.fftfreq(history_len, d=1.0/fps)
    
    # 양수 주파수 대역만 사용 (대칭이므로)
    positive_frequencies = frequencies[1:history_len//2]
    positive_power = fft_power[1:history_len//2]
    
    if len(positive_frequencies) == 0:
        return tremor_amplitude, 0.0

    # 3. 떨림 주파수 대역 내의 최대 파워 주파수 찾기
    
    # 떨림 대역 내의 인덱스 마스크
    mask = (positive_frequencies >= TREMOR_FREQUENCY_RANGE[0]) & \
           (positive_frequencies <= TREMOR_FREQUENCY_RANGE[1])

    if np.any(mask):
        # 떨림 대역 내에서 최대 파워를 가진 주파수
        tremor_index = np.argmax(positive_power[mask])
        tremor_frequency = positive_frequencies[mask][tremor_index]
    else:
        tremor_frequency = 0.0 # 떨림 대역에서 유의미한 주파수가 없음
        
    return tremor_amplitude, tremor_frequency

class AttentionMonitor:
    
    def __init__(self, camera_index=4):
        self.gaze = GazeTracking()
        self.pose_detector = mp.solutions.pose.Pose(
            static_image_mode=False, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5
        )
        self.cap = cv2.VideoCapture(camera_index)
        
        # 실제 카메라 FPS를 가져오거나 설정값 사용
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) 
        if self.fps <= 1.0: # FPS 획득 실패 시 기본값
            self.fps = FPS 

        # 떨림 관련 상태 변수 (업데이트)
        self.nose_history_x = [] # 코 X 랜드마크 이력
        self.nose_history_y = [] # 코 Y 랜드마크 이력
        self.tremor_status = "(Stable)" 
        self.current_amplitude = 0.0 # 현재 떨림 진폭
        self.current_frequency = 0.0 # 현재 떨림 주파수
        
        # 시선 관련 상태 변수 (기존과 동일)
        self.gaze_start_time = None 
        self.is_gaze_outside_center = False
        
        self.frame = None

    def __del__(self):
        self.pose_detector.close()
        self.cap.release()

    # (get_frame 메소드는 기존과 동일)
    def get_frame(self):
        ret, self.frame = self.cap.read()
        return ret, self.frame

    def process_frame(self):
        if self.frame is None:
            return None, "로드된 프레임 없음"

        current_time = time.time()
        
        # 1. 시선 추적 및 자세 추정 (기존과 동일)
        self.gaze.refresh(self.frame)
        annotated_frame = self.gaze.annotated_frame()
        rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        results = self.pose_detector.process(rgb_frame)
        
        # 2. 떨림 감지 로직 실행 (수정)
        self._detect_tremor(results)

        # 3. 시선 상태 로직 실행 (기존과 동일)
        gaze_text, elapsed_time, alert_text = self._check_gaze_status(current_time)

        # 4. 프레임에 정보 그리기 (수정)
        
        # # 시선 상태 텍스트
        # alert_color = (147, 58, 31) 
        # if alert_text:
        #     alert_color = (0, 0, 255) 
        # cv2.putText(annotated_frame, gaze_text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, alert_color, 2)
        
        # 떨림 상태 텍스트 (진폭 및 주파수 표시)
        text_color = (255, 255, 255)
        if "Tremor" in self.tremor_status:
            text_color = (0, 0, 255)
        elif "Stable" in self.tremor_status:
            text_color = (0, 255, 0)
            
        tremor_display = f"Tremor: {self.tremor_status}"
        tremor_info = f"Amp: {self.current_amplitude:.5f} | Freq: {self.current_frequency:.2f}Hz"
        
        # cv2.putText(annotated_frame, tremor_display, (90, 95), cv2.FONT_HERSHEY_DUPLEX, 0.9, text_color, 1) 
        # cv2.putText(annotated_frame, tremor_info, (90, 125), cv2.FONT_HERSHEY_DUPLEX, 0.7, text_color, 1)
            
        # 경고 메시지 표시
        if alert_text:
            cv2.putText(annotated_frame, alert_text, (90, 160), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 2)
        
        # 측정 결과 딕셔너리 반환
        return annotated_frame, {
            "gaze_text": gaze_text,
            "tremor_status": self.tremor_status,
            "tremor_amplitude": self.current_amplitude, 
            "tremor_frequency": self.current_frequency, 
            "gaze_elapsed_time": elapsed_time
        }

    def _detect_tremor(self, results): #떨림 감지 

        self.current_amplitude = 0.0
        self.current_frequency = 0.0
        
        if not results.pose_landmarks:
            self.tremor_status = "(None dectection)"
            self.nose_history_x.clear() 
            self.nose_history_y.clear()
            return

        # 1. 스케일링을 위한 기준점 정의 (귀)
        left_ear = results.pose_landmarks.landmark[LEFT_EAR_INDEX]
        right_ear = results.pose_landmarks.landmark[RIGHT_EAR_INDEX]

        # 2. 스케일 팩터 계산 
        scale_factor = math.sqrt(
            (right_ear.x - left_ear.x)**2 + (right_ear.y - left_ear.y)**2
        )
        
        # 3. 떨림 감지 대상 랜드마크 (코)
        nose_landmark = results.pose_landmarks.landmark[NOSE_INDEX]
        
        if nose_landmark.visibility > 0.8:
            
            # 랜드마크 이력 업데이트
            self.nose_history_x.append(nose_landmark.x)
            self.nose_history_y.append(nose_landmark.y)
            
            # 이력 크기 관리
            if len(self.nose_history_x) > FFT_WINDOW_SIZE:
                self.nose_history_x.pop(0)
                self.nose_history_y.pop(0)

            # 이력이 충분할 때 떨림 계산
            if len(self.nose_history_x) == FFT_WINDOW_SIZE:
                
                # 4. 떨림 점수 (진폭 및 주파수) 계산
                amp, freq = calculate_tremor_parameters(
                    self.nose_history_x, 
                    self.nose_history_y, 
                    scale_factor, 
                    self.fps
                )
                
                self.current_amplitude = amp #이걸 기준으로 잡아야할듯 
                self.current_frequency = freq
                
                # 떨림 기준치와 비교하여 상태 업데이트
                # 떨림 진폭과 주파수가 떨림 대역에 속하는지 동시 확인
                is_tremor_frequency = freq > 0.0
                is_significant_amplitude = amp > TREMOR_AMPLITUDE_THRESHOLD
                
                if is_tremor_frequency and is_significant_amplitude:
                    self.tremor_status = f"(Tremor)" #아니면 여기서 처리
                else:
                    self.tremor_status = f"(Stable)"
            
        else:
            self.tremor_status = "(Nose not Detection)"
            self.nose_history_x.clear() 
            self.nose_history_y.clear()

    def _check_gaze_status(self, current_time):
        gaze_text = ""
        elapsed_time = 0.0
        alert_text = ""
        
        if self.gaze.is_blinking():
            gaze_text = ""
        
        elif self.gaze.is_center():
            gaze_text = "Center"
            self.gaze_start_time = None
            self.is_gaze_outside_center = False
        
        elif self.gaze.is_right() or self.gaze.is_left():
            
            if not self.is_gaze_outside_center:
                self.gaze_start_time = current_time
                self.is_gaze_outside_center = True
                
            if self.gaze_start_time is not None:
                elapsed_time = current_time - self.gaze_start_time
                
            if self.gaze.is_right():
                gaze_text = f"focus on right ({elapsed_time:.2f}s)"
            else: 
                gaze_text = f"focus on left ({elapsed_time:.2f}s)"
                
        else:
            gaze_text = "None"
            self.gaze_start_time = None
            self.is_gaze_outside_center = False
        
        if self.is_gaze_outside_center and elapsed_time >= ALERT_THRESHOLD:#집중못한 시간 스코어로 내서 받아와야함
            gaze_text = f"distraction: {elapsed_time:.2f}s"
            alert_text = "Caution"

        return gaze_text, elapsed_time, alert_text