from renderer.meshes.base_mesh import BaseMesh
from renderer.meshes.cube_chunk_mesh_builder import CubeChunkMeshBuilder


class ChunkMesh(BaseMesh):
    def __init__(self, chunk):
        super().__init__()
        self.app = chunk.app
        self.chunk = chunk
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.chunk
        self.chunk_mesh_builder = CubeChunkMeshBuilder(self.chunk.world)

        self.vbo_format = '3u1 3u1 1u1'
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ('in_position', 'voxel_color_in', 'face_id')
        self.vao = self.get_vao()

    def get_vertex_data(self):
        mesh = self.chunk_mesh_builder.build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,
            format_size=self.format_size,
            chunk_pos=self.chunk.position,
            world_voxels=self.chunk.world.voxels
        )
        return mesh

    def rebuild(self):
        self.vao = self.get_vao()
