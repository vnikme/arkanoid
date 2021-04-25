from arkanoid.vector import (
    TVector,
    EPS,
)


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
    result = intersection_time_for_horizontal_segment_and_moving_ball(y1, y2, x, TVector(ball_position.y, ball_position.x), r, TVector(ball_direction.y, ball_direction.x))
    return (result[0], TVector(result[1].y, result[1].x)) if result else None


def intersect_brick_and_moving_ball(lu, rd, ball):
    x1, y1 = lu.x, lu.y
    x2, y2 = rd.x, rd.y
    ball_position = ball.position
    r = ball.radius
    ball_direction = ball.direction.scalar_multiply(ball.speed)
    t1 = intersection_time_for_horizontal_segment_and_moving_ball(x1, x2, y1, ball_position, r, ball_direction)
    t3 = intersection_time_for_horizontal_segment_and_moving_ball(x1, x2, y2, ball_position, r, ball_direction)
    t2 = intersection_time_for_vertical_segment_and_moving_ball(x1, y1, y2, ball_position, r, ball_direction)
    t4 = intersection_time_for_vertical_segment_and_moving_ball(x2, y1, y2, ball_position, r, ball_direction)
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

