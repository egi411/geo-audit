"""Render the homepage conveyor with Blender 4.5 (bpy).
Usage: python neural-line.py OUTPUT_DIRECTORY [preview|film]
"""

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

output = Path(sys.argv[1]).resolve()
mode = sys.argv[2] if len(sys.argv) > 2 else "preview"
output.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 14 if mode == "film" else 36
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 6
scene.cycles.transparent_max_bounces = 4
prefs = bpy.context.preferences.addons["cycles"].preferences
if sys.platform == "darwin":
    prefs.compute_device_type = "METAL"
    prefs.refresh_devices()
    if any(d.type == "METAL" for d in prefs.devices):
        scene.cycles.device = "GPU"
        for device in prefs.devices:
            device.use = device.type == "METAL"
scene.render.resolution_x = 1280 if mode == "film" else 1800
scene.render.resolution_y = 440 if mode == "film" else 620
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
scene.render.use_persistent_data = True
scene.render.fps = 24
scene.frame_start, scene.frame_end = 1, 96
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.view_settings.view_transform = "AgX"
world = bpy.data.worlds.new("Studio")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.19, 0.22, 0.3, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.24
scene.world = world


def finish(name, color, metal=0, rough=0.33, emission=0, transmission=0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    for key, val in [
        ("Base Color", (*color, 1)),
        ("Metallic", metal),
        ("Roughness", rough),
        ("Emission Color", (*color, 1)),
        ("Emission Strength", emission),
        ("Transmission Weight", transmission),
        ("IOR", 1.46),
    ]:
        shader.inputs[key].default_value = val
    return mat


graphite = finish("Hard anodized graphite", (0.032, 0.044, 0.062), 0.8, 0.28)
ceramic = finish("Porcelain ceramic", (0.70, 0.75, 0.82), 0.5, 0.23)
alloy = finish("Milled aluminium", (0.41, 0.48, 0.57), 0.94, 0.25)
chrome = finish("Polished chamfer", (0.72, 0.8, 0.92), 0.97, 0.16)
rubber = finish("Vulcanized belt", (0.014, 0.019, 0.024), 0.12, 0.53)
blue = finish("Cobalt anodized finish", (0.012, 0.048, 0.46), 0.7, 0.23)
light = finish("Scanner diode", (0.046, 0.18, 1), 0.17, 0.21, 3)
white = finish("Status light", (0.6, 0.81, 1), 0.1, 0.19, 2.2)
glass = finish("Optical shield", (0.72, 0.84, 0.99), 0.04, 0.075, transmission=0.97)
ground = finish("Black studio", (0.008, 0.010, 0.016), 0.18, 0.42)


def shape(name, material, bevel=0):
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    if bevel:
        mod = obj.modifiers.new("Machined edges", "BEVEL")
        mod.width = bevel
        mod.segments = 4
        normal = obj.modifiers.new("Face normals", "WEIGHTED_NORMAL")
        normal.keep_sharp = True
    return obj


def box(name, xyz, size, mat, bevel=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=xyz)
    obj = bpy.context.object
    obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return shape(name, mat, bevel)


def shaft(name, start, end, radius, mat, vertices=40):
    a, b = Vector(start), Vector(end)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=(b - a).length, location=(a + b) / 2
    )
    obj = bpy.context.object
    obj.rotation_euler = (b - a).to_track_quat("Z", "Y").to_euler()
    for face in obj.data.polygons:
        face.use_smooth = len(face.vertices) == 4
    return shape(name, mat, min(0.022, radius * 0.14))


def pipe(name, points, radius, material):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 12
    curve.bevel_resolution = 4
    curve.bevel_depth = radius
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for bp, pt in zip(spline.bezier_points, points):
        bp.co = pt
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    ob = bpy.data.objects.new(name, curve)
    scene.collection.objects.link(ob)
    curve.materials.append(material)
    return ob


def word(text, xyz, size, mat, rotation=(math.pi / 2, 0, 0)):
    data = bpy.data.curves.new(text, "FONT")
    data.body, data.size, data.extrude = text, size, 0.0015
    ob = bpy.data.objects.new(text, data)
    scene.collection.objects.link(ob)
    ob.location, ob.rotation_euler = xyz, rotation
    data.materials.append(mat)
    return ob


def motion(obj, key, start, end):
    setattr(obj, key, start)
    obj.keyframe_insert(data_path=key, frame=1)
    setattr(obj, key, end)
    obj.keyframe_insert(data_path=key, frame=97)
    for curve in obj.animation_data.action.fcurves:
        for pt in curve.keyframe_points:
            pt.interpolation = "LINEAR"


def softbox(name, xyz, target, watt, color, w, h):
    data = bpy.data.lights.new(name, "AREA")
    data.energy, data.color, data.shape, data.size, data.size_y = (
        watt,
        color,
        "RECTANGLE",
        w,
        h,
    )
    ob = bpy.data.objects.new(name, data)
    scene.collection.objects.link(ob)
    ob.location = xyz
    ob.rotation_euler = (
        (Vector(target) - Vector(xyz)).to_track_quat("-Z", "Y").to_euler()
    )


box("Cyclorama floor", (0, 0, -0.38), (220, 220, 0.65), ground)
for x in (-5.25, -0.3, 5.25):
    for y in (-0.88, 0.88):
        shaft("Isolation foot", (x, y, -0.052), (x, y, 0.11), 0.27, rubber)
        box("Machine leg", (x, y, 0.39), (0.47, 0.44, 0.64), graphite, 0.08)
        box("Mounting plate", (x, y, 0.14), (0.59, 0.56, 0.1), alloy)
box("Structural spine", (0, 0, 0.69), (12.8, 2.08, 0.46), graphite, 0.19)
box("Drive belt", (0, 0, 0.955), (12.5, 1.76, 0.28), rubber, 0.13)
for side in (-1, 1):
    y = side * 0.99
    box("Extruded side frame", (0, y, 0.89), (12.6, 0.14, 0.37), alloy, 0.065)
    box(
        "Machined groove",
        (0, y + side * 0.078, 0.91),
        (12.18, 0.022, 0.062),
        graphite,
        0.016,
    )
    for x in (-5.7, -4.35, -3, -1.65, -0.3, 1.05, 2.4, 3.75, 5.1, 5.85):
        shaft(
            "Recessed fastener",
            (x, y, 0.77),
            (x, y + side * 0.085, 0.77),
            0.041,
            chrome,
            12,
        )
# The graphite tread and small carriers move on the same pitch.
for n in range(48):
    x = -6.05 + n * 0.254
    strip = box("Belt rib", (x, 0, 1.103), (0.07, 1.68, 0.03), graphite, 0.013)
    drift = strip.driver_add("location", 0).driver
    drift.expression = f"{x:.5f} + ((frame - 1) % 12) * 0.254 / 12"

# Input magazine: stacked sheets and a precision feed mouth.
box("Feeder mount", (-4.95, 0, 1.33), (2.64, 2.1, 0.36), graphite, 0.13)
box("Feeder housing", (-4.97, 0, 1.64), (2.48, 2.02, 0.4), ceramic, 0.11)
for z in (1.88, 1.99, 2.10, 2.21):
    box("Document lamination", (-5.02, 0, z), (1.85, 1.36, 0.085), chrome, 0.04)
box("Input page", (-5.02, 0, 2.27), (1.81, 1.34, 0.06), ceramic, 0.04)
for y, length in ((0.30, 0.99), (0.14, 0.78), (-0.02, 1.23), (-0.18, 0.63)):
    box("Etched text", (-5.12, y, 2.306), (length, 0.04, 0.009), graphite, 0.003)
box("Feeder slit", (-4.99, -1.021, 1.65), (1.75, 0.035, 0.12), rubber, 0.035)
box("Feeder light", (-4.99, -1.046, 1.65), (1.36, 0.014, 0.023), white, 0.01)
for y in (-0.81, 0.81):
    box("Guide rail", (-5.0, y, 2.12), (2.28, 0.13, 0.61), alloy, 0.055)

# The inference head arches over moving cards. Its shell and optics are separate parts.
for y in (-1.05, 1.05):
    box("Scanner pedestal", (-0.15, y, 1.18), (2.65, 0.43, 0.45), graphite, 0.12)
    box("Optical tower", (-0.15, y, 1.90), (2.04, 0.32, 1.30), alloy, 0.09)
    box(
        "Dark inset",
        (-0.15, y + (0.18 if y > 0 else -0.18), 1.87),
        (1.70, 0.035, 0.88),
        graphite,
        0.055,
    )
    for n in range(13) if y > 0 else (0, 1, 2, 10, 11, 12):
        box(
            "Cooling fin",
            (-0.90 + n * 0.125, y + (0.21 if y > 0 else -0.21), 1.87),
            (0.071, 0.08, 0.65),
            alloy,
            0.024,
        )
# Through the front window, three processor dies light in order under the scanner.
for i in range(3):
    z = 1.60 + i * 0.20
    box("Processor die", (-0.15, -1.31, z), (0.78, 0.22, 0.115), alloy, 0.035)
    luminous = finish(f"Compute stage {i + 1}", (0.016, 0.13, 1), 0.25, 0.19, 1.4)
    signal = luminous.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    driver = signal.driver_add("default_value").driver
    driver.expression = f"0.6 + 3.0 * max(0, sin((frame-1) * 0.13 - {i * 1.35}))"
    box(
        "Processor activity",
        (-0.15, -1.424, z + 0.016),
        (0.62, 0.013, 0.034),
        luminous,
        0.005,
    )
box("Processor glass", (-0.15, -1.46, 1.83), (1.02, 0.029, 0.72), glass, 0.012)
box("Crown", (-0.15, 0, 2.65), (2.27, 2.56, 0.49), ceramic, 0.13)
box("Sapphire top", (-0.15, 0, 2.94), (1.99, 2.18, 0.13), blue, 0.06)
box("Machined lid", (-0.15, 0, 3.02), (1.62, 1.84, 0.055), graphite, 0.035)
for x in (-0.84, 0.54):
    for y in (-0.78, 0.78):
        shaft("Cover screw", (x, y, 3.045), (x, y, 3.071), 0.045, chrome, 8)
word("aileed", (-0.64, -0.15, 3.052), 0.36, ceramic, rotation=(0, 0, 0))
for x in (-1.22, 0.92):
    box("Scanner slit", (x, 0, 2.385), (0.052, 2.16, 0.048), light, 0.013)
# A low transparent guard reveals the cards to the camera.
for x0, x1 in ((-3.64, -1.38), (1.18, 4.08)):
    for y in (-0.91, 0.91):
        box(
            "Edge of optical glass",
            ((x0 + x1) / 2, y, 1.41),
            (x1 - x0, 0.043, 0.44),
            glass,
            0.017,
        )
        shaft("Guard trim", (x0, y, 1.64), (x1, y, 1.64), 0.027, chrome, 20)
        for x in (x0 + 0.08, x1 - 0.08):
            box("Glass clamp", (x, y, 1.22), (0.16, 0.14, 0.27), alloy, 0.025)
# Compute nodes and a bundled fibre harness between the rear modules.
for n in range(3):
    y = 1.09 + n * 0.14
    pipe(
        "Cable loom",
        [
            (-4.7, y, 1.82),
            (-4.23, y + 0.3, 1.31),
            (-2.72, y + 0.36, 1.29),
            (-1.77, y + 0.3, 1.30),
            (-1.17, y, 1.87),
        ],
        0.055,
        blue if n == 1 else graphite,
    )
# Output station: a slotted envelope and a luminous check on its glass display.
box("Output bed", (5.02, 0, 1.31), (2.55, 2.02, 0.32), graphite, 0.12)
for y in (-0.94, 0.94):
    box("Receiver cheek", (5.03, y, 1.60), (2.48, 0.17, 0.55), alloy, 0.075)
box("Front of receiver", (5.03, -1.048, 1.37), (2.17, 0.045, 0.23), blue, 0.035)
word("aileed", (4.64, -1.075, 1.31), 0.18, ceramic)
panel = box("Response screen", (5.56, 0.33, 1.94), (1.42, 0.14, 1.05), graphite, 0.10)
box("Screen glass", (5.56, 0.244, 1.94), (1.27, 0.045, 0.87), blue, 0.055)
pipe(
    "Confirmation mark",
    [(5.25, 0.21, 1.95), (5.46, 0.21, 1.77), (5.84, 0.21, 2.12)],
    0.043,
    white,
)
for n, x in enumerate((-3.95, -1.92, 0.11, 2.14)):
    packet = bpy.data.objects.new("Information packet", None)
    scene.collection.objects.link(packet)
    components = [
        box("Card substrate", (0, 0, 1.162), (1.37, 0.96, 0.089), blue, 0.07),
        box("Card face", (0, 0, 1.218), (1.29, 0.88, 0.038), ceramic, 0.045),
    ]
    for y, l in ((0.21, 0.73), (0.065, 0.89), (-0.08, 0.46)):
        components.append(
            box("Printed signal", (-0.11, y, 1.24), (l, 0.038, 0.009), graphite, 0.004)
        )
    components.append(
        box("Source tab", (0.46, -0.23, 1.243), (0.18, 0.16, 0.012), blue, 0.013)
    )
    for obj in components:
        obj.parent = packet
    motion(packet, "location", (x, 0, 0), (x + 2.03, 0, 0))
# A belt drive with a rotating index inside the front hub.
for x in (-6.03, 5.99):
    shaft("Drive flange", (x, -1.03, 0.91), (x, -1.13, 0.91), 0.19, graphite)
    shaft("Hub", (x, -1.12, 0.91), (x, -1.165, 0.91), 0.14, chrome)
    notch = box("Rotary index", (x, -1.17, 0.91), (0.19, 0.012, 0.035), graphite, 0.009)
    motion(notch, "rotation_euler", (0, 0, 0), (0, -2 * math.pi, 0))
softbox("Long silk", (-2, -4, 9), (0, 0, 1), 1650, (0.89, 0.94, 1), 10, 5)
softbox("White edge", (2, 5.5, 6), (0, 0, 1.3), 1800, (0.78, 0.87, 1), 11, 1.6)
softbox("Blue rim", (-6, 2.8, 3), (-2, 0, 1), 650, (0.05, 0.16, 1), 4, 2)
softbox("Return", (6, -3.2, 4), (4, 0, 1), 510, (0.58, 0.72, 1), 3, 3)
softbox("Scan light", (-0.15, 0, 2.32), (-0.15, 0, 1), 38, (0.05, 0.22, 1), 2.0, 1.8)
camera_data = bpy.data.cameras.new("Product camera")
camera = bpy.data.objects.new("Product camera", camera_data)
scene.collection.objects.link(camera)
target = Vector((0, 0, 1.34))
camera.location = (5.25, -19.5, 9.4)
camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
camera_data.type = "ORTHO"
camera_data.ortho_scale = 14.75
scene.camera = camera
if mode == "film":
    scene.render.filepath = str(output / "line-")
    bpy.ops.render.render(animation=True)
else:
    scene.frame_set(40)
    scene.render.filepath = str(output / "poster.png")
    bpy.ops.render.render(write_still=True)
