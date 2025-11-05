import cv2
import mediapipe as mp
from gaze_tracking import GazeTracking
import time
import math 

gaze = GazeTracking()
# NOTE: I
webcam = cv2.VideoCapture(4) 

# MediaPipe Solutions API 모듈 가져오기
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 떨림 감지를 위한 전역 설정
MAX_HISTORY_FRAMES = 30  # 떨림 판단을 위해 추적할 프레임 수
TREMOR_THRESHOLD = 0.3 # 떨림 판단 기준 (좌표 표준 편차 기준, 조정 가능) - 민감도를 더 낮추기 위해 값을 높임
nose_history = [] # 코 랜드마크 좌표 이력 저장 (Normalized X, Y)
tremor_status = "(Stable)" # 현재 떨림 상태 메시지
# ----------------------------------------------------

gaze_start_time = None
is_gaze_outside_center = False
ALERT_THRESHOLD = 3.0

def calculate_tremor(x_history, y_history):
    """주어진 좌표 이력의 표준 편차를 계산하여 떨림 정도를 반환합니다."""
    if len(x_history) < MAX_HISTORY_FRAMES:
        return 0.0 # 이력이 충분하지 않으면 0 반환
    
    # 평균 계산
    mean_x = sum(x_history) / MAX_HISTORY_FRAMES 
    mean_y = sum(y_history) / MAX_HISTORY_FRAMES
    
    # 분산 계산: (좌표 - 평균)^2의 합
    variance_x = sum([(x - mean_x) ** 2 for x in x_history]) / MAX_HISTORY_FRAMES
    variance_y = sum([(y - mean_y) ** 2 for y in x_history]) / MAX_HISTORY_FRAMES # <-- 수정: y_history로 수정해야 함
    
    # 표준 편차 계산 (루트 분산)
    std_dev_x = math.sqrt(variance_x)
    std_dev_y = math.sqrt(variance_y)
    
    # X와 Y 표준 편차의 합을 떨림 지수로 사용
    return std_dev_x + std_dev_y

# -------------------------

LANDMARK_SPEC = mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4)
CONNECTION_SPEC = mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)

with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1, 
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:

    while True:
        ret, frame = webcam.read()
        if not ret:
            break
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""
        
        current_time = time.time()
        elapsed_time = 0.0
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # ------------------- 감지 실행 (동기 방식) -------------------
        results = pose.process(rgb_frame)
        
        # 떨림 감지 및 랜드마크 그리기 초기화
        current_tremor_score = 0.0
        
        if results.pose_landmarks:
            # 랜드마크 그리기
            mp_drawing.draw_landmarks(
                frame, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                LANDMARK_SPEC,
                CONNECTION_SPEC
            )
            
            # ------------------- 떨림 감지 로직 -------------------
            # 🚨 왼쪽 손목 대신 코(NOSE) 랜드마크 인덱스로 변경
            NOSE_INDEX = mp_pose.PoseLandmark.NOSE.value
            nose_landmark = results.pose_landmarks.landmark[NOSE_INDEX]
            
            # 랜드마크 유효성 검사 (visibility가 충분히 높아야 함)
            if nose_landmark.visibility > 0.8:
                
                # 랜드마크 좌표 이력 업데이트 (Normalized X, Y 사용)
                nose_history.append((nose_landmark.x, nose_landmark.y))
                
                # 이력 관리를 위해 가장 오래된 이력 제거
                if len(nose_history) > MAX_HISTORY_FRAMES:
                    nose_history.pop(0)

                # 이력이 충분할 때 떨림 계산
                if len(nose_history) == MAX_HISTORY_FRAMES:
                    x_coords = [p[0] for p in nose_history]
                    y_coords = [p[1] for p in nose_history]
                    
                    current_tremor_score = calculate_tremor(x_coords, y_coords)
                    
                    if current_tremor_score > TREMOR_THRESHOLD:
                        tremor_status = f"(Tremor): {current_tremor_score:.5f}"
                        text_color = (0, 0, 255) # 빨간색
                    else:
                        tremor_status = f"(Stable): {current_tremor_score:.5f}"
                        text_color = (0, 255, 0) # 녹색
                
            else:
                tremor_status = "(Nose not visible)"
                text_color = (255, 255, 255) # 흰색
        else:
            tremor_status = "No pose detected)"
            text_color = (255, 255, 255) # 흰색

        
        if gaze.is_blinking():
            text = "Blinking"
        
        elif gaze.is_center():
            text = "Looking center"
            # 중앙을 볼 때 타이머 초기화
            gaze_start_time = None
            is_gaze_outside_center = False
        
        elif gaze.is_right() or gaze.is_left():
            # 왼쪽 또는 오른쪽을 볼 때 (중앙을 벗어난 경우)
            
            if not is_gaze_outside_center:
                # 중앙을 벗어난 상태가 '아니었다면' (새로 벗어남) 타이머 시작
                gaze_start_time = current_time
                is_gaze_outside_center = True
                
            # 경과 시간 계산
            if gaze_start_time is not None:
                elapsed_time = current_time - gaze_start_time
                
            if gaze.is_right():
                text = f"Looking right ({elapsed_time:.2f}s)"
            else: #
                text = f"Looking left ({elapsed_time:.2f}s)"
                
        else:
            # 감지되지 않거나 기타 상태일 경우
            text = "Undetermined"
            gaze_start_time = None
            is_gaze_outside_center = False

        
        alert_text = ""
        alert_color = (147, 58, 31) # 기본 텍스트 색상=
        
        # 중앙을 벗어난 상태이고, 경과 시간이 3초를 넘었을 때 경고 활성화
        if is_gaze_outside_center and elapsed_time >= ALERT_THRESHOLD:
            alert_text = ""
            alert_color = (0, 0, 255) # 빨간색 경고
            # 주 텍스트도 경고 메시지로 덮어쓸 수 있습니다.
            text = f"Distracted: {elapsed_time:.2f}s"


        # 시선 상태 및 시간 표시
        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, alert_color, 2)
        
        # 3초 경고 메시지 표시 (있을 경우)
        if alert_text:
            cv2.putText(frame, alert_text, (90, 210), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 2)


        # 동공 좌표 표시 (원래 코드 유지)
        cv2.putText(frame, "Tremor Status: " + tremor_status, (90, 95), cv2.FONT_HERSHEY_DUPLEX, 0.9, text_color, 1) # <--- 추가: 떨림 상태 표시
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        # cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        # cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        cv2.imshow("Demo", frame)

        if cv2.waitKey(1) == 27:
            break
   
webcam.release()
cv2.destroyAllWindows()