import os
import socket
import threading
import pickle

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # 현재 파일 디렉토리로 이동

HOST = '0.0.0.0'
PORT = 9999

clients = []
game_state = {
    'ball_pos': [400, 300],
    'ball_vel': [4, 4],
    'paddles': {0: [10, 250], 1: [780, 250]},
}

def handle_client(conn, addr, player_id):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            paddle_y = pickle.loads(data)
            game_state['paddles'][player_id][1] = paddle_y
        except:
            break
    conn.close()


def game_loop():
    while True:
        # 공 이동
        game_state['ball_pos'][0] += game_state['ball_vel'][0]
        game_state['ball_pos'][1] += game_state['ball_vel'][1]
        # 벽 충돌 처리 (위, 아래)
        if game_state['ball_pos'][1] <= 0 or game_state['ball_pos'][1] >= 600:
            game_state['ball_vel'][1] *= -1
        # 좌우 벽 충돌 시 속도 반전 (점수 처리 생략)
        if game_state['ball_pos'][0] <= 0 or game_state['ball_pos'][0] >= 800:
            game_state['ball_vel'][0] *= -1
        # 상태 전송
        for conn in clients:
            try:
                conn.sendall(pickle.dumps(game_state))
            except:
                pass
        threading.Event().wait(1/60)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(2)
    print(f"게임 서버 시작: {HOST}:{PORT}")
    threading.Thread(target=game_loop, daemon=True).start()
    player_id = 0
    while True:
        conn, addr = s.accept()
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr, player_id), daemon=True).start()
        print(f"플레이어 {player_id} 연결됨: {addr}")
        player_id += 1

if __name__ == '__main__':
    main()
