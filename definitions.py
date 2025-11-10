"""
main 제어부
- app 내에 돌아가는 기능 제어

"""
class Controller: #제어
    
    def startSessionFlow(self): #세션 시작
        game_data = self.runGame("g1") #임의로 게임코드 부여후 실행
        performance = self.checkGameAnswer(game_data) #게임 결과를 스코어로 저장
        behavior = self.analyzeBehavior() #행동점수를 저장
        final_score = self.calculateFinalScore(performance, behavior) #최종 점수로 결합
        self.displayScore(final_score)
    
    def runGame(self, gameId): #게임실행
        return GameLogic().runGame(gameId)
    
    def checkGameAnswer(self, input_data): #게임 답변 계산
        return GameLogic().checkGameAnswer(input_data)
    
    def analyzeBehavior(self): 
        eye_score = BehaviorTracker().trackEyeContact("eyeData")
        posture_score = BehaviorTracker().trackPosture("poseData")
        vocal_score = BehaviorTracker().trackVocalTremor("voiceData")
        
        return (eye_score.eye_discontact + posture_score.wrong_posture + vocal_score.vocal_tremor) / 3.0

    
    def calculateFinalScore(self, performance, behavior): # 최종 점수 계산
        gameScore = ScoringSystem().calculateGameScore(performance)
        behaviorScore = ScoringSystem().calculateBehaviorScore(behavior)
        return ScoringSystem().combineScores(gameScore, behaviorScore)
    
    def displayScore(self, data): #점수를 보여줌
        print(f"점수: {data.score:.2f}")




"""
GAME LOGIC
- gameID에 따라 게임이 실행된다.
- 게임은 30초 동안 진행 -> 시간이 끝나면 종료
- 랜덤하게 문제가 만들어짐
- 푼 숫자/ 푼 숫자 내에서의 정답 여부 저장
"""
class GameLogic: #게임 로직
    def runGame(self, gameId): #게임 실행
        #game Id를 조건으로 게임선택
        #실행될 게임 구현
        pass
    
    def checkGameAnswer(self, input) -> 'GamePerformanceMetrics': #게임 답변 체크
        pass


class GamePerformanceMetrics: #게임 수행 성능 데이터
    def __init__(self, accuracy, reaction_time):
        self.accuracy = accuracy  # 푸는 문제 중에서 정답 비율
        # self.reaction_time = reaction_time  # 문제 푸는 시간 측정(선택)

class GameScore: #게임점수
    def __init__(self, total):
        self.total = total


"""
Behavior Tracker 행동 추적시스템
<AI 모델을 사용하여 영상 내에서 tracking system 구현>
- 동공 흔들림 추적
- 자세 추적
- 음성 떨림 추적(선택)

<자료의 활용>
- 예시) 10초 이상 다른 곳을 보았다 score -= 1
- 예시) 몸을 10초이상 흔든다
"""

class BehaviorTracker: #행점 점수 추적

    def trackEyeContact(self, eyeData) -> 'BehaviorScore': # 시야 트랙킹
        pass
    
    def trackPosture(self, poseData) -> 'BehaviorScore': # 자세 추적 
        pass
    
    def trackVocalTremor(self, voiceData) -> 'BehaviorScore': # 음성 떨림 추적
        pass

# 밑의 함수 활용해서 행동 점수 계산

class BehaviorScore: #행동 점수 
    def __init__(self, eye_discontact, wrong_posture, vocal_tremor):
        self.eye_discontact = eye_discontact
        self.wrong_posture = wrong_posture
        self.vocal_tremor = vocal_tremor


class IFeedbackSystem: #피드백 시스템
    def generateFeedback(self, data): # 행동점수 깍일때마다 피드백 노출
        pass



"""
Final Report Page
최종 보고서 영역
- 게임 점수
- 면접 점수
- 종합 보고서 (시간 보고) -LLM 돌릴 수 있었으면 좋을듯
"""

class MainApp:
    def displayScore(self, data):
        print(f"점수: {data.combined_score:.2f}")

class ReportData: #보고 데이터
    def __init__(self, text_report, score_summary):
        self.text_report = text_report
        self.score_summary = score_summary


class ScoringSystem: #점수 시스템
    
    def calculateGameScore(self, metrics) -> 'GameScore': # 게임 정수계산
        pass
    def calculateBehaviorScore(self, metrics) -> 'BehaviorScore': # 행동 점수 계산
        pass
    def combineScores(self, gameScore, behaviorScore) -> 'FinalScore': # 점수 통합
        pass

class FinalScore: #최종 점수
    def __init__(self, combined_score):
        self.combined_score = combined_score


class FeedbackGenerator(IFeedbackSystem): # 피드백 생성 시스탬

    def generateRealtime(self, metrics) -> str: # 실시간 피드백 생성 
        pass
    
    def generateFinalReport(self, metrics) -> 'ReportData': # 최종 보고서 작성
        pass
    
    def generateFeedback(self, data): #피드백 생성 기본적으로 상속 받음
        pass


