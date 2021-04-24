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

