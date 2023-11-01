import os
import sys
from typing import Callable

import moderngl as mgl
import pygame as pg

from .flying_camera import FlyingCamera
from .scene import Scene
from .shader_program import ShaderProgram
from .world import *


class VoxelEngine:
    def __init__(self, custom_update=None, custom_init=None, world_size=(8, 8, 8), chunk_size=32,
                 bg_color=glm.vec3(0.15, 0.05, 0.05), voxel_array=None):
        self.window_has_focus = False
        self.scene = None
        self.shader_program = None
        self.camera = None

        self.bg_color = bg_color

        self.updates: list[Callable] = list()
        self.inits: list[Callable] = list()

        if custom_update is not None:
            self.updates.append(custom_update)

        if custom_init is not None:
            self.inits.append(custom_init)

        self.world_size = world_size
        self.chunk_size = chunk_size

        pg.init()

        package_dir = os.path.dirname(__file__)
        image_path = os.path.join(package_dir, 'assets', 'icon.png')
        pygame_icon = pg.image.load(image_path)
        pg.display.set_icon(pygame_icon)

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)

        pg.display.set_mode(glm.vec2(1600, 900), flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()

        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0

        self.is_running = True
        self.on_init(voxel_array=voxel_array)

    def on_init(self, voxel_array=None):
        self.camera = FlyingCamera(self, position=(
            int(self.world_size[0] * self.chunk_size / 2), self.world_size[1] * self.chunk_size,
            int(self.world_size[2] * self.chunk_size / 2)), yaw=-90, resolution=glm.vec2(1600,900))
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self, self.world_size, self.chunk_size, voxel_array=voxel_array)

        self.updates.append(self.camera.update)
        self.updates.append(self.shader_program.update)
        self.updates.append(self.scene.update)

        for init_function in self.inits:
            init_function(self)

    def update(self):
        for update_function in self.updates:
            update_function(self)

        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001

        pg.display.set_caption("Canopy Voxelation Renderer")

    def render(self):
        self.ctx.clear(color=self.bg_color)
        self.scene.render()
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.ACTIVEEVENT:
                if event.gain == 1:  # Window has gained focus
                    self.window_has_focus = True
                    pg.event.set_grab(True)
                    pg.mouse.set_visible(False)
                elif event.gain == 0:  # Window has lost focus
                    self.window_has_focus = False
                    pg.event.set_grab(False)
                    pg.mouse.set_visible(True)

            if self.window_has_focus:
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.window_has_focus = False
                    pg.event.set_grab(False)
                    pg.mouse.set_visible(True)

                if event.type == pg.KEYDOWN and event.key == pg.K_F11:
                    pg.display.toggle_fullscreen()

    def run(self):
        while self.is_running:
            self.step()
        pg.quit()
        sys.exit()

    def step(self):
        self.handle_events()
        self.update()
        self.render()
