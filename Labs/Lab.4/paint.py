# paint.py module
import math

#lecture stuff

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Empty canvas is a matrix with element being the "space" character
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, w, **kargs):
        for i in range(x,x+w):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y,y+h):
            self.set_pixel(x,i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        for y in range(y1,y2):
            x= int(slope * y)
            self.set_pixel(x,y, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))


# my stuff

class shape:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def area(self):
        raise NotImplementedError("area not implemented")

    def perim(self):
        raise NotImplementedError("perim not implemented")

    def points(self, n=16):
        raise NotImplementedError("points not implemented")

    def inside(self, x, y):
        raise NotImplementedError("inside not implemented")

    def paint(self, canvas):
        raise NotImplementedError("paint not implemented")

    def get_x(self):
        return self.__x
                        
    def get_y(self):
        return self.__y

    def overlap(self, other_shape):
        my_points = self.points()
        for point in my_points:
            x_coord = point[0]
            y_coord = point[1]
    
            if other_shape.inside(x_coord, y_coord):
                return True
    
        other_points = other_shape.points()
        for point in other_points:
            x_coord = point[0]
            y_coord = point[1]
    
            if self.inside(x_coord, y_coord):
                return True
    
        return False
            


class rectangle(shape):
    def __init__(self, l, w, x, y):
        shape.__init__(self, x, y)
        self.__l = l
        self.__w = w

    def __repr__(self):
        return "rectangle(" + repr(self.__l) + "," + repr(self.__w) + "," + repr(self.get_x()) + "," + repr(self.get_y()) + ")"

    def area(self):
        return self.__l * self.__w
    
    def perim(self):
        return 2 * (self.__l + self.__w)

    def points(self, n=16):
        n = min(16, max(1, int(n)))
        pts = []

        x0 = self.get_x()
        y0 = self.get_y()
        l = self.__l
        w = self.__w

        side = max(1, n // 4)

        for i in range(side):
            t = i / side
            pts.append((x0 + t * l, y0))

        for i in range(side):
            t = i / side
            pts.append((x0 + l, y0 + t * w))

        for i in range(side):
            t = i / side
            pts.append((x0 + l - t * l, y0 + w))

        for i in range(side):
            t = i / side
            pts.append((x0, y0 + w - t * w))

        return pts[:n]

    def inside(self, x, y):
        x0 = self.get_x()
        y0 = self.get_y()

        if x < x0:
            return False
        if x > x0 + self.__l:
            return False
        if y < y0:
            return False
        if y > y0 + self.__w:
            return False

        return True

    def paint(self, canvas):
        x0 = int(self.get_x())
        y0 = int(self.get_y())
        l = int(self.__l)
        w = int(self.__w)

        canvas.v_line(x0, y0, l + 1)
        canvas.v_line(x0, y0 + w, l + 1)
        canvas.h_line(x0, y0, w + 1)
        canvas.h_line(x0 + l, y0, w + 1)

    def get_l(self):
        return self.__l

    def get_w(self):
        return self.__w


class circle(shape):
    def __init__(self, r, x, y):
        shape.__init__(self, x, y)
        self.__r = r
        self.__pi = math.pi

    def __repr__(self):
        return "circle(" + repr(self.__r) + "," + repr(self.get_x()) + "," + repr(self.get_y()) + ")"

    def area(self):
        return self.__pi * (self.__r ** 2)

    def perim(self):
        return 2 * self.__pi * self.__r

    def points(self, n=16):
        n = min(16, max(1, int(n)))
        pts = []

        center_x = self.get_x()
        center_y = self.get_y()
        r = self.__r

        for i in range(n):
            t = 2 * math.pi * i / n
            pts.append((center_x + r * math.cos(t), center_y + r * math.sin(t)))

        return pts

    def inside(self, x, y):
        center_x = self.get_x()
        center_y = self.get_y()
    
        dx = x - center_x
        dy = y - center_y
    
        dist = math.sqrt(dx*dx + dy*dy)
        return dist <= self.__r

    def paint(self, canvas):
        pts = self.points(16)
        for p in pts:
            canvas.set_pixel(int(p[0]), int(p[1]))

    def get_r(self):
        return self.__r


class triangle(shape):
    def __init__(self, a, b, c, x, y):
        shape.__init__(self, x, y)
        self.__a = a
        self.__b = b
        self.__c = c

    def __repr__(self):
        return "triangle(" + repr(self.__a) + "," + repr(self.__b) + "," + repr(self.__c) + "," + repr(self.get_x()) + "," + repr(self.get_y()) + ")"

    def perim(self):
        return self.__a + self.__b + self.__c

    def area(self):
        s = self.perim() / 2
        return (s * (s - self.__a) * (s - self.__b) * (s - self.__c)) ** 0.5

    def points(self, n=16):
        n = min(16, max(1, int(n)))
        pts = []

        x1 = self.get_x()
        y1 = self.get_y()

        a = self.__a
        b = self.__b
        c = self.__c

        if a <= 0 or b <= 0 or c <= 0:
            return pts
        if a + b <= c or a + c <= b or b + c <= a:
            return pts

        x2 = x1 + a
        y2 = y1

        x3 = x1 + (b*b + a*a - c*c) / (2*a)
        y_sq = b*b - (x3 - x1)**2
        if y_sq < 0:
            return pts
        y3 = y1 + (y_sq ** 0.5)

        def line_points(xA, yA, xB, yB, count):
            out = []
            for i in range(count):
                t = i / count
                out.append((xA + t * (xB - xA), yA + t * (yB - yA)))
            return out

        base = n // 3
        rem = n % 3

        n1 = base + (1 if rem > 0 else 0)
        n2 = base + (1 if rem > 1 else 0)
        n3 = base

        pts += line_points(x1, y1, x2, y2, max(1, n1))
        pts += line_points(x2, y2, x3, y3, max(1, n2))
        pts += line_points(x3, y3, x1, y1, max(1, n3))

        return pts[:n]

    def inside(self, x, y):
        x1 = self.get_x()
        y1 = self.get_y()

        a = self.__a
        b = self.__b
        c = self.__c

        if a <= 0 or b <= 0 or c <= 0:
            return False
        if a + b <= c or a + c <= b or b + c <= a:
            return False

        x2 = x1 + a
        y2 = y1

        x3 = x1 + (b*b + a*a - c*c) / (2*a)
        y_sq = b*b - (x3 - x1)**2
        if y_sq < 0:
            return False
        y3 = y1 + (y_sq ** 0.5)

        def tri_area(xa, ya, xb, yb, xc, yc):
            return abs(xa*(yb-yc) + xb*(yc-ya) + xc*(ya-yb)) / 2

        full = tri_area(x1, y1, x2, y2, x3, y3)
        a1 = tri_area(x, y, x2, y2, x3, y3)
        a2 = tri_area(x1, y1, x, y, x3, y3)
        a3 = tri_area(x1, y1, x2, y2, x, y)

        return abs((a1 + a2 + a3) - full) < 1e-6

    def paint(self, canvas):
        x1 = self.get_x()
        y1 = self.get_y()
    
        a = self.__a
        b = self.__b
        c = self.__c
    
        if a <= 0 or b <= 0 or c <= 0:
            return
        if a + b <= c or a + c <= b or b + c <= a:
            return
    
        x2 = x1 + a
        y2 = y1
    
        x3 = x1 + (b*b + a*a - c*c) / (2*a)
        y_sq = b*b - (x3 - x1)**2
        if y_sq < 0:
            return
        y3 = y1 + (y_sq ** 0.5)
    
        def draw_edge(xA, yA, xB, yB):
            dx = xB - xA
            dy = yB - yA
            steps = int(max(abs(dx), abs(dy), 1))
        
            for i in range(steps + 1):
                t = i / steps
                x = int(xA + t * dx)
                y = int(yA + t * dy)
        
                if 0 <= x < canvas.height and 0 <= y < canvas.width:
                    canvas.set_pixel(x, y)
    
        draw_edge(x1, y1, x2, y2)
        draw_edge(x2, y2, x3, y3)
        draw_edge(x3, y3, x1, y1)

    def get_a(self):
        return self.__a

    def get_b(self):
        return self.__b

    def get_c(self):
        return self.__c 


class CompoundShape(shape):
    def __init__(self, shapes):
        shape.__init__(self, 0, 0)
        self.shapes = shapes

    def __repr__(self):
        return "CompoundShape(" + repr(self.shapes) + ")"

    def paint(self, canvas):
        for s in self.shapes:
            s.paint(canvas)


def raster_from_named_shapes(items):
    rd = RasterDrawing()
    for name, shp in items:
        shp.name = name
        rd.add_shape(shp)
    return rd


class RasterDrawing:
    def __init__(self):
        self.shapes = dict()
        self.shape_names = list()

    def assign_name(self):
        name_base = "shape"
        i = 0
        name = name_base + "_" + str(i)

        while name in self.shapes:
            i += 1
            name = name_base + "_" + str(i)

        return name

    def add_shape(self, shp):
        if not hasattr(shp, "name"):
            shp.name = ""

        if shp.name == "":
            shp.name = self.assign_name()

        self.shapes[shp.name] = shp

        if shp.name not in self.shape_names:
            self.shape_names.append(shp.name)

    def paint(self, canvas):
        for shape_name in self.shape_names:
            self.shapes[shape_name].paint(canvas)

    def update(self, canvas):
        canvas.clear_canvas()
        self.paint(canvas)

    def __repr__(self):
        items = [(name, self.shapes[name]) for name in self.shape_names]
        return "raster_from_named_shapes(" + repr(items) + ")"

    def save(self, filename):
        f = open(filename, "w")
        f.write(self.__repr__())
        f.close()


def raster_loader(filename):
    f = open(filename, "r")
    obj = eval(f.read(), globals())
    f.close()
    return obj