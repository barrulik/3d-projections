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


def projectPoint(point, angle, offset, scale):
    rotated = point.reshape(3, 1)
    rotated = np.dot(rotateX(pi / 2), rotated)
    rotated = np.dot(rotateX(angle[0]), rotated)
    rotated = np.dot(rotateY(angle[1]), rotated)
    rotated = np.dot(rotateZ(angle[2]), rotated)

    projected = np.dot(np.matrix([[1, 0, 0], [0, 1, 0]]), rotated)

    x = int(projected[0][0] * scale) + WIDTH/2
    y = int(projected[1][0] * scale) + HEIGHT/2
    return [x, y]


def renderObject(objectPath, offset, angle, scale, screen):
    f = open(objectPath)
    data = json.load(f)
    points = data.get("points")
    if points:
        temp = ""
        for pointName in points:
            point = points.get(pointName)
            point = np.matrix(point)+np.matrix([offset])
            temp += '"'+pointName+'":'+str(projectPoint(point, angle, offset, scale))+','
        projectedPoints = json.loads('{'+temp[:-1]+'}')
        lines = data.get("lines")
        if lines:
            for line in lines:
                for p1name in line:
                    p1 = p1name
                p2 = projectedPoints.get(line.get(p1))
                p1 = projectedPoints.get(p1)
                drawLine(p1, p2, screen)
    objects = data.get("objects")
    if objects:
        for obj in objects:
                renderObject(obj.get("objectPath"), np.squeeze(np.array(np.matrix(obj.get("offset"))+np.matrix(offset)*scale/obj.get("scale"))) ,np.squeeze(np.array(np.matrix(obj["angle"])+ angle)), obj.get("scale"), screen)


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


#   type ur code here

    renderObject("objects/2squares.json", [0, 0, 0], [angle, angle, angle], scale, screen)
    renderObject("objects/square.json", [0, 0, 1], [angle, angle, angle], scale, screen)




    pygame.display.update()
