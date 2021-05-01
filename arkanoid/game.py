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

    def serialize(self):
        result = {}
        result["size"] = { "width": self.size.x, "height": self.size.y }
        result["bricks"] = { "rows": self.bricks_rows, "cols": self.bricks_cols, "height": self.brick_height, "width": self.brick_width, "positions": [] }
        for brick in self.bricks:
            result["bricks"]["positions"].append({ "x": brick.position.x, "y": brick.position.y, "strength": brick.strength })
        result["ball"] = { "x": self.ball.position.x, "y": self.ball.position.y, "speed": self.ball.speed, "dx": self.ball.direction.x, "dy": self.ball.direction.y, "r": self.ball.radius }
        result["platform"] = { "x": self.platform.position, "r": self.platform.radius }
        return result

    def get_brick_lu(self, position):
        return TVector(position.x * self.brick_width, position.y * self.brick_height)

    def get_brick_rd(self, position):
        return TVector((position.x + 1) * self.brick_width, (position.y + 1) * self.brick_height)

    def move_platform(self, delta):
        x = self.platform.position
        if x + delta - self.platform.radius < 0 or x + delta + self.platform.radius >= self.size.x:
            return x
        if (x + delta - self.ball.position.x)**2 + (self.size.y - self.ball.position.y)**2 <= (self.ball.radius + self.platform.radius)**2:
            return x
        return x + delta

    def has_won(self):
        for brick in self.bricks:
            if brick.strength > 0:
                return False
        return True

    def has_lost(self):
        return self.ball.position.y + self.ball.radius >= self.size.y - EPS

