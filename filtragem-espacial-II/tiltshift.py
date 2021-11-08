import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--color', type=str, default='rgb',
    help='Color space: "rgb" (default), "gray"')
args = vars(parser.parse_args())

image = cv2.imread('resources/image.png')
if args['color'] == 'rgb':
    image = cv2.cvtColor(image, cv2.IMREAD_COLOR)
elif args['color'] == 'gray':
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

height, weigth = image.shape[:2]

cv2.namedWindow('Original')
cv2.imshow('Original', image)

cv2.namedWindow('Tiltshift')

cv2.createTrackbar('height', 'Tiltshift', int(height / 2), height, (lambda a: None))
cv2.createTrackbar('decay', 'Tiltshift', 50, 100, (lambda a: None))
cv2.createTrackbar('vertical', 'Tiltshift', int(height / 2), height, (lambda a: None))
cv2.createTrackbar('gauss', 'Tiltshift', 50, 100, (lambda a: None))

while True:
    center = cv2.getTrackbarPos('height', 'Tiltshift')
    decay = cv2.getTrackbarPos('decay', 'Tiltshift')
    vertical = cv2.getTrackbarPos('vertical', 'Tiltshift')
    gauss = cv2.getTrackbarPos('gauss', 'Tiltshift')

    l1 = center - (vertical / 2)
    l2 = center + (vertical / 2)

    x = np.arange(height, dtype=np.float32)

    if decay == 0:
        decay = 1
        alpha_x = np.sign((np.tanh((x - l1) / decay) - np.tanh((x - l2) / decay)) - 1)
        alpha_x[alpha_x < 0] = 0
        alpha_x[alpha_x > 1] = 1
    else:
        alpha_x = (np.tanh((x - l1) / decay) - np.tanh((x - l2) / decay)) / 2

    mask = np.repeat(alpha_x, weigth).reshape(image.shape[:2])

    image_blur = cv2.GaussianBlur(image, (gauss * 2 + 1, gauss * 2 + 1), 0)
    if len(image.shape) == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    output = cv2.convertScaleAbs(image * mask + image_blur * (1 - mask))

    cv2.imshow('Tiltshift', output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('output/output.png', output)
        print("Exit")
        break

cv2.destroyAllWindows()
