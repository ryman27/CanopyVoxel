import voxelTest as vt

# Sphere parameters
radius = 5  # Adjust the radius as needed
center = (10, 10, 10)  # Center of the sphere



chunkLength = 16
chunkSize = 64

# Create background and voxel window
bg = vt.rgba(0, 0, 0, 1)
vw = vt.voxelWindow(chunkLength,chunkSize,1200, 900, bg)




color = vt.rgba(1, 0.525, 0.525, 1)

for x in range(0,chunkSize):
    for y in range(0,chunkSize):
        for z in range(0,chunkSize):
            vw.SetVoxel(vt.coordinate(x,y,z), color)





print(color)

while not vw.ShouldClose():
    vw.update()

