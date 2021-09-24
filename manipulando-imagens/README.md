# Manipulando imagens

## Regions
implementar um programa regions.py. Esse programa deverá solicitar ao usuário as coordenadas de dois pontos P1 e P2 localizados dentro dos limites do tamanho da imagem e exibir que lhe for fornecida. Entretanto, a região definida pelo retângulo de vértices opostos definidos pelos pontos P1 e P2 será exibida com o negativo da imagem na região correspondente. O efeito é ilustrado na figura a seguir.

<table>
    <tr>
        <th>
            <img title="Original" src="resources/imagem.png"/>
            <img title="Manipulada" src="output/regions.png"/>
        </th>
    </tr>
</table>

```
import cv2 as cv

# Carregando a imagem
imagem_original = cv.imread('resources/imagem.png')
imagem_tratada = imagem_original.copy()

print("Informe as coordenadas para a seleção da imagem")
linha_inicio = int(input("P1 [linha] : "))
coluna_inicio = int(input("P1 [coluna] : "))

linha_fim = int(input("P2 [linha] : "))
coluna_fim = int(input("P2 [coluna] : "))

crop = imagem_tratada[linha_inicio:linha_fim, coluna_inicio:coluna_fim]

crop_negativa = cv.bitwise_not(crop)

imagem_tratada[linha_inicio:linha_fim, coluna_inicio:coluna_fim] = crop_negativa

cv.imwrite('output/regions.png', imagem_tratada)

cv.imshow('Imagem original', imagem_original)
cv.imshow('Imagem tratada', imagem_tratada)

cv.waitKey(0)
```



## Troca Regiões
Implementar um programa trocaregioes.cpp. Seu programa deverá trocar os quadrantes em diagonal na imagem. Explore o uso da classe Mat e seus construtores para criar as regiões que serão trocadas. O efeito é ilustrado na Figura 5.

<table>
    <tr>
        <th>
            <img title="Original" src="resources/imagem.png"/>
            <img title="Manipulada" src="output/trocaregioes.png"/>
        </th>
    </tr>
</table>

```
import cv2 as cv

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
```
