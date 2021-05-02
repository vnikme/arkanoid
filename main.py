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


def play_game(game, time_limit, model, processor):
    play_time, last_tick = 0.0, -1.0
    while not game.has_won():
        intersections = build_closest_intersections(game)
        t = min(intersections[-1][0][0], 1.0)
        d = game.ball.direction.get_normalised().scalar_multiply(game.ball.speed * t)
        if abs(t - intersections[-1][0][0]) < EPS:
            game.ball.direction = reflect_moving_point_from_lines(game.ball.position, game.ball.direction, d, list(map(lambda x: (x[0][1], x[1]), intersections)))
        game.ball.position = game.ball.position.add(d)
        #print("position and direction: {}, {}, {}".format(game.ball.position, game.ball.direction, d))
        play_time += t
        if play_time - last_tick >= 1.0 - EPS:
            delta = model.predict(game)
            processor.on_tick(play_time, game, delta)
            game.move_platform(delta)
            last_tick = play_time
        if play_time > time_limit or game.has_lost():
            return (False, play_time)
    return (True, play_time)


def prepare_pool(game, count, time_limit, model, steps):
    result = []
    queue = [game.serialize()]
    i = 0
    while i < len(queue):
        if len(result) >= count:
            break
        step_results = []
        processor = TMemoizeSomeProcessor(3)
        for step in steps:
            game = TGame(queue[i])
            patched_model = TModelWithOverridenFirstStep(model, step)
            has_won, time_play = play_game(game, time_limit, patched_model, processor)
            step_results.append((step, has_won, time_play))
        queue += processor.games
        result.append((step_results, queue[i]))
    return result


def extract_features(game):
    features = []
    features += [game.size.x, game.size.y, game.bricks_rows, game.bricks_cols, game.brick_width, game.brick_height]
    bricks = [0 for _ in range(game.bricks_rows * game.bricks_cols)]
    for brick in game.bricks:
        bricks[brick.position.y * game.bricks_cols + brick.position.x] = brick.strength
    features += bricks
    features += [game.ball.position.x, game.ball.position.y, game.ball.speed, game.ball.direction.x, game.ball.direction.y, game.ball.radius]
    features += [game.platform.position, game.platform.radius]
    return features


class TModelWithOverridenFirstStep:
    def __init__(self, base_model, first_result):
        self.base_model = base_model
        self.first_result = first_result
        self.is_first = True

    def predict(self, game):
        if self.is_first:
            self.is_first = False
            return self.first_result
        else:
            return self.base_model.predict(game)


class TRandomModel:
    def __init__(self):
        pass

    def predict(self, game):
        return random.uniform(-2.0, 2.0)


class TFollowXModel:
    def __init__(self):
        pass

    def predict(self, game):
        delta = game.ball.position.x - game.platform.position
        return min(max(delta, -3.0), 3.0)


class TPushProcessor:
    def __init__(self):
        pass

    def on_tick(self, play_time, game, delta):
        push_data('arkanoid', get_rendering_data(game))


class TMemoizeSomeProcessor:
    def __init__(self, number_to_memoize):
        self.number_to_memoize = number_to_memoize
        self.n = 0
        self.games = []

    def on_tick(self, play_time, game, delta):
        #push_data('arkanoid', get_rendering_data(game))
        self.n += 1
        if game.has_won() or game.has_lost():
            return
        if len(self.games) < self.number_to_memoize:
            self.games.append(game.serialize())
            return
        if random.random() > 1 / self.n:
            return
        k = random.randint(0, self.number_to_memoize - 1)
        self.games[k] = game.serialize()


def main():
    game = TGame(json.load(open("game.json", "rt")))
    #play_game(game, 1000000, TRandomModel(), TPushProcessor())
    #play_game(game, 100000, TFollowXModel(), TPushProcessor())
    #processor = TMemoizeSomeProcessor(3)
    #play_game(game, 100000, TFollowXModel(), processor)
    #print(processor.games)
    ts = time.time()
    print(list(map(lambda x: x[0], prepare_pool(game, 10, 10000, TRandomModel(), list(range(-2, 3))))))
    print('Time: {}'.format(time.time() - ts))
    ts = time.time()
    print(list(map(lambda x: x[0], prepare_pool(game, 10, 10000, TFollowXModel(), list(range(-2, 3))))))
    print('Time: {}'.format(time.time() - ts))
    print(extract_features(game))


if __name__ == '__main__':
    main()

