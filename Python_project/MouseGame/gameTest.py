from random import randint
from time import sleep
from tkinter import *
from wall import Wall
from mouse import Mouse
import _thread


class Game:

    def __init__(self):
        #constructor the windows of the game
        self.root = Tk()
        self.root.title('Labyrinte')
        self.width=600
        self.height=400
        self.canvas = Canvas(self.root, width= self.width, height= self.height, background='#FFF')
        self.canvas.pack()
        self.createWalls()
        self.mouse= Mouse()
        self.speed= 0.001
        self.draw()
        _thread.start_new_thread(self.animation, ())
        self.root.mainloop()

    def createWalls(self):
        # print("this is createwalls")
        self.walls =[]
        for x in range (0,self.width, 50):
            for y in range(0,self.height, 50):
                if x == 0 or y == 0 or x == self.width-50 or y == self.height- 50:
                    self.walls.append(Wall(x, y))
                if x>= 100 and x <= self.width-150 and y >=100 and y <=self.height-150:
                    if(x!=(self.width-150) and y!=100):
                        self.walls.append(Wall(x, y))
                    elif x>(self.width-200) and y <150:
                        continue
                    elif y>50:
                        self.walls.append(Wall(x, y))

    def draw(self):
        for i in range(len(self.walls)):
            self.walls[i].draw(self.canvas)
            self.canvasMouse= self.mouse.draw(self.canvas)

    
    def isColision(self):
        for i in range(len(self.walls)):
            if(self.walls[i].isCollision(self.mouse.coordX, self.mouse.coordY)):
                return True
        return False
    
    def onKeyPress(self, evt):
        oldCoord= self.mouseCoord.copy()
        #print(evt.char)
        if evt.char == 'z':
            self.forward()
        elif evt.char == 'q':
            self.turnLeft()
        elif evt.char == 'd':
            self.turnRight()

        if self.isColision(self):
              self.mouseCoord= oldCoord
        self.canvas.delete(self.canvasMouse)
        self.drawMouse()

        # def doAction(self, numAction):
        # oldCoord= (self.mouse.coordX, self.mouse.coordY)
        # if numAction ==0:
        #     self.mouse.forward()
        # if numAction ==1:
        #     self.mouse.turnLeft()   
        # if numAction ==2:
        #     self.mouse.turnRight()
        # if numAction ==3:
        #     self.mouse.touchFront()
        # if numAction ==4:
        #     self.mouse.turnLeft()   
        # if numAction ==5:
        #     self.mouse.turnRight()

        # collsion = self.isColision()
        # if collsion or numAction:
        #     self.mouse.coordX = oldCoord[0]
        #     self.mouse.coordY = oldCoord[1]
       
        # self.canvas.delete(self.canvasMouse)
        # self.canvasMouse = self.mouse.draw(self.canvas)
        # return self.performance(numAction, collsion)

    # def performance(self,numAction, collision):
    #     if numAction == 0:
    #         if collision:
    #             return -200
    #         else: 
    #             return 100
    #     elif numAction == 1 or numAction == 2:
    #         return -20
    #     else:
    #         if collision:
    #             return -10
    #         else: 
    #             return -5    
    
        
    def animation(self):
        while(True):
            sleep(self.speed)
            oldCoord= (self.mouse.coordX, self.mouse.coordY)
            numRandom= randint(0, 2)
            if numRandom==0:
                self.mouse.forward()
            elif numRandom==1:
                self.mouse.turnLeft()
            elif numRandom==2:
                self.mouse.turnRight()
        
            if self.isColision():
                self.mouse.coordX= oldCoord[0]
                self.mouse.coordY= oldCoord[1]
            self.canvas.delete(self.canvasMouse)
            self.canvasMouse= self.mouse.draw(self.canvas)
            
if __name__ == "__main__":
    Game()