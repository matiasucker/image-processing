import numpy as np
import matplotlib.pyplot as plt
import cv2
import time


def equalize():

    fig, ax = plt.subplots()
    ax.set_title('Histograma RGB equalizado')
    ax.set_xlabel('Bins')
    ax.set_ylabel('Frequency (N of Pixels)')

    lw = 3
    alpha = 0.5
    bins = 256
    lineR, = ax.plot(np.arange(bins), np.zeros((bins,)), c='r', lw=lw, alpha=alpha, label='Red')
    lineG, = ax.plot(np.arange(bins), np.zeros((bins,)), c='g', lw=lw, alpha=alpha, label='Green')
    lineB, = ax.plot(np.arange(bins), np.zeros((bins,)), c='b', lw=lw, alpha=alpha, label='Blue')

    ax.set_xlim(0, bins)
    ax.set_ylim(0, bins + 50)
    ax.legend()
    plt.ion()
    plt.show()

    capture = cv2.VideoCapture(0)
    while True:
        existe_frame, frame = capture.read()

        frame = cv2.flip(frame, 0)

        if not existe_frame:
            break

        (b, g, r) = cv2.split(frame)
        b = cv2.equalizeHist(b)
        g = cv2.equalizeHist(g)
        r = cv2.equalizeHist(r)
        frame_equalized = cv2.merge((b, g, r))
        cv2.imshow('RGB equalized', frame_equalized)

        histogramR = cv2.calcHist([r], [0], None, [bins], [0, 255])
        histogramG = cv2.calcHist([g], [0], None, [bins], [0, 255])
        histogramB = cv2.calcHist([b], [0], None, [bins], [0, 255])

        cv2.normalize(histogramR, histogramR, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(histogramG, histogramG, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(histogramB, histogramB, 0, 255, cv2.NORM_MINMAX)

        lineR.set_ydata(histogramR)
        lineG.set_ydata(histogramG)
        lineB.set_ydata(histogramB)

        fig.canvas.draw()
        fig.canvas.flush_events()

        time.sleep(0.1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()