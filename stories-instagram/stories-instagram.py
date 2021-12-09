import cv2

from equalize import equalize
from tiltshift import tiltshift
from tiltshiftvideo import tiltshiftvideo
from laplgauss import laplgauss
from homomorphic import homomorphicfilter
from cannypoints import cannypoints



print("Select Filter Function:")
print("1 - equalize")
print("2 - tiltshift")
print("3 - laplgauss")
print("4 - homomorphic")
print("5 - cannypoints")
op = input()

while True:
    if op == 'a':
        equalize()

    elif op == 'b':
        tiltshift()

    elif op == 'c':
        laplgauss()

    elif op == 'd':
        homomorphicfilter()

    elif op == 'e':
        cannypoints()

    elif op == 'q':
        break

cv2.destroyAllWindows()
