class Enemy(object):
    def __init__(self,x,y):  # initial position
        self.x = x 
        self.y = y
    def move(self, speed, px, py): # chase movement
        # Movement along x direction
        if self.x > px:
            self.x -= speed
        elif self.x < px:
            self.x += speed
        # Movement along y direction
        if self.y < py:
            self.y += speed
        elif self.y > py:
            self.y -= speed