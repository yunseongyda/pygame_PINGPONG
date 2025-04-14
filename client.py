import os
import socket
import threading
import pickle
import pygame

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # 현재 파일 디렉토리로 이동

HOST = '192.168.123.101'
PORT = 9999

game_state = None

def recv_loop(sock):
    global game_state
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            game_state = pickle.loads(data)
        except:
            break

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame PingPong Client")
    clock = pygame.time.Clock()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    threading.Thread(target=recv_loop, args=(sock,), daemon=True).start()

    paddle_y = 250
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            paddle_y -= 5
        if keys[pygame.K_DOWN]:
            paddle_y += 5
        # 패들 위치 서버로 전송
        sock.sendall(pickle.dumps(paddle_y))

        screen.fill((0,0,0))
        if game_state:
            # 공 그리기
            pygame.draw.circle(screen, (255,255,255), game_state['ball_pos'], 10)
            # 패들 그리기
            for pos in game_state['paddles'].values():
                pygame.draw.rect(screen, (255,255,255), (pos[0], pos[1], 10, 100))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()
