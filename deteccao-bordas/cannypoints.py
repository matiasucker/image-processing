import cv2
import numpy as np
import random

# Canny
TOP_SLIDER = 10
TOP_SLIDER_MAX = 200
t1 = 10
T1 = 10
edges = 0

# Pontilhismo
STEP = 5
JITTER = 3
RAIO = 3


def setT1(t1):
    global T1, height, width, edges, gray, points, image
    T1 = t1
    if T1 < TOP_SLIDER:
        T1 = 10
    edges = cv2.Canny(image, T1, 3*T1)
    cv2.imshow("canny", edges)
    cv2.imwrite("output/canny.png", edges)

    for i in range(height):
        for j in range(width):
            if(edges[i, j] != 0):
                gray = image[i,j]
                cv2.circle(points,
                        (j, i),
                        RAIO,
                        int(gray),
                        -1,
                        cv2.LINE_AA)

    cv2.imshow("cannypoints", points)
    cv2.imwrite("output/cannypoints.png", points)


image = cv2.imread("resources/img8.png", 0)
height, width = image.shape[:2]

xrange = np.zeros(int(height/STEP))
yrange = np.zeros(int(width/STEP))

xrange = np.arange(len(xrange))
yrange = np.arange(len(yrange))

for i in range(len(xrange)):
    xrange[i] = xrange[i] * STEP + STEP / 2

for i in range(len(yrange)):
    yrange[i] = yrange[i] * STEP + STEP / 2

points = np.repeat(255, width * height).reshape(image.shape[:2]).astype('uint8')

np.random.shuffle(xrange)

for i in xrange:
    np.random.shuffle(yrange)
    for j in yrange:
        x = int(i + random.randint(1, 2*JITTER-JITTER))
        y = int(j + random.randint(1, 2*JITTER-JITTER))
        if x >= height:
            x = height-1
        if y >= width:
            y = width-1
        gray = image[x, y]
        cv2.circle(points,
                   (y, x),
                   RAIO,
                   int(gray),
                   -1,
                   cv2.LINE_AA)

edges = cv2.Canny(points, T1, 3*T1)
cv2.imshow("canny", edges)
cv2.createTrackbar("T1", "canny", t1, TOP_SLIDER_MAX, setT1)

cv2.waitKey(0)
cv2.destroyAllWindows()