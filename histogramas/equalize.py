import numpy as np
import matplotlib.pyplot as plt
import argparse
import cv2
import time

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--color', type=str, default='gray',
    help='Color space: "gray" (default), "rgb"')
parser.add_argument('-b', '--bins', type=int, default=256,
    help='Number of bins per channel (default 256)')
args = vars(parser.parse_args())

color = args['color']
bins = args['bins']

fig, ax = plt.subplots()

if color == 'rgb':
    ax.set_title('Histograma RGB equalizado')
else:
    ax.set_title('Histograma escala de cinza equalizado')

ax.set_xlabel('Bins')
ax.set_ylabel('Frequency')

lw = 3
alpha = 0.5
if color == 'rgb':
    lineR, = ax.plot(np.arange(bins), np.zeros((bins,)), c='r', lw=lw, alpha=alpha, label='Red')
    lineG, = ax.plot(np.arange(bins), np.zeros((bins,)), c='g', lw=lw, alpha=alpha, label='Green')
    lineB, = ax.plot(np.arange(bins), np.zeros((bins,)), c='b', lw=lw, alpha=alpha, label='Blue')

else:
    lineGray, = ax.plot(np.arange(bins), np.zeros((bins,1)), c='k', lw=lw, label='intensity')

ax.set_xlim(0, bins)
ax.set_ylim(0, 0.03)
ax.legend()
plt.ion()
plt.show()

capture = cv2.VideoCapture(0)
while True:
    (grabbed, frame) = capture.read()

    frame = cv2.flip(frame, 0)



    if not grabbed:
        break

    numPixels = np.prod(frame.shape[:2])
    if color == 'rgb':
        #frame_equalized = cv2.equalizeHist(frame)
        #cv2.imshow('RGB equalized', frame_equalized)

        (b, g, r) = cv2.split(frame)
        b = cv2.equalizeHist(b)
        g = cv2.equalizeHist(g)
        r = cv2.equalizeHist(r)
        frame_equalized = cv2.merge((b, g, r))
        cv2.imshow('RGB equalized', frame_equalized)
        histogramR = cv2.calcHist([r], [0], None, [bins], [0, 255]) / numPixels
        histogramG = cv2.calcHist([g], [0], None, [bins], [0, 255]) / numPixels
        histogramB = cv2.calcHist([b], [0], None, [bins], [0, 255]) / numPixels
        lineR.set_ydata(histogramR)
        lineG.set_ydata(histogramG)
        lineB.set_ydata(histogramB)

    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_equalized = cv2.equalizeHist(gray)
        cv2.imshow('Grayscale equalized', frame_equalized)
        histogram = cv2.calcHist([frame_equalized], [0], None, [bins], [0, 255]) / numPixels
        lineGray.set_ydata(histogram)

    fig.canvas.draw()
    fig.canvas.flush_events()

    time.sleep(0.1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()