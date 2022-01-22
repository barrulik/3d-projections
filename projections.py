import pygame
import numpy as np
from math import *
import json

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RAINBOW = (0, 0, 0)
rainbow = True

WIDTH, HEIGHT = 800, 600
# WIDTH, HEIGHT = 1600, 900
scaling = 100


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


def projectPoint(point, angle):
    rotated = point.reshape(3, 1)
    rotated = np.dot(rotateX(pi / 2), rotated)
    rotated = np.dot(rotateX(angle), rotated)
    rotated = np.dot(rotateY(angle), rotated)
    rotated = np.dot(rotateZ(angle), rotated)

    projected = np.dot(np.matrix([[1, 0, 0], [0, 1, 0]]), rotated)

    x = int(projected[0][0] * scaling) + WIDTH / 2
    y = int(projected[1][0] * scaling) + HEIGHT / 2
    return [x, y]


def renderObject(file_path, point, angle, scaling, screen):
    f = open(file_path)
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

    renderObject("objects/quad_pyramid.json", [WIDTH / 2, HEIGHT / 2], angle, scaling, screen)
    #renderObject("objects/cube.json", [WIDTH / 2, HEIGHT / 2], angle, scaling, screen)

    pygame.display.update()
