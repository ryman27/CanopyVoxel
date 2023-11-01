from .world import *

import os


class ShaderProgram:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.camera = app.camera

        self.shader_dir = os.path.join(os.path.dirname(__file__), 'shaders')
        self.chunk = self.get_program(shader_name='chunk', shader_dir=self.shader_dir)

        self.set_uniforms()

    def refresh(self):
        self.set_uniforms()

    def set_uniforms(self):
        self.chunk['projection'].write(self.camera.projection_matrix)
        self.chunk['model'].write(glm.mat4())

    def update(self, app):
        self.chunk['view'].write(self.camera.view_matrix)

    def get_program(self, shader_name, shader_dir):
        with open(os.path.join(shader_dir, f'{shader_name}.vert')) as file:
            vertex_shader = file.read()

        with open(os.path.join(shader_dir, f'{shader_name}.frag')) as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
