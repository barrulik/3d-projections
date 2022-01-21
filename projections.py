import pygame
import numpy as np
from math import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scaling = 100

angle = 0

points = []
points.append(np.matrix([0, 0, 3]))
points.append(np.matrix([1, 1, 0]))
points.append(np.matrix([-1,  1, 0]))
points.append(np.matrix([-1, -1, 0]))
points.append(np.matrix([1, -1, 0]))


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


projectedCoords = [
    [n, n] for n in range(len(points))
]


def drawLine(point1, point2):
    pygame.draw.line(
        screen, BLACK, (point1[0], point1[1]), (point2[0], point2[1]))


clock = pygame.time.Clock()
while True:
    # so spin rate is not super fast/constant
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # rotation matrixes
    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])
    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])
    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    

    
    angle += 0.01

    screen.fill(WHITE)
    # drawining stuff

    for i in range(len(points)):
        point = points[i]
        rotated = np.dot(rotation_x, point.reshape((3, 1)))
        rotated = np.dot(rotation_y, rotated)
        rotated = np.dot(rotation_z, rotated)
        
        projected = np.dot(projection_matrix, rotated)

        x = int(projected[0][0] * scaling) + WIDTH/2
        y = int(projected[1][0] * scaling) + HEIGHT/2

        projectedCoords[i] = [x, y]

    for j in range(len(projectedCoords)):
        for k in range(j+1, len(projectedCoords)):
            drawLine(projectedCoords[j], projectedCoords[k])

    pygame.display.update()
