import pygame
import os
import random
import sys
import socket
import pickle
import time

# 현재 파일의 디렉토리로 경로 설정
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 패들 설정
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
player = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# 클라이언트 설정
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))

# 점수 및 설정
font = pygame.font.Font(None, 74)
winning_score = 11
deuce = True
mode = None
team_mode = False
player_score = 0
opponent_score = 0

# 기술 및 아이템
commands = []
command_time = 0
items = []
item_boxes = []
item_spawn_time = 0
player_items = []
BALL_GROW = False

# 게임 설정
FPS = 60
clock = pygame.time.Clock()

# 메인 화면
def main_menu():
    global winning_score, deuce
    while True:
        screen.fill(BLACK)
        title = font.render("Ping Pong", True, WHITE)
        pvp_text = font.render("1. PvP", True, WHITE)
        pve_text = font.render("2. PvE", True, WHITE)
        score_text = font.render(f"Score: {winning_score}", True, WHITE)
        deuce_text = font.render(f"Deuce: {'On' if deuce else 'Off'}", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(pvp_text, (WIDTH // 2 - pvp_text.get_width() // 2, 300))
        screen.blit(pve_text, (WIDTH // 2 - pve_text.get_width() // 2, 400))
        screen.blit(score_text, (50, 50))
        screen.blit(deuce_text, (50, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = sub_menu("PvP")
                    if mode:
                        return "PvP", mode
                if event.key == pygame.K_2:
                    mode = sub_menu("PvE")
                    if mode:
                        return "PvE", mode
                if event.key == pygame.K_s:
                    winning_score = int(input("Enter winning score: "))
                if event.key == pygame.K_d:
                    deuce = not deuce
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

def sub_menu(mode):
    while True:
        screen.fill(BLACK)
        title = font.render(f"{mode} Mode", True, WHITE)
        duel_text = font.render("1. 1:1 Duel", True, WHITE)
        team_text = font.render("2. 2:2 Team", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(duel_text, (WIDTH // 2 - duel_text.get_width() // 2, 300))
        screen.blit(team_text, (WIDTH // 2 - team_text.get_width() // 2, 400))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "1:1"
                if event.key == pygame.K_2:
                    return "2:2"
                if event.key == pygame.K_ESCAPE:
                    return None

        pygame.display.flip()

# 데이터 전송
def send_data(skill=None, item=None):
    data = {"paddle_y": player.y}
    if skill:
        data["skill"] = skill
    if item:
        data["item"] = item
    client.send(pickle.dumps(data))

# AI 움직임
def move_ai(ball, paddle):
    if ball[1] < paddle.centery - 20 and paddle.top > 0:
        paddle.y -= 4
    if ball[1] > paddle.centery + 20 and paddle.bottom < HEIGHT:
        paddle.y += 4

# 아이템 생성
def spawn_items():
    global item_spawn_time, item_boxes
    if time.time() - item_spawn_time > 10:
        item_boxes.append(pygame.Rect(random.randint(50, WIDTH // 2 - 50), random.randint(50, HEIGHT - 50), 30, 30))
        item_boxes.append(pygame.Rect(random.randint(WIDTH // 2 + 50, WIDTH - 50), random.randint(50, HEIGHT - 50), 30, 30))
        item_spawn_time = time.time()

# 기술 발동
def activate_skill(ball_x):
    global commands, BALL_GROW
    if commands == [] and pygame.K_SPACE in commands:
        send_data(skill="spike")
    elif commands == [pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_UP]:
        send_data(skill="stop")
    elif commands == [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT]:
        send_data(skill="flame")
    elif commands == [pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]:
        send_data(skill="curve")
    elif commands == [pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT]:
        send_data(skill="clone")
    commands = []

# 게임 루프
def game_loop(mode, sub_mode):
    global command_time, BALL_GROW, player_items, item_boxes, player_score, opponent_score
    connected_players = 0
    player_id = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_i and player_items:
                    send_data(item="Big Ball")
                    BALL_GROW = True
                if pygame.time.get_ticks() - command_time < 500:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        commands.append(event.key)
                    elif event.key == pygame.K_SPACE:
                        activate_skill(data["balls"][data["real_ball_idx"]][0] if "data" in locals() else 500)

        # 플레이어 이동 (W, S만 사용)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player.top > 0:
            player.y -= 7
        if keys[pygame.K_s] and player.bottom < HEIGHT:
            player.y += 7

        # 서버 데이터 수신
        try:
            data = pickle.loads(client.recv(4096))
            connected_players = len(data["players"])
            player_id = min(data["players"].keys())
            if connected_players > 1:
                opponent.y = list(data["players"].values())[1 if player_id == 0 else 0]["paddle_y"]
            player_score = data["players"][player_id]["score"]
            opponent_score = data["players"][1 if player_id == 0 else 0]["score"] if connected_players > 1 else 0

            # 공 충돌 처리
            for i, ball in enumerate(data["balls"]):
                ball_rect = pygame.Rect(ball[0], ball[1], 20, 20)
                if ball_rect.colliderect(player) and ball[2] < 0:
                    ball[2] = abs(ball[2])
                    command_time = pygame.time.get_ticks()
                elif ball_rect.colliderect(opponent) and ball[2] > 0:
                    ball[2] = -abs(ball[2])
                    command_time = pygame.time.get_ticks()
        except:
            pass

        # AI 처리 (PvE)
        if mode == "PvE":
            move_ai(data["balls"][data["real_ball_idx"]], opponent)

        # 아이템 처리
        spawn_items()
        for box in item_boxes[:]:
            for ball in data["balls"]:
                if pygame.Rect(ball[0], ball[1], 20, 20).colliderect(box):
                    if box.x < WIDTH // 2 and len(player_items) < 2:
                        player_items.append("Big Ball")
                    item_boxes.remove(box)

        # 데이터 전송
        send_data()

        # 승리 조건
        if player_score >= winning_score or opponent_score >= winning_score:
            if abs(player_score - opponent_score) >= 2 or not deuce:
                return

        # 그리기
        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
        pygame.draw.rect(screen, WHITE, player)
        pygame.draw.rect(screen, WHITE, opponent)
        for i, ball in enumerate(data["balls"]):
            size = 20 * (2 if BALL_GROW and i == data["real_ball_idx"] else 1)
            pygame.draw.ellipse(screen, WHITE if i == data["real_ball_idx"] else YELLOW, (ball[0], ball[1], size, size))
        for box in item_boxes:
            pygame.draw.rect(screen, RED, box)
        player_text = font.render(str(player_score), True, WHITE)
        opponent_text = font.render(str(opponent_score), True, WHITE)
        screen.blit(player_text, (WIDTH // 4, 20))
        screen.blit(opponent_text, (3 * WIDTH // 4, 20))
        status = font.render(f"{connected_players} Players Connected", True, WHITE)
        screen.blit(status, (WIDTH // 2 - status.get_width() // 2, HEIGHT - 50))

        pygame.display.flip()
        clock.tick(FPS)

# 메인 실행
if __name__ == "__main__":
    while True:
        mode, sub_mode = main_menu()
        if mode and sub_mode:
            game_loop(mode, sub_mode)