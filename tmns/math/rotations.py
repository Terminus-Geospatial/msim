#**************************** INTELLECTUAL PROPERTY RIGHTS ****************************#
#*                                                                                    *#
#*                           Copyright (c) 2025 Terminus LLC                          *#
#*                                                                                    *#
#*                                All Rights Reserved.                                *#
#*                                                                                    *#
#*          Use of this source code is governed by LICENSE in the repo root.          *#
#*                                                                                    *#
#**************************** INTELLECTUAL PROPERTY RIGHTS ****************************#
#

#  Python Standard Libraries
from enum import Enum
import logging
import math

#  Numerical Python
import numpy as np

class Axis(Enum):
    X = "X"
    Y = "Y"
    Z = "Z"


class Quaternion:

    def __init__(
        self, w: float = 1.0, x: float = 0.0, y: float = 0.0, z: float = 0.0, data=None
    ):
        if data is None:
            self.data = np.array([w, x, y, z], dtype=np.float64)
        else:
            self.data = data

    def get_real(self):
        return self.data[0]

    def set_real( self, value ):
        self.data[0] = value

    def get_imaginary(self):
        return self.data[1:]

    def set_imaginary(self, value):
        self.data[1:] = value

    def w(self):
        return self.get_real()

    def x(self):
        return self.data[1]

    def y(self):
        return self.data[2]

    def z(self):
        return self.data[3]

    def conj(self):
        return Quaternion(
            self.get_real(), self.x() * -1, self.y() * -1, self.z() * -1
        )

    def mag2(self):
        return self.w() ** 2 + np.dot(self.get_imaginary(), self.get_imaginary())

    def mag(self):
        return math.sqrt(self.mag2())

    def normalize(self):
        return self * (1 / self.mag())

    def is_normalized(self, TOLERANCE: float = 1e-8):

        if math.fabs(self.mag() - 1.0) > TOLERANCE:
            return False
        return True

    def inverse(self, TOLERANCE: float = 1e-8):

        if self.mag() < TOLERANCE:
            raise ArithmeticError("Quaternion is not large enough.")

        return self.conj() * (1.0 / self.mag())

    def __add__(self, other):

        if isinstance(other, Quaternion):
            return Quaternion(data=self.data + other.data)
        raise TypeError("Other type must be Quaternion")

    def __sub__(self, other):

        if isinstance(other, Quaternion):
            return Quaternion(data=self.data - other.data)
        raise TypeError("Other type must be Quaternion")

    def __mul__(self, other):

        #  Scalar multiplication
        if isinstance(other, int) or isinstance(other, float):
            return Quaternion(data=other * self.data)

        #  Quaternion x Quaternion
        if isinstance(other, Quaternion):

            return Quaternion( self.w() * other.w() - np.dot(self.get_imaginary(), other.get_imaginary()),
                              (self.w() * other.x()) + (self.x() * other.w()) + (self.y() * other.z()) - (self.z() * other.y()),
                              (self.w() * other.y()) + (self.y() * other.w()) - (self.x() * other.z()) + (self.z() * other.x()),
                              (self.w() * other.z()) + (self.z() * other.w()) + (self.x() * other.y()) - (self.y() * other.x()),
            )

        raise NotImplementedError(f"Not supported for other type: {type(other)}")

    def __rmul__(self, other):

        if isinstance(other, int) or isinstance(other, float):
            return self * other

        raise NotImplementedError(
            f"__rmul__ Not Implemented for other type: {type(other)}"
        )

    def __str__(self):

        return f"Quaternion( w: {self.w()}, x: {self.x()}, y: {self.y()}, z: {self.z()}, len: {self.mag()})"

    def to_directional_cosine_matrix( self, eps=1e-1 ):
        """
        Standard DCM transforms
        """

        if math.fabs(self.mag() - 1.0) > eps:
            logging.warning(f"Quaternion exceeds length. {self.mag()}")

        M = np.eye(3, 3, dtype=np.float64)

        w = self.w()
        x = self.x()
        y = self.y()
        z = self.z()

        M[0, 0] = x * x - y * y - z * z + w * w
        M[0, 1] = 2.0 * (x * y + w * z)
        M[0, 2] = 2.0 * (x * z - w * y)

        M[1, 0] = 2.0 * (x * y - z * w)
        M[1, 1] = -x * x + y * y - z * z + w * w
        M[1, 2] = 2.0 * (y * z + w * x)

        M[2, 0] = 2.0 * (x * z + w * y)
        M[2, 1] = 2.0 * (y * z - w * x)
        M[2, 2] = -x * x - y * y + z * z + w * w

        return M

    def to_rotation_matrix(self):
        """
        Reference: https://d3cw3dd2w32x2b.cloudfront.net/wp-content/uploads/2015/01/matrix-to-quat.pdf
        This paper uses opposize signs on the addition and subtraction operations.
        """

        w = self.w()
        x = self.x()
        y = self.y()
        z = self.z()

        xx2 = 2 * x * x
        yy2 = 2 * y * y
        zz2 = 2 * z * z
        xy2 = 2 * x * y
        wz2 = 2 * w * z
        zx2 = 2 * z * x
        wy2 = 2 * w * y
        yz2 = 2 * y * z
        wx2 = 2 * w * x

        #  Quaternion is eci2tel
        rot_mat = np.zeros((3, 3), dtype=np.float64)
        rot_mat[0, 0] = 1.0 - yy2 - zz2
        rot_mat[0, 1] = xy2 + wz2
        rot_mat[0, 2] = zx2 - wy2

        rot_mat[1, 0] = xy2 - wz2
        rot_mat[1, 1] = 1.0 - xx2 - zz2
        rot_mat[1, 2] = yz2 + wx2

        rot_mat[2, 0] = zx2 + wy2
        rot_mat[2, 1] = yz2 - wx2
        rot_mat[2, 2] = 1.0 - xx2 - yy2

        return rot_mat

    @staticmethod
    def from_angle_axis(angle_rad: float, axis):

        axis_norm = axis / np.linalg.norm(axis)

        return Quaternion(
            math.cos(0.5 * angle_rad),
            math.sin(0.5 * angle_rad) * axis_norm[0],
            math.sin(0.5 * angle_rad) * axis_norm[1],
            math.sin(0.5 * angle_rad) * axis_norm[2],
        )

    @staticmethod
    def from_euler_angle(axis: Axis, angle_rad: float):

        cos_angle = math.cos(angle_rad / 2.0)
        sin_angle = math.sin(angle_rad / 2.0)

        if axis == Axis.X:
            return Quaternion(cos_angle, sin_angle, 0.0, 0.0)
        elif axis == Axis.Y:
            return Quaternion(cos_angle, 0.0, sin_angle, 0.0)
        elif axis == Axis.Z:
            return Quaternion(cos_angle, 0.0, 0.0, sin_angle)
        else:
            return None

    @staticmethod
    def from_euler_angles(
        axis1: Axis,
        angle1_rad: float,
        axis2: Axis,
        angle2_rad: float,
        axis3: Axis,
        angle3_rad: float,
    ):

        q1 = Quaternion.from_euler_angle(axis1, angle1_rad)
        q2 = Quaternion.from_euler_angle(axis2, angle2_rad)
        q3 = Quaternion.from_euler_angle(axis3, angle3_rad)

        return q1 * q2 * q3

    @staticmethod
    def from_directional_cosine_matrix( matrix ):
        
        trace = matrix[0, 0] + matrix[1, 1] + matrix[2, 2]
        q = np.zeros(4, dtype=np.float64)

        choice = 0
        if (
            matrix[0, 0] > matrix[1, 1]
            and matrix[0, 0] > matrix[2, 2]
            and matrix[0, 0] > trace
        ):
            choice = 0
        elif (
            matrix[1, 1] > matrix[0, 0]
            and matrix[1, 1] > matrix[2, 2]
            and matrix[1, 1] > trace
        ):
            choice = 1
        elif (
            matrix[2, 2] > matrix[0, 0]
            and matrix[2, 2] > matrix[1, 1]
            and matrix[2, 2] > trace
        ):
            choice = 2
        elif trace > matrix[0, 0] and trace > matrix[1, 1] and trace > matrix[2, 2]:
            choice = 3

        if choice == 0:
            q[1] = 0.5 * math.sqrt(1 + 2.0 * matrix[0, 0] - trace)
            q[2] = (matrix[0, 1] + matrix[1, 0]) / (4 * q[1])
            q[3] = (matrix[0, 2] + matrix[2, 0]) / (4 * q[1])
            q[0] = (matrix[1, 2] - matrix[2, 1]) / (4 * q[1])

        elif choice == 1:
            q[2] = 0.5 * math.sqrt(1 + 2.0 * matrix[1, 1] - trace)
            q[1] = (matrix[0, 1] + matrix[1, 0]) / (4 * q[2])
            q[3] = (matrix[1, 2] + matrix[2, 1]) / (4 * q[2])
            q[0] = (matrix[2, 0] - matrix[0, 2]) / (4 * q[2])

        elif choice == 2:
            q[3] = 0.5 * math.sqrt(1 + 2.0 * matrix[2, 2] - trace)
            q[1] = (matrix[0, 2] + matrix[2, 0]) / (4 * q[3])
            q[2] = (matrix[1, 2] + matrix[2, 1]) / (4 * q[3])
            q[0] = (matrix[0, 1] - matrix[1, 0]) / (4 * q[3])

        else:
            q[0] = 0.5 * math.sqrt(1 + 2.0 * trace - trace)
            q[1] = (matrix[1, 2] - matrix[2, 1]) / (4 * q[0])
            q[2] = (matrix[2, 0] - matrix[0, 2]) / (4 * q[0])
            q[3] = (matrix[0, 1] - matrix[1, 0]) / (4 * q[0])

        return Quaternion(q[0], q[1], q[2], q[3])

    @staticmethod
    def from_rotation_matrix(M):
        """
        Reference: https://d3cw3dd2w32x2b.cloudfront.net/wp-content/uploads/2015/01/matrix-to-quat.pdf
        """
        t = None
        q = None
        if M[2, 2] < 0:
            if M[0, 0] > M[1, 1]:
                t = 1 + M[0, 0] - M[1, 1] - M[2, 2]
                q = Quaternion(
                    M[1, 2] - M[2, 1], t, M[0, 1] + M[1, 0], M[2, 0] + M[0, 2]
                )
            else:
                t = 1 - M[0, 0] + M[1, 1] - M[2, 2]
                q = Quaternion(
                    M[2, 0] - M[0, 2], M[0, 1] + M[1, 0], t, M[1, 2] + M[2, 1]
                )
        else:
            if M[0, 0] < -M[1, 1]:
                t = 1 - M[0, 0] - M[1, 1] + M[2, 2]
                q = Quaternion(
                    M[0, 1] - M[1, 0], M[2, 0] + M[0, 2], M[1, 2] + M[2, 1], t
                )
            else:
                t = 1 + M[0, 0] + M[1, 1] + M[2, 2]
                q = Quaternion(
                    t, M[1, 2] - M[2, 1], M[2, 0] - M[0, 2], M[0, 1] - M[1, 0]
                )

        return q * (0.5 / math.sqrt(t))


def rotation_matrix(axis: Axis, theta_rad: float):
    """
    Reference: https://mathworld.wolfram.com/RotationMatrix.html
    """

    if axis == Axis.X:
        return np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, math.cos(theta_rad), math.sin(theta_rad)],
                [0.0, -math.sin(theta_rad), math.cos(theta_rad)],
            ],
            dtype=np.float64,
        )
    elif axis == Axis.Y:
        return np.array(
            [
                [math.cos(theta_rad), 0.0, -math.sin(theta_rad)],
                [0.0, 1.0, 0.0],
                [math.sin(theta_rad), 0.0, math.cos(theta_rad)],
            ],
            dtype=np.float64,
        )
    elif axis == Axis.Z:
        return np.array(
            [
                [math.cos(theta_rad), math.sin(theta_rad), 0.0],
                [-math.sin(theta_rad), math.cos(theta_rad), 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        )
    else:
        return None


def euler_angles_to_rotation_matrix(
    axis1: Axis,
    psi_rad: float,
    axis2: Axis,
    theta_rad: float,
    axis3: Axis,
    phi_rad: float,
):
    M_a = rotation_matrix(axis1, psi_rad)
    M_b = rotation_matrix(axis2, theta_rad)
    M_c = rotation_matrix(axis3, phi_rad)

    return M_c @ M_b @ M_a

