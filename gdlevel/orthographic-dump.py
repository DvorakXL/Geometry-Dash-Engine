class Point:

    def __init__(self, position=tuple(), group_id=0):
        self.data = []
        self.position = position
        self.group_id = group_id

    def Spawn(self):

        point = {
                "id": 1764,
                "x": self.position[0],
                "y": self.position[1],
                "group": self.group_id
        }
        self.data.append(point)
        return self.data

class Rectangle():

    def __init__(self, pivot_position=tuple(), size=tuple(), group_id=0):
        self.data = []
        self.pivot_position = pivot_position
        self.size = size
        self.group_id = group_id

    def Spawn(self):

        index = 0
        for x in range(0,2):
            for y in range(0,2):
                offset = (self.pivot_position[0] + x, self.pivot_position[1] + y)
                size = (self.size[0] * x, self.size[1] * y)
                pos = (offset[0] + size[0], offset[1] + size[1])

                if self.group_id:
                    vertex = Point((pos[0], pos[1]), self.group_id + index).Spawn()
                else:
                    vertex = Point((pos[0], pos[1])).Spawn()
                self.data += vertex
                index += 1
        return self.data

class Square(Rectangle):

    def __init__(self, pivot_position=tuple(), size=None, group_id=0):
        super().__init__(pivot_position, (size, size), group_id)
    
    def Spawn(self):
        return super().Spawn()

class Cuboid:

    def __init__(self, pivot_position=list(), size=list(), group_id=0):
        self.data = []
        self.pivot_position = pivot_position
        self.size = size
        self.group_id = group_id
    
    def Spawn(self):
        
        for z in range(0,2):
            offset = [self.pivot_position[0], self.pivot_position[1], self.pivot_position[2] + z]
            size = [self.size[0], self.size[1], self.size[2] * z]

            if self.group_id:
                vertex = Rectangle((offset[0], offset[1]), (size[0], size[1]), self.group_id + z*4).Spawn()
            else:
                vertex = Rectangle((offset[0], offset[1]), (size[0], size[1])).Spawn()
            self.data += vertex
        return self.data