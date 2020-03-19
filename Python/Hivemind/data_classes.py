import math
import numpy as np

from utils import *

class Vector3:
    """
    Creates a Vector3 Object that can be used for any data which need 3 numbers.
    Create an Object by calling 'Vector3([x, y, z])' where x, y, z are your values.
    """

    def __init__(self, data):
        if isinstance(data, Vector3):
            self.data = data.data
        elif isinstance(data, tuple):
            self.data = list(data)
        elif isinstance(data, np.ndarray):
            self.data = data.tolist()
        else:
            self.data = data

    def __getitem__(self, item):
        return self.data[item]

    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        return Vector3([self.data[0] + other.data[0], self.data[1] + other.data[1], self.data[2] + other.data[2]])

    def __sub__(self, other):
        return Vector3([self.data[0] - other.data[0], self.data[1] - other.data[1], self.data[2] - other.data[2]])

    def __mul__(self, other):
        return Vector3([self.data[0] * other.data[0], self.data[1] * other.data[1], self.data[2] * other.data[2]])

    def __truediv__(self, other):
        return Vector3([self.data[0] / other.data[0], self.data[1] / other.data[1], self.data[2] / other.data[2]])

    def __abs__(self):
        return Vector3([abs(self.data[0]), abs(self.data[1]), abs(self.data[2])])

    def __eq__(self, other):
        return self.data[0] == other.data[0], self.data[1] == other.data[1], self.data[2] == other.data[2]

    def __gt__(self, other):
        return self.data[0] > other.data[0], self.data[1] > other.data[1], self.data[2] > other.data[2]

    def __lt__(self, other):
        return self.data[0] < other.data[0], self.data[1] < other.data[1], self.data[2] < other.data[2]

    def tolist(self):
        return self.data

    def cap(self, low, high):
        return Vector3([max(min(self.data[0], high[0]), low[0]), max(min(self.data[1], high[1]), low[1]),
                        max(min(self.data[2], high[2]), low[2])])

    def magnitude(self):
        return math.sqrt((self.data[0] * self.data[0]) + (self.data[1] * self.data[1]) + (self.data[2] * self.data[2]))

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            return Vector3([self.data[0] / mag, self.data[1] / mag, self.data[2] / mag])
        else:
            return Vector3([0, 0, 0])


class Object:
    """
    Object is used for game objects.
    It hold all the needed values of a game object and has several functions for decluttering.
    """

    def __init__(self):
        self.location = Vector3([0, 0, 0])
        self.velocity = Vector3([0, 0, 0])
        self.rotation = Vector3([0, 0, 0])
        self.angular_velocity = Vector3([0, 0, 0])

        self.local_angular_velocity = None
        self.matrix = None
        self.index = None

    def calculate_data(self):
        """Calculates matrix and local_angular_velocity."""
        self.matrix = rotator_to_matrix(self)
        self.local_angular_velocity = Vector3([self.angular_velocity * self.matrix[0],
                                               self.angular_velocity * self.matrix[1],
                                               self.angular_velocity * self.matrix[2]])

    def to_local(self, target):
        """Returns target's local position."""
        x = (to_value(target, 'location') - self.location) * self.matrix[0]
        y = (to_value(target, 'location') - self.location) * self.matrix[1]
        z = (to_value(target, 'location') - self.location) * self.matrix[2]
        return Vector3([x, y, z])

    def velocity2d(self):
        """Returns own velocity."""
        return abs(self.velocity.data[0]) + abs(self.velocity.data[1])

    def distance_to_target_2d(self, target):
        """Calculates 2d distance to target."""
        diff = self.location - to_value(target, 'location')
        return math.sqrt(diff.data[0] ** 2 + diff.data[1] ** 2)

    def angle_to_target(self, target, local=True):
        """Returns angle to target between -pi and pi."""
        diff = to_value(target, 'location') - self.location
        angle_to_target = math.atan2(diff.data[1], diff.data[0])

        if local:
            local_angle_to_target = angle_to_target - self.rotation.data[1]

            # Correct the values
            if local_angle_to_target < -math.pi:
                local_angle_to_target += 2 * math.pi
            if local_angle_to_target > math.pi:
                local_angle_to_target -= 2 * math.pi
            return local_angle_to_target
        return math.atan2(diff.data[1], diff.data[0])

class Data:
    def __init__(self):
        self.ball = Object()
        self.players = []
        self.is_kickoff = False

    def preprocess(self, packet):
        """ Collects and formats game data """
        self.is_kickoff = packet.game_info.is_kickoff_pause

        # Collects info for all cars in match, updates objects in agent.players accordingly.
        if packet.num_cars < len(self.players):
            self.players = []

        for i in range(packet.num_cars):
            car = packet.game_cars[i]
            temp = Object()
            temp.index = i
            temp.team = sign(car.team)
            temp.name = car.name

            temp.location.data = [car.physics.location.x,
                                  car.physics.location.y,
                                  car.physics.location.z]

            temp.velocity.data = [car.physics.velocity.x,
                                  car.physics.velocity.y,
                                  car.physics.velocity.z]

            temp.rotation.data = [car.physics.rotation.pitch,
                                  car.physics.rotation.yaw,
                                  car.physics.rotation.roll]

            temp.angular_velocity.data = [car.physics.angular_velocity.x,
                                          car.physics.angular_velocity.y,
                                          car.physics.angular_velocity.z]

            temp.boost = car.boost
            temp.grounded = car.has_wheel_contact

            temp.calculate_data()

            flag = False
            for item in self.players:
                if item.index == i:
                    # Replace last frame car data with current frame
                    self.players[i] = temp
                    flag = True
                    break
            if not flag:
                # There is no last frame car data so we create a new car.
                self.players.append(temp)

        # Collect ball information and updates agent.ball accordingly.
        ball = packet.game_ball.physics
        self.ball.location.data = [ball.location.x,
                                   ball.location.y,
                                   ball.location.z]

        self.ball.velocity.data = [ball.velocity.x,
                                   ball.velocity.y,
                                   ball.velocity.z]

        self.ball.rotation.data = [ball.rotation.pitch,
                                   ball.rotation.yaw,
                                   ball.rotation.roll]

        self.ball.angular_velocity.data = [ball.angular_velocity.x,
                                           ball.angular_velocity.y,
                                           ball.angular_velocity.z]

        self.ball.calculate_data()
