import numpy as np
import gdlevel.triggers as triggers
import gdlevel.matrices as matrices

m_projection = matrices.ProjectionMatrix()
#Maybe do Point - Planes - Cubes in an abstract manner!!

class Point:

    def __init__(self, position=list(), group=0, scale=30):
        self.data = []
        self.triggers = []
        #position = [x,y,z]
        self.position = position
        self.group = group
        self.scale = scale
    
    def Spawn(self):

        #Assign the json object for the point
        self.data = [{
            "id": 1764,
            "x": self.position[0]*self.scale,
            "y": self.position[1]*self.scale,
            "group": self.group
        }]
        return self

    #Generates a move trigger for this object
    def Move(self, trigger_pos=tuple(), move_to=list(), duration=0.5,
            easing=0, spawned=0, multi_trigger=0, group=0):
        
        pos = (trigger_pos[0]*self.scale, trigger_pos[1]*self.scale)
        trigger = triggers.Move(pos, self.group, move_to, duration, easing=easing, spawned=spawned, multi_trigger=multi_trigger, group_id=group).Spawn()
        self.data += trigger
        self.triggers += trigger
        return self

    #Rotates this object
    def Rotate(self, trigger_pos=tuple(), angle=0.0, duration=2, resolution=10):
        #Divide the angles times the resolution
        angle *= np.pi/180
        angle = angle/resolution
        
        m_rotation_x = matrices.RotationMatrixX(angle)
        m_rotation_y = matrices.RotationMatrixY(angle)
        m_rotation_z = matrices.RotationMatrixZ(angle)

        #Loop resolution times
        for index in range(resolution):

            #Get next vertex position with transformations
            next_keyframe = np.matmul(m_rotation_x, self.position)
            next_keyframe = np.matmul(m_rotation_y, next_keyframe)
            # next_keyframe = np.matmul(m_rotation_z, self.position)
            
            move_vector = np.around(next_keyframe-self.position,10) * self.scale
            span = (duration/resolution)

            #Move the old position into the transformed one
            self.position = next_keyframe
            
            #Position makes a line where x = index
            pos = (trigger_pos[0]*self.scale+300*span*index, trigger_pos[1]*self.scale)
            trigger = triggers.Move(pos, self.group, move_vector, span).Spawn()
            self.data += trigger
            self.triggers += trigger
        return self

class Segment:

    def __init__(self, positions=list(), group=0, scale=30):
        self.data = []
        self.points = []
        self.triggers = []
        for i in range(2):
            #position = [[x,y,z][x,y,z]]
            self.points.append(Point(positions[i], group+i, scale))

    def Spawn(self):

        #Calls spawn of the points
        for points in self.points:
            self.data += points.Spawn().data
        return self
    
    def Move(self, trigger_pos=tuple(), move_to=list(), duration=0.5,
            easing=0, spawned=0, multi_trigger=0, group=0):
        
        index = 0
        for vertex in self.points:
            #Adjust the trigger position in Y for each trigger so they don't overlap
            pos = (trigger_pos[0], trigger_pos[1]+index)
            move = [move_to[0] * vertex.scale, move_to[1] * vertex.scale]
            triggers = vertex.Move(pos, move, duration, easing, spawned, multi_trigger, group).triggers
            self.data += triggers
            self.triggers += triggers
            index += 1
        return self

    def Rotate(self, trigger_pos=tuple(), angle=0.0, duration=2, resolution=10):
        index = 0
        for vertex in self.points:
            #Adjust the trigger position in Y for each vertex so they don't overlap
            pos = (trigger_pos[0], trigger_pos[1]+index)
            triggers = vertex.Rotate(pos, angle, duration, resolution).triggers
            self.data += triggers
            self.triggers += triggers
            index += 1
        return self

class Quad:

    def __init__(self, positions=list(), group=0, scale=30):
        self.data = []
        self.segments = []
        self.triggers = []
        for i in range(2):
            segment_pos = positions[i*2:i*2+2]
            self.segments.append(Segment(segment_pos, group+2*i, scale))

    def Spawn(self):
        
        #Calls spawn of the segments
        for segment in self.segments:
            self.data += segment.Spawn().data
        return self

    def Rotate(self, trigger_pos=tuple(), angle=0.0, duration=2, resolution=10):

        index = 0
        for vertex in self.segments:
            #Adjust the trigger position in Y for each vertex so they don't overlap
            pos = (trigger_pos[0], trigger_pos[1]+2*index)
            triggers = vertex.Rotate(pos, angle, duration, resolution).triggers
            self.data += triggers
            self.triggers += triggers
            index += 1
        return self