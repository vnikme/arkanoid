from arkanoid.vector import (
    TVector,
    EPS,
)
from arkanoid.line import TLine


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
    #print("square equation: {}, {}, {}".format(a, b, c))
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


def is_approaching_line(p, d, l):
    if (l.a * p.x + l.b * p.y + l.c) * (l.a * d.x + l.b * d.y) > -EPS:      # going away from the line
        return False
    return True


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
    result = (t_line, TLine(0, 1, -y)) if t_line != None and is_approaching_line(ball_position, ball_direction, TLine(0, 1, -y)) else None
    #print(x1, x2, y, t1, t2, TVector(x1 - x2, 0).dot(ball_direction), TVector(x2 - x1, 0).dot(ball_direction))
    if t1 != None and (result == None or t1 < result[0]):
        if TVector(x1 - x2, 0).dot(ball_direction) < 0.0:
            l = TLine(1, 0, -x1)
        else:
            l = TLine(0, 1, -y)
        if is_approaching_line(ball_position, ball_direction, l):
            result = (t1, l)
    if t2 != None and (result == None or t2 < result[0]):
        if TVector(x2 - x1, 0).dot(ball_direction) < 0.0:
            l = TLine(1, 0, -x2)
        else:
            l = TLine(0, 1, -y)
        if is_approaching_line(ball_position, ball_direction, l):
            result = (t2, l)
    return result


def intersection_time_for_vertical_segment_and_moving_ball(x, y1, y2, ball_position, r, ball_direction):
    result = intersection_time_for_horizontal_segment_and_moving_ball(y1, y2, x, TVector(ball_position.y, ball_position.x), r, TVector(ball_direction.y, ball_direction.x))
    return (result[0], TLine(result[1].b, result[1].a, result[1].c)) if result else None


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
    if t3 != None and (result == None or t3[0] < result[0]):
        result = t3
    if t4 != None and (result == None or t4[0] < result[0]):
        result = t4
    return result


def intersect_static_ball_and_moving_ball(static_ball_position, static_ball_radius, ball_position, ball_radius, ball_direction):
    x1, y1 = static_ball_position.x, static_ball_position.y
    r1 = static_ball_radius
    x0, y0 = ball_position.x, ball_position.y
    dx, dy = ball_direction.x, ball_direction.y
    r0 = ball_radius
    if (x1 - x0)**2 + (y1 - y0)**2 > (r0 + r1)**2:
        # (x0 + dx * t - x1) ^ 2 + (y0 + dy * t - y1) ^ 2 = (r0 + r1) ^ 2
        # (dx^2 + dy^2) * t^2 + 2 * (x0 * dx - x1 * dx + y0 * dy - y1 * dy) * t + (x0^2 + x1^2 + y0^2 + y1^2 - 2*x0*x1 - 2*y0*y1 - (r0 + r1)^2) = 0
        t = solve_square_equation(dx**2 + dy**2, 2 * (x0 * dx - x1 * dx + y0 * dy - y1 * dy), (x0**2 + x1**2 + y0**2 + y1**2 - 2*x0*x1 - 2*y0*y1 - (r0 + r1)**2))
        #print("Platform intersection: {}".format(t))
        if t is None:
            return None
    else:
        t = ((x1 - x0)**2 + (y1 - y0)**2)**0.5 / (r0 + r1)
        r0 *= t
        r1 *= t
        t = 0.0
    x, y = x0 + dx * t, y0 + dy * t
    a, b = x1 - x, y1 - y
    x2, y2 = x + r0 / (r0 + r1) * a, y + r0 / (r0 + r1) * b
    # a * x2 + b * y2 + c = 0
    c = -(a * x2 + b * y2)
    return (t, TLine(a, b, c))


def reflect_vector_by_normal(d, n):
    n = n.get_normalised()
    dn = d.dot(n)
    r = d.sub(n.scalar_multiply(2 * dn))
    return r


def reflect_moving_point_from_lines(p, d, first_move, intersections):
    # (p.x + d.x * t) * l.a + (p.y + d.y * t) * l.b + l.c
    # t * (l.a * d.x + l.b * d.y) + (l.a * p.x + l.b * p.y + l.c)
    # d(g(f(t)))/dt = dg/df * df/dt
    # df(t)^2/dt = 2f(t) * df/dt
    # 2 * (l.a * p.x + l.b * p.y + l.c) * (l.a * d.x + l.b * d.y)
    #print('reflecting: {}'.format(d))
    is_first = True
    for l, intersection in intersections:
        if not is_approaching_line(p, d, l):
            #print('skipping: {} {} {}'.format(p, d, l))
            continue
        #print('doing')
        if is_first:
            is_first = False
            p = p.add(first_move)
        d = reflect_vector_by_normal(d, TVector(l.a, l.b)).get_normalised()
        intersection.on_intersection()
    #print('result: {}'.format(d))
    return d
    

def test_basic_functions():
    print(intersect_static_ball_and_moving_ball(TVector(200, 400), 50, TVector(300, 300), 10, TVector(-1, 1)))
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

