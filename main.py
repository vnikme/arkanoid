# coding: utf-8


import json
import sys
from arkanoid.vector import TVector
from arkanoid.game import (
    TBrick,
    TBall,
    TPlatform,
    TGame,
)
from arkanoid.intersectable import (
    TIntersectableVerticalSegment,
    TIntersectableHorizontalSegment,
)


def build_intersection_times_and_normals(game):
    objects = [
        TIntersectableVerticalSegment(0, 0, game.size.y),
        TIntersectableVerticalSegment(game.size.x, 0, game.size.y),
        TIntersectableHorizontalSegment(0, game.size.x, 0),
        TIntersectableHorizontalSegment(0, game.size.x, game.size.y),
    ]
    intersections = list(map(lambda obj: obj.intersect(game.ball), objects))
    print(intersections)


def main():
    #test_basic_functions()
    game = TGame(json.load(open("game.json", "rt")))
    build_intersection_times_and_normals(game)


if __name__ == '__main__':
    main()

