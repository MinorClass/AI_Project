import pygame
import sys
import random
import time

# 초기화
pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("조건부 순서 클릭 게임")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
GREEN = (0, 200, 0)

# 폰트
font = pygame.font.SysFont(None, 120)
info_font = pygame.font.SysFont(None, 60)

# 숫자 객체
class NumberObj:
    def __init__(self, num, x, y):
        self.num = num
        self.state = "normal"  # normal, correct, wrong
        self.image = font.render(str(num), True, BLACK)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface):
        if self.state == "correct":
            color = RED
        elif self.state == "wrong":
            color = BLUE
        else:
            color = BLACK
        self.image = font.render(str(self.num), True, color)
        surface.blit(self.image, self.rect)

# 숫자 배치 함수 (3x3 격자)
def generate_numbers():
    positions = []
    grid_size = 200
    start_x = WIDTH // 2 - grid_size
    start_y = HEIGHT // 2 - grid_size

    for row in range(3):
        for col in range(3):
            x = start_x + col * grid_size
            y = start_y + row * grid_size
            positions.append((x, y))

    nums = list(range(1, 10))
    random.shuffle(positions)

    numbers = [NumberObj(n, x, y) for n, (x, y) in zip(nums, positions)]
    return numbers

def main():
    clock = pygame.time.Clock()
    numbers = generate_numbers()

    # 정답 시퀀스 정의 (2,3은 두 번 / 5는 제외)
    order = [1,2,2,3,3,4,6,7,8,9]

    current_index = 0
    start_time = None
    end_time = None
    score = 0
    result_message = ""
    result_color = BLACK

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if current_index < len(order):
                    target_num = order[current_index]
                    for num in numbers:
                        if num.rect.collidepoint(pos):
                            if start_time is None:
                                start_time = time.time()

                            if num.num == target_num:
                                num.state = "correct"
                                score += 10
                                current_index += 1
                            elif num.num == 5:
                                num.state = "wrong"
                                score -= 5
                            else:
                                score -= 5
                            break

                    if current_index >= len(order):
                        end_time = time.time()
                        elapsed = end_time - start_time
                        # 평가 메시지 결정
                        if elapsed <= 7:
                            result_message = "잘했다!"
                            result_color = GREEN
                        elif elapsed <= 10:
                            result_message = "평범하다"
                            result_color = BLACK
                        else:
                            result_message = "못했다"
                            result_color = BLUE
                        print(f"게임 클리어! 점수: {score}, 걸린 시간: {elapsed:.2f}초, 결과: {result_message}")

        # 숫자 그리기
        for num in numbers:
            num.draw(screen)

        # 조건 안내
        info_text = info_font.render("조건: 2와 3은 두 번(★), 5는 건너뛰기(■)", True, BLACK)
        screen.blit(info_text, (50, 50))

        # 점수 표시
        score_text = info_font.render(f"점수: {score}", True, BLACK)
        screen.blit(score_text, (50, 120))

        # 시간 표시
        if start_time is not None and end_time is None:
            elapsed = time.time() - start_time
            timer_text = info_font.render(f"시간: {elapsed:.2f}초", True, BLACK)
            screen.blit(timer_text, (50, 190))

        # 게임 종료 후 결과 메시지 표시
        if end_time is not None:
            result_text = info_font.render(f"결과: {result_message}", True, result_color)
            screen.blit(result_text, (WIDTH//2 - 150, HEIGHT//2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()