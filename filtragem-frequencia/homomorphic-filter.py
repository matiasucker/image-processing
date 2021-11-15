import cv2
import numpy as np
from math import exp, sqrt

image = cv2.imread("resources/p3.jpg", 0)
height, width = image.shape[:2]

dft_M = cv2.getOptimalDFTSize(height)
dft_N = cv2.getOptimalDFTSize(width)


yh, yl, c, d0 = 0, 0, 0, 0

y_track, d0_track, c_track = 0, 0, 0

complex_image = 0


def homomorphic():
    global yh, yl, c, d0, complex_image
    d = np.zeros(complex_image.shape, dtype=np.float32)

    for u in range(dft_M):
        for v in range(dft_N):
            d[u, v] = sqrt((u - dft_M / 2.0) * (u - dft_M / 2.0) + (v - dft_N / 2.0) * (v - dft_N / 2.0))

    d2 = cv2.multiply(d, d) / (d0 * d0)
    re = np.exp(- c * d2)
    h = (yh - yl) * (1 - re) + yl

    filtered = cv2.mulSpectrums(complex_image, h, 0)

    filtered = np.fft.ifftshift(filtered)
    filtered = cv2.idft(filtered)

    filtered = cv2.magnitude(filtered[:, :, 0], filtered[:, :, 1])
    cv2.normalize(filtered, filtered, 0, 1, cv2.NORM_MINMAX)

    filtered = np.exp(filtered - 1.0)
    cv2.normalize(filtered, filtered, 0, 1, cv2.NORM_MINMAX)

    cv2.namedWindow('homomorphic', cv2.WINDOW_AUTOSIZE)
    cv2.imshow("homomorphic", filtered)
    cv2.imwrite("output/output.png", filtered * 255)


def setyl(y_track):
    global yl
    yl = y_track / 100.0
    if yl == 0:
        yl = 0.1
    if yl > yh:
        yl = yh - 1
    homomorphic()


def setyh(y_track):
    global yh
    yh = y_track / 100.0
    if yh == 0:
        yh = 0.1
    if yl > yh:
        yh = yl + 1
    homomorphic()


def setc(c_track):
    global c
    c = c_track / 1000.0
    if c == 0:
        c = 1
    homomorphic()


def setd0(d0_track):
    global d0
    d0 = d0_track
    if d0 == 0:
        d0 = 1
    homomorphic()


def main():

    padded = cv2.copyMakeBorder(image, 0, dft_M - height, 0, dft_N - width, cv2.BORDER_CONSTANT, 0)

    padded = np.log(padded + 1.0)

    global complex_image
    complex_image = cv2.dft(np.float32(padded), flags=cv2.DFT_COMPLEX_OUTPUT)
    # complex_image = np.fft.fft2(padded)

    complex_image = np.fft.fftshift(complex_image)

    magnitude_spectrum = 15 * np.log(cv2.magnitude(complex_image[:, :, 0], complex_image[:, :, 1]))
    # magnitude_spectrum = 15 * np.log(np.abs(complex_image))

    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.imshow("Image", image)
    cv2.imwrite("output/original-gray.png", image)
    cv2.resizeWindow("Image", 600, 600)

    cv2.namedWindow('DFT', cv2.WINDOW_NORMAL)
    cv2.imshow("DFT", np.uint8(magnitude_spectrum))
    cv2.imwrite("output/dft.png", np.uint8(magnitude_spectrum))
    cv2.resizeWindow("DFT", 600, 600)

    cv2.createTrackbar("YL", "Image", y_track, 100, setyl)
    cv2.createTrackbar("YH", "Image", y_track, 100, setyh)
    cv2.createTrackbar("C", "Image", c_track, 100, setc)
    cv2.createTrackbar("D0", "Image", d0_track, 100, setd0)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
