# -*- coding: utf-8 -*-
"""Aplicações da Ciência de Dados em Tecnologias Disruptivas - Módulo 6

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18NSxyM2waAYbNUZmXUcoZwMvzNZDh4_6

Funcionamento do CSRT
"""

import cv2
from google.colab.patches import cv2_imshow

# Fazer o upload do vídeo
from google.colab import files
uploaded = files.upload()

# Verificar se o arquivo foi carregado
if len(uploaded) > 0:
    video_path = list(uploaded.keys())[0]  # Obter o caminho do arquivo carregado
else:
    print("Erro: Nenhum vídeo foi carregado.")

# Abrir o vídeo
cap = cv2.VideoCapture(video_path)

# Verifica se o vídeo foi aberto corretamente
if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
else:
    # Ler o primeiro frame do vídeo
    ret, frame = cap.read()

    if not ret:
        print("Erro ao ler o primeiro frame do vídeo.")
    else:
        # Ajustar a região de interesse (ROI) para centralizar a marcação no carro
        # Exemplo de coordenadas ajustadas: (x, y, largura, altura)
        bbox = (180, 280, 500, 300)  # Novos ajustes de coordenadas para centralizar no carro

        # Inicializar o rastreador CSRT
        tracker = cv2.TrackerCSRT_create()
        tracker.init(frame, bbox)

        # Contador para exibir apenas os 4 primeiros frames
        frame_count = 0

        # Loop para rastrear o carro nos frames subsequentes
        while frame_count < 4:
            ret, frame = cap.read()
            if not ret:
                break

            # Atualizar o rastreamento
            ret, bbox = tracker.update(frame)

            if ret:
                # Desenhar a caixa delimitadora ao redor do carro rastreado
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
            else:
                cv2.putText(frame, "Rastreamento falhou", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            # Exibir o frame com a caixa delimitadora no Colab
            cv2_imshow(frame)

            # Aumentar o contador de frames
            frame_count += 1

cap.release()
cv2.destroyAllWindows()

"""CSRT no Google Colab

"""

import cv2
from google.colab.patches import cv2_imshow
from google.colab import files

# Fazer upload de um vídeo
uploaded = files.upload()

# Obter o nome do vídeo que foi carregado
video_path = next(iter(uploaded))

# Carregar o vídeo
cap = cv2.VideoCapture(video_path)

# Verifica se o vídeo foi aberto corretamente
if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
else:
    # Ler o primeiro frame do vídeo
    ret, frame = cap.read()

    if not ret:
        print("Erro ao ler o primeiro frame do vídeo.")
    else:
        # Ajustar a região de interesse (ROI)
        altura, largura, _ = frame.shape
        bbox = (largura // 4, altura // 4, largura // 2, altura // 2)  # ROI maior e centralizada

        # Inicializar o rastreador CSRT
        tracker = cv2.legacy.TrackerCSRT_create()  # Usar a API legacy do OpenCV no Colab
        tracker.init(frame, bbox)

        # Contador para exibir apenas os primeiros frames
        frame_count = 0

        # Loop para rastrear o objeto nos frames subsequentes
        while frame_count < 50:  # Reduzido o número de frames para teste
            ret, frame = cap.read()
            if not ret:
                break

            # Atualizar o rastreamento
            ret, bbox = tracker.update(frame)

            if ret:
                # Desenhar a caixa delimitadora ao redor do objeto rastreado
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
            else:
                cv2.putText(frame, "Rastreamento falhou", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            # Exibir o frame com a caixa delimitadora no Colab
            cv2_imshow(frame)

            # Aumentar o contador de frames
            frame_count += 1

cap.release()
cv2.destroyAllWindows()