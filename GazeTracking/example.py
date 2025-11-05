import cv2
import mediapipe as mp
from gaze_tracking import GazeTracking
import time
import math

# ====================================================================
# 설정 상수
# ====================================================================

# 떨림 감지 설정
MAX_HISTORY_FRAMES = 30  # 떨림 판단을 위해 추적할 프레임 수
TREMOR_THRESHOLD = 0.03  # 떨림 판단 기준 (이 값보다 크면 'Tremor')

# 시선 경고 설정
ALERT_THRESHOLD = 3.0 # 초 (중앙을 벗어난 시선 지속 시간)

# MediaPipe 떨림 계산 및 추적을 위한 랜드마크 인덱스
LEFT_EAR_INDEX = mp.solutions.pose.PoseLandmark.LEFT_EAR.value
RIGHT_EAR_INDEX = mp.solutions.pose.PoseLandmark.RIGHT_EAR.value
NOSE_INDEX = mp.solutions.pose.PoseLandmark.NOSE.value

# ====================================================================
# 떨림 계산 도우미 함수
# ====================================================================

def calculate_tremor(x_history, y_history, scale_factor):
    """
    정규화된 랜드마크 좌표의 '분산 합의 제곱근(RSV)'을 기반으로 
    귀 사이 거리로 스케일링된 떨림 지수를 계산합니다.
    """
    history_len = len(x_history)
    # 이력이 충분하지 않거나 스케일 팩터(귀 사이 거리)가 0이면 0 반환
    if history_len == 0 or history_len < MAX_HISTORY_FRAMES or scale_factor == 0:
        return 0.0
    
    # 평균 계산
    mean_x = sum(x_history) / history_len
    mean_y = sum(y_history) / history_len
    
    # 분산 계산: (좌표 - 평균)^2의 합
    variance_x = sum([(x - mean_x) ** 2 for x in x_history]) / history_len
    variance_y = sum([(y - mean_y) ** 2 for y in x_history]) / history_len 
    
    # 떨림 지수 (분산 합의 제곱근)
    tremor_index = math.sqrt(variance_x + variance_y)
    
    # 귀 사이 거리(scale_factor)로 나누어 정규화
    return tremor_index / scale_factor

# ====================================================================
# 주의력 모니터링 클래스
# ====================================================================

class AttentionMonitor:
    """
    시선 추적과 머리 떨림 감지를 통합하여 주의력과 안정성을 모니터링하는 클래스입니다.
    """
    def __init__(self, camera_index=4):
        # 추적 객체 초기화
        self.gaze = GazeTracking()
        # MediaPipe Pose 객체 초기화
        self.pose_detector = mp.solutions.pose.Pose(
            static_image_mode=False,
            model_complexity=1, 
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        # 웹캠 캡처 객체 초기화
        self.cap = cv2.VideoCapture(camera_index)
        
        # 떨림 관련 상태 변수
        self.nose_history = []  # 코 랜드마크 이력 저장 (정규화된 X, Y)
        self.tremor_status = "(Stable)" # 현재 떨림 상태 메시지
        self.current_tremor_score = 0.0 # 현재 떨림 점수
        
        # 시선 관련 상태 변수
        self.gaze_start_time = None # 중앙을 벗어난 시선 시작 시간
        self.is_gaze_outside_center = False # 중앙을 벗어난 상태 여부
        
        # 현재 프레임 저장 변수
        self.frame = None

    def __del__(self):
        """객체가 소멸될 때 리소스를 정리합니다."""
        self.pose_detector.close()
        self.cap.release()

    def get_frame(self):
        """웹캠에서 프레임을 읽어옵니다."""
        ret, self.frame = self.cap.read()
        return ret, self.frame

    def process_frame(self):
        """
        현재 프레임을 처리하여 시선 추적 및 자세 추정을 수행하고,
        상태를 업데이트하며, 주석이 달린 프레임과 측정 결과를 반환합니다.
        """
        if self.frame is None:
            return None, "로드된 프레임 없음"

        current_time = time.time()
        elapsed_time = 0.0
        
        # 1. 시선 추적 실행
        self.gaze.refresh(self.frame)
        annotated_frame = self.gaze.annotated_frame()
        
        # 2. 자세 추정 실행 (떨림 감지용)
        rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        results = self.pose_detector.process(rgb_frame)
        
        # 3. 떨림 감지 로직 실행
        self._detect_tremor(results)

        # 4. 시선 상태 로직 실행
        gaze_text, elapsed_time, alert_text = self._check_gaze_status(current_time)

        # 5. 프레임에 정보 그리기
        
        # 시선 상태 텍스트
        alert_color = (147, 58, 31) # 기본 텍스트 색상
        if alert_text:
            alert_color = (0, 0, 255) # 경고 시 빨간색
        cv2.putText(annotated_frame, gaze_text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, alert_color, 2)
        
        # 떨림 상태 텍스트
        text_color = (255, 255, 255) # 기본 흰색
        if "Tremor" in self.tremor_status:
            text_color = (0, 0, 255) # 떨림 시 빨간색
        elif "Stable" in self.tremor_status:
            text_color = (0, 255, 0) # 안정 시 녹색

        cv2.putText(annotated_frame, "Tremor: " + self.tremor_status, (90, 95), cv2.FONT_HERSHEY_DUPLEX, 0.9, text_color, 1) 
            
        # 경고 메시지 표시
        if alert_text:
            cv2.putText(annotated_frame, alert_text, (90, 130), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 2)
        
        # 측정 결과 딕셔너리 반환
        return annotated_frame, {
            "gaze_text": gaze_text,
            "tremor_status": self.tremor_status,
            "tremor_score": self.current_tremor_score,
            "gaze_elapsed_time": elapsed_time
        }

    def _detect_tremor(self, results):
        """떨림 감지 로직을 처리하는 내부 메서드."""
        self.current_tremor_score = 0.0
        
        if not results.pose_landmarks:
            self.tremor_status = "(None dectection)"
            self.nose_history.clear() # 감지 실패 시 이력 초기화
            return

        # 1. 스케일링을 위한 기준점 정의 (귀)
        left_ear = results.pose_landmarks.landmark[LEFT_EAR_INDEX]
        right_ear = results.pose_landmarks.landmark[RIGHT_EAR_INDEX]

        # 2. 스케일 팩터 계산 (귀 사이의 정규화된 거리)
        scale_factor = math.sqrt(
            (right_ear.x - left_ear.x)**2 + (right_ear.y - left_ear.y)**2
        )
        
        # 3. 떨림 감지 대상 랜드마크 (코)
        nose_landmark = results.pose_landmarks.landmark[NOSE_INDEX]
        
        # 랜드마크 가시성(visibility) 확인
        if nose_landmark.visibility > 0.8:
            # 랜드마크 이력 업데이트 (정규화된 X, Y)
            self.nose_history.append((nose_landmark.x, nose_landmark.y))
            
            # 이력 크기 관리
            if len(self.nose_history) > MAX_HISTORY_FRAMES:
                self.nose_history.pop(0)

            # 이력이 충분할 때 떨림 계산
            if len(self.nose_history) == MAX_HISTORY_FRAMES:
                x_coords = [p[0] for p in self.nose_history]
                y_coords = [p[1] for p in self.nose_history]
                
                # 4. 떨림 점수 계산
                self.current_tremor_score = calculate_tremor(x_coords, y_coords, scale_factor)
                
                # 떨림 기준치와 비교하여 상태 업데이트
                if self.current_tremor_score > TREMOR_THRESHOLD:
                    self.tremor_status = f"(Tremor): {self.current_tremor_score:.5f}"
                else:
                    self.tremor_status = f"(Stable): {self.current_tremor_score:.5f}"
            
        else:
            self.tremor_status = "(Nose not Detection)"
            self.nose_history.clear() # 랜드마크 손실 시 이력 초기화

    def _check_gaze_status(self, current_time):
        """시선 상태 및 경고 로직을 처리하는 내부 메서드."""
        gaze_text = ""
        elapsed_time = 0.0
        alert_text = ""
        
        if self.gaze.is_blinking():
            gaze_text = ""
        
        elif self.gaze.is_center():
            gaze_text = "Center"
            # 중앙을 볼 때 타이머 초기화
            self.gaze_start_time = None
            self.is_gaze_outside_center = False
        
        elif self.gaze.is_right() or self.gaze.is_left():
            # 중앙을 벗어난 시선
            
            if not self.is_gaze_outside_center:
                # 새로 벗어났다면 타이머 시작
                self.gaze_start_time = current_time
                self.is_gaze_outside_center = True
                
            # 경과 시간 계산
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
        
        # 경고 확인
        if self.is_gaze_outside_center and elapsed_time >= ALERT_THRESHOLD:
            # 중요한 경고를 위해 메인 텍스트를 덮어씀
            gaze_text = f"distraction: {elapsed_time:.2f}s"
            alert_text = "Caution"

        return gaze_text, elapsed_time, alert_text