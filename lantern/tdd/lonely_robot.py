class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Robot:
    def __init__(self, x, y, asteroid, direction):
        self.x = x
        self.y = y
        self.asteroid = asteroid
        self.direction = direction
        if self.x > self.asteroid.x:
            raise MissAsteroidError()
        if self.y > self.asteroid.y:
            raise MissAsteroidError()

    def turn_left(self):
        turns = {"E": "N", "S": "E", "W": "S", "N": "W"}
        self.direction = turns[self.direction]

    def turn_right(self):
        turns = {"N": "E", "E": "S", "S": "W", "W": "N"}
        self.direction = turns[self.direction]

    def move(self):
        turns = {"N": [self.x, self.y + 1], "E": [self.x + 1, self.y],
                 "S": [self.x, self.y - 1], "W": [self.x - 1, self.y]}
        if turns["N"][0] > self.asteroid.x or turns["N"][1] > self.asteroid.y:
            raise RobotFallsFromAsteroidError()
        elif turns["E"][0] > self.asteroid.x or turns["E"][1] > self.asteroid.y:
            raise RobotFallsFromAsteroidError()
        elif turns["S"][0] > self.asteroid.x or turns["S"][1] > self.asteroid.y:
            raise RobotFallsFromAsteroidError()
        elif turns["W"][0] > self.asteroid.x or turns["W"][1] > self.asteroid.y:
            raise RobotFallsFromAsteroidError()
        self.new_coordinates = turns[self.direction]

class MissAsteroidError(Exception):
    pass

class RobotFallsFromAsteroidError(Exception):
    pass