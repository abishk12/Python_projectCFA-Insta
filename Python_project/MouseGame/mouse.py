from PIL import ImageTk
from PIL import Image

class Mouse:

    def __init__(self):
        self.image= Image.open("./mouse.jpg")
        self.image=  self.image.resize((48,48))
        self.rotation= -90
        self.coordX= 51
        self.coordY= 51
        self.speed= 25
    
    def draw(self, canvas):
        self.tkImage= ImageTk.PhotoImage(self.image.rotate(self.rotation))
        return canvas.create_image(self.coordX, self.coordY, image=self.tkImage, anchor="nw")

    def turnLeft(self):
        if self.rotation == 270:
            self.rotation = 0
        else:
            self.rotation+=90
    
    def turnRight(self):
        if self.rotation == -270:
            self.rotation = 0
        else:
            self.rotation-=90
    
    def forward(self):
        if self.rotation == 0:
            self.coordY-= self.speed
        elif self.rotation == 180 or self.rotation == -180:
            self.coordY+= self.speed
        elif self.rotation == 270 or self.rotation == -90:
            self.coordX+= self.speed
        elif self.rotation == -270 or self.rotation == 90:
            self.coordX-= self.speed

    def touchLeft(self):
        if self.rotation == 0 :
            self.coordX-=self.speed
        elif self.rotation == 90 or self.rotation == -270:
            self.coordY-=self.speed
        elif self.rotation == 270 or self.rotation == -90:
            self.coordY+=self.speed
        elif self.rotation == 180 or self.rotation == -180:
            self.coordX+=self.speed   
    
    def touchRight(self):
        if self.rotation == 0 :
            self.coordX+=self.speed
        elif self.rotation == 90 or self.rotation == -270:
            self.coordY+=self.speed
        elif self.rotation == 270 or self.rotation == -90:
            self.coordY-=self.speed
        elif self.rotation == 180 or self.rotation == -180:
            self.coordX-=self.speed 
    
         
    def touchFront(self):
        self.forward()