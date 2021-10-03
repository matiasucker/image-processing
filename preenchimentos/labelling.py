import cv2 as cv
import numpy as np
import math
import sys

image = cv.imread('resources/bolhas.png', cv.IMREAD_GRAYSCALE)

height, width = image.shape[:2]

seedpoint = [0, 0]

nobjects = 0

for j in range(width):
    if image[0, j] == 255:
        seedpoint[0] = j
        seedpoint[1] = 0
        cv.floodFill(image, None, seedpoint, 0)

    if image[height-1, j] == 255:
        seedpoint[0] = j
        seedpoint[1] = height-1
        cv.floodFill(image, None, seedpoint, 0)



for i in range(height):
    for j in range(width):
        if image[i, j] == 255:
            nobjects += 1
            seedpoint[0] = j
            seedpoint[1] = i

            cv.floodFill(image, None, seedpoint, 100)

print("A figura tem " + str(nobjects) + " bolhas")


cv.imshow('gray',image)

print(image.shape)

cv.waitKey(0)


