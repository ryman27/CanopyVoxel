import math


def map_to_cie1931_color_space(color):
    # Scale the input values if they are arbitrarily large

    x, y, z = color

    max_value = max(x, y, z)

    x /= max_value
    y /= max_value
    z /= max_value

    # Observer = 2°, Illuminant = D65
    r = x * 3.2406 - y * 1.5372 - z * 0.4986
    g = -x * 0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 - y * 0.2040 + z * 1.0570

    # Ensure color components are within the 0-1 range
    r = max(0, min(r, 1)) * 255
    g = max(0, min(g, 1)) * 255
    b = max(0, min(b, 1)) * 255

    return r, g, b


class Demo:

    def __init__(self, width, height, depth):
        self.phi_counter = 0
        self.z_counter = 0
        self.theta_counter = 0

        self.timer = 0

        self.width = width
        self.height = height
        self.depth = depth

        self.radius = min(self.width, self.height, self.depth) / 2
        self.initial_radius = self.radius

    def update(self, app):

        phi = ((self.phi_counter / (self.width - 1)) * 2 * math.pi)
        theta = ((self.theta_counter / (self.height - 1)) * math.pi)

        phi += (self.z_counter * 30)
        theta += (self.z_counter * 30)

        x = (self.radius * math.sin(theta) * math.cos(phi) + 10)
        y = (self.radius * math.sin(theta) * math.sin(phi) + 10)
        z = (self.radius * math.cos(theta) + 10)

        coords = (int(x) + self.initial_radius, int(y) + self.initial_radius, int(z) + self.initial_radius)

        color = map_to_cie1931_color_space(coords)

        # Add the voxel to the current sphere
        app.scene.world.voxelManager.add_voxel(coords, color)

        self.phi_counter += 1
        if self.phi_counter >= self.height:
            self.phi_counter = 0
            self.theta_counter += 1

        if self.theta_counter >= self.width:
            self.theta_counter = 0
            self.phi_counter = 0
            self.radius = self.initial_radius + ((self.z_counter % 3) - 1)

            if self.radius < 0:
                self.radius = 0

            self.z_counter += 1
