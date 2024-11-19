import base64

class Text:

    def __init__(self, position=tuple(), text='', group=0, size=0.5 , scale=30):
        self.data = []
        self.position = position
        self.text = text
        self.group = group
        self.size = size
        self.scale = scale
    
    def Spawn(self):
        
        self.data = [{
            "id": 914,
            "x": self.position[0]*self.scale,
            "y": self.position[1]*self.scale,
            "text": base64.b64encode(self.text.encode('utf-8')).decode('utf-8'),
            "group": self.group,
            "scale": self.size,
            "64": "1",
            "67": "1"
        }]
        return self