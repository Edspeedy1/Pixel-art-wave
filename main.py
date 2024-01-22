import pygame
from perlin_noise import PerlinNoise
import colorsys
import math
import copy
import os
pygame.init()

MAIN_SCREEN = pygame.display.set_mode((1920,1080))
SCREEN = pygame.Surface((480, 360))
CENTRE = (SCREEN.get_width() / 2, SCREEN.get_height()/2-50)

def update():
    MAIN_SCREEN.blit(pygame.transform.scale(SCREEN, MAIN_SCREEN.get_size()), (0, 0))
    pygame.display.update()

def calculatePoint(x,y,z):
    FOCAL = 500
    ZSCALE = 10

    dist = y/FOCAL
    scale = max(dist, 0.00001)
    return (x/scale + CENTRE[0], (z*ZSCALE/scale) + CENTRE[1])

def colorMaker(i):
    c = colorsys.hsv_to_rgb((i/180)+0.45, 1, 1)
    scale = 255-i*2.5
    return (c[0]*scale, c[1]*scale, c[2]*scale)

def updateMesh(mesh, time):
    bMesh = copy.deepcopy(mesh)
    for ii, i in enumerate(mesh):
        for jj, j in enumerate(i):
            yscale = 1 if ii < 30 else 1.2 + ii/100
            point = calculatePoint(mesh[ii][jj][0], mesh[ii][jj][1], mesh[ii][jj][2] + math.sin(math.radians((time/8+(jj/2-ii/4)/3))*30)*0.5*yscale)
            bMesh[ii][jj] = point
    return bMesh

def main():
    running = True
    count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        bMesh = updateMesh(mesh, count)
        drawGrid(bMesh, count)
        update()

        pygame.image.save(SCREEN, f"small/image{count}.png")

        count += 1
        if count > 96:
            running = False



def drawGrid(nMesh, count):
    SCREEN.blit(pygame.image.load(f"stars\\image{count%96}.png"), (0,0))
    for i in reversed(range(len(nMesh))):
        for j in range(len(nMesh[i])-4):
            try:
                if i > 0 and j < len(mesh[i])-1:
                    pygame.draw.line(SCREEN, colorMaker(i), nMesh[i-1][j], nMesh[i][j+2])
                if j > 0:
                    pygame.draw.line(SCREEN, colorMaker(i), nMesh[i][j-1], nMesh[i][j])
            except:
                print(i, j)

mesh = [[0 for i in range(40+4*j)] for j in range(80)]
noise = PerlinNoise(octaves=11, seed=99327)

for j in range(len(mesh)):
    for i in range(len(mesh[j])):
        x = (i-(40+4*j)/2)*6
        y = (j*3+10)*6
        z = 3-0.0025*((i/2.2) - j)**2 + noise((i/41.123, j/41.123))*min(40/(y**0.3),3)
        if j==0: z+=2
        mesh[j][i] = (x,y,z)

if __name__ == '__main__':
    print(noise.seed)
    # for i in os.listdir("images"):
    #     print(i)
    #     os.remove(f"images\\{i}")
    main()