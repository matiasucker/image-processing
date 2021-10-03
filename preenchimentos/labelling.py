import cv2
import numpy as np
import math
import sys

# Leitura da imagem
image = cv2.imread('resources/bolhas.png')

# Transformação da imagem para escala de cinza
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicação do desfoque Gaussian Blur na imagem, ajuda a remover algumas das bordas de alta frequência,
# com as quais não estamos preocupados e nos permite obter uma segmentação mais limpa
image_gray_blurred = cv2.GaussianBlur(image_gray, (7, 7), 0)

# Obtendo as dimensões da imagem, altura e largura.
height, width = image.shape[:2]

# Ponto no qual será usdado como semente para utilizar a função floodFill
seedpoint = [0, 0]

# Análise das bordas esquerda e direita
for i in range(height):

    # Eliminação de objetos na borda esquerda da cena
    if image_gray_blurred[i, 0] == 255:
        seedpoint[0] = 0
        seedpoint[1] = i
        cv2.floodFill(image, None, seedpoint, 0)

    # Eliminação de objetos na borda direita da cena
    if image_gray_blurred[i, width-1] == 255:
        seedpoint[0] = width-1
        seedpoint[1] = i
        cv2.floodFill(image, None, seedpoint, 0)

# Análise das bordas superior e inferior
for j in range(width):

    # Eliminação de objetos na borda superior da cena
    if image_gray_blurred[0, j] == 255:
        seedpoint[0] = j
        seedpoint[1] = 0
        cv2.floodFill(image, None, seedpoint, 0)

    # Eliminação de objetos na borda inferior da cena
    if image_gray_blurred[height-1, j] == 255:
        seedpoint[0] = j
        seedpoint[1] = height-1
        cv2.floodFill(image, None, seedpoint, 0)



# Identificando regiões sem buracos
nobjects = 0
for i in range(height):
    for j in range(width):
        if image_gray_blurred[i, j] == 255:
            nobjects += 1
            seedpoint[0] = j
            seedpoint[1] = i
            cv2.floodFill(image, None, seedpoint, 100)


# Obtendo o threshold da imagem
# Primeiro argumento: a imagem
# Segundo argumento: o valor de threshold, pixels com valor menor recebem 0, pixels com valor maior recebem o output (255)
# Terceito argumento: o valor de output (255 é o valor máximo para uma imagem em escala de cinza)
# Quarto argumento: função que inverte, pixels com valor menor do threshold recebem 255, pixels com valor maior recebem 0
(T, threshInv) = cv2.threshold(image_gray_blurred, 200, 255, cv2.THRESH_BINARY_INV)

# Obtendo os contornos dos objetos e a hierarquia destes contornos
# Primeiro argumento: A imagem
# Segundo argumento: Recupera todos os contornos e os organiza em uma hierarquia de dois níveis
(contours, hierarchy) = cv2.findContours(threshInv, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)


print("A figura tem " + str(nobjects) + " objetos sem buracos")


cv2.imshow('gray',image)

print(image.shape)

cv2.waitKey(0)


