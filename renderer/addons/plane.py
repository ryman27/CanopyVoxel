class plane:
    def __init__(self, size):
        self.x = 0
        self.y = 0
        self.z = 0
        self.size = size

    def update(self, app):
        app.scene.world.voxelManager.add_voxel((self.x, self.y, self.z), (255, 255, 255))
        self.x += 1
        if self.x > self.size[0]:
            self.x = 0
            self.z += 1
        if self.z > self.size[2]:
            self.z = 0
            self.y += 1
        if self.y > self.size[1]:
            self.y = 0
            self.z += 1
