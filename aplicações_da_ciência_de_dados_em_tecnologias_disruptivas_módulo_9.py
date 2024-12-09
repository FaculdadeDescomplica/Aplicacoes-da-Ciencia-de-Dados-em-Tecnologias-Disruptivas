# -*- coding: utf-8 -*-
"""Aplicações da Ciência de Dados em Tecnologias Disruptivas - Módulo 9

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17OoBd3hkH1X7_46AlT00BIJV177jRHUA

*MOSSE no Google Colab*
"""

!pip install opencv-python matplotlib

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Função para processar o vídeo
def process_video(video_url):
    # Captura do vídeo
    cap = cv2.VideoCapture(video_url)

    # Verifica se o vídeo foi aberto corretamente
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    # Inicializa o primeiro frame para comparação
    ret, prev_frame = cap.read()
    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Converte o frame atual para escala de cinza
        current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calcula a diferença entre o frame atual e o anterior
        diff_frame = cv2.absdiff(prev_frame_gray, current_frame_gray)

        # Aplica um threshold para detectar movimento
        _, thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)

        # Encontra contornos na imagem binária
        contours, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Desenha os contornos no frame original
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Filtra pequenos contornos
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Exibe o frame com detecções
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.axis('off')  # Oculta os eixos
        plt.show()

        # Atualiza o frame anterior
        prev_frame_gray = current_frame_gray

        # Pause para visualizar
        plt.pause(0.1)

    # Libera a captura
    cap.release()

# URL do vídeo do OpenCV (exemplo: vídeo de corrida)
video_url = 'https://github.com/opencv/opencv/blob/master/samples/data/vtest.avi?raw=true'
process_video(video_url)

"""Comparação do MOSSE com Algoritmos Similares

"""

# Instalação das bibliotecas necessárias
!pip install opencv-python-headless matplotlib requests

import cv2
import matplotlib.pyplot as plt
import numpy as np
import requests

# Função para baixar um vídeo de exemplo
def download_video(url, filename):
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)

# URL do vídeo de exemplo
video_url = "https://github.com/opencv/opencv/raw/master/samples/data/vtest.avi"
video_filename = "vtest.avi"

# Baixar o vídeo
download_video(video_url, video_filename)

# Carregar o vídeo
cap = cv2.VideoCapture(video_filename)

# Defina o ponto inicial para o rastreamento (ajuste esses valores conforme necessário)
bbox = (200, 200, 100, 100)  # Exemplo de ROI fixo

# Ler o primeiro frame e inicializar os rastreadores
ret, frame = cap.read()
if not ret:
    print("Erro ao ler o vídeo.")
    cap.release()
    exit()

# Inicialize o rastreador MOSSE
mosse_tracker = cv2.legacy.TrackerMOSSE_create()  # Uso correto da nova API
mosse_tracker.init(frame, bbox)

# Inicialize o rastreador KCF
kcf_tracker = cv2.legacy.TrackerKCF_create()  # Uso correto da nova API
kcf_tracker.init(frame, bbox)

# Listas para armazenar posições dos rastreadores
mosse_positions = []
kcf_positions = []

# Para armazenar frames para visualização
frames_for_display = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Atualizar rastreador MOSSE
    mosse_success, mosse_bbox = mosse_tracker.update(frame)
    if mosse_success:
        mosse_positions.append(mosse_bbox)
        (x, y, w, h) = [int(v) for v in mosse_bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2, 1)

    # Atualizar rastreador KCF
    kcf_success, kcf_bbox = kcf_tracker.update(frame)
    if kcf_success:
        kcf_positions.append(kcf_bbox)
        (x, y, w, h) = [int(v) for v in kcf_bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)

    # Adicionar o frame à lista para visualização
    frames_for_display.append(frame)

cap.release()

# Visualizando os resultados com Matplotlib
plt.figure(figsize=(15, 8))

# Plotando os frames com as posições do rastreador
for i, frame in enumerate(frames_for_display[::5]):  # Seleciona a cada 5 frames para evitar excesso
    plt.subplot(2, 5, (i % 5) + 1)
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.title(f'Frame {i * 5}')
    plt.axis('off')

plt.suptitle('Frames com Rastreamento (MOSSE em azul, KCF em verde)')
plt.tight_layout()
plt.show()

# Visualizando as posições dos rastreadores
plt.figure(figsize=(10, 5))

# Plotando as posições do rastreador MOSSE
plt.subplot(1, 2, 1)
plt.plot([pos[0] for pos in mosse_positions], [pos[1] for pos in mosse_positions], label='MOSSE', color='blue')
plt.title('Posições do Rastreador MOSSE')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.axis('equal')

# Plotando as posições do rastreador KCF
plt.subplot(1, 2, 2)
plt.plot([pos[0] for pos in kcf_positions], [pos[1] for pos in kcf_positions], label='KCF', color='green')
plt.title('Posições do Rastreador KCF')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.axis('equal')

plt.tight_layout()
plt.show()

"""Otimização do Algoritmo MOSSE"""

# Instalação das bibliotecas necessárias
!pip install opencv-python-headless matplotlib requests

import cv2
import matplotlib.pyplot as plt
import numpy as np
import requests
import time

# Função para baixar um vídeo de exemplo
def download_video(url, filename):
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)

# URL do vídeo de exemplo
video_url = "https://github.com/opencv/opencv/raw/master/samples/data/vtest.avi"
video_filename = "vtest.avi"

# Baixar o vídeo
download_video(video_url, video_filename)

# Carregar o vídeo
cap = cv2.VideoCapture(video_filename)

# Defina o ponto inicial para o rastreamento (ajuste esses valores para a sua necessidade)
bbox = (200, 200, 100, 100)  # Exemplo de ROI fixo

# Inicialize o rastreador MOSSE
mosse_tracker = cv2.legacy.TrackerMOSSE_create()
ret, frame = cap.read()
if ret:
    mosse_tracker.init(frame, bbox)

# Listas para armazenar posições dos rastreadores
mosse_positions = []

# Para armazenar frames para visualização
frames_for_display = []

# Medir o tempo total de rastreamento
start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Atualizar rastreador MOSSE
    mosse_success, mosse_bbox = mosse_tracker.update(frame)
    if mosse_success:
        mosse_positions.append(mosse_bbox)
        (x, y, w, h) = [int(v) for v in mosse_bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2, 1)

    # Adicionar o frame à lista para visualização
    frames_for_display.append(frame)

cap.release()

# Calcular e imprimir o tempo total
end_time = time.time()
total_time = end_time - start_time
print(f'Tempo total de rastreamento: {total_time:.2f} segundos')

# Visualizando os resultados com Matplotlib
plt.figure(figsize=(15, 8))

# Plotando os frames com as posições do rastreador
for i, frame in enumerate(frames_for_display[::5]):  # Seleciona a cada 5 frames para evitar excesso
    plt.subplot(2, 5, (i % 5) + 1)
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.title(f'Frame {i * 5}')
    plt.axis('off')

plt.suptitle('Frames com Rastreamento (MOSSE)')
plt.tight_layout()
plt.show()

# Visualizando as posições do rastreador MOSSE
plt.figure(figsize=(10, 5))
plt.plot([pos[0] for pos in mosse_positions], [pos[1] for pos in mosse_positions], label='MOSSE', color='blue')
plt.title('Posições do Rastreador MOSSE')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.axis('equal')
plt.tight_layout()
plt.show()