# coding: utf-8


import json
import random
import sys
import time
import urllib.request
import urllib.parse
from arkanoid.vector import (
    EPS,
)
from arkanoid.game import (
    TBrick,
    TBall,
    TPlatform,
    TGame,
)
from arkanoid.intersectable import (
    build_closest_intersections,
)
from arkanoid.intersections import (
    reflect_moving_point_from_lines,
    test_basic_functions,
)


hostName = "ai.church"
serverPort = 19091


def push_data(key_name, data):
    url = 'http://{}:{}/push'.format(hostName, serverPort)
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'key': key_name,
        'value': data,
    }
    data = bytes(json.dumps(data), 'utf-8')
    request = urllib.request.Request(url, headers=headers, data=data, method='POST')
    try:
        response = urllib.request.urlopen(request)
    except Exception as e:
        response = e
    return response.read().decode('utf-8')


def get_rendering_data(game):
    figures = []
    figures.append({'type': 'rectangle', 'color': 'black', 'x': 0, 'y': 0, 'width': game.size.x, 'height': game.size.y})
    for brick in game.bricks:
        if brick.strength == 0:
            continue
        lu = game.get_brick_lu(brick.position)
        color = min(127 + brick.strength * 10, 255)
        color = '#00{}00'.format(hex(color)[2:])
        figures.append({'type': 'rectangle', 'color': color, 'x': lu.x, 'y': lu.y, 'width': game.brick_width, 'height': game.brick_height})
    figures.append({'type': 'circle', 'color': 'red', 'x': game.ball.position.x, 'y': game.ball.position.y, 'r': game.ball.radius})
    figures.append({'type': 'circle', 'color': 'blue', 'x': game.platform.position, 'y': game.size.y, 'r': game.platform.radius})
    return { 'figures': figures }


def play_game(game, model, logger):
    play_time = 0.0
    while not game.has_won():
        intersections = build_closest_intersections(game)
        t = min(intersections[-1][0][0], 1.0)
        #t = intersections[-1][0]
        d = game.ball.direction.get_normalised().scalar_multiply(game.ball.speed * t)
        if abs(t - intersections[-1][0][0]) < EPS:
            #print('reflections count: {}'.format(len(intersections)))
            game.ball.direction = reflect_moving_point_from_lines(game.ball.position, game.ball.direction, d, list(map(lambda x: (x[0][1], x[1]), intersections)))
        game.ball.position = game.ball.position.add(d)
        #print("position and direction: {}, {}, {}".format(game.ball.position, game.ball.direction, d))
        push_data('arkanoid', get_rendering_data(game))
        game.platform.position = game.move_platform(random.uniform(-3, 3))
        #time.sleep(0.3)
        data = game.serialize()
        game = TGame(data)
        sys.stdout.flush()


    return (True, play_time)


def main():
    game = TGame(json.load(open("game.json", "rt")))
    while True:
        intersections = build_closest_intersections(game)
        t = min(intersections[-1][0][0], 1.0)
        #t = intersections[-1][0]
        d = game.ball.direction.get_normalised().scalar_multiply(game.ball.speed * t)
        if abs(t - intersections[-1][0][0]) < EPS:
            #print('reflections count: {}'.format(len(intersections)))
            game.ball.direction = reflect_moving_point_from_lines(game.ball.position, game.ball.direction, d, list(map(lambda x: (x[0][1], x[1]), intersections)))
        game.ball.position = game.ball.position.add(d)
        #print("position and direction: {}, {}, {}".format(game.ball.position, game.ball.direction, d))
        push_data('arkanoid', get_rendering_data(game))
        game.platform.position = game.move_platform(random.uniform(-3, 3))
        #time.sleep(0.3)
        data = game.serialize()
        game = TGame(data)
        sys.stdout.flush()


if __name__ == '__main__':
    main()

