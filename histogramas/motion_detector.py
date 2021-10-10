import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
import time


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--color', type=str, default='gray',
    help='Color space: "gray" (default), "rgb"')
parser.add_argument('-b', '--bins', type=int, default=256,
    help='Number of bins per channel (default 256)')
parser.add_argument('-s', '--sim', type=float, default=0.995,
    help='Similarity of histograms (default 0.995)')
args = vars(parser.parse_args())

color = args['color']
bins = args['bins']
sim = args['sim']


fig, ax = plt.subplots()
if color == 'rgb':
    ax.set_title('Histograma RGB')
else:
    ax.set_title('Histograma escala de cinza')
ax.set_xlabel('Bins')
ax.set_ylabel('Frequency')

lw = 3
alpha = 0.5
if color == 'rgb':
    lineR, = ax.plot(np.arange(bins), np.zeros((bins,)), c='r', lw=lw, alpha=alpha, label='Red')
    lineG, = ax.plot(np.arange(bins), np.zeros((bins,)), c='g', lw=lw, alpha=alpha, label='Green')
    lineB, = ax.plot(np.arange(bins), np.zeros((bins,)), c='b', lw=lw, alpha=alpha, label='Blue')

    image_referenceR = np.zeros((480, 640), dtype="uint8")
    histogram_referenceR = cv2.calcHist([image_referenceR], [0], None, [bins], [0, 255])

    image_referenceG = np.zeros((480, 640), dtype="uint8")
    histogram_referenceG = cv2.calcHist([image_referenceG], [0], None, [bins], [0, 255])

    image_referenceB = np.zeros((480, 640), dtype="uint8")
    histogram_referenceB = cv2.calcHist([image_referenceB], [0], None, [bins], [0, 255])

else:
    lineGray, = ax.plot(np.arange(bins), np.zeros((bins,1)), c='k', lw=lw, label='intensity')

    image_referenceGRAY = np.zeros((480, 640), dtype="uint8")
    histogram_referenceGRAY = cv2.calcHist([image_referenceGRAY], [0], None, [bins], [0, 255])

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

    numPixels = np.prod(frame.shape[:2])
    if color == 'rgb':
        cv2.imshow('RGB', frame)
        (b, g, r) = cv2.split(frame)
        histogramR = cv2.calcHist([r], [0], None, [bins], [0, 255])
        histogramG = cv2.calcHist([g], [0], None, [bins], [0, 255])
        histogramB = cv2.calcHist([b], [0], None, [bins], [0, 255])

        cv2.normalize(histogramR, histogramR, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(histogramG, histogramG, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(histogramB, histogramB, 0, 255, cv2.NORM_MINMAX)

        lineR.set_ydata(histogramR)
        lineG.set_ydata(histogramG)
        lineB.set_ydata(histogramB)

        similarityR = cv2.compareHist(histogram_referenceR, histogramR, cv2.HISTCMP_CORREL)
        similarityG = cv2.compareHist(histogram_referenceG, histogramG, cv2.HISTCMP_CORREL)
        similarityB = cv2.compareHist(histogram_referenceB, histogramB, cv2.HISTCMP_CORREL)

        similarity = (similarityR + similarityG + similarityB) / 3
        print(similarity)

        if (similarityR < sim) or (similarityG < sim) or (similarityB < sim):
            print("[INFO] ALARME: movimento detectado " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        histogram_referenceR = histogramR.copy()
        histogram_referenceG = histogramG.copy()
        histogram_referenceB = histogramB.copy()

    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Grayscale', gray)
        histogramGRAY = cv2.calcHist([gray], [0], None, [bins], [0, 255])

        cv2.normalize(histogramGRAY, histogramGRAY, 0, 255, cv2.NORM_MINMAX)

        lineGray.set_ydata(histogramGRAY)

        similarityGRAY = cv2.compareHist(histogram_referenceGRAY, histogramGRAY, cv2.HISTCMP_CORREL)

        print(similarityGRAY)

        if similarityGRAY < sim:
            print("[INFO] ALARME: movimento detectado " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        histogram_referenceGRAY = histogramGRAY.copy()

    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()