"""W04 노트북 공용 도우미 — 형상 모으기 · glb 내보내기 · 정적 렌더 · 3D 뷰어.

수업 내용이 아니라 '보여 주기'용 배관이다. 형상을 어떻게 만드는지는 각 노트북 본문에 있다.

* PartSet  : (부재 그룹, 재질) 별로 삼각형을 모아 trimesh Scene / .glb 로 만든다.
* box_vf   : 원점 + 세 변 벡터 → 상자 8점 12삼각형 (Blender build_model.py 의 box 와 같은 순서)
* render   : numpy z-버퍼 래스터라이저. OpenGL 없이 Colab CPU 에서 PNG 를 만든다.
* show_glb : <model-viewer> 로 노트북 안에서 돌려 보기 (glb 를 base64 로 심는다)
"""
from __future__ import annotations

import base64
import hashlib
import math

import numpy as np

# ---------------------------------------------------------------- 색


def hex_rgb(h: str, default=(0.75, 0.75, 0.75)) -> tuple[float, float, float]:
    h = (h or "").strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return default
    try:
        return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return default


# ---------------------------------------------------------------- 상자

_BOX_QUADS = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]


def box_vf(o, du, dv, dw):
    """o 에서 시작해 du·dv·dw 세 변을 갖는 평행육면체 → (V 8x3, F 12x3)."""
    o, du, dv, dw = (np.asarray(x, float) for x in (o, du, dv, dw))
    V = np.array([o, o + du, o + du + dv, o + dv, o + dw, o + du + dw, o + du + dv + dw, o + dv + dw])
    F = []
    for a, b, c, d in _BOX_QUADS:
        F += [(a, b, c), (a, c, d)]
    return V, np.array(F)


# ---------------------------------------------------------------- 부재 모음


class PartSet:
    """(그룹, 재질) → 삼각형 묶음. 같은 입력이면 같은 순서로 쌓이므로 결과도 같다."""

    def __init__(self):
        self.mats: dict[str, dict] = {}
        self.buf: dict[tuple[str, str], list] = {}
        self.calls = 0

    def material(self, name, color, roughness=0.6, metallic=0.0):
        self.mats[str(name)] = {"color": str(color), "roughness": float(roughness),
                                "metallic": float(metallic)}

    def add(self, group: str, mat: str, V, F):
        V = np.asarray(V, float)
        F = np.asarray(F, np.int64)
        if len(F) == 0:
            return
        if mat not in self.mats:
            self.material(mat, "#C9C4BA")
        key = (str(group), str(mat))
        b = self.buf.setdefault(key, [[], [], 0])
        b[0].append(V)
        b[1].append(F + b[2])
        b[2] += len(V)
        self.calls += 1

    # -- 통계
    def stats(self) -> dict:
        tris = sum(sum(len(f) for f in b[1]) for b in self.buf.values())
        groups = sorted({g for g, _ in self.buf})
        return {"parts": self.calls, "groups": len(groups), "materials": len({m for _, m in self.buf}),
                "triangles": int(tris), "nodes": len(self.buf)}

    def bounds(self):
        allv = [np.concatenate(b[0]) for b in self.buf.values() if b[0]]
        if not allv:
            return np.zeros(3), np.zeros(3)
        v = np.concatenate(allv)
        return v.min(0), v.max(0)

    # -- 내보내기
    def scene(self):
        import trimesh
        from trimesh.visual.material import PBRMaterial
        sc = trimesh.Scene()
        for (g, m), (Vs, Fs, _) in self.buf.items():
            mesh = trimesh.Trimesh(np.concatenate(Vs), np.concatenate(Fs), process=False)
            d = self.mats[m]
            r, gg, b = hex_rgb(d["color"])
            mesh.visual = trimesh.visual.TextureVisuals(material=PBRMaterial(
                name=m, baseColorFactor=[int(r * 255), int(gg * 255), int(b * 255), 255],
                metallicFactor=d["metallic"], roughnessFactor=d["roughness"], doubleSided=True))
            name = f"{g}__{m}"
            sc.add_geometry(mesh, node_name=name, geom_name=name)
        return sc

    def glb(self) -> bytes:
        """glTF 는 Y 가 위다. 우리 좌표(LOCAL_ENU: X 동, Y 북, Z 위)를 돌려서 내보낸다."""
        sc = self.scene()
        rot = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 1]], float)
        sc.apply_transform(rot)
        return sc.export(file_type="glb")

    def triangles(self):
        T, C = [], []
        for (g, m), (Vs, Fs, _) in self.buf.items():
            V = np.concatenate(Vs)
            F = np.concatenate(Fs)
            T.append(V[F])
            C.append(np.tile(hex_rgb(self.mats[m]["color"]), (len(F), 1)))
        if not T:
            return np.zeros((0, 3, 3)), np.zeros((0, 3))
        return np.concatenate(T), np.concatenate(C)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


# ---------------------------------------------------------------- 정적 렌더 (z-버퍼)


def render(parts: PartSet, size=(1280, 720), azim=215.0, elev=12.0, fov=28.0, margin=1.04,
           bg=(255, 255, 255), ground="#F0F1F3", target=None, supersample=1, light=None, edges=True):
    """PartSet → RGB uint8 이미지.

    azim: 카메라가 건물을 바라보는 '위치'의 방위각 (0 = 북쪽에서, 90 = 동쪽에서, 시계방향).
    """
    T, C = parts.triangles()
    W, H = size[0] * supersample, size[1] * supersample
    lo, hi = parts.bounds()
    if ground:
        cx, cy = (lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2
        R = max(hi[0] - lo[0], hi[1] - lo[1]) * 0.75 + 4
        g = np.array([[cx - R, cy - R, -0.02], [cx + R, cy - R, -0.02], [cx + R, cy + R, -0.02], [cx - R, cy + R, -0.02]])
        T = np.concatenate([T, g[[[0, 1, 2], [0, 2, 3]]]])
        C = np.concatenate([C, np.tile(hex_rgb(ground), (2, 1))])
    tgt = np.asarray(target if target is not None else (lo + hi) / 2, float)
    rad = np.linalg.norm(hi - lo) / 2
    a, e = math.radians(azim), math.radians(elev)
    back = np.array([math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)])
    fpx = (H / 2) / math.tan(math.radians(fov) / 2)
    # 화면 비율이 넓으면 세로 시야가 기준이 된다
    dist = rad * margin / math.sin(math.radians(fov) / 2)
    eye = tgt + back * dist
    f = -back
    r = np.cross(f, [0, 0, 1.0])
    r /= np.linalg.norm(r)
    u = np.cross(r, f)

    P = T - eye
    x, y, z = P @ r, P @ u, P @ f
    keep = (z > 0.5).all(1)
    x, y, z, T, C = x[keep], y[keep], z[keep], T[keep], C[keep]
    sx = W / 2 + fpx * x / z
    sy = H / 2 - fpx * y / z

    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    nl = np.linalg.norm(n, axis=1)
    ok = nl > 1e-12
    n[ok] /= nl[ok, None]
    view = eye - T.mean(1)
    flip = (n * view).sum(1) < 0
    n[flip] *= -1
    # 빛은 카메라 왼쪽 위에서 — 보이는 두 면이 서로 다른 밝기로 나뉘게
    L = np.asarray(light, float) if light is not None else (back * 0.55 - r * 0.6 + np.array([0, 0, 0.9]))
    L /= np.linalg.norm(L)
    lam = np.clip(n @ L, 0, 1)
    sky = 0.5 * (n[:, 2] + 1)
    shade = 0.42 + 0.48 * lam + 0.16 * sky
    col = np.clip(C * shade[:, None], 0, 1)

    img = np.empty((H, W, 3), np.float32)
    img[:] = np.asarray(bg, np.float32) / 255
    zb = np.full((H, W), np.inf, np.float32)
    ib = np.full((H, W), -1, np.int32)

    x0 = np.clip(np.floor(sx.min(1)).astype(int), 0, W)
    x1 = np.clip(np.ceil(sx.max(1)).astype(int) + 1, 0, W)
    y0 = np.clip(np.floor(sy.min(1)).astype(int), 0, H)
    y1 = np.clip(np.ceil(sy.max(1)).astype(int) + 1, 0, H)
    for i in np.nonzero((x1 > x0) & (y1 > y0))[0]:
        ax_, ay_, bx_, by_, cx_, cy_ = sx[i, 0], sy[i, 0], sx[i, 1], sy[i, 1], sx[i, 2], sy[i, 2]
        den = (by_ - cy_) * (ax_ - cx_) + (cx_ - bx_) * (ay_ - cy_)
        if abs(den) < 1e-9:
            continue
        gy, gx = np.mgrid[y0[i]:y1[i], x0[i]:x1[i]]
        px, py = gx + 0.5, gy + 0.5
        w0 = ((by_ - cy_) * (px - cx_) + (cx_ - bx_) * (py - cy_)) / den
        w1 = ((cy_ - ay_) * (px - cx_) + (ax_ - cx_) * (py - cy_)) / den
        w2 = 1 - w0 - w1
        inside = (w0 >= -1e-4) & (w1 >= -1e-4) & (w2 >= -1e-4)
        if not inside.any():
            continue
        zz = 1.0 / (w0 / z[i, 0] + w1 / z[i, 1] + w2 / z[i, 2])     # 원근 보정 깊이
        sub = zb[y0[i]:y1[i], x0[i]:x1[i]]
        m = inside & (zz < sub)
        sub[m] = zz[m]
        img[y0[i]:y1[i], x0[i]:x1[i]][m] = col[i]
        ib[y0[i]:y1[i], x0[i]:x1[i]][m] = i
    if edges:
        # 모서리 선: 깊이가 튀거나(윤곽) 면 방향이 꺾이는(주름) 픽셀을 어둡게
        e = np.zeros((H, W), bool)
        for a_, b_ in (((slice(None), slice(0, -1)), (slice(None), slice(1, None))),
                       ((slice(0, -1), slice(None)), (slice(1, None), slice(None)))):
            ia, ibb = ib[a_], ib[b_]
            za, zbb = zb[a_], zb[b_]
            both = (ia >= 0) & (ibb >= 0)
            jump = ~both & ((ia >= 0) | (ibb >= 0))
            zz = np.zeros_like(both)
            zz[both] = np.abs(za[both] - zbb[both]) / np.minimum(za[both], zbb[both]) > 0.012
            crease = both & ((n[np.maximum(ia, 0)] * n[np.maximum(ibb, 0)]).sum(-1) < 0.9)
            e[a_] |= jump | zz | crease
        img[e] *= 0.55
    out = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    if supersample > 1:
        from PIL import Image
        out = np.asarray(Image.fromarray(out).resize(size, Image.LANCZOS))
    return out


# ---------------------------------------------------------------- 3D 뷰어


def show_glb(glb: bytes, height: int = 520, note: str = ""):
    """노트북 안에 돌려 볼 수 있는 3D 뷰어. 인터넷이 없으면 빈 칸으로 보인다(정적 렌더를 함께 볼 것)."""
    from IPython.display import HTML, display
    b64 = base64.b64encode(glb).decode()
    display(HTML(
        '<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js"></script>'
        f'<model-viewer src="data:model/gltf-binary;base64,{b64}" camera-controls auto-rotate '
        'shadow-intensity="1" exposure="1.05" camera-orbit="225deg 75deg auto" '
        f'style="width:100%;height:{height}px;background:#f3f4f6;border-radius:8px"></model-viewer>'
        + (f'<div style="font-size:12px;color:#666">{note}</div>' if note else "")))
