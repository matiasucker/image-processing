# importação da biblioteca OpenCV
import cv2

# Leitura da imagem
image = cv2.imread('resources/bolhas.png')

# Transformação da imagem para escala de cinza
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Cópia da imagem original
imagem_tratada = image_gray.copy()

# Obtendo as dimensões da imagem: altura e largura.
height, width = image.shape[:2]

# Ponto no qual será usdado como semente para utilizar a função floodFill
seedpoint = [0, 0]

# Análise das bordas esquerda e direita
for i in range(height):

    # Eliminação de objetos na borda esquerda da cena
    if imagem_tratada[i, 0] == 255:
        seedpoint[0] = 0
        seedpoint[1] = i
        cv2.floodFill(imagem_tratada, None, seedpoint, 0)

    # Eliminação de objetos na borda direita da cena
    if imagem_tratada[i, width-1] == 255:
        seedpoint[0] = width-1
        seedpoint[1] = i
        cv2.floodFill(imagem_tratada, None, seedpoint, 0)

# Análise das bordas superior e inferior
for j in range(width):

    # Eliminação de objetos na borda superior da cena
    if imagem_tratada[0, j] == 255:
        seedpoint[0] = j
        seedpoint[1] = 0
        cv2.floodFill(imagem_tratada, None, seedpoint, 0)

    # Eliminação de objetos na borda inferior da cena
    if imagem_tratada[height-1, j] == 255:
        seedpoint[0] = j
        seedpoint[1] = height-1
        cv2.floodFill(imagem_tratada, None, seedpoint, 0)

# A imagem em escala de cinza tem o fundo com o tom no valor 0,
# vamos alterar para 1 para diferenciar na busca por objetos com buracos
seedpoint[0] = 0
seedpoint[1] = 0
cv2.floodFill(imagem_tratada, None, seedpoint, 1)

# Identificando regiões com buracos
nobjects_com_buracos = 0
for i in range(height):
    for j in range(width):
        if imagem_tratada[i, j] == 0:
            if imagem_tratada[i, j -1] == 255:
                nobjects_com_buracos += 1
                seedpoint[0] = j-1
                seedpoint[1] = i
                cv2.floodFill(imagem_tratada, None, seedpoint, 100)

# Identificando regiões sem buracos
nobjects_sem_buracos = 0
for i in range(height):
    for j in range(width):
        if imagem_tratada[i, j] == 255:
            nobjects_sem_buracos += 1
            seedpoint[0] = j
            seedpoint[1] = i
            cv2.floodFill(imagem_tratada, None, seedpoint, 50)

# Identificando regiões na imagem original, sem aprimoração
nobjects = 0
for i in range(height):
    for j in range(width):
        if image_gray[i, j] == 255:
            nobjects += 1
            seedpoint[0] = j
            seedpoint[1] = i
            cv2.floodFill(image_gray, None, seedpoint, nobjects)

# Impressão da saída normal, sem aprimoração
cv2.imwrite('output/Saida-normal.PNG', image_gray)
cv2.imshow('Saida do programa labeling', image_gray)
print("A figura tem " + str(nobjects) + " objetos no total")

# Impressão da saída do algoritmo aprimorado
cv2.imwrite('output/Saida-aprimorada.PNG', imagem_tratada)
cv2.imshow('Saida do programa labeling aprimorado', imagem_tratada)
print("A figura tem " + str(nobjects_sem_buracos) + " objetos sem buracos que não tocam as bordas da imagem")
print("A figura tem " + str(nobjects_com_buracos) + " objetos com buracos que não tocam as bordas da imagem")

cv2.waitKey(0)
