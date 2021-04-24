from arkanoid.intersections import (
    intersection_time_for_vertical_segment_and_moving_ball,
    intersection_time_for_horizontal_segment_and_moving_ball,
)

class TIntersectableBase:
    def __init__(self):
        pass


class TIntersectableVerticalSegment(TIntersectableBase):
    def __init__(self, x, y0, y1):
        self.x = x
        self.y0 = y0
        self.y1 = y1

    def intersect(self, ball):
        ball_direction = ball.direction.scalar_multiply(ball.speed)
        result = intersection_time_for_vertical_segment_and_moving_ball(self.x, self.y0, self.y1, ball.position, ball.radius, ball_direction)
        if result is None:
            return None
        return result


class TIntersectableHorizontalSegment(TIntersectableBase):
    def __init__(self, x0, x1, y):
        self.x0 = x0
        self.x1 = x1
        self.y = y

    def intersect(self, ball):
        ball_direction = ball.direction.scalar_multiply(ball.speed)
        result = intersection_time_for_horizontal_segment_and_moving_ball(self.x0, self.x1, self.y, ball.position, ball.radius, ball_direction)
        if result is None:
            return None
        return result

