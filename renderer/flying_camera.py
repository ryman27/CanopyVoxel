import pygame as pg  # Import pygame as pg for brevity
import glm

from renderer.camera import Camera


class FlyingCamera(Camera):
    def __init__(self, app, position=(0, 150, 0), yaw=-90, pitch=0, speed=0.01, sensitivity=0.004,
                 resolution=glm.vec2(1600, 900)):
        super().__init__(position, yaw, pitch, 50, resolution)

        self.app = app
        self.speed = speed
        self.min_speed = speed / 100
        self.sensitivity = sensitivity
        self.velocity = glm.vec3(0, 0, 0)
        self.damping = 0.95  # Adjust this value to control damping strength

        self.scroll_speed = 0.05  # Speed adjustment per scroll step
        self.scroll_sensitivity = 0.002  # Sensitivity adjustment per scroll step

    def update(self, app):
        if self.app.window_has_focus:
            self.movement_control()
            self.view_control()
            self.scroll_control()

        self.apply_movement()
        super().update(app)

    def view_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        self.rotate_yaw(delta_x=mouse_dx * self.sensitivity)
        self.rotate_pitch(delta_y=mouse_dy * self.sensitivity)

    def movement_control(self):
        key_state = pg.key.get_pressed()
        vel = glm.vec3(0, 0, 0)
        move_directions = [pg.K_w, pg.K_s, pg.K_d, pg.K_a, pg.K_SPACE, pg.K_LSHIFT]
        move_vectors = [self.vec3_forward, -self.vec3_forward, self.vec3_right, -self.vec3_right, self.vec3_up,
                        -self.vec3_up]

        for key, vector in zip(move_directions, move_vectors):
            if key_state[key]:
                vel += vector * self.speed

        self.velocity += vel

    def apply_movement(self):
        self.position += self.velocity * self.app.delta_time

        # Apply damping to velocity components
        self.velocity *= self.damping

        # Stop the camera if the velocity falls below the minimum speed
        if glm.length(glm.abs(self.velocity)) < self.min_speed:
            self.velocity = glm.vec3(0, 0, 0)

    def scroll_control(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.MOUSEWHEEL:
                self.speed = max(self.speed + event.y * self.scroll_speed, 0)
                self.sensitivity = max(self.sensitivity + event.y * self.scroll_sensitivity, 0)
