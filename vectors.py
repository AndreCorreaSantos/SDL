class Vec2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def scale(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"


class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def scale(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"


class Vec4:
    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __add__(self, other):
        return Vec4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other):
        return Vec4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    def scale(self, scalar):
        return Vec4(self.x * scalar, self.y * scalar, self.z * scalar, self.w * scalar)

    def __repr__(self):
        return f"Vec4({self.x}, {self.y}, {self.z}, {self.w})"
