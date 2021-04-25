from arkanoid.vector import (
    TVector,
    EPS,
)

class TLine:
    def __init__(self, a = 0.0, b = 0.0, c = 0.0):
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self):
        return '({}x + {}y + {} = 0)'.format(self.a, self.b, self.c)

    def __str__(self):
        return '({}x + {}y + {} = 0)'.format(self.a, self.b, self.c)

    def get_normalised(self):
        l = TVector(self.a, self.b).get_length()
        if abs(l) < EPS:
            return TLine(0.0, 0.0, 0.0)
        return TLine(self.a / l, self.b / l, self.c / l)

