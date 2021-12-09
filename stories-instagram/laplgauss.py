import cv2
import numpy as np


def laplgauss():

    media = np.array([[0.1111, 0.1111, 0.1111],
                      [0.1111, 0.1111, 0.1111],
                      [0.1111, 0.1111, 0.1111]])

    gauss = np.array([[0.0625, 0.125, 0.0625],
                      [0.125, 0.25, 0.125],
                      [0.0625, 0.125, 0.0625]])

    horizontal = np.array([[-1, 0, 1],
                           [-2, 0, 2],
                           [-1, 0, 1]])

    vertical = np.array([[-1, -2, -1],
                         [0, 0, 0],
                         [1, 2, 1]])

    laplacian = np.array([[0, 1, 0],
                          [1, -4, 1],
                          [0, 1, 0]])

    boost = np.array([[0, -1, 0],
                      [-1, 5.2, -1],
                      [0, -1, 0]])

    def menu():
        print("Select Filter Function:")
        print("m - media")
        print("g - gauss")
        print("h - horizontal")
        print("v - vertical")
        print("l - laplacian")
        print("b - boost")
        print("x - laplaciano do gaussiano")

    menu()
    key = 0
    kernel_reference = media
    capture = cv2.VideoCapture(0)
    while True:
        exist_frame, frame = capture.read()
        frame = cv2.flip(frame, 0)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if not exist_frame:
            break

        cv2.imshow("Original", frame_gray)

        if key == 103 or key == 120:
            image_filtered = cv2.GaussianBlur(frame_gray, (3, 3), 0)
        else:
            image_filtered = cv2.filter2D(src=frame_gray, ddepth=-1, kernel=kernel_reference)

        if key == 108 or key == 120:
            # image_filtered = cv2.filter2D(src=image_filtered, ddepth=-1, kernel=laplacian, borderType=cv2.BORDER_DEFAULT)
            image_filtered = cv2.Laplacian(src=image_filtered, ddepth=-1, ksize=3)

        image_filtered = cv2.convertScaleAbs(image_filtered)

        cv2.imshow("Filter", image_filtered)

        if cv2.waitKey(1) & 0xFF == ord('m'):
            key = ord('m')
            kernel_reference = media
            print("\nMask Media\n" + str(media))
        if cv2.waitKey(1) & 0xFF == ord('g'):
            key = ord('g')
            kernel_reference = gauss
            print("\nMask Gauss\n" + str(gauss))
        if cv2.waitKey(1) & 0xFF == ord('h'):
            key = ord('h')
            kernel_reference = horizontal
            print("\nMask Horizontal\n" + str(horizontal))
        if cv2.waitKey(1) & 0xFF == ord('v'):
            key = ord('v')
            kernel_reference = vertical
            print("\nMask Vertical\n" + str(vertical))
        if cv2.waitKey(1) & 0xFF == ord('l'):
            key = ord('l')
            kernel_reference = laplacian
            print("\nMask Laplacian\n" + str(laplacian))
        if cv2.waitKey(1) & 0xFF == ord('b'):
            key = ord('b')
            kernel_reference = boost
            print("\nMask Boost\n" + str(boost))
        if cv2.waitKey(1) & 0xFF == ord('x'):
            key = ord('x')
            kernel_reference = gauss
            print("\nMask Laplaciano do Gaussiano\nMask Gauss\n" + str(gauss) + "\nMask Laplacian\n" + str(laplacian))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exit")
            break

    capture.release()
    cv2.destroyAllWindows()