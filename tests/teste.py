import cv2

frame = cv2.imread('resources/image.png', cv2.IMREAD_COLOR)

cv2.imshow('Original', frame)

aspect_ratio = 640.0 / frame.shape[1]
new_dimension = (640, int(frame.shape[0] * aspect_ratio))
frame_resize = cv2.resize(frame, new_dimension, fx=0, fy=0, interpolation=cv2.INTER_AREA)

cv2.imshow('Resize', frame_resize)

cv2.waitKey(0)
