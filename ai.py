def ai_move(paddle_y, ball_pos, speed=5):
    """
    공의 y좌표를 기준으로 패들이 중앙으로 이동하도록 함.
    :param paddle_y: 현재 패들 y좌표
    :param ball_pos: [x, y] 공 좌표
    :param speed: 이동 속도
    :return: 업데이트된 paddle_y
    """
    paddle_center = paddle_y + 50
    if paddle_center < ball_pos[1]:
        paddle_y += speed
    elif paddle_center > ball_pos[1]:
        paddle_y -= speed
    return paddle_y
