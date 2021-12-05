import cv2

ideal = cv2.imread("resources/ideal.png", cv2.IMREAD_COLOR)
real = cv2.imread("resources/real.png", cv2.IMREAD_COLOR)

resultado = cv2.addWeighted(real, 0.5, ideal, 0.5, 0.0)

cv2.imwrite("output/Resultado.png", resultado)
