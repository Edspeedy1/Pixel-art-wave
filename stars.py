import pygame
import random
import math

MAIN_SCREEN = pygame.display.set_mode()
SCREEN = pygame.Surface((480, 360))

starList = []
class starClass:
    def __init__(self, x, y, color, size):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.cycle = random.random()*2*math.pi
        self.speed = random.choice((0,1,1,1,1,1,2,2,3))*2*math.pi/96
        self.Cchange = random.randint(0, 150)

        self.maxColor = color
        starList.append(self)
    
    def draw(self, screen):
        if self.y > 130: return
        paraballa = lambda x: -0.0005*(x-240)**2+138
        if self.y > paraballa(self.x):
            return

        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
    
    def change(self):
        self.color = tuple([max(min(i-self.Cchange*math.sin(self.cycle),255), 0) for i in self.maxColor])
        self.cycle += self.speed

def update():
    MAIN_SCREEN.blit(pygame.transform.scale(SCREEN, MAIN_SCREEN.get_size()), (0, 0))
    pygame.display.update()

for i in range(0, 50):
    blue = (10,200,255)
    scale = random.random()/2+0.5
    star = starClass(random.randint(0, 480), random.randint(0, 160), tuple((i*scale for i in blue)), 1)
    star.change()
    star.change()

clock = pygame.time.Clock()
count = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    SCREEN.fill((0,0,0))
    for star in starList:
        star.change()
        star.draw(SCREEN)
    # pygame.draw.rect(SCREEN, (100,100,0), (0, 130, 400, 20))
    
    update()

    clock.tick(60)
    if count <= 96:
        pygame.image.save(SCREEN, f"stars\\image{count}.png")
    else:
        running = False
    count += 1