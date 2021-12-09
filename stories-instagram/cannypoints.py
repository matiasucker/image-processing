import cv2
import numpy as np


def cannypoints():

    TOP_SLIDER = 10
    TOP_SLIDER_MAX = 400
    T1 = 10

    STEP = 5
    JITTER = 3
    RAIO = 3

    def setT1(t1):
        global T1, points
        T1 = t1
        edges = cv2.Canny(points, T1, 3 * T1)
        cv2.imshow("canny", edges)
        cv2.imwrite("output/canny.png", edges)

        cannypoints = points.copy()

        edges_filter = np.where(edges != 0)
        coordinates = zip(edges_filter[0], edges_filter[1])
        for p in coordinates:
            color = cannypoints[p]
            cv2.circle(cannypoints, (p[1], p[0]), RAIO//2, (int(color[0]), int(color[1]), int(color[2])), -1, cv2.LINE_AA)

        cv2.imshow("cannypoints", cannypoints)
        cv2.imwrite("output/cannypoints.png", cannypoints)

    image = cv2.imread("resources/img1.png", cv2.IMREAD_COLOR)
    height, width = image.shape[:2]

    xrange = np.arange(0, image.shape[0] - STEP, STEP) + STEP // 2
    yrange = np.arange(0, image.shape[1] - STEP, STEP) + STEP // 2

    points = np.zeros(image.shape, dtype=np.uint8)

    np.random.shuffle(xrange)
    for i in xrange:
        np.random.shuffle(yrange)
        for j in yrange:
            x = i + np.random.randint((2 * JITTER) - JITTER + 1)
            y = j + np.random.randint((2 * JITTER) - JITTER + 1)
            color = image[x, y]
            cv2.circle(points, (y, x), RAIO, (int(color[0]), int(color[1]), int(color[2])), -1, cv2.LINE_AA)

    cv2.imshow("points", points)
    cv2.imwrite("output/points.png", points)

    cv2.namedWindow("canny", cv2.WINDOW_GUI_NORMAL)
    cv2.createTrackbar("T1", "canny", TOP_SLIDER, TOP_SLIDER_MAX, setT1)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
