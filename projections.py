import pygame
import numpy as np
from math import *
import json

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
#WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
scaling = 100

angle = 0

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

def drawLine(point1, point2):
    pygame.draw.line(
        screen, BLACK, (point1[0], point1[1]), (point2[0], point2[1]))

def rotateX(angle):
    return np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])
def rotateY(angle):
    return np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])
def rotateZ(angle):
    return np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

def projectPoint(point, angle):
    rotated = point.reshape(3, 1)
    rotated = np.dot(rotateX(pi/2), rotated)
    rotated = np.dot(rotateX(angle), rotated)
    rotated = np.dot(rotateY(angle), rotated)
    rotated = np.dot(rotateZ(angle), rotated)

    projected = np.dot(projection_matrix, rotated)

    
    x = int(projected[0][0] * scaling) + WIDTH/2
    y = int(projected[1][0] * scaling) + HEIGHT/2
    return [x, y]


def drawlinesAndProject(angle):
    f = open('config.json')
    data = json.load(f)
    points = data.get("points")
    lines = data.get("lines")
    for line in lines:
        for l in line:
            p1 = l
        p2 = points.get(line.get(p1))
        p1 = points.get(p1)
        p1 = np.matrix(p1)
        p2 = np.matrix(p2)
        p1 = projectPoint(p1, angle)
        p2 = projectPoint(p2, angle)
        drawLine(p1, p2)


clock = pygame.time.Clock()
while True:
    # so spin rate is not super fast/constant
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    

    
    screen.fill(WHITE)
    angle += 0.01
    drawlinesAndProject(angle)
    pygame.display.update()
