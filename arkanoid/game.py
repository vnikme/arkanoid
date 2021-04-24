from arkanoid.vector import TVector


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

