import trimesh

mesh = trimesh.load('models/tube.obj')
trimesh.Trimesh()

mesh.show()

print(mesh.vertices)
print(type(mesh.metadata['vertex_texture']))
