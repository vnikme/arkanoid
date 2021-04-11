# coding: utf-8


import json
import sys


EPS = 0.00001


class TVector:
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def get_length(self):
        return (self.x**2 + self.y**2)**0.5

    def get_normalised(self):
        l = self.get_length()
        if abs(l) < EPS:
            return TVector(0.0, 0.0)
        return TVector(self.x / l, self.y / l)

    def scalar_multiply(self, val):
        return TVector(self.x * val, self.y * val)

    def add(self, other):
        return TVector(self.x + other.x, self.y + other.y)

    def sub(self, other):
        return TVector(self.x - other.x, self.y - other.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y


class TBrick:
    def __init__(self, position, strength):
        self.position = position
        self.strength = strength


class TBall:
    def __init__(self, position, speed, direction, radius):
        self.position = position
        self.speed = speed
        self.direction = direction.get_normalised()
        self.radius = radius


class TPlatform:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius


"""
Example:
{
    "size": { "width": 400, "height": 400 },
    "bricks": {
        "rows": 20,
        "cols": 10,
        "height": 20,
        "width": 40,
        "positions": [
            { "x": 1, "y": 1, "strength": 3 },
            { "x": 3, "y": 5, "strength": 2 },
            { "x": 5, "y": 3, "strength": 1 }
        ]
    },
    "ball": {
        "x": 150.0,
        "y": 150.0,
        "speed": 1.0,
        "dx": -1.0,
        "dy": -1.0,
        "r": 10.0,
    },
    "platform": { "x": 200, "r": 50 }
}

"""

class TGame:
    def __init__(self, data):
        self.size = TVector(data["size"]["width"], data["size"]["height"])
        self.bricks_rows = data["bricks"]["rows"]
        self.bricks_cols = data["bricks"]["cols"]
        self.brick_height = data["bricks"]["height"]
        self.brick_width = data["bricks"]["width"]
        self.bricks = list(map(lambda brick: TBrick(TVector(brick["x"], brick["y"]), brick["strength"]), data["bricks"]["positions"]))
        self.ball = TBall(
            TVector(data["ball"]["x"], data["ball"]["y"]),
            data["ball"]["speed"],
            TVector(data["ball"]["dx"], data["ball"]["dy"]),
            data["ball"]["r"]
        )
        self.platform = TPlatform(data["platform"]["x"], data["platform"]["r"])


def intersection_time_for_horizontal_line_and_moving_ball(y, y0, r, vy):
    # y0+vy*t=+-r+y
    # t=(+-r+y-y0)/vy
    if abs(vy) < EPS:
        return None
    t0 = (-r+y-y0) / vy
    t1 = (r+y-y0) / vy
    if t0 > t1:
        t0, t1 = t1, t0
    if t1 < -EPS:
        return None
    if abs(t0) < EPS:
        return 0.0
    if t0 < -EPS:
        return max(t1, 0.0)
    return t0


def solve_square_equation(a, b, c):
    d = b**2 - 4*a*c
    if d < -EPS:
        return None
    if d < EPS:
        d = 0.0
    x = (-b - d**0.5) / 2 / a
    if x > -EPS:
        if x < EPS:
            return 0.0
        return x
    x = (-b + d**0.5) / 2 / a
    if x < -EPS:
        return None
    if x < EPS:
        return 0.0
    return x


def intersection_time_for_horizontal_segment_and_moving_ball(x1, x2, y, ball_position, r, ball_direction):
    x0, y0 = ball_position.x, ball_position.y
    vx, vy = ball_direction.x, ball_direction.y
    t_line = intersection_time_for_horizontal_line_and_moving_ball(y, y0, r, vy)
    if t_line != None:
        x = x0 + vx * t_line
        if x < min(x1, x2) - EPS or x > max(x1, x2) + EPS:
            t_line = None
    # (x0+vx*t-x)**2+(y0+vy*t-y)**2=r**2
    # (vx**2+vy**2)*t**2+2*(x0*vx-vx*x+y0*vy-vy*y)*t+x0**2+x**2-2*x0*x+y0**2+y**2-2*y0*y-r**2=0
    t1 = solve_square_equation(vx**2+vy**2, 2*(x0*vx-vx*x1+y0*vy-vy*y), x0**2+x1**2-2*x0*x1+y0**2+y**2-2*y0*y-r**2)
    t2 = solve_square_equation(vx**2+vy**2, 2*(x0*vx-vx*x2+y0*vy-vy*y), x0**2+x2**2-2*x0*x2+y0**2+y**2-2*y0*y-r**2)
    result = (t_line, TVector(0, 1)) if t_line != None else None
    if t1 != None and (result == None or t1 < result[0]):
        result = (t1, TVector(0, 1))
    if t2 != None and (result == None or t2 < result[0]):
        result = (t2, TVector(0, 1))
    return result


def intersection_time_for_vertical_segment_and_moving_ball(x, y1, y2, ball_position, r, ball_direction):
    result = intersection_time_for_horizontal_segment_and_moving_ball(y1, y2, x, ball_position, r, ball_direction)
    return (result[0], TVector(result[1].y, result[1].x)) if result else None


def intersect_brick_and_moving_ball(lu, rd, ball):
    x1, y1 = lu.x, lu.y
    x2, y2 = rd.x, rd.y
    ball_position = ball.position
    r = ball.radius
    ball_direction = ball.direction.scalar_multiply(ball.speed)
    t1 = intersection_time_for_horizontal_segment_and_moving_ball(x1, x2, y1, ball_position, r, ball_direction)
    t3 = intersection_time_for_horizontal_segment_and_moving_ball(x1, x2, y2, ball_position, r, ball_direction)
    t2 = intersection_time_for_vertical_segment_and_moving_ball(x1, x2, y1, ball_position, r, ball_direction)
    t4 = intersection_time_for_vertical_segment_and_moving_ball(x1, x2, y2, ball_position, r, ball_direction)
    result = t1
    if t2 != None and (result == None or t2[0] < result[0]):
        result = t2
    if t1 != None and (result == None or t1[0] < result[0] - EPS):
        result = t1
    if t3 != None and (result == None or t3[0] < result[0] - EPS):
        result = t3
    return result


def reflect_vector(d, n):
    n = n.get_normalised()
    dn = d.dot(n)
    r = d.sub(n.scalar_multiply(2 * dn))
    return r


def test_basic_functions():
    print(intersection_time_for_horizontal_segment_and_moving_ball(0, 1, 0, TVector(0, -2), 2, TVector(-1, -1)))
    print(intersection_time_for_horizontal_segment_and_moving_ball(0, 1, 0, TVector(1, -3), 2, TVector(0, -1)))
    print(intersection_time_for_horizontal_segment_and_moving_ball(0.1, 1, 0, TVector(1, -3), 2, TVector(-1, 1)))
    print(intersect_brick_and_moving_ball(TVector(0, 1), TVector(2, 0), TBall(TVector(3, -2), 1, TVector(-1, 1), 1)))
    print(intersect_brick_and_moving_ball(TVector(0, 1), TVector(2, 0), TBall(TVector(3, 3), 1, TVector(-1, -1), 1)))
    print(intersect_brick_and_moving_ball(TVector(0, 1), TVector(2, 0), TBall(TVector(2, -2), 1, TVector(0, 1), 1)))
    print(intersect_brick_and_moving_ball(TVector(0, 1), TVector(2, 0), TBall(TVector(2, 3), 1, TVector(0, -1), 1)))
    ball = TBall(TVector(3, 3), 1, TVector(-1, -1), 1)
    v = ball.direction.scalar_multiply(ball.speed)
    intersection = intersect_brick_and_moving_ball(TVector(0, 1), TVector(2, 0), ball)
    rv = reflect_vector(v, intersection[1])
    print(v, rv)


def build_intersection_times_and_normals(game):
    intersect_brick_and_moving_ball(0.0, 0.0, game.size.x, game.size.y, game.ball.x, game.ball.y, game.ball.r, game.ball, -1)


def main():
    test_basic_functions()
    #game = TGame(json.load(open("game.json", "rt")))


if __name__ == '__main__':
    main()

