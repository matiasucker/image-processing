import cv2 as cv

imagem_original = cv.imread('resources/imagem.png')
imagem_tratada = imagem_original.copy()

print("Informe as coordenadas para a seleção da imagem")
linha_inicio = int(input("P1 [linha] : "))
coluna_inicio = int(input("P1 [coluna] : "))

linha_fim = int(input("P2 [linha] : "))
coluna_fim = int(input("P2 [coluna] : "))

roi = imagem_tratada[linha_inicio:linha_fim, coluna_inicio:coluna_fim]

roi_negativa = cv.bitwise_not(roi)

imagem_tratada[linha_inicio:linha_fim, coluna_inicio:coluna_fim] = roi_negativa

cv.imwrite('output/regions.png', imagem_tratada)

cv.imshow('Imagem original', imagem_original)
cv.imshow('Imagem tratada', imagem_tratada)

cv.waitKey(0)
