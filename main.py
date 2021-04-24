# coding: utf-8


import json
import sys


def build_intersection_times_and_normals(game):
    #consider segments separately
    bounds_intersection = intersect_brick_and_moving_ball(TVector(0.0, 0.0), game.size, game.ball)
    print(bounds_intersection)


def main():
    #test_basic_functions()
    game = TGame(json.load(open("game.json", "rt")))
    build_intersection_times_and_normals(game)


if __name__ == '__main__':
    main()

