import math
from rlutilities.data_classes import Vector3, Object


def sign(x):
    """Returns -1 if number is negative or zero, otherwise it return 1."""
    return -1 if x <= 0 else 1


def rotator_to_matrix(object):
    r = object.rotation.data
    CR = math.cos(r[2])
    SR = math.sin(r[2])
    CP = math.cos(r[0])
    SP = math.sin(r[0])
    CY = math.cos(r[1])
    SY = math.sin(r[1])

    matrix = []
    matrix.append(Vector3([CP * CY, CP * SY, SP]))
    matrix.append(Vector3([CY * SP * SR - CR * SY, SY * SP * SR + CR * CY, -CP * SR]))
    matrix.append(Vector3([-CR * CY * SP - SR * SY, -CR * SY * SP + SR * CY, CP * CR]))
    return matrix


def to_value(data, value):
    """ Makes more input variables possible. """
    if isinstance(data, Object):
        if value == 'location':
            return data.location
        elif value == 'velocity':
            return data.velocity
        elif value == 'rotation':
            return data.rotation
        elif value == 'angular_velocity':
            return data.angular_velocity
        else:
            raise ValueError('Unknown Value (' + value + ')')
    else:
        return Vector3(data)
