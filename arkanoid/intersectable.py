from arkanoid.intersections import (
    intersection_time_for_vertical_segment_and_moving_ball,
    intersection_time_for_horizontal_segment_and_moving_ball,
    intersect_brick_and_moving_ball,
    intersect_static_ball_and_moving_ball,
    is_approaching_line,
)

class TIntersectableBase:
    def __init__(self):
        pass

    def intersect(self, ball):
        result = self.do_intersect(ball)
        if not result:
            return result
        if not is_approaching_line(ball.position, ball.direction, result[1]):
            return None
        return result

    def on_intersection(self):
        pass


class TIntersectableVerticalWall(TIntersectableBase):
    def __init__(self, x, y0, y1):
        self.x = x
        self.y0 = y0
        self.y1 = y1

    def do_intersect(self, ball):
        ball_direction = ball.direction.scalar_multiply(ball.speed)
        return intersection_time_for_vertical_segment_and_moving_ball(self.x, self.y0, self.y1, ball.position, ball.radius, ball_direction)


class TIntersectableHorizontalWall(TIntersectableBase):
    def __init__(self, x0, x1, y):
        self.x0 = x0
        self.x1 = x1
        self.y = y

    def do_intersect(self, ball):
        ball_direction = ball.direction.scalar_multiply(ball.speed)
        return intersection_time_for_horizontal_segment_and_moving_ball(self.x0, self.x1, self.y, ball.position, ball.radius, ball_direction)


class TIntersectableBrick(TIntersectableBase):
    def __init__(self, lu, rd, brick):
        self.lu = lu
        self.rd = rd
        self.brick = brick

    def do_intersect(self, ball):
        if self.brick.strength == 0:
            return None
        return intersect_brick_and_moving_ball(self.lu, self.rd, ball)

    def on_intersection(self):
        self.brick.strength = max(self.brick.strength - 1, 0)


class TIntersectablePlatform(TIntersectableBase):
    def __init__(self, platform_position, platform_radius):
        self.platform_position = platform_position
        self.platform_radius = platform_radius

    def do_intersect(self, ball):
        ball_direction = ball.direction.scalar_multiply(ball.speed)
        return intersect_static_ball_and_moving_ball(self.platform_position, self.platform_radius, ball.position, ball.radius, ball_direction)

