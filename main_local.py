import os
import pygame
from ai import ai_move

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # 현재 파일 디렉토리로 이동

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame PingPong PvE")
clock = pygame.time.Clock()

ball_pos = [400, 300]
ball_vel = [4, 4]
player_y = 250
ai_y = 250

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= 5
    if keys[pygame.K_DOWN]:
        player_y += 5
    # AI 이동
    ai_y = ai_move(ai_y, ball_pos, speed=4)

    # 공 이동
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] <= 0 or ball_pos[1] >= 600:
        ball_vel[1] *= -1
    if ball_pos[0] <= 0 or ball_pos[0] >= 800:
        ball_vel[0] *= -1

    screen.fill((0,0,0))
    pygame.draw.circle(screen, (255,255,255), ball_pos, 10)
    pygame.draw.rect(screen, (255,255,255), (10, player_y, 10, 100))
    pygame.draw.rect(screen, (255,255,255), (780, ai_y, 10, 100))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
