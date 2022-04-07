import pygame
import os
import math
import sys
import neat

#SCREEN size
SCREEN_WIDTH = 1058
SCREEN_HEIGHT = 864
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#adding image
TRACK = pygame.image.load(os.path.join( "./Track_1.png"))


class Vehicle(pygame.sprite.Sprite):
    def __init__(self) :
        super().__init__()
        self.original_image = pygame.image.load(os.path.join("./car-outline-15.png"))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(430, 700)) #image rectangle starting x,y coordinates
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.rotation_vel = 10
        self.direction = 0
        self.alive = True
        self.radars = [] #empty list to collect data of 5 sensors 
        
#update function to update radar, drive positions and radars
    def update(self):
        self.radars.clear()
        self.drive()
        self.rotate()
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        self.collision()
        self.data()
    
    # to move the car by multiplying valocity by 6
    def drive(self):
        self.rect.center += self.vel_vector * 6

    def collision(self):
        #collision distance from car to the collision point
        length = 40
        collision_point_right = [int(self.rect.center[0] + math.cos(math.radians(self.angle + 20)) * length),
                                 int(self.rect.center[1] - math.sin(math.radians(self.angle + 20)) * length)]
        collision_point_left = [int(self.rect.center[0] + math.cos(math.radians(self.angle - 20)) * length),
                                int(self.rect.center[1] - math.sin(math.radians(self.angle - 20)) * length)]

        # Die on Collision
        if SCREEN.get_at(collision_point_right) == pygame.Color(0, 153, 0, 255)  \
                or SCREEN.get_at(collision_point_left) == pygame.Color(0, 153, 0, 255):
            self.alive = False
       
        #Draw collision Points 

        pygame.draw.circle(SCREEN, (0, 0, 255, 0), collision_point_right, 4)
        pygame.draw.circle(SCREEN, (0, 0, 255, 0), collision_point_left, 4)
    
    #if the rotation is -1 for left and 1 for right
    def rotate(self): 
        if self.direction == 1:
            self.angle -= self.rotation_vel
            self.vel_vector.rotate_ip(self.rotation_vel)
        if self.direction == -1:
            self.angle += self.rotation_vel
            self.vel_vector.rotate_ip(-self.rotation_vel)

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def radar(self, radar_angle):
        length = 0 
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])
        # print(x, y) # x, y are the center of the car and  
        while not SCREEN.get_at((x, y)) == pygame.Color(0, 153, 0, 255) and length < 100:
                length += 1
                #to calculate the end of the radars
                x = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle)) * length)
                y = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle)) * length)
      
        # Draw Radar
        pygame.draw.line(SCREEN, (255, 255, 255, 255), self.rect.center, (x, y), 1)
        pygame.draw.circle(SCREEN, (153, 0, 0, 0), (x, y), 3)

        # distance from center of car to tip of radar 
        dist = int(math.sqrt(math.pow(self.rect.center[0] - x, 2)
                              + math.pow(self.rect.center[1] - y, 2)))

        self.radars.append([radar_angle, dist])

    def data(self):
        input = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
        return input


def remove(index):
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)

#main loop
def eval_genomes(genomes, config):
    global cars, ge, nets

    cars = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Vehicle()))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    run = True
    while run:
        for event in pygame.event.get():  #to close the loop when closing window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.blit(TRACK, (0, 0))

        if len(cars) == 0:
            break

        for i, car in enumerate(cars):
            ge[i].fitness += 1
            if not car.sprite.alive:
                remove(i)

        for i, car in enumerate(cars):
            output = nets[i].activate(car.sprite.data())
            if output[0] > 0.7:
                car.sprite.direction = 1
            if output[1] > 0.7:
                car.sprite.direction = -1
            if output[0] <= 0.7 and output[1] <= 0.7:
                car.sprite.direction = 0

        # Update
        for car in cars:
            car.draw(SCREEN)
            car.update()
        pygame.display.update()

# to remove the car in case of collisions
def remove(index):
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)


# Setup NEAT Neural Network
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

 # eval_genomes 50 times if it breaks

    pop.run(eval_genomes, 50) 

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
