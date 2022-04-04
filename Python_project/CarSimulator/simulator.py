import pygame
import os
import math
import sys
import neat

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

TRACK = pygame.image.load(os.path.join( "./Piste_image.jpg"))


class Vehicle(pygame.sprite.Sprite):
    def __init__(self) :
        super().__init__()
        self.orignial_image = pygame.image.load(os.path.join("./car.png"))
        self.image = self.orignial_image
        self.rect = self.image.get_rect(center=(490, 820))
        self.drive_state = False
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0

    def update(self):
        self.drive()
        self.rotate()

    def drive(self):
        if self.drive_state:
            self.rect.center += self.vel_vector * 6
    
    def rotate(self):
        self.image = pygame.transform.rotozoom(self.orignial_image, self.angle, 0.1)

vehicle = pygame.sprite.GroupSingle(Vehicle())

def eval_genomes():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.blit(TRACK, (0,0))

        #user input 
        user_input = pygame.key.get_pressed() 
        if sum(pygame.key.get_pressed()) <= 1:
            vehicle.sprite.drive_state = False
        
        #Drive 
        if user_input[pygame.K_UP]:
            vehicle.sprite.drive_state = True

        #update
        vehicle.draw(SCREEN)
        vehicle.update()
        pygame.display.update()

eval_genomes()

# if __name__ == '__simulator__':
#     local_dir = os.path.dirname(__file__)
#     config_path = os.path.join(local_dir, 'config.txt')
#     run(config_path)