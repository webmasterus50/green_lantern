import pytest
from lonely_robot import Robot, Asteroid, MissAsteroidError, RobotFallsFromAsteroidError


class TestRobotCreation:
    def test_parameters(self):
        x, y = 10, 15
        asteroid = Asteroid(x, y)
        direction = "E"
        robot = Robot(x, y, asteroid, direction)
        assert robot.x == 10
        assert robot.y == 15
        assert robot.asteroid == asteroid
        assert robot.direction == direction

    @pytest.mark.parametrize(
        "asteroid_size,robot_coordinates",
        (
                ((15, 25), (26, 30)),
                ((15, 25), (26, 24)),
                ((15, 25), (15, 27)),
        )
    )
    def test_check_if_robot_on_asteroid(self, asteroid_size, robot_coordinates):
        with pytest.raises(MissAsteroidError):
            asteroid = Asteroid(*asteroid_size)
            Robot(*robot_coordinates, asteroid, "W")


class TestTurns():

    def setup(self):
        self.asteroid = Asteroid(5, 5)

    @pytest.mark.parametrize(
        "curent_direction,expected_direction",
        (
                ("N", "W"),
                ("W", "S"),
                ("S", "E"),
                ("E", "N")
        )
    )
    def test_turn_left(self, curent_direction, expected_direction):
        robot = Robot(3, 3, self.asteroid, curent_direction)
        robot.turn_left()
        assert robot.direction == expected_direction

    @pytest.mark.parametrize(
        "curent_direction,expected_direction",
        (
                ("W", "N"),
                ("S", "W"),
                ("E", "S"),
                ("N", "E")
        )
    )
    def test_turn_right(self, curent_direction, expected_direction):
        robot = Robot(3, 3, self.asteroid, curent_direction)
        robot.turn_right()
        assert robot.direction == expected_direction

    @pytest.mark.parametrize(
        "curent_direction, expected_x, expected_y",
        (
                ("W", 2, 3),
                ("S", 3, 2),
                ("E", 4, 3),
                ("N", 3, 4)
        ))
    def test_move(self, curent_direction, expected_x, expected_y):
        robot = Robot(3, 3, self.asteroid, curent_direction)
        robot.move()
        assert robot.direction[0] == expected_x and robot.direction[1] == expected_y

    @pytest.mark.parametrize(
        "curent_direction,asteroid_size,robot_coordinates",
        (
                ("w", (15, 26), (15, 26)),
                ("S", (25, 28), (25, 28)),
                ("N", (12, 10), (12, 10)),
                ("E", (5, 8), (5, 8))
        )
    )
    def test_check_if_robot_falls_from_asteroid(self, asteroid_size, robot_coordinates, curent_direction):
        with pytest.raises(RobotFallsFromAsteroidError):
            asteroid = Asteroid(*asteroid_size)
            robot = Robot(*robot_coordinates, asteroid, curent_direction)
            robot.move()


