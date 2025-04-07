# v0.1.2
import os
import sys
import pygame
import subprocess
from ai import ai_move

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # 현재 파일 디렉토리로 이동

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame PingPong")
clock = pygame.time.Clock()

# 설정 변수
deuce_enabled = False
target_score = 5

# 글자 출력 헬퍼
font = pygame.font.Font(None, 36)
def draw_text(text, x, y, color=(255,255,255)):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))

# 메뉴 화면
def menu_screen():
    options = ["Play PvE", "Play PvP", "Settings", "Quit"]
    selected = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected]
        screen.fill((0, 0, 0))
        draw_text("PingPong Game", 300, 150, (255, 200, 0))
        for i, opt in enumerate(options):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            draw_text(opt, 330, 250 + i * 50, color)
        pygame.display.flip()
        clock.tick(60)

# 설정 화면
def settings_screen():
    global deuce_enabled, target_score
    opts = ["Deuce: {}", "Target Score: {}", "Back"]
    selected = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(opts)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(opts)
                elif event.key == pygame.K_LEFT and selected == 1:
                    target_score = max(1, target_score - 1)
                elif event.key == pygame.K_RIGHT and selected == 1:
                    target_score += 1
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        deuce_enabled = not deuce_enabled
                    elif selected == 2:
                        return
        screen.fill((0, 0, 0))
        draw_text("Settings", 350, 150, (255, 200, 0))
        for i, opt in enumerate(opts):
            text = opt.format("On" if i == 0 and deuce_enabled else "Off" if i == 0 else target_score if i == 1 else "")
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            draw_text(text, 300, 250 + i * 50, color)
        pygame.display.flip()
        clock.tick(60)

# PvE 실행 함수
def run_pve():
    while True:
        ball_pos = [400, 300]
        ball_vel = [4, 4]
        player_y = 250
        ai_y = 250
        score_p = 0
        score_ai = 0
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]: player_y -= 5
            if keys[pygame.K_DOWN]: player_y += 5
            ai_y = ai_move(ai_y, ball_pos, speed=4)
            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]
            if ball_pos[1] <= 0 or ball_pos[1] >= 600:
                ball_vel[1] *= -1
            if ball_pos[0] <= 0:
                score_ai += 1
                ball_pos = [400, 300]
            elif ball_pos[0] >= 800:
                score_p += 1
                ball_pos = [400, 300]
            def check_win(p, ai):
                if p >= target_score or ai >= target_score:
                    if deuce_enabled and abs(p - ai) < 2:
                        return False
                    return True
                return False
            if check_win(score_p, score_ai):
                winner = "Player" if score_p > score_ai else "AI"
                screen.fill((0,0,0))
                draw_text(f"{winner} Wins!", 300, 280, (255,255,0))
                pygame.display.flip()
                pygame.time.wait(2000)
                playing = False
                continue
            screen.fill((0,0,0))
            draw_text(f"P: {score_p}", 350, 20)
            draw_text(f"AI: {score_ai}", 350, 60)
            pygame.draw.circle(screen, (255,255,255), ball_pos, 10)
            pygame.draw.rect(screen, (255,255,255), (10, player_y, 10, 100))
            pygame.draw.rect(screen, (255,255,255), (780, ai_y, 10, 100))
            pygame.display.flip()
            clock.tick(60)

# PvP 실행 함수
def run_pvp():
    try:
        subprocess.run([sys.executable, "client.py"])
    except Exception as e:
        print("[연결 오류] 클라이언트 실행 중 문제가 발생했습니다:", e)
        if hasattr(e, 'errno') and e.errno == 10054:
            print("[연결 끊김] 상대방이 연결을 종료했습니다.")
        else:
            print("[예외 정보]", e)

# 메인 루프
while True:
    choice = menu_screen()
    if choice == "Quit":
        break
    elif choice == "Settings":
        settings_screen()
    elif choice == "Play PvE":
        run_pve()
    elif choice == "Play PvP":
        run_pvp()

pygame.quit()
