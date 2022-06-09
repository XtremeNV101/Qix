class Wall(object):

    defaultWallSize = 50
    defaultColor = (27, 255, 50)
    defaultFilled = 0
    def __init__(self, x=0, y=0, width=defaultWallSize, height=defaultWallSize,color=defaultColor,*args, **kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
