class TIntersectableBase:
    def __init__(self):
        pass


class TIntersectableVerticalSegment(TIntersectableBase):
    def __init__(self, x, y0, y1):
        self.x = x
        self.y0 = y0
        self.y1 = y1


