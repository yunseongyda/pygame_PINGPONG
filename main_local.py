# pygame 설치 필요
import os
import sys
import pygame
import subprocess
import random
import time
import math
from ai import ai_move

# 기본 초기화
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame PingPong")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# 상자 이미지 로드
box_image = pygame.image.load("box.png").convert_alpha()

# 텍스트 출력 함수
def draw_text(text, x, y, color=(255, 255, 255), background_color=None):
    surf = font.render(text, True, color, background_color)
    screen.blit(surf, (x, y))

# 랜덤 스킬 반환 함수
def get_random_skill():
    return random.choice(['spike', 'freeze', 'breaking', 'clone', 'invisible', 'heavy', 'warp'])

class Settings:
    def __init__(self):
        self.deuce_enabled = False
        self.target_score = 5
        self.fps = 60

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
                        return self.options[self.selected]

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
                            self.settings.fps = max(10, self.settings.fps - 10)
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
                text = opt.format("On" if i == 0 and self.settings.deuce_enabled else self.settings.target_score if i == 1 else self.settings.fps if i == 2 else "Off")
                color = (0, 255, 0) if i == self.selected else (255, 255, 255)
                draw_text(text, 300, 250 + i * 50, color)
            pygame.display.flip()
            clock.tick(self.settings.fps)

class Box:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.image = pygame.image.load("box.png").convert_alpha()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def check_collision(self, ball_rect):
        return self.rect.colliderect(ball_rect)

class PvEGame:
    def __init__(self, settings):
        self.settings = settings
        self.start_time = time.time()
        self.last_box_spawn_time = {"left": self.start_time, "right": self.start_time}
        self.boxes = {"left": [], "right": []}
        self.last_hitter = None

        # 스킬 관리
        self.skills = []
        self.ball_trail = []
        # 스파이크
        self.spike_active = False
        self.spike_original_speed = None
        # 프리즈
        self.freeze_active = False
        self.breaking_ball_end_time = 0
        self.freeze_end_time = 0
        self.freeze_original_speed = [0, 0]
        # 변화구
        self.breaking_ball_active = False
        # 분신술
        self.fake_balls = []
        # 투명
        self.invisible_active = False
        self.invisible_end_time = 0
        # 헤비
        self.heavy_ball_active = False
        self.heavy_ball_end_time = 0
        # 워프
        self.warp_active = False
        self.warp_end_time = 0
        # 지그제그
        self.zigzag_active = False
        self.zigzag_end_time = 0
        # 섬광
        self.flash_active = False
        self.flash_end_time = 0
        self.flash_strong_time = 0

    def check_win(self, p, ai):
        if p >= self.settings.target_score or ai >= self.settings.target_score:
            if self.settings.deuce_enabled and abs(p - ai) < 2:
                return False
            return True
        return False

    def spawn_box(self, side):
        y = random.randint(0, 570)
        x = random.randint(50, 200) if side == "left" else random.randint(600, 750)
        return Box(x, y)

    def use_skill(self):
        if not self.skills:
            print("[SKILL] No skill available!")
            return

        skill = self.skills.pop(0)
        print(f"[SKILL] {skill} used!")

        if skill == "spike" and not self.spike_active:
            self.spike_active = True
            self.spike_original_speed = self.ball_vel.copy()
            self.ball_vel[0] *= 2
            self.ball_vel[1] *= 2
            print("[EFFECT] Spike activated: Ball speed doubled.")

        elif skill == "freeze" and not self.freeze_active:
            self.freeze_active = True
            self.freeze_end_time = time.time() + 1
            self.freeze_original_speed = self.ball_vel.copy()
            self.ball_vel[0] = 0
            self.ball_vel[1] = 0
            print("[EFFECT] Freeze activated: Ball stopped for 1 second.")

        elif skill == "breaking":
            angle_deg = random.uniform(-50, 50)
            angle_rad = math.radians(angle_deg)
            speed = math.hypot(self.ball_vel[0], self.ball_vel[1])
            direction = math.atan2(self.ball_vel[1], self.ball_vel[0])
            new_direction = direction + angle_rad
            self.ball_vel[0] = speed * math.cos(new_direction)
            self.ball_vel[1] = speed * math.sin(new_direction)
            self.breaking_ball_active = True
            self.breaking_ball_end_time = time.time() + 1.5 # 1.5초 동안 효과 지속
            print(f"[EFFECT] Breaking Ball: angle changed by {angle_deg:.2f} degrees")

        elif skill == "clone":
            self.fake_balls = []

            original_speed = math.hypot(self.ball_vel[0], self.ball_vel[1])
            original_angle = math.atan2(self.ball_vel[1], self.ball_vel[0])

            for offset_deg in [-20, 20]:
                offset_rad = math.radians(offset_deg)
                new_angle = original_angle + offset_rad
                dx = original_speed * math.cos(new_angle)
                dy = original_speed * math.sin(new_angle)
                self.fake_balls.append({
                    "pos": self.ball_pos.copy(),
                    "vel": [dx, dy]
                })
            print("[EFFECT] Clone Ball: Two fake balls created.")
        
        elif skill == "invisible":
            self.invisible_active = True
            self.invisible_end_time = time.time() + 2
            print("[EFFECT] Invisible: Ball is now hidden for 2 seconds.")

        elif skill == "heavy":
            if not self.heavy_ball_active:
                self.heavy_ball_active = True
                self.heavy_ball_end_time = time.time() + 2
                self.heavy_original_speed = self.ball_vel[1]
                self.ball_vel[1] *= 2 
                print("[EFFECT] Heavy Ball activated: Y speed increased.")
        
        elif skill == "warp":
            new_x = random.randint(100, 700)
            new_y = random.randint(100, 500)
            self.ball_pos = [new_x, new_y]
            self.warp_active = True
            self.warp_end_time = time.time() + 1.5
            print(f"[EFFECT] Warp: Ball teleported to ({new_x}, {new_y})")

        elif skill == "zigzag":
            self.zigzag_active = True
            self.zigzag_end_time = time.time() + 4
            print("[EFFECT] Zigzag: Ball will wobble for 4 seconds.")

        elif skill == "flash":
            self.flash_active = True
            self.flash_end_time = time.time() + 1.5
            self.flash_strong_time = time.time() + 1
            print("[EFFECT] Flash: Visual interference activated.")

    def draw_ball(self):
        # 4) invisivle ball 일 때
        if self.invisible_active:
            return  # 투명 상태면 공 안 그림
        
        # 1) spike일 때: 잔상 그리기
        if self.spike_active:
            for i, pos in enumerate(self.ball_trail):
                alpha = int(255 * (i + 1) / len(self.ball_trail))
                trail_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, (255, 255, 255, alpha), (10, 10), 10)
                screen.blit(trail_surface, (int(pos[0]) - 10, int(pos[1]) - 10))

        # 2) freeze일 때: 하늘색으로 표시
        if self.freeze_active:
            color = (150, 220, 255)
        # 7) 지그재그 일 때: 공 색상을 흰색 ~ 노란색 사이로 진동
        elif self.zigzag_active:
            t = time.time()
            brightness = int(200 + 55 * math.sin(t * 20))
            color = (255, 255, brightness)

        else:
            color = (255, 255, 255)

        pygame.draw.circle(screen, color, (int(self.ball_pos[0]), int(self.ball_pos[1])), 10)

        # 3) breaking ball일 때: 빨간색 테두리
        if self.breaking_ball_active:
            pygame.draw.circle(screen, (255, 100, 100), (int(self.ball_pos[0]), int(self.ball_pos[1])), 12, 1)
        
        # 5) warp 했을 때: 하늘색 테두리
        if self.warp_active:
            pygame.draw.circle(screen, (150, 200, 255), (int(self.ball_pos[0]), int(self.ball_pos[1])), 12, 1)

        # 6) heavy ball 효과일 때 노란색 테두리
        if self.heavy_ball_active:
            pygame.draw.circle(screen, (255, 200, 50), (int(self.ball_pos[0]), int(self.ball_pos[1])), 12, 1)

        # 8) flash 상태일 때: 공 주변에 번쩍이는 점 여러 개
        if self.flash_active:
            for _ in range(5):
                offset_x = random.randint(-10, 10)
                offset_y = random.randint(-10, 10)
                color = random.choice([(255, 255, 255), (255, 255, 100), (255, 180, 0)])
                pygame.draw.circle(screen, color, (int(self.ball_pos[0]) + offset_x, int(self.ball_pos[1]) + offset_y), 4)


    def run(self):
        score_p = 0
        score_ai = 0
        playing = True
        self.ball_pos = [400.0, 300.0]
        self.ball_vel = [300.0, 300.0]
        player_y = 250.0
        ai_y = 250.0
        player_speed = 400.0

        self.boxes = {"left": [], "right": []}
        self.skills = []
        self.fake_balls = []
        self.spike_active = False
        self.freeze_active = False
        self.breaking_ball_active = False
        self.breaking_ball_end_time = 0
        self.invisible_active = False
        self.warp_active = False
        self.heavy_ball_active = False
        self.zigzag_active = False
        self.ball_trail = []
        self.last_hitter = None


        last_hit_time = 0
        skill_window = 0.5
        skill_ready = False

        while playing:
            dt = clock.tick(self.settings.fps) / 1000.0
            current_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_SPACE:
                        self.use_skill()

                    elif event.key == pygame.K_1:
                        self.skills.append("spike")
                        print("[CHEAT] spike 스킬 획득!")

                    elif event.key == pygame.K_2:
                        self.skills.append("freeze")
                        print("[CHEAT] freeze 스킬 획득!")

                    elif event.key == pygame.K_3:
                        self.skills.append("breaking")
                        print("[CHEAT] breaking ball 스킬 획득!")

                    elif event.key == pygame.K_4:
                        self.skills.append("clone")
                        print("[CHEAT] clone ball 스킬 획득!")

                    elif event.key == pygame.K_5:
                        self.skills.append("invisible")
                        print("[CHEAT] invisible 스킬 획득!")

                    elif event.key == pygame.K_6:
                        self.skills.append("heavy")
                        print("[CHEAT] heavy ball 스킬 획득!")

                    elif event.key == pygame.K_7:
                        self.skills.append("warp")
                        print("[CHEAT] warp 스킬 획득!")

                    elif event.key == pygame.K_8:
                        self.skills.append("zigzag")
                        print("[CHEAT] zigzag 스킬 획득!")

                    elif event.key == pygame.K_9:
                        self.skills.append("flash")
                        print("[CHEAT] flash 스킬 획득!")


            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_y -= player_speed * dt
            if keys[pygame.K_DOWN]:
                player_y += player_speed * dt

            self.ball_trail.append(tuple(self.ball_pos))
            if len(self.ball_trail) > 10:
                self.ball_trail.pop(0)

            player_y = max(0, min(player_y, 500))
            ai_y = ai_move(ai_y, self.ball_pos, speed=300 * dt)
            ai_y = max(0, min(ai_y, 500))

            # 플레이어가 공을 침
            if 10 <= self.ball_pos[0] <= 20 and player_y < self.ball_pos[1] < player_y + 100 and self.ball_vel[0] < 0:
                self.ball_vel[0] *= -1
                self.ball_pos[0] = 21
                last_hit_time = current_time
                skill_ready = True
                self.last_hitter = "player"
                if self.spike_active:
                    self.ball_vel = self.spike_original_speed.copy()
                    self.spike_active = False
                    print("[EFFECT] Spike deactivated (player hit).")

            # AI가 공을 침
            elif 770 <= self.ball_pos[0] <= 780 and ai_y < self.ball_pos[1] < ai_y + 100 and self.ball_vel[0] > 0:
                self.ball_vel[0] *= -1
                self.ball_pos[0] = 779
                self.last_hitter = "ai"
                if self.spike_active:
                    self.ball_vel = self.spike_original_speed.copy()
                    self.spike_active = False
                    print("[EFFECT] Spike deactivated (AI hit).")

            # freeze 해제 처리
            if self.freeze_active and time.time() >= self.freeze_end_time:
                self.ball_vel = self.freeze_original_speed.copy()
                self.freeze_active = False
                print("[EFFECT] Freeze ended: Ball resumed.")

            # breaking ball 적용 중일 때 계속 랜덤하게 공 방향 휘게 하기
            if self.breaking_ball_active:
                # 약간의 방향 회전
                angle_deg = random.uniform(-5, 5)
                angle_rad = math.radians(angle_deg)
                speed = math.hypot(self.ball_vel[0], self.ball_vel[1])
                direction = math.atan2(self.ball_vel[1], self.ball_vel[0])
                new_direction = direction + angle_rad
                self.ball_vel[0] = speed * math.cos(new_direction)
                self.ball_vel[1] = speed * math.sin(new_direction)

                # 3초 지나면 비활성화
                if time.time() >= self.breaking_ball_end_time:
                    self.breaking_ball_active = False
                    print("[EFFECT] Breaking Ball ended.")

            # heavy ball 처리
            if self.heavy_ball_active and time.time() >= self.heavy_ball_end_time:
                self.ball_vel[1] = self.heavy_original_speed
                self.heavy_ball_active = False
                print("[EFFECT] Heavy Ball ended.")

            # invisible 처리
            if self.invisible_active and time.time() >= self.invisible_end_time:
                self.invisible_active = False
                print("[EFFECT] Invisible ended.")

            # warp 처리
            if self.warp_active and time.time() >= self.warp_end_time:
                self.warp_active = False
            
            # 지그제그 처리
            zigzag_offset = 0
            if self.zigzag_active:
                zigzag_offset = 80 * math.sin(time.time() * 20)
                if time.time() >= self.zigzag_end_time:
                    self.zigzag_active = False
                    print("[EFFECT] Zigzag ended.")

            # 섬광 처리
            if self.flash_active and time.time() >= self.flash_end_time:
                self.flash_active = False
                print("[EFFECT] Flash ended.")


            self.ball_pos[0] += self.ball_vel[0] * dt
            self.ball_pos[1] += self.ball_vel[1] * dt

            # zigzag 효과 적용
            self.ball_pos[0] += zigzag_offset * dt

            for fake in self.fake_balls:
                fake["pos"][0] += fake["vel"][0] * dt
                fake["pos"][1] += fake["vel"][1] * dt

            if self.ball_pos[1] <= 0 or self.ball_pos[1] >= 590:
                self.ball_vel[1] *= -1
                self.ball_pos[1] = max(0, min(self.ball_pos[1], 590))

            if self.ball_pos[0] <= 0: # 플레이어가 득점함
                score_ai += 1
                self.ball_pos = [400.0, 300.0]
                self.ball_vel = [300.0, 300.0]

                self.boxes = {"left": [], "right": []}
                self.skills = []
                self.fake_balls = []
                self.spike_active = False
                self.freeze_active = False
                self.breaking_ball_active = False
                self.breaking_ball_end_time = 0
                self.invisible_active = False
                self.warp_active = False
                self.heavy_ball_active = False
                self.zigzag_active = False
                self.ball_trail = []
                self.last_hitter = None

            elif self.ball_pos[0] >= 800: # AI가 득점함
                score_p += 1
                self.ball_pos = [400.0, 300.0]
                self.ball_vel = [-300.0, 300.0]

                self.boxes = {"left": [], "right": []}
                self.skills = []
                self.fake_balls = []
                self.spike_active = False
                self.freeze_active = False
                self.breaking_ball_active = False
                self.breaking_ball_end_time = 0
                self.invisible_active = False
                self.warp_active = False
                self.heavy_ball_active = False
                self.zigzag_active = False
                self.ball_trail = []
                self.last_hitter = None

            if self.check_win(score_p, score_ai):
                winner = "Player" if score_p > score_ai else "AI"
                screen.fill((0, 0, 0))
                draw_text(f"{winner} Wins!", 300, 280, (255, 255, 0))
                pygame.display.flip()
                pygame.time.wait(2000)
                break

            # 상자 생성
            for side in ["left", "right"]:
                if current_time - self.last_box_spawn_time[side] >= 10:
                    self.boxes[side].append(self.spawn_box(side))
                    self.last_box_spawn_time[side] = current_time

            # 상자 충돌
            ball_rect = pygame.Rect(self.ball_pos[0], self.ball_pos[1], 10, 10)
            for side in ["left", "right"]:
                new_boxes = []
                for box in self.boxes[side]:
                    if box.check_collision(ball_rect):
                        skill = get_random_skill()
                        print(f"[ITEM] {self.last_hitter} got skill: {skill}")
                        if len(self.skills) < 2:
                            self.skills.append(skill)
                    else:
                        new_boxes.append(box)
                self.boxes[side] = new_boxes

            screen.fill((0, 0, 0))
            # flash 시 화면 전체를 덮는 밝은 레이어
            if self.flash_active:
                flash_overlay = pygame.Surface((800, 600), pygame.SRCALPHA)

                if time.time() < self.flash_strong_time:
                    flash_overlay.fill((255, 255, 255, 250))  # 강한 흰색, 거의 다 덮임
                else:
                    flash_overlay.fill((255, 255, 255, 80))   # 잔상 느낌만

                screen.blit(flash_overlay, (0, 0))

            # 상자 그리기
            for side in ["left", "right"]:
                for box in self.boxes[side]:
                    box.draw(screen)

            pygame.draw.line(screen, (255, 255, 255), (400, 80), (400, 600), 5)
            draw_text(f"P: {score_p}", 380, 20, (255, 255, 255), (0, 0, 0))
            draw_text(f"AI: {score_ai}", 380, 60, (255, 255, 255), (0, 0, 0))

            for fake in self.fake_balls:
                pygame.draw.circle(screen, (180, 180, 180), (int(fake["pos"][0]), int(fake["pos"][1])), 10)

            

            self.draw_ball()
            pygame.draw.rect(screen, (255, 255, 255), (10, int(player_y), 10, 100))
            pygame.draw.rect(screen, (255, 255, 255), (780, int(ai_y), 10, 100))
            pygame.display.flip()

class PvPGame:
    def run(self):
        try:
            subprocess.run([sys.executable, "client.py"])
        except Exception as e:
            print("[연결 오류] 클라이언트 실행 중 문제가 발생했습니다:", e)

# 인스턴스 생성 및 루프 실행
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