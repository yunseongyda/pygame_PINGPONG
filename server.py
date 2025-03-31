import socket
import threading
import pickle
import random

# 서버 설정
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen()

clients = []
game_state = {
    "players": {},  # 클라이언트별 위치 및 점수
    "balls": [[500, 400, 5, 5]],  # (x, y, speed_x, speed_y)
    "real_ball_idx": 0,
    "items": [],
    "player_items": {}
}

def handle_client(client, client_id):
    clients.append(client)
    game_state["players"][client_id] = {"paddle_y": 400, "score": 0}
    game_state["player_items"][client_id] = []

    while True:
        try:
            data = client.recv(4096)
            if not data:
                break
            received = pickle.loads(data)
            game_state["players"][client_id]["paddle_y"] = received["paddle_y"]
            if "skill" in received:
                apply_skill(client_id, received["skill"])
            if "item" in received:
                use_item(client_id)
            broadcast(pickle.dumps(game_state))
        except:
            break

    clients.remove(client)
    del game_state["players"][client_id]
    del game_state["player_items"][client_id]
    client.close()

def apply_skill(client_id, skill):
    player_name = f"Player {client_id + 1}"
    if skill == "spike":
        game_state["balls"][game_state["real_ball_idx"]][2] *= 1.5
        print(f"{player_name} used Spike!")
    elif skill == "stop":
        game_state["balls"][game_state["real_ball_idx"]][2] = 0
        game_state["balls"][game_state["real_ball_idx"]][3] = 0
        print(f"{player_name} used Stop!")
        threading.Timer(1, reset_ball_speed).start()  # 수정: personallyTimer -> Timer
    elif skill == "flame":
        game_state["balls"][game_state["real_ball_idx"]][2] *= 2
        print(f"{player_name} used Flame Shot!")
    elif skill == "curve":
        if game_state["balls"][game_state["real_ball_idx"]][0] > 500:
            angle = random.uniform(-30, 30)
            game_state["balls"][game_state["real_ball_idx"]][3] += angle
            print(f"{player_name} used Curve!")
    elif skill == "clone":
        for _ in range(2):
            game_state["balls"].append(game_state["balls"][0].copy())
        print(f"{player_name} used Clone!")

def use_item(client_id):
    if "Big Ball" in game_state["player_items"][client_id]:
        game_state["player_items"][client_id].remove("Big Ball")
        print(f"Player {client_id + 1} used Big Ball!")

def reset_ball_speed():
    game_state["balls"][game_state["real_ball_idx"]][2] = 5 * random.choice((1, -1))
    game_state["balls"][game_state["real_ball_idx"]][3] = 5 * random.choice((1, -1))

def broadcast(data):
    for client in clients:
        try:
            client.send(data)
        except:
            pass

def update_game_state():
    while True:
        for i, ball in enumerate(game_state["balls"]):
            ball[0] += ball[2]
            ball[1] += ball[3]
            if ball[1] <= 0 or ball[1] >= 800:
                ball[3] = -ball[3]
            if ball[0] <= 0 and len(game_state["players"]) > 1:
                for cid in game_state["players"]:
                    if cid != 0:
                        game_state["players"][cid]["score"] += 1
                reset_ball()
            elif ball[0] >= 1000 and 0 in game_state["players"]:
                game_state["players"][0]["score"] += 1
                reset_ball()
        threading.Event().wait(1 / 60)

def reset_ball():
    game_state["balls"] = [[500, 400, 5 * random.choice((1, -1)), 5 * random.choice((1, -1))]]
    game_state["real_ball_idx"] = 0

print("Server running on port 5555...")
threading.Thread(target=update_game_state, daemon=True).start()

client_id = 0
while True:
    client, addr = server.accept()
    print(f"Connected: {addr}")
    threading.Thread(target=handle_client, args=(client, client_id), daemon=True).start()
    client_id += 1