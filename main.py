import time
import keyboard

import shapes
from vector import *


class DrawFrames:
    '''Class rendering the frame'''

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen = [str(i) for i in range(self.width * self.height)]
        self.aspect = width / height
        self.pixel_aspect = 11 / 24
        self.gradient = " .:!/r(l1Z4H9W8$@"
        self.gradient_size = len(self.gradient) - 1
        self.light = Vector3(-.5, .5, -1).norm()

    def draw_frame(self, frame_num) -> str:
        start_time = time.perf_counter()
        '''Method renders the frame'''
        # self.screen[self.width * self.height] = '\0'
        global da
        global ws
        global ud
        global rotz
        global roty

        frame = ''
        sphere_pos1 = Vector3(0, 4, 0)
        sphere_pos2 = Vector3(0, -1.75, 0)

        if keyboard.is_pressed('w'):
            ws += .2
        elif keyboard.is_pressed('s'):
            ws -= .2

        if keyboard.is_pressed('a'):
            da -= .2
        elif keyboard.is_pressed('d'):
            da += .2

        if keyboard.is_pressed('shift'):
            ud += .2
        elif keyboard.is_pressed('space'):
            ud -= .2

        if keyboard.is_pressed('4'):
            rotz += .1
        elif keyboard.is_pressed('6'):
            rotz -= .1

        if keyboard.is_pressed('8'):
            roty += .1
        elif keyboard.is_pressed('2'):
            roty -= .1

        for i in range(self.width):
            for j in range(self.height):
                uv = Vector3(i, j) / Vector3(self.width, self.height) * Vector3(2.0, 2.0) - Vector3(1.0, 1.0)
                uv.x *= float(self.aspect * self.pixel_aspect)

                ro = Vector3(-12 + ws, da, ud)

                rd = Vector3(3, uv.x, uv.y).norm()
                ro = ro.rotate_y(roty + .0001)
                rd = rd.rotate_y(roty + .0001)
                ro = ro.rotate_z(rotz)
                rd = rd.rotate_z(rotz)

                color = 0
                diff = 1.0

                for k in range(5):
                    min_it = 99999
                    n = Vector3()

                    # goursat render
                    d = smoothstep(-1.0, -0.4, -cos(0.3 * frame_num * 0.05))
                    ra = (0.3 + d * .6 * sin(1.311 * frame_num * 0.05))
                    rb = (abs(ra) + 0.6 + d * .25 * sin(0.73 * frame_num + 3.0))
                    goursat = shapes.Goursat(ro, rd.norm(), ra, rb)
                    intersection = goursat.render_goursat()

                    if intersection > 0:
                        pos = ro + Vector3(intersection, intersection, intersection) * rd
                        min_it = intersection
                        n = goursat.goursat_normal(pos)


                    # # capsule render
                    # pa = Vector3(0, 0, -1)
                    # pb = Vector3(0, 0, -0.99)
                    # capsule = shapes.Capsule(ro, rd, pa, pb, 1)
                    # intersection = Vector3(capsule.render_capsule(), capsule.render_capsule(), capsule.render_capsule())
                    #
                    # if intersection.x > 0:
                    #     it_point = ro + rd * Vector3(intersection.x, intersection.x, intersection.x)
                    #     min_it = intersection.x
                    #     n = it_point.norm()


                    # spheres render
                    sphere = shapes.Sphere(ro + sphere_pos1, rd, 1)
                    intersection = sphere.render_sphere()
                    # pixel color selection for sphere
                    if intersection.x > 0:
                        it_point = ro + sphere_pos1 + rd * Vector3(intersection.x, intersection.x, intersection.x)
                        min_it = intersection.x
                        n = it_point.norm()
                    #
                    # sphere = shapes.Sphere(ro + sphere_pos2, rd, 1)
                    # intersection = sphere.render_sphere()
                    # # pixel color selection for sphere
                    # if intersection.x > 0:
                    #     it_point = ro + sphere_pos2 + rd * Vector3(intersection.x, intersection.x, intersection.x)
                    #     min_it = intersection.x
                    #     n = it_point.norm()
                    #
                    #
                    # # cylinder render
                    # ca = Vector3(0, 0, 1).norm()
                    # cylinder = shapes.Cylinder(ro, rd, Vector3(0, 0, 0), ca, 1)
                    # intersection = cylinder.render_cylinder()
                    #
                    # if intersection.x > 0:
                    #     min_it = intersection.x
                    #     n = intersection.norm()


                    # cube render
                    cube = shapes.Cube(ro, rd, 2)
                    intersection = cube.render_cube()

                    # pixel color selection for cube
                    if 0 < intersection.x < min_it:
                        min_it = intersection.x
                        n = shapes.out_normal


                    # # plane render
                    # plane = shapes.Plane(ro, rd, Vector3(0, 0, -1), 1)
                    # intersection = Vector3(plane.render_plane(), plane.render_plane())
                    #
                    # # pixel color selection for plane
                    # if 0 < intersection.x < min_it:
                    #     min_it = intersection.x
                    #     n = Vector3(0, 0, -1)

                    if min_it < 99999:
                        diff *= dot(n, self.light) * 0.5 + 0.5
                        ro = ro + rd * Vector3((min_it - 0.01), (min_it - 0.01), (min_it - 0.01))
                        rd = reflect(rd, n)
                        color = int(diff * 17)
                    else: break

                color = border(color, 0, self.gradient_size)
                pixel = self.gradient[color]
                self.screen[i + j * self.width] = pixel

        for symbol in self.screen:
            frame += symbol  # filling the frame with pixels

        return frame + str(1 / (time.perf_counter() - start_time)) + ' FPS'



da = 0
ws = 0
ud = 0
rotz = 0
roty = 0


def main():
    frame = DrawFrames(120, 30)
    frame_num = 0

    # frame rendering cycle
    while True:
        try:
            frame_num += 1
            if keyboard.is_pressed('q'):
                break
        except: break

        print(frame.draw_frame(frame_num))


if __name__ == '__main__':
    main()
