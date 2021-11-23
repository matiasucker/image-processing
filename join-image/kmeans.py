import cv2

ideal = cv2.imread("RX-CIO-ideal.png", cv2.IMREAD_COLOR)
real = cv2.imread("RX-CIO-real.png", cv2.IMREAD_COLOR)

resultado = cv2.addWeighted(real, 0.5, ideal, 0.5, 0.0)

cv2.imwrite("RX-CIO-Resultado.png", resultado)
