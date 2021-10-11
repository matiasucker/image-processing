# Histogramas

## Requisitos
- Python 3.8
- OpenCV 4.5.3

## 4.2 Exercícios
Utilizando o programa exemplos/histogram.cpp como referência, implemente um programa equalize.cpp. Este deverá, para cada imagem capturada, realizar a equalização do histogram antes de exibir a imagem. Teste sua implementação apontando a câmera para ambientes com iluminações variadas e observando o efeito gerado. Assuma que as imagens processadas serão em tons de cinza.

Utilizando o programa exemplos/histogram.cpp como referência, implemente um programa motiondetector.cpp. Este deverá continuamente calcular o histograma da imagem (apenas uma componente de cor é suficiente) e compará-lo com o último histograma calculado. Quando a diferença entre estes ultrapassar um limiar pré-estabelecido, ative um alarme. Utilize uma função de comparação que julgar conveniente.

# Programa Equalize.py
Desenvolvido em Python

## Exemplos de entrada e saída

<table>
    <tr>
        <th align="Center">Histograma RGB</th>
    </tr> 
    <tr>
        <td>
            <img title="Histograma RGB" src="output/rgb.png"/>
        </td>
    </tr>
</table>
\
<table>
    <tr>
        <th align="Center">Histograma RGB equalizado</th>
    </tr> 
    <tr>
        <td>
            <img title="Histograma RGB equalizado" src="output/rgb_equalized.png"/>
        </td>
    </tr>
</table>

<table>
    <tr>
        <th align="Center">Histograma GRAY</th>
    </tr> 
    <tr>
        <td>
            <img title="Histograma GRAY" src="output/gray.png"/>
        </td>
    </tr>
</table>

<table>
    <tr>
        <th align="Center">Histograma GRAY equalizado</th>
    </tr> 
    <tr>
        <td>
            <img title="Histograma GRAY equalizado" src="output/gray_equalized.png"/>
        </td>
    </tr>
</table>

## Funcionamento do código

Importação das bibliotecas
```
import numpy as np
import matplotlib.pyplot as plt
import argparse
import cv2
import time
```
\
Analisador de argumentos por linha de comando, usado para escolher se o vídeo será tratado em RGB ou CINZA, e ainda a quantidade de bins para plotar no gráfico do histograma.
```
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--color', type=str, default='gray',
    help='Color space: "gray" (default), "rgb"')
parser.add_argument('-b', '--bins', type=int, default=256,
    help='Number of bins per channel (default 256)')
args = vars(parser.parse_args())

color = args['color']
bins = args['bins']
```
\
Prepara uma figura [fig] e um array de eixos [ax] para plotagem.
```
fig, ax = plt.subplots()
```
\
Verifica se o argumento passado por linha de comando foi RGB ou CINZA, para cada caso será inserido o título apropriado na plotagem.
```
if color == 'rgb':
    ax.set_title('Histograma RGB')
else:
    ax.set_title('Histograma escala de cinza')
```
\
Inserção dos labels nos eixos X e Y na plotagem.
```
ax.set_xlabel('Bins')
ax.set_ylabel('Frequency (N of Pixels)')
```
\
Verifica se o argumento passado por linha de comando foi RGB ou CINZA, se foi RGB é configurado um eixo para cada linha RGB. Se foi CINZA, apenas um eixo é configurado.\
Os parâmetros para configuração da função plot() são:\
np.arange(bins) -> um range com o tamanho dos bins\
np.zeros((bins, )) -> um array preenchido com zeros com o tamanho dos bins\
c -> a cor
lw -> largura da linha\
alpha -> scalar\
label -> nome
```
lw = 3
alpha = 0.5
if color == 'rgb':
    lineR, = ax.plot(np.arange(bins), np.zeros((bins,)), c='r', lw=lw, alpha=alpha, label='Red')
    lineG, = ax.plot(np.arange(bins), np.zeros((bins,)), c='g', lw=lw, alpha=alpha, label='Green')
    lineB, = ax.plot(np.arange(bins), np.zeros((bins,)), c='b', lw=lw, alpha=alpha, label='Blue')
else:
    lineGray, = ax.plot(np.arange(bins), np.zeros((bins,1)), c='k', lw=lw, label='intensity')
```
\
Configura os limites dos eixos X e Y
```
ax.set_xlim(0, bins)
ax.set_ylim(0, bins + 50)
```
\
Habilita a legenda.\
Torna a plotagem interativa com o plt.ion()\
Faz a plotagem com o plt.show()
```
ax.legend()
plt.ion()
plt.show()
```
\
Captura o vídeo da webcam.
```
capture = cv2.VideoCapture(0)
```
\
Início do loop infinito, até que a tecla 'q' seja pressionada.\
A cada iteração do while, captura cada frame e armazena em 'frame', e também uma condição booleana True ou False se existe frame em 'existe_frame'.\
Faz o flip do frame para inverter corrigindo a amostragem.\
Testa se não existir frame, sai do loop infinito e encerra a execução do programa.
```
while True:
    existe_frame, frame = capture.read()

    frame = cv2.flip(frame, 0)

    if not existe_frame:
        break
```
\
Testa se a cor é RGB.\
Se sim, faz um split do frame, separando em seus respectivos canais R G B.
```
    if color == 'rgb':
        (b, g, r) = cv2.split(frame)
```
\
Para cada canal, faz a equalização.
```
        b = cv2.equalizeHist(b)
        g = cv2.equalizeHist(g)
        r = cv2.equalizeHist(r)
```
\
Realiza o merge dos canais R G B em um único frame.\
Mostra o frame RGB equalizado.
```
        frame_equalized = cv2.merge((b, g, r))
        cv2.imshow('RGB equalized', frame_equalized)
```
\
Calcula o histograma para cada canal R G B
```
        histogramR = cv2.calcHist([r], [0], None, [bins], [0, 255])
        histogramG = cv2.calcHist([g], [0], None, [bins], [0, 255])
        histogramB = cv2.calcHist([b], [0], None, [bins], [0, 255])
```
\
Normaliza cada canal R G B individualmente, para melhorar a visualização da plotagem dos histogramas.
```
        cv2.normalize(histogramR, histogramR, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(histogramG, histogramG, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(histogramB, histogramB, 0, 255, cv2.NORM_MINMAX)
```
\
Para cada linha da plotagem, é carregado o histograma correspondente.
```
        lineR.set_ydata(histogramR)
        lineG.set_ydata(histogramG)
        lineB.set_ydata(histogramB)
```
\
Caso não for passado a cor de argumento por linha de comando, a execução cairá aqui, para tratamento do frame em escala de cinza.\
O frame é convertido para escala de cinza.
```
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```
\
O frame em escala de cinza é equalizado e mostrado.
```
        frame_equalized = cv2.equalizeHist(gray)
        cv2.imshow('Grayscale equalized', frame_equalized)
```
\
Calculado o histograma.
```
        histogramGRAY = cv2.calcHist([frame_equalized], [0], None, [bins], [0, 255])
```
\
Normaliza o canal cinza, para melhorar a visualização da plotagem.
```
        cv2.normalize(histogramGRAY, histogramGRAY, 0, 255, cv2.NORM_MINMAX)
```
\
Para a linha em escala de cinza, é carregado o seu histograma.
```
        lineGray.set_ydata(histogramGRAY)
```
\
Atualiza a plotagem automaticamente e limpa a plotagem antiga.
```
    fig.canvas.draw()
    fig.canvas.flush_events()
```
\
Aguarda um tempo para a próxima leitura.
```
    time.sleep(0.1)
```
\
Testa se a tecla pressionada foi 'q', se for encerra o loop infinito e o programa encerra sua execução.
```
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```
\
Libera todos os recursos utilizados, fecha as janelas abertas e encerra o programa.
```
capture.release()
cv2.destroyAllWindows()
```

## Código completo em Python
```
import numpy as np
import matplotlib.pyplot as plt
import argparse
import cv2
import time

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--color', type=str, default='gray',
    help='Color space: "gray" (default), "rgb"')
parser.add_argument('-b', '--bins', type=int, default=256,
    help='Number of bins per channel (default 256)')
args = vars(parser.parse_args())

color = args['color']
bins = args['bins']

fig, ax = plt.subplots()

if color == 'rgb':
    ax.set_title('Histograma RGB equalizado')
else:
    ax.set_title('Histograma escala de cinza equalizado')

ax.set_xlabel('Bins')
ax.set_ylabel('Frequency (N of Pixels)')

lw = 3
alpha = 0.5
if color == 'rgb':
    lineR, = ax.plot(np.arange(bins), np.zeros((bins,)), c='r', lw=lw, alpha=alpha, label='Red')
    lineG, = ax.plot(np.arange(bins), np.zeros((bins,)), c='g', lw=lw, alpha=alpha, label='Green')
    lineB, = ax.plot(np.arange(bins), np.zeros((bins,)), c='b', lw=lw, alpha=alpha, label='Blue')
else:
    lineGray, = ax.plot(np.arange(bins), np.zeros((bins,1)), c='k', lw=lw, label='intensity')

ax.set_xlim(0, bins)
ax.set_ylim(0, bins + 50)
ax.legend()
plt.ion()
plt.show()

capture = cv2.VideoCapture(0)
while True:
    existe_frame, frame = capture.read()

    frame = cv2.flip(frame, 0)

    if not existe_frame:
        break

    if color == 'rgb':
        (b, g, r) = cv2.split(frame)
        b = cv2.equalizeHist(b)
        g = cv2.equalizeHist(g)
        r = cv2.equalizeHist(r)
        frame_equalized = cv2.merge((b, g, r))
        cv2.imshow('RGB equalized', frame_equalized)

        histogramR = cv2.calcHist([r], [0], None, [bins], [0, 255])
        histogramG = cv2.calcHist([g], [0], None, [bins], [0, 255])
        histogramB = cv2.calcHist([b], [0], None, [bins], [0, 255])

        cv2.normalize(histogramR, histogramR, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(histogramG, histogramG, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(histogramB, histogramB, 0, 255, cv2.NORM_MINMAX)

        lineR.set_ydata(histogramR)
        lineG.set_ydata(histogramG)
        lineB.set_ydata(histogramB)

    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_equalized = cv2.equalizeHist(gray)
        cv2.imshow('Grayscale equalized', frame_equalized)

        histogramGRAY = cv2.calcHist([frame_equalized], [0], None, [bins], [0, 255])

        cv2.normalize(histogramGRAY, histogramGRAY, 0, 255, cv2.NORM_MINMAX)

        lineGray.set_ydata(histogramGRAY)

    fig.canvas.draw()
    fig.canvas.flush_events()

    time.sleep(0.1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
```
-------------------------------------------------------------------
# Programa motion_detector.py
Desenvolvido em Python

## Exemplos de entrada e saída

<table>
    <tr>
        <th align="Center">Histograma RGB sem movimentos</th>
    </tr> 
    <tr>
        <td>
            <img title="Histograma RGB sem movimentos" src="output/rgb_motionless.png"/>
        </td>
    </tr>
</table>
\
<table>
    <tr>
        <th align="Center">Histograma RGB com movimentos detectados</th>
    </tr> 
    <tr>
        <td>
            <img title="Histograma RGB com movimentos detectados" src="output/rgb_motion.png"/>
        </td>
    </tr>
</table>

<table>
    <tr>
        <th align="Center">Histograma GRAY sem movimentos</th>
    </tr> 
    <tr>
        <td>
            <img title="Histograma GRAY sem movimentos" src="output/gray_motionless.png"/>
        </td>
    </tr>
</table>

<table>
    <tr>
        <th align="Center">Histograma GRAY com movimentos detectados</th>
    </tr> 
    <tr>
        <td>
            <img title="Histograma GRAY com movimentos detectados" src="output/gray_motion_.png"/>
        </td>
    </tr>
</table>

## Funcionamento do código

Importação das bibliotecas
```
import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
import time
```
\
Analisador de argumentos por linha de comando, usado para escolher se o vídeo será tratado em RGB ou CINZA, e ainda a quantidade de bins para plotar no gráfico do histograma.
```
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--color', type=str, default='gray',
    help='Color space: "gray" (default), "rgb"')
parser.add_argument('-b', '--bins', type=int, default=256,
    help='Number of bins per channel (default 256)')
parser.add_argument('-s', '--sim', type=float, default=0.995,
    help='Similarity of histograms (default 0.995)')
args = vars(parser.parse_args())

color = args['color']
bins = args['bins']
sim = args['sim']
```
\
Prepara uma figura [fig] e um array de eixos [ax] para plotagem.
```
fig, ax = plt.subplots()
```
\
Verifica se o argumento passado por linha de comando foi RGB ou CINZA, para cada caso será inserido o título apropriado na plotagem.
```
if color == 'rgb':
    ax.set_title('Histograma RGB')
else:
    ax.set_title('Histograma escala de cinza')
```
\
Inserção dos labels nos eixos X e Y na plotagem.
```
ax.set_xlabel('Bins')
ax.set_ylabel('Frequency (N of Pixels)')
```
\
Verifica se o argumento passado por linha de comando foi RGB ou CINZA, se foi RGB é configurado um eixo para cada linha RGB. Se foi CINZA, apenas um eixo é configurado.\
Os parâmetros para configuração da função plot() são:\
np.arange(bins) -> um range com o tamanho dos bins\
np.zeros((bins, )) -> um array preenchido com zeros com o tamanho dos bins\
c -> a cor
lw -> largura da linha\
alpha -> scalar\
label -> nome
```
lw = 3
alpha = 0.5
if color == 'rgb':
    lineR, = ax.plot(np.arange(bins), np.zeros((bins,)), c='r', lw=lw, alpha=alpha, label='Red')
    lineG, = ax.plot(np.arange(bins), np.zeros((bins,)), c='g', lw=lw, alpha=alpha, label='Green')
    lineB, = ax.plot(np.arange(bins), np.zeros((bins,)), c='b', lw=lw, alpha=alpha, label='Blue')
```
\
Cria três canais R G B através do np.zeros e calcula o histograma de cada canal, será utilizado como comparação posterior para ativação do alarme.
```
    image_referenceR = np.zeros((480, 640), dtype="uint8")
    histogram_referenceR = cv2.calcHist([image_referenceR], [0], None, [bins], [0, 255])

    image_referenceG = np.zeros((480, 640), dtype="uint8")
    histogram_referenceG = cv2.calcHist([image_referenceG], [0], None, [bins], [0, 255])

    image_referenceB = np.zeros((480, 640), dtype="uint8")
    histogram_referenceB = cv2.calcHist([image_referenceB], [0], None, [bins], [0, 255])
```
\
Caso o frame não for RGB, será então em escala de CINZA.\
Os parâmetros para configuração da função plot() são:\
np.arange(bins) -> um range com o tamanho dos bins\
np.zeros((bins, )) -> um array preenchido com zeros com o tamanho dos bins\
c -> a cor
lw -> largura da linha\
alpha -> scalar\
label -> nome
```
else:
    lineGray, = ax.plot(np.arange(bins), np.zeros((bins,1)), c='k', lw=lw, label='intensity')
```
\
Cria um canal cinza através do np.zeros e calcula o histograma deste canal, será utilizado como comparação posterior para ativação do alarme.
```
    image_referenceGRAY = np.zeros((480, 640), dtype="uint8")
    histogram_referenceGRAY = cv2.calcHist([image_referenceGRAY], [0], None, [bins], [0, 255])
```


\
Configura os limites dos eixos X e Y
```
ax.set_xlim(0, bins)
ax.set_ylim(0, bins + 50)
```
\
Habilita a legenda.\
Torna a plotagem interativa com o plt.ion()\
Faz a plotagem com o plt.show()
```
ax.legend()
plt.ion()
plt.show()
```
\
Captura o vídeo da webcam.
```
capture = cv2.VideoCapture(0)
```
\
Início do loop infinito, até que a tecla 'q' seja pressionada.\
A cada iteração do while, captura cada frame e armazena em 'frame', e também uma condição booleana True ou False se existe frame em 'existe_frame'.\
Faz o flip do frame para inverter corrigindo a amostragem.\
Testa se não existir frame, sai do loop infinito e encerra a execução do programa.
```
while True:
    existe_frame, frame = capture.read()

    frame = cv2.flip(frame, 0)

    if not existe_frame:
        break
```
\
Testa se a cor é RGB.\
Se sim, mostra o frame e faz um split do frame, separando em seus respectivos canais R G B.
```
    if color == 'rgb':
        cv2.imshow('RGB', frame)
        (b, g, r) = cv2.split(frame)
```
\
Calcula o histograma de cada canal R G B.
```
        histogramR = cv2.calcHist([r], [0], None, [bins], [0, 255])
        histogramG = cv2.calcHist([g], [0], None, [bins], [0, 255])
        histogramB = cv2.calcHist([b], [0], None, [bins], [0, 255])
```
\
Normaliza cada canal R G B individualmente, para melhorar a visualização da plotagem dos histogramas.
```
        cv2.normalize(histogramR, histogramR, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(histogramG, histogramG, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(histogramB, histogramB, 0, 255, cv2.NORM_MINMAX)
```
\
Para cada linha da plotagem, é carregado o histograma correspondente.
```
        lineR.set_ydata(histogramR)
        lineG.set_ydata(histogramG)
        lineB.set_ydata(histogramB)
```
\
Para cada canal R G B é realizada a comparação do respectivo histograma atual com o histograma anterior armazenado.
```
        similarityR = cv2.compareHist(histogram_referenceR, histogramR, cv2.HISTCMP_CORREL)
        similarityG = cv2.compareHist(histogram_referenceG, histogramG, cv2.HISTCMP_CORREL)
        similarityB = cv2.compareHist(histogram_referenceB, histogramB, cv2.HISTCMP_CORREL)
```
\
É calculada a média das similaridades dos canais R G B e impresso esta média.
```
        similarity = (similarityR + similarityG + similarityB) / 3
        print(similarity)
```
\
É testado se a similaridade calculada for menor que um valor estipulado, se sim, significa que os frames são diferentes, e um alarme deve ser acionado.
```
        if (similarityR < sim) or (similarityG < sim) or (similarityB < sim):
            print("[INFO] ALARME: movimento detectado " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
```
\
É realizada a cópia do histograma de cada canal para ser usado como referência para a próxima iteração do laço 'while'.
```
        histogram_referenceR = histogramR.copy()
        histogram_referenceG = histogramG.copy()
        histogram_referenceB = histogramB.copy()
```
\
Caso o frame não for RGB, será em escala de cinza.
```
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Grayscale', gray)
```
\
Calcula o histograma do canal cinza.
```
histogramGRAY = cv2.calcHist([gray], [0], None, [bins], [0, 255])
```
\
Normaliza o canal cinza, para melhorar a visualização da plotagem.
```
cv2.normalize(histogramGRAY, histogramGRAY, 0, 255, cv2.NORM_MINMAX)
```
\
Calcula a similaridade do histograma atual com o histograma anterior armazenado como referência.
```
similarityGRAY = cv2.compareHist(histogram_referenceGRAY, histogramGRAY, cv2.HISTCMP_CORREL)
```
\
Imprime a similaridade.
```
print(similarityGRAY)
```
\
É testado se a similaridade calculada for menor que um valor estipulado, se sim, significa que os frames são diferentes, e um alarme deve ser acionado.
```
        if similarityGRAY < sim:
            print("[INFO] ALARME: movimento detectado " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
```
\
É realizada a cópia do histograma do canal cinza para ser usado como referência para a próxima iteração do laço 'while'.
```
histogram_referenceGRAY = histogramGRAY.copy()
```
\
Atualiza a plotagem automaticamente e limpa a plotagem antiga.
```
    fig.canvas.draw()
    fig.canvas.flush_events()
```
\
Aguarda um tempo para a próxima leitura.
```
    time.sleep(0.1)
```
\
Testa se a tecla pressionada foi 'q', se for encerra o loop infinito e o programa encerra sua execução.
```
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```
\
Libera todos os recursos utilizados, fecha as janelas abertas e encerra o programa.
```
capture.release()
cv2.destroyAllWindows()
```
## Código completo em Python
```
import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
import time


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--color', type=str, default='gray',
    help='Color space: "gray" (default), "rgb"')
parser.add_argument('-b', '--bins', type=int, default=256,
    help='Number of bins per channel (default 256)')
parser.add_argument('-s', '--sim', type=float, default=0.995,
    help='Similarity of histograms (default 0.995)')
args = vars(parser.parse_args())

color = args['color']
bins = args['bins']
sim = args['sim']

fig, ax = plt.subplots()
if color == 'rgb':
    ax.set_title('Histograma RGB')
else:
    ax.set_title('Histograma escala de cinza')
ax.set_xlabel('Bins')
ax.set_ylabel('Frequency (N of Pixels)')

lw = 3
alpha = 0.5
if color == 'rgb':
    lineR, = ax.plot(np.arange(bins), np.zeros((bins,)), c='r', lw=lw, alpha=alpha, label='Red')
    lineG, = ax.plot(np.arange(bins), np.zeros((bins,)), c='g', lw=lw, alpha=alpha, label='Green')
    lineB, = ax.plot(np.arange(bins), np.zeros((bins,)), c='b', lw=lw, alpha=alpha, label='Blue')

    canal_referenceR = np.zeros((480, 640), dtype="uint8")
    histogram_referenceR = cv2.calcHist([canal_referenceR], [0], None, [bins], [0, 255])

    canal_referenceG = np.zeros((480, 640), dtype="uint8")
    histogram_referenceG = cv2.calcHist([canal_referenceG], [0], None, [bins], [0, 255])

    canal_referenceB = np.zeros((480, 640), dtype="uint8")
    histogram_referenceB = cv2.calcHist([canal_referenceB], [0], None, [bins], [0, 255])

else:
    lineGray, = ax.plot(np.arange(bins), np.zeros((bins,1)), c='k', lw=lw, label='intensity')

    image_referenceGRAY = np.zeros((480, 640), dtype="uint8")
    histogram_referenceGRAY = cv2.calcHist([image_referenceGRAY], [0], None, [bins], [0, 255])

ax.set_xlim(0, bins)
ax.set_ylim(0, bins + 50)
ax.legend()
plt.ion()
plt.show()

capture = cv2.VideoCapture(0)
while True:
    existe_frame, frame = capture.read()
    frame = cv2.flip(frame, 0)

    if not existe_frame:
        break

    if color == 'rgb':
        cv2.imshow('RGB', frame)
        (b, g, r) = cv2.split(frame)
        histogramR = cv2.calcHist([r], [0], None, [bins], [0, 255])
        histogramG = cv2.calcHist([g], [0], None, [bins], [0, 255])
        histogramB = cv2.calcHist([b], [0], None, [bins], [0, 255])

        cv2.normalize(histogramR, histogramR, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(histogramG, histogramG, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(histogramB, histogramB, 0, 255, cv2.NORM_MINMAX)

        lineR.set_ydata(histogramR)
        lineG.set_ydata(histogramG)
        lineB.set_ydata(histogramB)

        similarityR = cv2.compareHist(histogram_referenceR, histogramR, cv2.HISTCMP_CORREL)
        similarityG = cv2.compareHist(histogram_referenceG, histogramG, cv2.HISTCMP_CORREL)
        similarityB = cv2.compareHist(histogram_referenceB, histogramB, cv2.HISTCMP_CORREL)

        similarity = (similarityR + similarityG + similarityB) / 3
        print(similarity)

        if (similarityR < sim) or (similarityG < sim) or (similarityB < sim):
            print("[INFO] ALARME: movimento detectado " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        histogram_referenceR = histogramR.copy()
        histogram_referenceG = histogramG.copy()
        histogram_referenceB = histogramB.copy()

    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Grayscale', gray)
        histogramGRAY = cv2.calcHist([gray], [0], None, [bins], [0, 255])

        cv2.normalize(histogramGRAY, histogramGRAY, 0, 255, cv2.NORM_MINMAX)

        lineGray.set_ydata(histogramGRAY)

        similarityGRAY = cv2.compareHist(histogram_referenceGRAY, histogramGRAY, cv2.HISTCMP_CORREL)

        print(similarityGRAY)

        if similarityGRAY < sim:
            print("[INFO] ALARME: movimento detectado " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        histogram_referenceGRAY = histogramGRAY.copy()

    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
```
-------------------------------------------------------
## Código do exemplo em C++
```
#include <iostream>
#include <opencv2/opencv.hpp>

int main(int argc, char** argv){
  cv::Mat image;
  int width, height;
  cv::VideoCapture cap;
  std::vector<cv::Mat> planes;
  cv::Mat histR, histG, histB;
  int nbins = 64;
  float range[] = {0, 255};
  const float *histrange = { range };
  bool uniform = true;
  bool acummulate = false;
  int key;

	cap.open(2);

  if(!cap.isOpened()){
    std::cout << "cameras indisponiveis";
    return -1;
  }

  cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
  cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);
  width = cap.get(cv::CAP_PROP_FRAME_WIDTH);
  height = cap.get(cv::CAP_PROP_FRAME_HEIGHT);

  std::cout << "largura = " << width << std::endl;
  std::cout << "altura  = " << height << std::endl;

  int histw = nbins, histh = nbins/2;
  cv::Mat histImgR(histh, histw, CV_8UC3, cv::Scalar(0,0,0));
  cv::Mat histImgG(histh, histw, CV_8UC3, cv::Scalar(0,0,0));
  cv::Mat histImgB(histh, histw, CV_8UC3, cv::Scalar(0,0,0));

  while(1){
    cap >> image;
    cv::split (image, planes);
    cv::calcHist(&planes[0], 1, 0, cv::Mat(), histR, 1,
                 &nbins, &histrange,
                 uniform, acummulate);
    cv::calcHist(&planes[1], 1, 0, cv::Mat(), histG, 1,
                 &nbins, &histrange,
                 uniform, acummulate);
    cv::calcHist(&planes[2], 1, 0, cv::Mat(), histB, 1,
                 &nbins, &histrange,
                 uniform, acummulate);

    cv::normalize(histR, histR, 0, histImgR.rows, cv::NORM_MINMAX, -1, cv::Mat());
    cv::normalize(histG, histG, 0, histImgG.rows, cv::NORM_MINMAX, -1, cv::Mat());
    cv::normalize(histB, histB, 0, histImgB.rows, cv::NORM_MINMAX, -1, cv::Mat());

    histImgR.setTo(cv::Scalar(0));
    histImgG.setTo(cv::Scalar(0));
    histImgB.setTo(cv::Scalar(0));

    for(int i=0; i<nbins; i++){
      cv::line(histImgR,
               cv::Point(i, histh),
               cv::Point(i, histh-cvRound(histR.at<float>(i))),
               cv::Scalar(0, 0, 255), 1, 8, 0);
      cv::line(histImgG,
               cv::Point(i, histh),
               cv::Point(i, histh-cvRound(histG.at<float>(i))),
               cv::Scalar(0, 255, 0), 1, 8, 0);
      cv::line(histImgB,
               cv::Point(i, histh),
               cv::Point(i, histh-cvRound(histB.at<float>(i))),
               cv::Scalar(255, 0, 0), 1, 8, 0);
    }
    histImgR.copyTo(image(cv::Rect(0, 0       ,nbins, histh)));
    histImgG.copyTo(image(cv::Rect(0, histh   ,nbins, histh)));
    histImgB.copyTo(image(cv::Rect(0, 2*histh ,nbins, histh)));
    cv::imshow("image", image);
    key = cv::waitKey(30);
    if(key == 27) break;
  }
  return 0;
}
```