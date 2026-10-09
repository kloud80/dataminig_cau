mat("midnight_glass", "#253e4a", kind="glass", roughness=0.19, metallic=0.42)
mat("blue_glass", "#416779", kind="glass", roughness=0.17, metallic=0.38)
mat("blue_glass_light", "#537c89", kind="glass", roughness=0.18, metallic=0.35)
mat("circle_glass", "#729699", kind="glass", roughness=0.18, metallic=0.4)
mat("circle_glass_light", "#84a7a8", kind="glass", roughness=0.2, metallic=0.35)
mat("circle_glass_dark", "#628489", kind="glass", roughness=0.17, metallic=0.42)
mat("rear_glass", "#44798e", kind="glass", roughness=0.16, metallic=0.3)
mat("rear_spandrel", "#67868e", kind="glass", roughness=0.25, metallic=0.32)
mat("entrance_glass", "#679397", kind="storefront_glass", roughness=0.16)
mat("dark_frame", "#293b41", kind="frame", roughness=0.32, metallic=0.65)
mat("aluminium", "#b8c4c6", kind="metal", roughness=0.3, metallic=0.72)
mat("silver_cladding", "#d3dadb", kind="metal_panel", unit=[1.25, 1.05], accent="#9eabad", roughness=0.34, metallic=0.45)
mat("silver_band", "#c5d0d1", kind="metal_panel", unit=[1.4, 0.65], accent="#a2afb1", roughness=0.31, metallic=0.5)
mat("ring_face", "#bbc5c5", kind="metal_panel", unit=[1.1, 1.0], accent="#9ca7a8", roughness=0.32, metallic=0.65)
mat("ring_edge", "#68777b", kind="metal", roughness=0.36, metallic=0.6)
mat("burgundy", "#873f50", kind="metal_panel", unit=[1.05, 1.0], accent="#6c3041", roughness=0.35, metallic=0.4)
mat("burgundy_side", "#492b36", kind="metal", roughness=0.4, metallic=0.5)
mat("red_wire", "#8a4554", kind="metal", roughness=0.37, metallic=0.55)
mat("art_steel", "#354348", kind="metal", roughness=0.36, metallic=0.65)
mat("louvre_dark", "#515b60", kind="metal", roughness=0.4, metallic=0.5)
mat("louvre_blade", "#8f9b9e", kind="metal", roughness=0.35, metallic=0.62)
mat("paving", "#858d8d", kind="stone", unit=[0.8, 0.8], accent="#636c6c", roughness=0.75)
mat("roof", "#545e5c", kind="concrete", roughness=0.9)
mat("equipment", "#b5bbb7", kind="metal_panel", unit=[1.0, 1.0], accent="#89938f", roughness=0.5, metallic=0.3)
mat("fan_dark", "#333f3d", kind="metal", roughness=0.65)
mat("white_letters", "#f2f0df", kind="sign", roughness=0.4)
mat("logo_blue", "#23a5ce", kind="sign", roughness=0.35)
mat("logo_green", "#80bd45", kind="sign", roughness=0.4)
mat("planting", "#425744", kind="plaster", roughness=1.0)
mat("planting_light", "#5b6e4d", kind="plaster", roughness=1.0)

# The long southwest elevation is the local u axis.
length = (28.88 * 28.88 + 63.61 * 63.61) ** 0.5
ex = 28.88 / length
ey = -63.61 / length
vx = -ey
vy = ex
rotation = -65.58

def point(u, v, z=0):
    return [-22.13 + ex * u + vx * v, 25.91 + ey * u + vy * v, z]

def local_box(u, v, z, w, d, h, material, turn=0):
    p = point(u, v)
    box(p[0], p[1], z, w, d, h, material, rot=rotation + turn)

def local_prism(ring, z0, z1, material):
    world = []
    for a in ring:
        p = point(a[0], a[1])
        world.append([p[0], p[1]])
    prism(world, z0, z1, material)

def front_quad(u0, u1, z0, z1, v, material):
    quad(point(u0, v, z0), point(u1, v, z0),
         point(u1, v, z1), point(u0, v, z1), material)

def rod(u0, v0, z0, u1, v1, z1, radius, material):
    a = point(u0, v0, z0)
    b = point(u1, v1, z1)
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    dz = b[2] - a[2]
    h = (dx * dx + dy * dy + dz * dz) ** 0.5
    cyl(a[0], a[1], a[2], radius, h, material, seg=12,
        axis=[dx / h, dy / h, dz / h])

def art_beam(u0, z0, u1, z1, width, v, depth, material):
    du = u1 - u0
    dz = z1 - z0
    h = (du * du + dz * dz) ** 0.5
    pu = -dz * width / (2 * h)
    pz = du * width / (2 * h)
    corners = [[u0 + pu, z0 + pz], [u1 + pu, z1 + pz],
               [u1 - pu, z1 - pz], [u0 - pu, z0 - pz]]
    front = []
    back = []
    for c in corners:
        front.append(point(c[0], v, c[1]))
        back.append(point(c[0], v + depth, c[1]))
    quad(front[0], front[1], front[2], front[3], material)
    quad(back[3], back[2], back[1], back[0], material)
    for i in range(4):
        j = (i + 1) % 4
        quad(front[i], back[i], back[j], front[j], material)

def edge_length(a, b):
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5

def edge_point(a, b, s, out, z):
    ln = edge_length(a, b)
    tu = (b[0] - a[0]) / ln
    tv = (b[1] - a[1]) / ln
    return point(a[0] + tu * s + tv * out,
                 a[1] + tv * s - tu * out, z)

def panel(a, b, s0, s1, z0, z1, out, depth, material):
    ln = edge_length(a, b)
    tu = (b[0] - a[0]) / ln
    tv = (b[1] - a[1]) / ln
    ring = []
    for s, t in [[s0, out], [s1, out], [s1, out - depth], [s0, out - depth]]:
        ring.append([a[0] + tu * s + tv * t, a[1] + tv * s - tu * t])
    local_prism(ring, z0, z1, material)

def edge_glass(a, b, s0, s1, z0, z1, out, material):
    quad(edge_point(a, b, s0, out, z0), edge_point(a, b, s1, out, z0),
         edge_point(a, b, s1, out, z1), edge_point(a, b, s0, out, z1), material)

def front_text(s, u, v, z, height, material):
    p = point(u, v, z)
    text(s, p[0], p[1], p[2], height, material, rot=rotation, depth=0.035)

parcel = [[-22.13, 25.91], [6.75, -37.70], [16.46, -33.36],
          [16.12, -28.27], [16.62, -28.15], [14.17, -22.24],
          [16.09, -21.36], [16.16, -11.08], [-2.14, 32.02],
          [-6.25, 30.46], [-7.08, 32.28]]

# The glazing sits behind the parcel-edge plinth, leaving room for the applied artwork.
upper = [[0.05, 1.25], [69.76, 1.25], [69.78, 10.46],
         [65.15, 12.26], [65.12, 12.78], [58.73, 13.00],
         [58.72, 15.07], [49.38, 19.39], [2.84, 20.51],
         [2.56, 16.15], [0.62, 16.15]]

group("01_SURVEY_PLINTH")
prism(parcel, 0, 0.46, "paving")
local_prism(upper, 0.46, 92.72, "midnight_glass")

floors = [0.50]
for i in range(15):
    floors.append(8.0 + 6.0 * i)

front_levels = [0.50, 4.10, 8.0]
for i in range(14):
    front_levels.append(11.0 + 6.0 * i)
    front_levels.append(14.0 + 6.0 * i)
front_levels.append(94.0)

group("02_SOUTHWEST_CONTINUOUS_CURTAIN_WALL")
start_u = 0.12
end_u = 69.70
pane_w = (end_u - start_u) / 42
for row in range(len(front_levels) - 1):
    z0 = front_levels[row]
    z1 = front_levels[row + 1]
    zm = (z0 + z1) / 2
    for col in range(42):
        u0 = start_u + col * pane_w
        u1 = u0 + pane_w
        um = (u0 + u1) / 2
        pattern = (col * 7 + row * 3) % 13
        in_circle = (um - 39.0) ** 2 + (zm - 61.9) ** 2 < 29.2 ** 2
        material = "blue_glass"
        if um < 23.0 or zm < 20.0:
            material = "midnight_glass"
        elif pattern > 9:
            material = "blue_glass_light"
        if in_circle:
            material = "circle_glass"
            if pattern == 0 or pattern == 7:
                material = "circle_glass_light"
            elif pattern == 4:
                material = "circle_glass_dark"
        front_quad(u0 + 0.028, u1 - 0.028, z0 + 0.035, z1 - 0.035,
                   1.185, material)

for col in range(43):
    u = start_u + col * pane_w
    local_box(u, 1.12, 0.5, 0.052, 0.13, 93.5, "dark_frame")
for z in front_levels:
    local_box((start_u + end_u) / 2, 1.10, z - 0.028,
              end_u - start_u, 0.17, 0.056, "dark_frame")
for z in floors[1:]:
    local_box(34.91, 1.085, z - 0.07, 69.58, 0.19, 0.14, "dark_frame")
local_box(34.91, 1.12, 93.94, 69.62, 0.28, 0.16, "aluminium")
local_box(0.16, 1.09, 0.5, 0.15, 0.23, 93.5, "aluminium")
local_box(69.66, 1.09, 0.5, 0.15, 0.23, 93.5, "aluminium")

group("03_TANGRAM_PROJECTING_RED_FORMS")
red_forms = [
    [29.2, 81.7, 5.1, 4.0],
    [41.9, 81.0, 2.6, 3.1],
    [53.0, 79.7, 2.7, 3.0],
    [31.4, 72.2, 3.0, 4.1],
    [46.7, 69.5, 3.3, 3.8],
    [58.0, 68.3, 3.1, 3.2],
    [33.1, 61.3, 3.2, 4.9],
    [49.2, 58.0, 3.6, 4.1]
]
for u, z, w, h in red_forms:
    local_box(u, 0.72, z, w, 0.90, h, "burgundy_side")
    local_box(u, 0.235, z + 0.08, w, 0.08, h - 0.08, "burgundy")
    local_box(u, 0.28, z + h - 0.06, w + 0.12, 0.35, 0.13, "burgundy")
front_text("HDC", 29.2, 0.18, 83.35, 1.43, "white_letters")

art_beam(14.1, 45.4, 63.9, 45.4, 1.30, 0.16, 0.85, "burgundy")
local_box(60.2, 0.68, 53.0, 7.5, 0.95, 6.0, "ring_edge")
local_box(60.2, 0.175, 53.12, 7.3, 0.08, 5.82, "silver_cladding")
for u in [57.8, 60.2, 62.6]:
    local_box(u, 0.125, 53.13, 0.045, 0.07, 5.8, "ring_edge")
local_box(60.2, 0.125, 56.02, 7.3, 0.07, 0.045, "ring_edge")

group("04_SUSPENDED_WOVEN_METAL_ARTWORK")
outline = [[17.4, 76.7], [45.8, 69.5], [58.5, 42.6], [31.6, 34.8]]
for i in range(4):
    j = (i + 1) % 4
    art_beam(outline[i][0], outline[i][1], outline[j][0], outline[j][1],
             0.15, 0.50, 0.17, "art_steel")

for i in range(34):
    u0 = 17.6 + i * 0.85
    z0 = 76.5 - i * 0.21
    u1 = 31.8 + i * 0.80
    z1 = 35.0 + i * 0.23
    rod(u0, 0.35, z0, u1, 0.35, z1, 0.047, "red_wire")
    if i % 4 == 0:
        rod(u0, 0.37, z0, u0, 1.15, z0, 0.052, "art_steel")
        rod(u1, 0.37, z1, u1, 1.15, z1, 0.052, "art_steel")

for i in range(22):
    u0 = 18.0 + i * 0.56
    z0 = 75.2 - i * 1.85
    u1 = 45.0 + i * 0.57
    z1 = 69.0 - i * 1.24
    art_beam(u0, z0, u1, z1, 0.075, 0.57, 0.14, "art_steel")

for i in range(8):
    u = 21.0 + 4.2 * i
    rod(u, 0.38, 45.3, u, 1.17, 45.3, 0.10, "art_steel")

art_beam(16.5, 54.0, 48.2, 73.1, 0.48, 0.10, 0.36, "aluminium")
art_beam(23.7, 36.4, 55.1, 67.7, 0.52, 0.075, 0.39, "aluminium")
art_beam(19.0, 79.0, 62.2, 74.3, 0.62, 0.08, 0.39, "aluminium")
art_beam(22.2, 58.1, 53.4, 66.1, 0.18, 0.42, 0.18, "art_steel")

group("05_GIANT_CIRCULAR_SILVER_FRAME")
cu = 39.0
cz = 61.9
outer_radius = 30.15
inner_radius = 29.12
co = 1.0
si = 0.0
step_cos = 0.9987954562
step_sin = 0.0490676743
for i in range(128):
    nc = co * step_cos - si * step_sin
    ns = si * step_cos + co * step_sin
    outer0 = [cu + outer_radius * co, cz + outer_radius * si]
    outer1 = [cu + outer_radius * nc, cz + outer_radius * ns]
    inner0 = [cu + inner_radius * co, cz + inner_radius * si]
    inner1 = [cu + inner_radius * nc, cz + inner_radius * ns]
    quad(point(outer0[0], 0.025, outer0[1]), point(outer1[0], 0.025, outer1[1]),
         point(inner1[0], 0.025, inner1[1]), point(inner0[0], 0.025, inner0[1]), "ring_face")
    quad(point(outer0[0], 0.025, outer0[1]), point(outer0[0], 0.96, outer0[1]),
         point(outer1[0], 0.96, outer1[1]), point(outer1[0], 0.025, outer1[1]), "ring_edge")
    quad(point(inner1[0], 0.025, inner1[1]), point(inner1[0], 0.96, inner1[1]),
         point(inner0[0], 0.96, inner0[1]), point(inner0[0], 0.025, inner0[1]), "ring_edge")
    if i % 4 == 0:
        rod(inner0[0], 0.018, inner0[1], outer0[0], 0.018, outer0[1],
            0.017, "ring_edge")
    if i % 8 == 0:
        bu = cu + 29.63 * co
        bz = cz + 29.63 * si
        p = point(bu, 0.012, bz)
        cyl(p[0], p[1], p[2], 0.065, 0.035, "aluminium", seg=12,
            axis=[vx, vy, 0])
        rod(bu, 0.85, bz, bu, 1.24, bz, 0.17, "ring_edge")
    co = nc
    si = ns

group("06_NORTHEAST_OFFICE_ELEVATION")
a = upper[7]
b = upper[8]
rear_len = edge_length(a, b)
core_start = 34.1
panel(a, b, core_start, rear_len, 0.5, 94.1, 0.09, 0.25, "silver_cladding")

for floor in range(15):
    z0 = floors[floor]
    z1 = floors[floor + 1]
    panel(a, b, 0, core_start, z0, z0 + 0.65, 0.13, 0.31, "silver_band")
    panel(a, b, 0, core_start, z1 - 0.16, z1, 0.15, 0.32, "aluminium")
    for bay in range(5):
        s0 = 2.65 + bay * 6.29
        s1 = s0 + 6.29
        edge_glass(a, b, s0 + 0.36, s1 - 0.36, z0 + 0.68, z1 - 0.18,
                   -0.08, "rear_glass")
        edge_glass(a, b, s0 + 0.36, s1 - 0.36, z0 + 0.68, z0 + 1.45,
                   -0.065, "rear_spandrel")
        panel(a, b, s0, s0 + 0.67, z0 + 0.64, z1, 0.12, 0.29, "silver_cladding")
        for k in range(1, 4):
            s = s0 + 0.36 + (6.29 - 0.72) * k / 4
            panel(a, b, s - 0.032, s + 0.032, z0 + 0.67, z1 - 0.17,
                  0.0, 0.14, "aluminium")
        zm = z0 + (z1 - z0) * 0.62
        panel(a, b, s0 + 0.35, s1 - 0.35, zm, zm + 0.065, 0.0, 0.13, "aluminium")
    panel(a, b, 0.0, 0.40, z0, z1, 0.12, 0.28, "silver_band")
    edge_glass(a, b, 0.45, 2.6, z0 + 0.67, z1 - 0.18, -0.07, "rear_glass")
    panel(a, b, 1.48, 1.54, z0 + 0.67, z1 - 0.18, 0.0, 0.14, "aluminium")
    edge_glass(a, b, 39.10, 40.15, z0 + 3.08, z0 + 3.88, 0.105, "midnight_glass")
    panel(a, b, 39.08, 40.17, z0 + 3.05, z0 + 3.14, 0.15, 0.11, "aluminium")

edge_glass(a, b, 43.22, 44.25, 5.5, 86.3, 0.11, "rear_glass")
for z in floors[1:-1]:
    panel(a, b, 43.20, 44.27, z - 0.12, z + 0.12, 0.15, 0.1, "silver_band")
panel(a, b, 0, core_start, 92.0, 93.0, 0.10, 0.24, "silver_band")
p = edge_point(a, b, 36.0, 0.18, 88.4)
text("HDC", p[0], p[1], p[2], 1.30, "burgundy", rot=113.0, depth=0.07, align="LEFT")
p = edge_point(a, b, 39.35, 0.18, 88.50)
text("현대산업개발", p[0], p[1], p[2], 0.76, "white_letters", rot=113.0, depth=0.06, align="LEFT")

group("07_REAR_CHAMFER_LOUVRE_BANK")
a = upper[6]
b = upper[7]
ln = edge_length(a, b)
for floor in range(15):
    z0 = floors[floor]
    z1 = floors[floor + 1]
    panel(a, b, 0, ln, z0, z0 + 0.63, 0.11, 0.29, "silver_band")
    panel(a, b, 0.15, ln - 0.15, z0 + 0.67, z1 - 0.1, -0.07, 0.12, "louvre_dark")
    count = 28
    pitch = (z1 - z0 - 0.90) / count
    for j in range(count):
        z = z0 + 0.77 + j * pitch
        panel(a, b, 0.20, ln - 0.20, z, z + 0.065, 0.055, 0.20, "louvre_blade")
    for j in range(5):
        s = 0.13 + (ln - 0.26) * j / 4
        panel(a, b, s - 0.05, s + 0.05, z0 + 0.64, z1,
              0.10, 0.22, "aluminium")
panel(a, b, 0, ln, 92.0, 94.1, 0.06, 0.23, "silver_cladding")

group("08_SOUTHEAST_NARROW_GLAZED_END")
a = upper[1]
b = upper[2]
ln = edge_length(a, b)
split = 3.0
for floor in range(15):
    z0 = floors[floor]
    z1 = floors[floor + 1]
    edge_glass(a, b, 0.04, split - 0.12, z0 + 0.04, z1 - 0.04, 0.025, "blue_glass")
    panel(a, b, 1.46, 1.52, z0, z1, 0.11, 0.16, "aluminium")
    panel(a, b, 0, split, z1 - 0.075, z1 + 0.015, 0.12, 0.17, "dark_frame")
    panel(a, b, split, ln, z0, z0 + 0.67, 0.19, 0.37, "silver_band")
    panel(a, b, split, split + 0.38, z0 + 0.65, z1, 0.16, 0.36, "silver_cladding")
    panel(a, b, ln - 0.65, ln, z0 + 0.65, z1, 0.16, 0.36, "silver_cladding")
    edge_glass(a, b, split + 0.40, ln - 0.67, z0 + 0.70, z1 - 0.12,
               -0.045, "rear_glass")
    for j in range(1, 3):
        s = split + 0.4 + (ln - split - 1.07) * j / 3
        panel(a, b, s - 0.035, s + 0.035, z0 + 0.69, z1 - 0.10,
              0.03, 0.16, "aluminium")
    zm = z0 + (z1 - z0) * 0.59
    panel(a, b, split + 0.39, ln - 0.65, zm, zm + 0.075, 0.03, 0.16, "aluminium")
panel(a, b, split - 0.1, split + 0.10, 0.5, 94.1, 0.20, 0.29, "aluminium")
panel(a, b, 0, ln, 92.0, 94.1, 0.08, 0.22, "silver_cladding")

for label, z, ht in [["MetLife", 8.14, 0.49], ["하나은행", 20.13, 0.36], ["DIGNITY", 26.12, 0.40]]:
    p = edge_point(a, b, 5.7, 0.28, z)
    text(label, p[0], p[1], p[2], ht, "white_letters", rot=24.3, depth=0.04)
p = edge_point(a, b, 7.85, 0.28, 8.20)
text("강남고객플라자", p[0], p[1], p[2], 0.23, "white_letters", rot=24.3, depth=0.025)
panel(a, b, 3.85, 4.26, 8.15, 8.78, 0.28, 0.06, "logo_blue")
panel(a, b, 4.27, 4.64, 8.15, 8.78, 0.28, 0.06, "logo_green")

group("09_STEPPED_SERVICE_RETURN")
for edge in [2, 3, 4, 5, 8, 9]:
    a = upper[edge]
    b = upper[(edge + 1) % len(upper)]
    ln = edge_length(a, b)
    panel(a, b, 0, ln, 0.5, 94.1, 0.08, 0.24, "silver_cladding")
    if ln > 3.0:
        for floor in range(15):
            z0 = floors[floor]
            z1 = floors[floor + 1]
            s0 = ln * 0.37
            s1 = ln * 0.67
            edge_glass(a, b, s0, s1, z0 + 2.1, z0 + 3.15, 0.095, "midnight_glass")
            panel(a, b, s0 - 0.035, s1 + 0.035, z0 + 2.05, z0 + 2.14,
                  0.16, 0.11, "aluminium")
            if edge == 4:
                panel(a, b, 0.20, ln - 0.20, z0 + 0.70, z1 - 0.15,
                      0.095, 0.12, "louvre_dark")
                for j in range(20):
                    z = z0 + 0.80 + (z1 - z0 - 1.0) * j / 20
                    panel(a, b, 0.22, ln - 0.22, z, z + 0.07,
                          0.18, 0.15, "louvre_blade")
                panel(a, b, 0, ln, z0, z0 + 0.63, 0.19, 0.25, "silver_band")

group("10_NORTHWEST_CORE_AND_GLASS_RETURN")
a = upper[10]
b = upper[0]
ln = edge_length(a, b)
panel(a, b, 0, 9.6, 0.5, 94.1, 0.10, 0.29, "silver_cladding")
edge_glass(a, b, 6.6, 7.47, 5.0, 86.0, 0.12, "blue_glass")
for z in floors[1:-1]:
    panel(a, b, 6.58, 7.49, z - 0.14, z + 0.14, 0.16, 0.13, "silver_band")
for row in range(len(front_levels) - 1):
    z0 = front_levels[row]
    z1 = front_levels[row + 1]
    for j in range(4):
        s0 = 9.6 + (ln - 9.6) * j / 4
        s1 = 9.6 + (ln - 9.6) * (j + 1) / 4
        edge_glass(a, b, s0 + 0.025, s1 - 0.025, z0 + 0.025, z1 - 0.025,
                   0.04, "midnight_glass")
        panel(a, b, s0 - 0.027, s0 + 0.027, z0, z1, 0.12, 0.14, "dark_frame")
    panel(a, b, 9.6, ln, z0, z0 + 0.055, 0.12, 0.13, "dark_frame")
panel(a, b, 9.50, 9.67, 0.5, 94.1, 0.16, 0.25, "aluminium")
p = edge_point(a, b, 4.5, 0.20, 88.4)
text("HDC 현대산업개발", p[0], p[1], p[2], 0.72, "white_letters",
     rot=-157.8, depth=0.055)

group("11_FRONT_TENANT_IDENTIFICATION")
front_text("MetLife", 8.0, 1.005, 14.0, 0.86, "white_letters")
front_quad(4.15, 4.95, 14.0, 15.05, 1.005, "logo_blue")
front_quad(5.02, 5.80, 14.0, 15.05, 1.005, "logo_green")
front_text("MetLife", 7.5, 1.005, 90.7, 0.93, "white_letters")
front_quad(3.1, 3.93, 90.7, 91.8, 1.005, "logo_blue")
front_quad(4.00, 4.80, 90.7, 91.8, 1.005, "logo_green")

group("12_GROUND_GLAZING_AND_RECESSED_ACCESS")
for u in [46.1, 47.7, 49.3, 50.9]:
    front_quad(u, u + 1.48, 0.53, 4.5, 1.07, "entrance_glass")
    local_box(u, 1.015, 0.53, 0.075, 0.16, 3.99, "aluminium")
    local_box(u + 0.75, 0.98, 1.45, 0.042, 0.07, 0.82, "aluminium")
local_box(49.1, 1.00, 4.48, 6.25, 0.20, 0.17, "aluminium")
local_box(49.0, 0.66, 4.72, 8.0, 1.17, 0.16, "silver_band")
local_box(49.0, 0.66, 4.87, 7.68, 1.05, 0.055, "entrance_glass")

for u in range(54, 70, 2):
    rod(u, 0.24, 0.48, u, 0.24, 1.54, 0.036, "aluminium")
rod(53.5, 0.24, 1.54, 69.3, 0.24, 1.54, 0.045, "aluminium")
rod(53.5, 0.24, 1.04, 69.3, 0.24, 1.04, 0.028, "aluminium")
for u in range(54, 68, 2):
    front_quad(u + 0.08, u + 1.92, 0.66, 1.42, 0.27, "entrance_glass")

group("13_MAIN_ROOF_AND_COPINGS")
local_prism(upper, 92.72, 92.91, "roof")
for i in range(len(upper)):
    a = upper[i]
    b = upper[(i + 1) % len(upper)]
    ln = edge_length(a, b)
    if i != 0:
        panel(a, b, 0, ln, 92.91, 94.02, -0.08, 0.22, "silver_cladding")
        panel(a, b, 0, ln, 94.02, 94.10, 0.025, 0.39, "aluminium")
    else:
        panel(a, b, 0, ln, 93.99, 94.10, -0.01, 0.30, "aluminium")

group("14_ROOFTOP_MECHANICAL_RACKS")
for u, v, w, d in [[15.8, 13.7, 17.0, 5.9], [45.0, 11.2, 16.0, 5.4]]:
    local_box(u, v, 92.92, w + 0.6, d + 0.6, 0.18, "silver_band")
    local_box(u, v, 93.10, w, d, 0.72, "equipment")
    local_box(u, v, 93.80, w + 0.12, d + 0.12, 0.12, "aluminium")
    for k in range(6):
        local_box(u, v - d / 2 - 0.015, 93.19 + k * 0.09,
                  w - 0.3, 0.07, 0.035, "louvre_dark")
        local_box(u, v + d / 2 + 0.015, 93.19 + k * 0.09,
                  w - 0.3, 0.07, 0.035, "louvre_dark")
    for row in range(2):
        for k in range(5):
            fu = u - w * 0.39 + k * w * 0.195
            fv = v - 1.3 + row * 2.6
            p = point(fu, fv)
            cyl(p[0], p[1], 93.92, 0.78, 0.17, "aluminium", seg=24)
            cyl(p[0], p[1], 94.085, 0.66, 0.028, "fan_dark", seg=24)
            cyl(p[0], p[1], 94.11, 0.15, 0.085, "equipment", seg=16)
            local_box(fu, fv, 94.125, 1.20, 0.09, 0.045, "louvre_blade", turn=30)
            local_box(fu, fv, 94.125, 1.20, 0.09, 0.045, "louvre_blade", turn=120)

local_box(30.0, 14.5, 92.92, 4.5, 3.2, 0.72, "equipment")
local_box(30.0, 14.5, 93.64, 4.65, 3.35, 0.12, "aluminium")
for k in range(8):
    local_box(30.0, 12.875, 93.03 + 0.067 * k, 4.10, 0.07, 0.031, "louvre_dark")
rod(24.6, 16.7, 93.15, 36.7, 16.7, 93.15, 0.14, "equipment")
rod(36.7, 16.7, 93.15, 36.7, 11.7, 93.15, 0.14, "equipment")
for u in [25.0, 29.0, 33.0, 36.0]:
    local_box(u, 16.7, 92.93, 0.22, 0.60, 0.21, "aluminium")

group("15_ROOF_FRONT_TERRACE_STRIPS")
for u, w in [[11.0, 9.0], [27.0, 8.0], [48.0, 10.0]]:
    local_box(u, 4.2, 92.92, w, 2.3, 0.30, "paving")
    local_box(u, 4.2, 93.22, w - 0.28, 2.02, 0.10, "planting")
    for k in range(4):
        local_box(u - w * 0.33 + k * w * 0.22, 4.25, 93.29,
                  w * 0.19, 1.55, 0.22 + 0.06 * (k % 2),
                  "planting_light" if k % 2 == 0 else "planting")
local_box(62.8, 5.9, 92.93, 4.1, 2.7, 0.20, "silver_band")
local_box(62.8, 5.9, 93.13, 3.55, 2.2, 0.42, "equipment")
local_box(62.8, 5.9, 93.55, 3.75, 2.4, 0.09, "aluminium")