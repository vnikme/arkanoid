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
    TIntersectableVerticalWall,
    TIntersectableHorizontalWall,
    TIntersectableBrick,
)


def build_intersection_times_and_normals(game):
    objects = [
        TIntersectableVerticalWall(0, 0, game.size.y),
        TIntersectableVerticalWall(game.size.x, 0, game.size.y),
        TIntersectableHorizontalWall(0, game.size.x, 0),
        TIntersectableHorizontalWall(0, game.size.x, game.size.y),
    ] + list(
        map(
            lambda obj: TIntersectableBrick(
                game.get_brick_lu(obj[1].position),
                game.get_brick_rd(obj[1].position),
                obj[0]
            ),
            enumerate(game.bricks)
        )
    )
    intersections = list(map(lambda obj: obj.intersect(game.ball), objects))
    print(intersections)


def main():
    #test_basic_functions()
    game = TGame(json.load(open("game.json", "rt")))
    build_intersection_times_and_normals(game)


if __name__ == '__main__':
    main()

