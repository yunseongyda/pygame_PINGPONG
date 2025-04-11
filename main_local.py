import os
import sys
import pygame
import subprocess
from ai import ai_move
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame PingPong")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=(255, 255, 255)):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))

class Settings:
    def __init__(self):
        self.deuce_enabled = False
        self.target_score = 5
        self.fps = 60  # FPS 설정 추

# Menu에서 Settings로 넘어가게 수정
class Menu:
    def __init__(self, settings):
        self.settings = settings
        self.options = ["Play PvE", "Play PvP", "Settings", "Quit"]
        self.selected = 0

    def show(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.options[self.selected]  # 선택된 메뉴 반환

            screen.fill((0, 0, 0))
            draw_text("PingPong Game", 300, 150, (255, 200, 0))
            for i, opt in enumerate(self.options):
                color = (0, 255, 0) if i == self.selected else (255, 255, 255)
                draw_text(opt, 330, 250 + i * 50, color)
            pygame.display.flip()
            clock.tick(self.settings.fps)

class SettingsScreen:
    def __init__(self, settings):
        self.settings = settings
        self.selected = 0
        self.opts = ["Deuce: {}", "Target Score: {}", "FPS: {}", "Back"]

    def show(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.opts)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.opts)
                    elif event.key == pygame.K_LEFT:
                        if self.selected == 1:
                            self.settings.target_score = max(1, self.settings.target_score - 1)
                        elif self.selected == 2:
                            self.settings.fps = max(30, self.settings.fps - 10)
                    elif event.key == pygame.K_RIGHT:
                        if self.selected == 1:
                            self.settings.target_score += 1
                        elif self.selected == 2:
                            self.settings.fps = min(240, self.settings.fps + 10)
                    elif event.key == pygame.K_RETURN:
                        if self.selected == 0:
                            self.settings.deuce_enabled = not self.settings.deuce_enabled
                        elif self.selected == 3:
                            return
                    elif event.key == pygame.K_ESCAPE:
                        return

            screen.fill((0, 0, 0))
            draw_text("Settings", 350, 150, (255, 200, 0))
            for i, opt in enumerate(self.opts):
                value = "On" if i == 0 and self.settings.deuce_enabled else \
                        "Off" if i == 0 else \
                        self.settings.target_score if i == 1 else \
                        self.settings.fps if i == 2 else ""
                text = opt.format(value)
                color = (0, 255, 0) if i == self.selected else (255, 255, 255)
                draw_text(text, 300, 250 + i * 50, color)
            pygame.display.flip()
            clock.tick(self.settings.fps)

class PvEGame:
    def __init__(self, settings):
        self.settings = settings
        self.boost_skill_active = False  # Boost 스킬 활성화 여부
        self.skill_command_time = 0  # 스킬 커맨드를 입력한 시간 기록
        self.last_boost_time = 0  # Boost 스킬 발동 시간 기록

    def check_win(self, p, ai):
        if p >= self.settings.target_score or ai >= self.settings.target_score:
            if self.settings.deuce_enabled and abs(p - ai) < 2:
                return False
            return True
        return False

    def run(self):
        score_p = 0
        score_ai = 0
        playing = True
        ball_pos = [400, 300]
        ball_vel = [4, 4]
        player_y = 250
        ai_y = 250
        last_paddle_hit_time = 0
        boost_move = 0  # 막대가 이동한 정도

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

            player_y = max(0, min(player_y, 500))
            ai_y = ai_move(ai_y, ball_pos, speed=4)
            ai_y = max(0, min(ai_y, 500))

            if 10 <= ball_pos[0] <= 20 and player_y < ball_pos[1] < player_y + 100:
                if ball_vel[0] < 0:
                    ball_vel[0] *= -1
                    ball_pos[0] = 21
                    last_paddle_hit_time = time.time()
                    self.skill_command_time = time.time()

            elif 770 <= ball_pos[0] <= 780 and ai_y < ball_pos[1] < ai_y + 100:
                if ball_vel[0] > 0:
                    ball_vel[0] *= -1
                    ball_pos[0] = 779

            if keys[pygame.K_SPACE] and time.time() - self.skill_command_time <= 0.5:
                if not self.boost_skill_active and time.time() - last_paddle_hit_time <= 0.5:
                    self.boost_skill_active = True
                    ball_vel[0] *= 1.5
                    self.last_boost_time = time.time()
                    print("Boost 스킬 발동됨")

            if self.boost_skill_active:
                elapsed_time = time.time() - self.last_boost_time
                if elapsed_time < 0.5:
                    boost_move = (elapsed_time / 0.5) * 30
                else:
                    self.boost_skill_active = False
                    boost_move = 0
            else:
                boost_move = 0

            pygame.draw.rect(screen, (255, 255, 255), (10, player_y - boost_move, 10, 100))

            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]

            if ball_pos[1] <= 0 or ball_pos[1] >= 590:
                ball_vel[1] *= -1
                ball_pos[1] = max(0, min(ball_pos[1], 590))

            if ball_pos[0] <= 0:
                score_ai += 1
                ball_pos = [400, 300]
                ball_vel = [4, 4]

            elif ball_pos[0] >= 800:
                score_p += 1
                ball_pos = [400, 300]
                ball_vel = [-4, 4]

            if self.check_win(score_p, score_ai):
                winner = "Player" if score_p > score_ai else "AI"
                screen.fill((0, 0, 0))
                draw_text(f"{winner} Wins!", 300, 280, (255, 255, 0))
                pygame.display.flip()
                pygame.time.wait(2000)
                playing = False
                break

            screen.fill((0, 0, 0))
            draw_text(f"P: {score_p}", 350, 20)
            draw_text(f"AI: {score_ai}", 350, 60)
            pygame.draw.circle(screen, (255, 255, 255), ball_pos, 10)
            pygame.draw.rect(screen, (255, 255, 255), (10, player_y, 10, 100))
            pygame.draw.rect(screen, (255, 255, 255), (780, ai_y, 10, 100))
            pygame.display.flip()
            clock.tick(self.settings.fps)

class PvPGame:
    def run(self):
        try:
            subprocess.run([sys.executable, "client.py"])
        except Exception as e:
            print("[연결 오류] 클라이언트 실행 중 문제가 발생했습니다:", e)

settings = Settings()
menu = Menu(settings)
settings_screen = SettingsScreen(settings)
pve_game = PvEGame(settings)
pvp_game = PvPGame()

while True:
    choice = menu.show()
    if choice == "Quit":
        break
    elif choice == "Settings":
        settings_screen.show()
    elif choice == "Play PvE":
        pve_game.run()
    elif choice == "Play PvP":
        pvp_game.run()

pygame.quit()
