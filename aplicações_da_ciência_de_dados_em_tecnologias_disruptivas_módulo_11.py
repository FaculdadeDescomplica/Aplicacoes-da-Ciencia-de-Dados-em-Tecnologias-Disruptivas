# -*- coding: utf-8 -*-
"""Aplicações da Ciência de Dados em Tecnologias Disruptivas - Módulo 11

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1n3WKG8iCQc7zIMiPruXS83IqzXgLJ7na

Meanshift no Google Colab
"""

# Instalando a biblioteca OpenCV (caso não esteja instalada)
!pip install opencv-python

# Importando as bibliotecas necessárias
import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

# Usando uma imagem de exemplo da biblioteca OpenCV
# Criando uma imagem preta de 400x400 como exemplo
image = np.zeros((400, 400, 3), dtype=np.uint8)

# Exibindo a imagem original
plt.imshow(image)
plt.axis('off')
plt.title('Imagem Original (Imagem Preta)')
plt.show()

# Convertendo a imagem para o espaço de cor HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

# Definindo parâmetros para o Meanshift
sp = 10  # Tamanho do espaço de cores
sr = 10  # Tamanho do espaço de região
max_level = 2  # Nível máximo para a pirâmide de imagens

# Aplicando o Meanshift
meanshift_result = cv2.pyrMeanShiftFiltering(hsv_image, sp, sr, max_level)

# Convertendo de volta para o espaço de cor RGB
meanshift_result = cv2.cvtColor(meanshift_result, cv2.COLOR_HSV2RGB)

# Exibindo a imagem segmentada
plt.imshow(meanshift_result)
plt.axis('off')
plt.title('Resultado do Meanshift (Imagem Preta)')
plt.show()

# Criando um vídeo sintético com um círculo se movendo
video_path = 'synthetic_video.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))

# Criando o vídeo
for i in range(100):
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.circle(frame, (i*6, 240), 20, (255, 0, 0), -1)  # Círculo se movendo
    out.write(frame)

out.release()

# Lendo o vídeo gerado
cap = cv2.VideoCapture(video_path)

# Lendo o primeiro quadro e definindo a ROI (manual)
ret, frame = cap.read()
if not ret:
    print("Erro ao ler o quadro do vídeo.")
else:
    # Definindo uma ROI fixa como exemplo (x, y, w, h)
    x, y, w, h = 300, 220, 60, 60  # Ajuste conforme necessário
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Desenhando a ROI para visualização
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title('Quadro do Vídeo com ROI')
    plt.show()

    # Inicializando o histograma da ROI
    roi_hist = cv2.calcHist([frame[y:y+h, x:x+w]], [0], None, [256], [0, 256])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    # Definindo o codec e criando um objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec para vídeo
    out = cv2.VideoWriter('output_meanshift.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertendo o quadro atual para HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Calculando a retroprojeção do histograma
        back_proj = cv2.calcBackProject([hsv_frame], [0], roi_hist, [0, 256], 1)

        # Aplicando o Meanshift
        _, track_window = cv2.meanShift(back_proj, (x, y, w, h), (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1))

        # Desenhando o retângulo na imagem
        x, y, w, h = track_window
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Salvando o quadro processado no vídeo
        out.write(frame)

    cap.release()
    out.release()

# Download do vídeo gerado
files.download('output_meanshift.avi')

"""Testar a Eficiência do Meanshift"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

# Criando um vídeo sintético com um círculo se movendo
video_path = 'synthetic_video.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))

# Criando o vídeo
circle_center = []
for i in range(100):
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    center_x = i * 6
    center_y = 240
    cv2.circle(frame, (center_x, center_y), 20, (255, 0, 0), -1)  # Círculo se movendo
    out.write(frame)
    circle_center.append((center_x, center_y))  # Armazenando o centro do círculo

out.release()
print("Vídeo sintético criado com sucesso!")

# Lendo o vídeo gerado
cap = cv2.VideoCapture(video_path)

# Lendo o primeiro quadro e definindo a ROI (manual)
ret, frame = cap.read()
if not ret:
    print("Erro ao ler o quadro do vídeo.")
else:
    # Definindo uma ROI fixa como exemplo (x, y, w, h)
    x, y, w, h = 300, 220, 60, 60  # Ajuste conforme necessário
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Desenhando a ROI para visualização
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title('Quadro do Vídeo com ROI')
    plt.show()
    print("Quadro inicial exibido com a ROI definida.")

    # Inicializando o histograma da ROI
    roi_hist = cv2.calcHist([frame[y:y+h, x:x+w]], [0], None, [256], [0, 256])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    # Definindo o codec e criando um objeto VideoWriter
    out = cv2.VideoWriter('output_meanshift.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))

    distances = []  # Lista para armazenar as distâncias
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertendo o quadro atual para HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Calculando a retroprojeção do histograma
        back_proj = cv2.calcBackProject([hsv_frame], [0], roi_hist, [0, 256], 1)

        # Aplicando o Meanshift
        _, track_window = cv2.meanShift(back_proj, (x, y, w, h), (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1))

        # Desenhando o retângulo na imagem
        x, y, w, h = track_window
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Calculando a posição estimada do centro do objeto
        estimated_center = (x + w // 2, y + h // 2)
        actual_center = circle_center[frame_count]

        # Calculando a distância entre a posição estimada e a posição real
        distance = np.linalg.norm(np.array(estimated_center) - np.array(actual_center))
        distances.append(distance)

        # Salvando o quadro processado no vídeo
        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()
    print("O processamento do vídeo foi concluído.")

# Calculando a distância média
average_distance = np.mean(distances)
print(f"A distância média entre a posição estimada e a posição real é: {average_distance:.2f} pixels.")

# Exibindo o vídeo resultante
from IPython.display import Video
print("O vídeo com o resultado do rastreamento foi exibido.")
Video('output_meanshift.avi')

# Download do vídeo gerado
files.download('output_meanshift.avi')

"""Otimização do Algoritmo Meanshift"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

# Criando um vídeo sintético com um círculo se movendo
video_path = 'synthetic_video.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))

circle_center = []
for i in range(100):
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    center_x = i * 6
    center_y = 240
    cv2.circle(frame, (center_x, center_y), 20, (255, 0, 0), -1)  # Círculo se movendo
    out.write(frame)
    circle_center.append((center_x, center_y))

out.release()

# Lendo o vídeo gerado
cap = cv2.VideoCapture(video_path)

# Lendo o primeiro quadro e definindo a ROI (manual)
ret, frame = cap.read()
if not ret:
    print("Erro ao ler o quadro do vídeo.")
else:
    # Definindo uma ROI fixa
    x, y, w, h = 300, 220, 60, 60  # Ajuste conforme necessário
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Desenhando a ROI para visualização
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title('Quadro do Vídeo com ROI')
    plt.show()

    # Inicializando o histograma da ROI
    roi_hist = cv2.calcHist([frame[y:y+h, x:x+w]], [0], None, [256], [0, 256])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    # Definindo o codec e criando um objeto VideoWriter
    out = cv2.VideoWriter('output_meanshift.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))

    iteration = 0  # Contador de iterações
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertendo o quadro atual para HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Calculando a retroprojeção do histograma
        back_proj = cv2.calcBackProject([hsv_frame], [0], roi_hist, [0, 256], 1)

        # Aplicando o Meanshift
        _, track_window = cv2.meanShift(back_proj, (x, y, w, h), (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1))

        # Desenhando o retângulo na imagem
        x, y, w, h = track_window
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Feedback para o aluno
        estimated_center = (x + w // 2, y + h // 2)
        actual_center = circle_center[iteration]
        distance = np.linalg.norm(np.array(estimated_center) - np.array(actual_center))

        print(f"Iteração: {iteration}")
        print(f"Centro estimado: {estimated_center}, Centro real: {actual_center}")
        print(f"Distância entre estimativa e realidade: {distance:.2f} pixels\n")

        # Salvando o quadro processado no vídeo
        out.write(frame)
        iteration += 1

    cap.release()
    out.release()