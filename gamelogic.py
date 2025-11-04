"""
GAME LOGIC
- gameID에 따라 게임이 실행된다.
- 게임은 30초 동안 진행 -> 시간이 끝나면 종료
- 랜덤하게 문제가 만들어짐
- 푼 숫자/ 푼 숫자 내에서의 정답 여부 저장
"""
import time
import threading


class GameLogic: #게임 로직
    def runGame(self, gameId, duration = 30): #게임 실행
        raise NotImplementedError("Subclasses should implement this method.")
    
    def checkGameAnswer(self, input) -> 'GamePerformanceMetrics': #게임 답변 체크
        raise NotImplementedError("Subclasses should implement this method.")

class GamePerformanceMetrics: #게임 수행 성능 데이터
    def __init__(self, accuracy, reaction_time):
        self.accuracy = accuracy  # 푸는 문제 중에서 정답 비율
        # self.reaction_time = reaction_time  # 문제 푸는 시간 측정(선택)

class GameScore: #게임점수
    def __init__(self, total):
        self.total = total


class GameManager:
    def __init__(self):
        self.is_game_running = False
        self.duration = 30  # 지속시간
        self.games = {
            1: RockPaperScissorsGame()
            # 다른 게임들 추가
        }
    
    def timer(self):
        start_time = time.time()
        while self.is_game_running:
            remaining_time = int(self.duration - (time.time()-start_time))

            print(f'\r남은 시간: {remaining_time}초', end='', flush=True)

            if remaining_time <=0:
                self.is_game_running = False
                print("\n시간종료!")
                break

            time.sleep(0.1)
    
    def start_game(self, gameId):
        self.is_game_running = True

        # 타이머 스레드
        timer_thread = threading.Thread(target=self.timer)
        timer_thread.daemon = True
        timer_thread.start()

        if gameId in self.games:
            return self.games[gameId].runGame(self, gameId)
        else:
            raise ValueError("Invalid game ID")
        





"""
Rock-Paper-Scissors 게임 로직
- 가위바위보 게임을 30초 동안 진행
- 플레이어의 선택과 컴퓨터의 선택을 비교하여 승패 결정
- 승리 횟수, 패배 횟수, 무승부 횟수를 기록
- 최종 점수는 승리 횟수에 기반하여 계산

"""

class RockPaperScissorsGame(GameLogic): #가위바위보 게임
    def __init__(self):
        self.choices = ['rock', 'paper', 'scissors']
        self.who = ['computer', 'you']
        self.correct_count = 0
        self.solved_count = 0
        self.score_rsp = 0

    def runGame(self, manger, gameId): #게임 실행

        import random

        print('\n----------------------------------------------')
        print('내가 이겨야합니다(30초 경과 시 자동 종료)')

        while manager.is_game_running:
            blank_pick = random.choice(self.choices)
            who_pick = random.choice(self.who)
            print('\n----------------------------------------------')

            # --- 가위바위보 게임 로직 시작 ---
            if who_pick == 'computer':
                print (f'\nComputer: {blank_pick}')
                player_pick = input('\nrock scissors paper <-- One choice   ').upper()
                if  (blank_pick == 'rock' and player_pick == 'paper') or \
                    (blank_pick == 'scissors' and player_pick == 'rock') or \
                    (blank_pick == 'paper' and player_pick == 'scissors'):
                    self.correct_count += 1
            elif who_pick =='you':
                print (f'\nYou: {blank_pick}')
                computer_pick = input('\nrock scissors paper <-- One choice   ').upper()
                if  (blank_pick == 'paper' and computer_pick == 'rock') or \
                    (blank_pick == 'rock' and computer_pick == 'scissors') or \
                    (blank_pick == 'scissors' and computer_pick == 'paper'):
                    self.correct_count += 1
            
            self.solved_count += 1
        
        # --- 최종점수 출력 ---
        self.score_rsp = (self.correct_count / self.solved_count) *100
        print(f'Score: {self.score_rsp}점')



manager = GameManager()
manager.start_game(1)