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


capture = cv2.VideoCapture(0)
while True:
    (grabbed, frame) = capture.read()
    frame = cv2.flip(frame, 0)
    if not grabbed:
        break

    if color == 'rgb':
        cv2.imshow('RGB', frame)
        (b, g, r) = cv2.split(frame)


    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Grayscale', gray)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()