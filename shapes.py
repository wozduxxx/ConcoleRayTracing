from vector import *
from math import sqrt, acos

out_normal = Vector3()


class Shapes:
    '''Abstract shape class'''

    def __init__(self, ro: Vector3, rd: Vector3):
        self.ro = ro
        self.rd = rd


class Sphere(Shapes):
    '''Class calculates spheres'''

    def __init__(self, ro: Vector3, rd: Vector3, r: float):
        super().__init__(ro, rd)
        self.r = r

    def render_sphere(self) -> Vector3:
        '''sphere of size r'''
        b = dot(self.ro, self.rd)
        c = dot(self.ro, self.ro) - self.r ** 2
        h = b ** 2 - c

        if h < 0: return Vector3(-1, -1)
        h = sqrt(h)

        return Vector3(-b - h, -b + h)


class Cube(Shapes):
    '''Class calculates cubes'''

    def __init__(self, ro, rd, cube_size: Vector3):
        super().__init__(ro, rd)
        self.cube_size = cube_size

    def render_cube(self) -> Vector3:
        global out_normal
        m = Vector3(1, 1, 1) / (self.rd + Vector3(0, .0001, 0))
        n = m * self.ro
        k = Vector3(abs(m.x), abs(m.y), abs(m.z), ) * Vector3(self.cube_size, self.cube_size, self.cube_size)

        t1 = -n - k
        t2 = -n + k

        tn = max(max(t1.x, t1.y), t1.z)
        tf = min(min(t2.x, t2.y), t2.z)

        if tn > tf or tf < 0: return Vector3(-1, -1)

        yzx = Vector3(t1.y, t1.z, t1.x)
        zxy = Vector3(t1.z, t1.x, t1.y)

        out_normal = -self.rd.sign() * t1.step(yzx) * t1.step(zxy)

        return Vector3(tn, tf)


class Cylinder(Shapes):
    '''Class calculates infinite cylinder'''

    def __init__(self, ro, rd, cb: Vector3, ca: Vector3, cr: Vector3):
        super().__init__(ro, rd)
        self.cb = cb
        self.ca = ca
        self.cr = cr

    def render_cylinder(self) -> Vector3:
        oc = self.ro - self.cb
        card = dot(self.ca, self.rd)
        caoc = dot(self.ca, oc)

        a = 1.0 - card * card
        b = dot(oc, self.rd) - caoc * card
        c = dot(oc, oc) - caoc * caoc - self.cr * self.cr
        h = b * b - a * c

        if h < .0: return Vector3(-1.0, -1.0)

        h = sqrt(h)

        return Vector3(-b - h, -b + h) / Vector3(a, a, a)


class Capsule(Shapes):
    '''Class calculates capsule'''

    def __init__(self, ro, rd, pa: Vector3, pb: Vector3, ra: float):
        super().__init__(ro, rd)
        self.pa = pa
        self.pb = pb
        self.ra = ra

    def render_capsule(self) -> float:
        '''capsule defined by extremes pa and pb, and radius ra
            Note that only ONE of the two spherical caps is checked for intersections,
            which is a nice optimization'''
        ba = self.pb - self.pa
        oa = self.ro - self.pa
        baba = dot(ba, ba)
        bard = dot(ba, self.rd)
        baoa = dot(ba, oa)
        rdoa = dot(self.rd, oa)
        oaoa = dot(oa, oa)
        a = baba - bard * bard
        b = baba * rdoa - baoa * bard
        c = baba * oaoa - baoa * baoa - self.ra * self.ra * baba

        h = b * b - a * c

        if h >= .0:
            t = (-b - sqrt(h)) / a
            y = baoa + t * bard

            if .0 > y < baba: return t

            if y <= .0:
                oc = oa
            else:
                oc = self.ro - self.pb

            b = dot(self.rd, oc)
            c = dot(oc, oc) - self.ra * self.ra
            h = b * b - c

            if h > .0: return -b - sqrt(h)

        return -1.0


class Goursat(Shapes):
    '''Class calculates goursat'''

    def __init__(self, ro, rd, ka: float, kb: float):
        super().__init__(ro, rd)
        self.ka = ka
        self.kb = kb

    def render_goursat(self) -> float:
        po = 1.0
        rd2 = self.rd * self.rd
        rd3 = rd2 * self.rd
        ro2 = self.ro * self.ro
        ro3 = ro2 * self.ro

        k4 = dot(rd2, rd2)
        k3 = dot(self.ro, rd3)
        k2 = dot(ro2, rd2) - self.kb / 6.0
        k1 = dot(ro3, self.rd) - self.kb * dot(self.rd, self.ro) / 2.0
        k0 = dot(ro2, ro2) + self.ka - self.kb * dot(self.ro, self.ro)

        k3 /= k4
        k2 /= k4
        k1 /= k4
        k0 /= k4

        c2 = k2 - k3 ** 2
        c1 = k1 + k3 * (2.0 * k3 * k3 - 3.0 * k2)
        c0 = k0 + k3 * (k3 * (c2 + k2) * 3.0 - 4.0 * k1)

        if abs(c1) < 0.1 * abs(c2):
            po = -1.0
            tmp = k1
            k1 = k3
            k3 = tmp
            k0 = 1.0 / k0
            k1 = k1 * k0
            k2 = k2 * k0
            k3 = k3 * k0
            c2 = k2 - k3 * k3
            c1 = k1 + k3 * (2.0 * k3 * k3 - 3.0 * k2)
            c0 = k0 + k3 * (k3 * (c2 + k2) * 3.0 - 4.0 * k1)

        c0 /= 3.0
        Q = c2 * c2 + c0
        R = c2 * c2 * c2 - 3.0 * c0 * c2 + c1 * c1
        h = R * R - Q * Q * Q

        if h > 0.0: # 2 intersections
            h = sqrt(h)
            s = sign(R + h) * pow(abs(R + h), 1.0 / 3.0) # cube root
            u = sign(R - h) * pow(abs(R - h), 1.0 / 3.0) # cube root
            x = s + u + 4.0 * c2
            y = s - u
            ks = x * x + y * y * 3.0
            k = sqrt(ks)
            t = -0.5 * po * abs(y) * sqrt(6.0 / (k + x)) - 2.0 * c1 * (k + x) / (ks + x * k) - k3

            if po < 0.0: return 1.0/t
            else: return t

        sQ = sqrt(Q)
        w = sQ * cos(acos(-R / (sQ * Q)) / 3.0)
        d2 = -w - c2
        if d2 < 0.0: return -1.0 # no intersection
        d1 = sqrt(d2)
        h1 = sqrt(w - 2.0 * c2 + c1 / d1)
        h2 = sqrt(w - 2.0 * c2 - c1 / d1)

        t1 = -d1 - h1 - k3
        if po < 0: t1 = 1.0 / t1

        t2 = -d1 + h1 - k3
        if po < 0: t1 = 1.0 / t2

        t3 = d1 - h2 - k3
        if po < 0: t1 = 1.0 / t3

        t4 = d1 + h2 - k3
        if po < 0: t1 = 1.0 / t4

        t = 1e20
        if t1 > 0: t = t1
        if t2 > 0: t = min(t, t2)
        if t3 > 0: t = min(t, t3)
        if t4 > 0: t = min(t, t4)
        return t

    def goursat_normal(self, pos: Vector3) -> Vector3:
        gou_normal = Vector3(4.0, 4.0, 4.0) * pos * pos * pos - Vector3(2.0, 2.0, 2.0) * pos * Vector3(self.kb, self.kb, self.kb)
        return gou_normal.norm()


class Plane(Shapes):
    '''Class calculates plane'''

    def __init__(self, ro, rd, p: Vector3, w: float):
        super().__init__(ro, rd)
        self.p = p
        self.w = w

    def render_plane(self) -> float:
        return -(dot(self.ro, self.p) + self.w) / dot(self.rd, self.p)
