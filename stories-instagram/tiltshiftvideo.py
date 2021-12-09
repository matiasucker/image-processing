import cv2
import numpy as np


def tiltshiftvideo():

    def resize(frame):
        aspect_ratio = 640.0 / frame.shape[1]
        new_dimension = (640, int(frame.shape[0] * aspect_ratio))
        return cv2.resize(frame, new_dimension, fx=0, fy=0, interpolation=cv2.INTER_AREA)

    capture = cv2.VideoCapture('resources/tigre.mp4')
    exist_frame, frame = capture.read()

    frame = resize(frame)

    height, weigth = frame.shape[:2]

    cv2.namedWindow('Original')
    cv2.namedWindow('Tiltshift')

    cv2.createTrackbar('height', 'Tiltshift', int(height / 2), height, (lambda a: None))
    cv2.createTrackbar('d', 'Tiltshift', 50, 100, (lambda a: None))
    cv2.createTrackbar('vertical', 'Tiltshift', int(height / 2), height, (lambda a: None))
    cv2.createTrackbar('gauss', 'Tiltshift', 50, 100, (lambda a: None))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output/output.avi', fourcc, 5, (weigth, height))

    speed = 20
    discard_frames = 0
    while True:
        exist_frame, frame = capture.read()
        if not exist_frame:
            break

        frame = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
        frame = resize(frame)
        cv2.imshow('Original', frame)

        if discard_frames == 0:
            center = cv2.getTrackbarPos('height', 'Tiltshift')
            decay = cv2.getTrackbarPos('d', 'Tiltshift')
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

            mask = np.repeat(alpha_x, weigth).reshape(frame.shape[:2])

            image_blur = cv2.GaussianBlur(frame, (gauss * 2 + 1, gauss * 2 + 1), 0)
            if len(frame.shape) == 3:
                mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

            output = cv2.convertScaleAbs(frame * mask + image_blur * (1 - mask))

            cv2.imshow('Tiltshift', output)

            out.write(output)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exit")
                break

            discard_frames += 1
            discard_frames = discard_frames % speed

        else:
            discard_frames += 1
            discard_frames = discard_frames % speed

    capture.release()
    out.release()
    cv2.destroyAllWindows()
