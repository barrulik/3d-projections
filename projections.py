import pygame
import numpy as np
from math import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
#WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
scaling = 100

angle = 0

points = []
points.append(np.matrix([0, 0,2]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1,  1, -1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))


# cube
# points.append(np.matrix([-1, -1, 1]))
# points.append(np.matrix([1, -1, 1]))
# points.append(np.matrix([1,  1, 1]))
# points.append(np.matrix([-1, 1, 1]))
# points.append(np.matrix([-1, -1, -1]))
# points.append(np.matrix([1, -1, -1]))
# points.append(np.matrix([1, 1, -1]))
# points.append(np.matrix([-1, 1, -1]))


projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])


projectedPoints = [
    [n, n] for n in range(len(points))
]

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
    #rotated = np.dot(rotateY(angle), rotated)
    rotated = np.dot(rotateZ(angle), rotated)
    rotated = np.dot(rotateX(pi/2), rotated)

    projected = np.dot(projection_matrix, rotated)

    
    x = int(projected[0][0] * scaling) + WIDTH/2
    y = int(projected[1][0] * scaling) + HEIGHT/2
    return [x, y]

    
clock = pygame.time.Clock()
while True:
    # so spin rate is not super fast/constant
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    


    angle += 0.01
    screen.fill(WHITE)
    # drawining stuff

    for i in range(len(points)):
        projectedPoints[i] = projectPoint(points[i], angle)

    for j in range(len(projectedPoints)):
        for k in range(j+1, len(projectedPoints)):
            drawLine(projectedPoints[j], projectedPoints[k])

    pygame.display.update()
