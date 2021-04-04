# coding: utf-8


EPS = 0.00001


def intersection_time_for_horizontal_line_and_moving_ball(y, y0, r, vy):
    # y0+vy*t=+-r+y
    # t=(+-r+y-y0)/vy
    assert(abs(vy) > EPS)
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
    x = (b - d**0.5) / 2 / a
    if x < -EPS:
        return None
    if x < EPS:
        return 0.0
    return x


def intersection_time_for_horizontal_segment_and_moving_ball(x1, x2, y, x0, y0, r, vx, vy):
    t_line = intersection_time_for_horizontal_line_and_moving_ball(y, y0, r, vy)
    if t_line != None:
        x = x0 + vx * t_line
        if x < min(x1, x2) - EPS or x > max(x1, x2) + EPS:
            t_line = None
    # (x0+vx*t-x)**2+(y0+vy*t-y)**2=r**2
    # (vx**2+vy**2)*t**2+2*(x0*vx-vx*x+y0*vy-vy*y)*t+x0**2+x**2-2*x0*x+y0**2+y**2-2*y0*y-r**2=0
    t1 = solve_square_equation(vx**2+vy**2, 2*(x0*vx-vx*x1+y0*vy-vy*y), x0**2+x1**2-2*x0*x1+y0**2+y**2-2*y0*y-r**2)
    t2 = solve_square_equation(vx**2+vy**2, 2*(x0*vx-vx*x2+y0*vy-vy*y), x0**2+x2**2-2*x0*x2+y0**2+y**2-2*y0*y-r**2)
    print(t_line, t1, t2)
    result = (t_line, 0, 1, y) if t_line != None else None
    if t1 != None and (result == None or t1 < result[0]):
        result = (t1, 0, 1, y)
    if t2 != None and (result == None or t2 < result[0]):
        result = (t2, 0, 1, y)
    return result


#def intersect_brick_and_moving_ball(x1, y1, x2, y2, x3, y3, x4, y4, x0, y0, r, vx, vy):
def main():
    print(intersection_time_for_horizontal_segment_and_moving_ball(0, 1, 0, 0, -2, 2, -1, -1))
    print(intersection_time_for_horizontal_segment_and_moving_ball(0, 1, 0, 1, -3, 2, 0, -1))
    print(intersection_time_for_horizontal_segment_and_moving_ball(0.1, 1, 0, 1, -3, 2, -1, 1))


if __name__ == '__main__':
    main()

