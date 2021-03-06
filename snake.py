#!/usr/bin/python3

from enum import Enum
import numpy as np

import copy
import time


def snake_ray(position, N):
    dists = []
    # for dirs in [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0),
    #              (-1, -1)]:
    for dirs in [(0, -1),  (1, 0), (0, 1), (-1, 0)]:
        done = False
        pos = list(position[0][-1])
        step = 0
        while pos[0] >= 0 and pos[1] >= 0 and pos[0] < N and pos[1] < N:
            pos[0] += dirs[0]
            pos[1] += dirs[1]
            for seg in position[0]:
                if seg[0] == pos[0] and seg[1] == pos[1]:
                    dists.append(step)
                    done = True
                    break
            step += 1
            if done:
                break
        if not done:
            dists.append(N * N + 1)
    return dists


def apple_ray(position, N):
    head = position[0][-1]
    apple = position[1]
    ret = [N**2 + 1 for i in range(8)]

    horiz = apple[0] - head[0]
    vert = apple[1] - head[1]
    diag1 = (apple[1] - head[1]) - (apple[0] - head[0])
    diag2 = (apple[1] - head[1]) + (apple[0] - head[0])

    if (horiz == 0 and vert < 0):
        ret[0] = abs(vert)

    elif (horiz == 0 and vert > 0):
        ret[4] = vert

    elif (vert == 0 and horiz > 0):
        ret[2] = horiz

    elif (vert == 0 and horiz < 0):
        ret[6] = abs(horiz)

    elif (diag1 == 0 and vert > 0):
        ret[3] = abs(horiz) + abs(vert)

    elif (diag1 == 0 and vert < 0):
        ret[7] = abs(horiz) + abs(vert)

    elif (diag2 == 0 and vert > 0):
        ret[5] = abs(horiz) + abs(vert)

    elif (diag2 == 0 and vert < 0):
        ret[1] = abs(horiz) + abs(vert)

    return [ret[0], ret[2], ret[4], ret[6]]
    # return ret


def wall_ray(position, N):
    #position[0][-1][0] # the head'x
    #position[0][-1][1] # the head's y
    # dists = [
    #     position[0][-1][1], 0, N - 1 - position[0][-1][0], 0,
    #     N - 1 - position[0][-1][1], 0, position[0][-1][0], 0
    # ]
    # dists[1] = 2 * min(dists[0], dists[2])
    # dists[3] = 2 * min(dists[2], dists[4])
    # dists[5] = 2 * min(dists[4], dists[6])
    # dists[7] = 2 * min(dists[6], dists[0])
    dists = [
        position[0][-1][1], N - 1 - position[0][-1][0],
        N - 1 - position[0][-1][1],  position[0][-1][0]
    ]
    return dists


def get_pref(position, num_steps, N):
    prefs = [0, 0, 0, 0]
    for move in range(4):
        step = update(position, move, N)
        if len(step[0]) > len(position[0]):
            prefs[move] = 2.0 * take_step(step, num_steps - 1, N)
        else:
            prefs[move] = 1.0 * take_step(step, num_steps - 1, N)
    return prefs


# def take_step(position, num_steps,N):
#     if not valid(position,N):
#         return 0
#     elif num_steps == 0:
#         return 1
#     weights = [take_step(update(position,move,N),num_steps-1,N) for move in range(4)]
#     return np.sum(weights)/4
def take_step(position, num_steps, N):
    if not valid(position, N):
        return 0
    elif num_steps == 0:
        return 1
    weights = [0, 0, 0, 0]
    for move in range(4):
        step = update(position, move, N)
        if len(step[0]) > len(position[0]):
            weights[move] = 2.0 * take_step(step, num_steps - 1, N)
        else:
            weights[move] = 1.0 * take_step(step, num_steps - 1, N)
    return np.sum(weights) / 4.0


def valid(position, N):
    """Valid if the following things are not true:
    1. has not intersected with the edge, so no x or y = 0 or N
    2. has not intersected with itself, so no tuple is the same as another tuple
    """
    if len([
            item for item in position[0]
            if item[0] == -1 or item[0] == N or item[1] == -1 or item[1] == N
    ]) != 0:
        return False
    elif position[0][-1] in position[0][:-1]:
    # elif len(position[0]) != len(set(position[0])):
        return False
    return True


def update(position, move, N):
    apple = copy.deepcopy(position[1])
    snake = copy.deepcopy(position[0])
    new_square = [snake[-1][0], snake[-1][1]]
    if move == 0:
        new_square[1] -= 1
    if move == 1:
        new_square[1] += 1
    if move == 2:
        new_square[0] += 1
    if move == 3:
        new_square[0] -= 1
    new_square = tuple(new_square)
    snake.append(new_square)
    if (new_square == apple):
        apple = (np.random.randint(1, N - 1), np.random.randint(1, N - 1))
        while apple in snake:
            apple = (np.random.randint(1, N - 1), np.random.randint(1, N - 1))
    else:
        snake.pop(0)
    return (snake, apple)


def draw(position, N):
    print("\u250f{}\u2513".format("\u2501" * (N * 2)))
    for i in range(N):
        row = ['  '] * N
        for seg in position[0]:
            if seg[1] == i:
                row[seg[0]] = '\u2588\u2588'
        if position[1][1] == i:
            row[position[1][0]] = '\033[32m\u2588\u2588\033[0m'
        print("\u2503{}\u2503".format(''.join(row)))
    print("\u2517{}\u251B".format("\u2501" * (N * 2)))
    print("\033[H", end='', flush=True)


def user_input(position, N):
    while True:
        move = input()
        if move == 'w':
            return 0
        elif move == 's':
            return 1
        elif move == 'd':
            return 2
        elif move == 'a':
            return 3
        elif move == 'q':
            return -1
        elif move == 'r':
            print(apple_ray(position, N))


def init(N):
    return [[(np.random.randint(1, N - 1), np.random.randint(1, N - 1))],
            (np.random.randint(1, N - 1), np.random.randint(1, N - 1))]


def snake(N, get_move, max_turn = 0, display=False, sleep=None):
    score = 0
    turn = 0
    length = 1
    position = [[(N //2, N//2)],
                (np.random.randint(1, N - 1), np.random.randint(1, N - 1))]
    for i in range(3):
        position[0].append(position[0][0])
    # position = [[(np.random.randint(1, N - 1), np.random.randint(1, N - 1))],
    #             (np.random.randint(1, N - 1), np.random.randint(1, N - 1))]
    while (True):
        if sleep:
            time.sleep(sleep)
        score += 1
        if display:
            draw(position, N)
        move = get_move(position, N)
        if move < 0:
            break
        position = update(position, move, N)
        if max_turn < 0 and len(position[0]) != length:
            length = len(position[0])
            turn = -1
        if not valid(position, N):
            break
        turn += 1
        if max_turn > 0 and turn >= max_turn:
            break
        if max_turn < 0 and turn >= abs(max_turn):
            break
    return score + (1000 * len(position[0]))
