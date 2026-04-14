""" Author: Logan Wright Description: This program is an implementation of the quad tree data structure for massless points in space. """

class Rectangle:
    def __init__(self, x: float, y: float, w: float, h: float):
        # x, y are the coords of the center of the rectangle w, h are the width and height, respectively, of the rectangle
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point: tuple[float, float]) -> bool:
        # point has coordinates [x, y] and must be within the bounds of the rectangle to be enclosed
        if (self.x - self.w / 2 <= point[0] < self.x + self.w / 2) and (self.y - self.h / 2 <= point[1] < self.y + self.h / 2):
            return True
        return False

    def intersects(self, other: 'Rectangle') -> bool:
        # Pick a corner from self to use based on whichever is closest to other
        # Then check if that corner is contained in other
        if other.x - self.x >= 0:
            x_coord = self.x + self.w / 2
        else:
            x_coord = self.x - self.w / 2

        if other.y - self.y >= 0:
            y_coord = self.y + self.h / 2
        else:
            y_coord = self.y - self.h / 2

        return other.contains((x_coord, y_coord))


class QuadTree:
    def __init__(self, boundary: Rectangle, capacity: int = 4):
        self.boundary: Rectangle = boundary
        self.capacity: int = capacity
        self.children: dict[str, Rectangle] = {
            "NW": None,
            "NE": None,
            "SW": None,
            "SE": None
        }
        self.points: list[tuple[float, float]] = []
        self.subdivided = False

    def insert(self, point: tuple[float, float]) -> bool:
        if not self.boundary.contains(point):
            # Handle the case where we won't accept a point because it's not enclosed in the boundary
            return False
        if len(self.points) >= self.capacity and not self.subdivided:
            # Still add the point for more efficient query_range method
            self.points.append(point)
            self.subdivide()
            bx, by = self.boundary.x, self.boundary.y
            for (x, y) in self.points:
                ew = "W" if x < bx else "E"
                ns = "S" if y < by / 2 else "N"
                self.children[ns + ew].insert((x, y))
        
        self.points.append(point)
        return True

    def subdivide(self):
        # Create rectangle instances in the children variable
        bx, by, bw, bh = self.boundary.x, self.boundary.y, self.boundary.w, self.boundary.h
        wx = bx - bw / 4
        ex = bx + bw / 4
        ny = by + bh / 4
        sy = by - bh / 4

        self.children["NW"] = QuadTree(Rectangle(wx, ny, bw / 2, bh / 2))
        self.children["NE"] = QuadTree(Rectangle(ex, ny, bw / 2, bh / 2))
        self.children["SW"] = QuadTree(Rectangle(wx, sy, bw / 2, bh / 2))
        self.children["SE"] = QuadTree(Rectangle(ex, sy, bw / 2, bh / 2))

    def query_range(self, range_rect: Rectangle) -> list[tuple[float, float]]:
        # Generate a list of points in this quad tree that are contained within the query rectangle
        out = []
        for point in self.points:
            if range_rect.contains(point):
                out.append(point)
        return out
