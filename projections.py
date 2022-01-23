import pygame
import numpy as np
from math import *
import json

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RAINBOW = (0, 0, 0)
rainbow = True

WIDTH, HEIGHT = 800, 600
#WIDTH, HEIGHT = 1600, 900
scale = 100


def drawLine(point1, point2, screen):
    if rainbow:
        pygame.draw.line(screen, RAINBOW, (point1[0], point1[1]), (point2[0], point2[1]))
    else:
        pygame.draw.line(screen, BLACK, (point1[0], point1[1]), (point2[0], point2[1]))


def rotateX(angle):
    return np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)]
    ])


def rotateY(angle):
    return np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)]
    ])


def rotateZ(angle):
    return np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1]
    ])


def projectPoint(point, angle, offset):
    rotated = point.reshape(3, 1)
    rotated = np.dot(rotateX(pi / 2), rotated)
    rotated = np.dot(rotateX(angle[0]), rotated)
    rotated = np.dot(rotateY(angle[1]), rotated)
    rotated = np.dot(rotateZ(angle[2]), rotated)

    projected = np.dot(np.matrix([[1, 0, 0], [0, 1, 0]]), rotated)

    x = int(projected[0][0] * scale) + WIDTH/2
    y = int(projected[1][0] * scale) + HEIGHT/2
    return [x, y]


def renderObject(file_path, offset, angle, scale, screen):
    # rounding offset
    offset[0] = round(offset[0]/scale*100)/100
    offset[1] = round(offset[1]/scale*100)/100
    offset[2] = round(offset[2]/scale*100)/100
    
    
    f = open(file_path)
    data = json.load(f)
    points = data.get("points")
    temp = ""
    for pointName in points:
        point = points.get(pointName)
        point = np.matrix(point)+np.matrix([offset])
        temp += '"'+pointName+'":'+str(projectPoint(point, angle, offset))+','
    projectedPoints = json.loads('{'+temp[:-1]+'}')
    lines = data.get("lines")
    for line in lines:
        for p1name in line:
            p1 = p1name
        p2 = projectedPoints.get(line.get(p1))
        p1 = projectedPoints.get(p1)
        drawLine(p1, p2, screen)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
angle = 0
while True:
    # so spin rate is not super fast/constant
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    angle += 0.01
    screen.fill(WHITE)

    renderObject("objects/cube.json", [0, 0, 0], [angle, angle, angle], scale, screen)


    pygame.display.update()
