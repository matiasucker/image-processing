import cv2 as cv

# Carregando a imagem
imagem_original = cv.imread('resources/imagem.png')
imagem_tratada = imagem_original.copy()

vetor = imagem_original.shape
w = int(vetor[0])
h = int(vetor[1])
x = int(vetor[0]/2)
y = int(vetor[1]/2)

cv.imwrite('tmp/quadrante_1.png', imagem_original[0 : x, y : w])
cv.imwrite('tmp/quadrante_2.png', imagem_original[0 : x, 0 : y])
cv.imwrite('tmp/quadrante_3.png', imagem_original[x : h, 0 : y])
cv.imwrite('tmp/quadrante_4.png', imagem_original[x : h, y : w])

imagem_tratada[0 : x, y : w] = cv.imread('tmp/quadrante_3.png')
imagem_tratada[0 : x, 0 : y] = cv.imread('tmp/quadrante_4.png')
imagem_tratada[x : h, 0 : y] = cv.imread('tmp/quadrante_1.png')
imagem_tratada[x : h, y : w] = cv.imread('tmp/quadrante_2.png')

cv.imwrite('output/trocaregioes.png', imagem_tratada)

cv.imshow('Imagem original', imagem_original)
cv.imshow('Troca regioes', imagem_tratada)

cv.waitKey(0)
