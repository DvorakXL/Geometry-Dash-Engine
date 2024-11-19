class Trigger:

    def __init__(self, id, position=tuple(), spawned=0, multi_trigger=0, group_id=0):
        self.data = []
        self.id = id
        self.position = position
        self.spawned = spawned
        self.multi_trigger = multi_trigger
        self.group_id = group_id
    
    def Spawn(self):

        trigger = {
            "id": self.id,
            "x": self.position[0],
            "y": self.position[1],
            "is_trigger": 1,
            "spawned": self.spawned,
            "multi_trigger": self.multi_trigger,
            "group": self.group_id
        }
        self.data.append(trigger)
        return self.data

class Move(Trigger):

    def __init__(
        self, position=tuple(), target_id=0, move_vector=list(), duration=0.0,
        easing = 0, easing_rate=2, spawned=0, multi_trigger=0, group_id=0
        ):
        super().__init__(901, position, spawned, multi_trigger, group_id)
        self.data = []
        self.target_id = target_id
        self.move_vector = move_vector
        self.duration = duration
        self.easing = easing
        self.easing_rate = easing_rate
    
    def Spawn(self, object=list()):

        trigger = super().Spawn()
        move = {
            "target": self.target_id,
            "move_x": self.move_vector[0],
            "move_y": self.move_vector[1],
            "duration": self.duration,
            "easing": self.easing,
            "easing_rate": self.easing_rate
        }

        new_trigger = {**trigger[0], **move}
        self.data = [new_trigger]
        if object:
            self.data += (object)
        return self.data

class Spawn(Trigger):

    def __init__(
        self, position=tuple(), target_id=0, delay=0.0,
        spawned=0, multi_trigger=0, group_id=0
        ):
        super().__init__(1268, position, spawned, multi_trigger, group_id)
        self.data = []
        self.target_id = target_id
        self.delay = delay
    
    def Spawn(self):

        trigger = super().Spawn()
        spawn = {
            "target": self.target_id,
            "delay": self.delay
        }

        new_trigger = {**trigger[0], **spawn}
        self.data = [new_trigger]
        return self.data
    
class Toggle(Trigger):

    def __init__(
        self, position=tuple(), target_id=0, activate=0,
        spawned=0, multi_trigger=0, group_id=0
        ):
        super().__init__(1049, position, spawned, multi_trigger, group_id)
        self.data = []
        self.target_id = target_id
        self.activate = activate
    
    def Spawn(self):

        trigger = super().Spawn()
        spawn = {
            "target": self.target_id,
            "activate": self.activate
        }

        new_trigger = {**trigger[0], **spawn}
        self.data = [new_trigger]
        return self.data