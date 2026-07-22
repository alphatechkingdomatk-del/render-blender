import bpy
import os
import sys

# Récupérer le texte depuis les arguments (passé par n8n)
text_to_display = sys.argv[-1] if len(sys.argv) > 1 else "Alpha Tech Kingdom"

# Supprimer tous les objets existants
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Ajouter une sphère dorée au centre
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
sphere = bpy.context.object
mat = bpy.data.materials.new(name="Or")
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()
node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
node_principled.inputs['Base Color'].default_value = (1.0, 0.843, 0.0, 1.0)
node_principled.inputs['Metallic'].default_value = 1.0
node_principled.inputs['Roughness'].default_value = 0.2
node_output = nodes.new(type='ShaderNodeOutputMaterial')
mat.node_tree.links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])
sphere.data.materials.append(mat)

# Ajouter un texte
bpy.ops.object.text_add(location=(0, 1.5, 0))
text_obj = bpy.context.object
text_obj.data.body = text_to_display
text_obj.data.alignment_x = 'CENTER'
text_obj.data.extrude = 0.05
text_obj.data.bevel_depth = 0.01
text_obj.data.size = 0.5

# Matériau cyan pour le texte
mat_text = bpy.data.materials.new(name="Cyan")
mat_text.use_nodes = True
nodes_text = mat_text.node_tree.nodes
nodes_text.clear()
node_principled_text = nodes_text.new(type='ShaderNodeBsdfPrincipled')
node_principled_text.inputs['Base Color'].default_value = (0.0, 0.9, 1.0, 1.0)
node_principled_text.inputs['Metallic'].default_value = 0.0
node_output_text = nodes_text.new(type='ShaderNodeOutputMaterial')
mat_text.node_tree.links.new(node_principled_text.outputs['BSDF'], node_output_text.inputs['Surface'])
text_obj.data.materials.append(mat_text)

# Caméra
bpy.ops.object.camera_add(location=(4, -4, 3))
cam = bpy.context.object
bpy.context.scene.camera = cam
constraint = cam.constraints.new(type='TRACK_TO')
constraint.target = sphere
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

# Lumière
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sun = bpy.context.object
sun.data.energy = 3

# Animation simple : rotation de la sphère
sphere.rotation_euler = (0, 0, 0)
sphere.keyframe_insert(data_path="rotation_euler", frame=1)
sphere.rotation_euler = (0, 0, 6.28318)
sphere.keyframe_insert(data_path="rotation_euler", frame=60)

# Rendu vidéo
output_dir = os.path.dirname(os.path.abspath(__file__))
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.fps = 30
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 60
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'MPEG4'
bpy.context.scene.render.ffmpeg.codec = 'H264'
bpy.context.scene.render.filepath = os.path.join(output_dir, "video_virale.mp4")

bpy.ops.render.render(animation=True)
print(f"Rendu terminé : {os.path.join(output_dir, 'video_virale.mp4')}")