import cv2 as cv
import numpy as np
import math
import sys

image = cv.imread('resources/bolhas.png', cv.IMREAD_GRAYSCALE)

height, width = image.shape[:2]

seedpoint = [0, 0]



# Análise das bordas esquerda e direita
for i in range(height):

    # Eliminação de objetos na borda esquerda da cena
    if image[i, 0] == 255:
        seedpoint[0] = 0
        seedpoint[1] = i
        cv.floodFill(image, None, seedpoint, 0)

    # Eliminação de objetos na borda direita da cena
    if image[i, width-1] == 255:
        seedpoint[0] = width-1
        seedpoint[1] = i
        cv.floodFill(image, None, seedpoint, 0)

# Análise das bordas superior e inferior
for j in range(width):

    # Eliminação de objetos na borda superior da cena
    if image[0, j] == 255:
        seedpoint[0] = j
        seedpoint[1] = 0
        cv.floodFill(image, None, seedpoint, 0)

    # Eliminação de objetos na borda inferior da cena
    if image[height-1, j] == 255:
        seedpoint[0] = j
        seedpoint[1] = height-1
        cv.floodFill(image, None, seedpoint, 0)

# Identificando regiões sem buracos
nobjects = 0
for i in range(height):
    for j in range(width):
        if image[i, j] == 255:
            nobjects += 1
            seedpoint[0] = j
            seedpoint[1] = i
            cv.floodFill(image, None, seedpoint, 100)

print("A figura tem " + str(nobjects) + " objetos sem buracos")


cv.imshow('gray',image)

print(image.shape)

cv.waitKey(0)


