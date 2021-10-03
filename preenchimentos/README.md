# Preenchimentos

## Requisitos
- Python 3.8
- OpenCV 4.5.3

## 3.2 Exercícios
Observando-se o programa labeling.cpp como exemplo, é possível verificar que caso existam mais de 255 objetos na cena, o processo de rotulação poderá ficar comprometido. Identifique a situação em que isso ocorre e proponha uma solução para este problema.

### Resposta
Se existir mais de 255 objetos na cena, o processo de rotulação ficará comprometido, porque estamos trabalhando com a imagem em tons de cinza, os tons de cinza variam de 0 à 255 e contém apenas um canal, não sendo possível criar rótulos únicos diferente destes valores.

Para solucionar este problema, precisamos trabalhar com a imagem em formato RGB, o formato RGB possui 3 canais ((0 à 255), (0 à 255), (0 à 255)), criando milhares de possibilidades para rotulação dos objetos encontrados na cena.
Caso a imagem recebida seja em escala de cinza, podemos utilizar uma função do OpenCV para converter de escala de cinza para o formato RGB.
A função para conversão é ```cv.COLOR_GRAY2BGR```, e um exemplo de aplicação em Python seria ```imagem_rgb = cv2.cvtColor(imagem_gray, cv.COLOR_GRAY2BGR)```



-------------------------------------------------------------------------------------------------------------------------------------------------------------

## 3.2 Exercícios
Aprimore o algoritmo de contagem apresentado para identificar regiões com ou sem buracos internos que existam na cena. Assuma que objetos com mais de um buraco podem existir. Inclua suporte no seu algoritmo para não contar bolhas que tocam as bordas da imagem. Não se pode presumir, a priori, que elas tenham buracos ou não.

<table>
    <tr>
        <th align="Center">Imagem original</th>
        <th align="Center">Imagem manipulada</th>
    </tr> 
    <tr>
        <td>
            <img title="Original" src="resources/imagem.png"/>
        </td>
        <td>
            <img title="Manipulada" src="output/trocaregioes.png"/>
        </td>
    </tr>
</table>

## Funcionamento do código

Importação da biblioteca OpenCV
```
import cv2 as cv
```

Carregando a imagem original para uma variável e realizando uma cópia da mesma.
O conteúdo da variável "imagem_original" será mantido para exibição posterior.
O conteúdo da variável "imagem_tratada" será alterado para cumprir com o objetivo do progama.
```
imagem_original = cv.imread('resources/imagem.png')
imagem_tratada = imagem_original.copy()
```

Usando a função shape sobre a imagem para extrair a suas features, com essa função é possível extrair em um vetor as informações do tamanho da largura e altura da imagem.
A primeira posição do vetor (vetor[0]) será a largura da imagem, a segunda posição do vetor (vetor[1]) será a altura da imagem, ambas as informações são salvas nas variáveis "w' e "h".
Para descobrir o ponto médio, ou seja, o meio da imagem, pode-se dividir os valores das variáveis w e h por dois, e salvar os resultados em outas duas variáveis "x" e "y".
O ponto médio será essencial para dividir a imagem em quatro quadrantes.
```
vetor = imagem_original.shape
w = int(vetor[0])
h = int(vetor[1])
x = int(vetor[0]/2)
y = int(vetor[1]/2)
```

Dividindo a imagem em quatro quadrantes, e salvando cada quadrante de imagem. Neste caso é utilizado as variáveis "w", "h", "x" e "y" para selecionar as áreas de interesse em quatro quadrantes.
```
cv.imwrite('tmp/quadrante_1.png', imagem_original[0 : x, y : w])
cv.imwrite('tmp/quadrante_2.png', imagem_original[0 : x, 0 : y])
cv.imwrite('tmp/quadrante_3.png', imagem_original[x : h, 0 : y])
cv.imwrite('tmp/quadrante_4.png', imagem_original[x : h, y : w])
```

Inserindo os quadrantes de imagem trocando as diagonais.
```
imagem_tratada[0 : x, y : w] = cv.imread('tmp/quadrante_3.png')
imagem_tratada[0 : x, 0 : y] = cv.imread('tmp/quadrante_4.png')
imagem_tratada[x : h, 0 : y] = cv.imread('tmp/quadrante_1.png')
imagem_tratada[x : h, y : w] = cv.imread('tmp/quadrante_2.png')
```

Salvamos a imagem tratada, já com as diagonais trocadas.
```
cv.imwrite('output/trocaregioes.png', imagem_tratada)
```

Imprimimos a imagem original e a imagem tratada para comparação.
```
cv.imshow('Imagem original', imagem_original)
cv.imshow('Troca regioes', imagem_tratada)
```

Função para o programa aguardar o fim da execução quando uma tecla for pressionada.
```
cv.waitKey(0)
```

## Exemplo de funcionamento

<table>
    <tr>
        <th align="Center">Exemplo de entrada e a saída resultante</th>
    </tr> 
    <tr>
        <td>
            <img title="Exemplo" src="tmp/exemplo_trocaregioes.png"/>
        </td>
    </tr>
</table>

## Código
```
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
```
---------------------------------------------------------------------------------------------------------------------------------------------------

## Código original labeling.cpp em C++ 

```
#include <iostream>
#include <opencv2/opencv.hpp>

using namespace cv;

int main(int argc, char** argv){
  cv::Mat image, realce;
  int width, height;
  int nobjects;

  cv::Point p;
  image = cv::imread(argv[1], cv::IMREAD_GRAYSCALE);

  if(!image.data){
    std::cout << "imagem nao carregou corretamente\n";
    return(-1);
  }

  width=image.cols;
  height=image.rows;
  std::cout << width << "x" << height << std::endl;

  p.x=0;
  p.y=0;

  // busca objetos presentes
  nobjects=0;
  for(int i=0; i<height; i++){
    for(int j=0; j<width; j++){
      if(image.at<uchar>(i,j) == 255){
        // achou um objeto
        nobjects++;
        p.x=j;
        p.y=i;
  		// preenche o objeto com o contador
		  cv::floodFill(image,p,nobjects);
      }
    }
  }
  std::cout << "a figura tem " << nobjects << " bolhas\n";
  cv::equalizeHist(image, realce);
  cv::imshow("image", image);
  cv::imshow("realce", realce);
  cv::imwrite("labeling.png", image);
  cv::waitKey();
  return 0;
}
```
