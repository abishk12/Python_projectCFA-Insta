class Wall:

    def __init__(self, x, y):
        self.coordX= x
        self.coordY= y

    def draw(self, canevas):
        canevas.create_rectangle(self.coordX, self.coordY, self.coordX+50, self.coordY+50, fill='#0F0')

    def isCollision(self, mouseX, mouseY):
        wallX= self.coordX
        wallY= self.coordY
        for x in range(mouseX, mouseX+49):
            for y in range(mouseY, mouseY+49):
                if x >= wallX and x <= wallX+50 and y >= wallY and y <= wallY+50:
                    return True
        return False