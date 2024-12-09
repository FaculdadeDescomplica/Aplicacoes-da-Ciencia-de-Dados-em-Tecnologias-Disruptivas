# -*- coding: utf-8 -*-
"""Aplicações da Ciência de Dados em Tecnologias Disruptivas - Módulo 8

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oMn74DEq76cwKQwjBgqo5TVWR1gosGqc

TLD no Google Colab
"""

import cv2
from google.colab import files
from google.colab.patches import cv2_imshow

# Fazer upload de um vídeo
uploaded = files.upload()

# Obter o nome do vídeo carregado
video_path = next(iter(uploaded))

# Carregar o vídeo
cap = cv2.VideoCapture(video_path)

# Verificar se o vídeo foi carregado corretamente
if not cap.isOpened():
    print("Erro ao carregar o vídeo.")
else:
    print("Vídeo carregado com sucesso!")

# Ler o primeiro frame do vídeo
ret, frame = cap.read()

if not ret:
    print("Erro ao ler o primeiro frame.")
else:
    # Definir manualmente a ROI (Região de Interesse) em vez de usar cv2.selectROI
    # bbox = (x, y, largura, altura)
    bbox = (100, 100, 200, 200)  # Ajuste essas coordenadas conforme necessário para o vídeo

    # Inicializar o rastreador TLD
    tracker = cv2.legacy.TrackerTLD_create()
    tracker.init(frame, bbox)

    print("Rastreador TLD inicializado com sucesso!")

# Loop para rastrear o objeto ao longo do vídeo
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Atualizar o rastreamento
    success, bbox = tracker.update(frame)

    if success:
        # Desenhar a caixa ao redor do objeto rastreado
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    else:
        cv2.putText(frame, "Rastreamento falhou", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Exibir o frame com a caixa delimitadora no Google Colab
    cv2_imshow(frame)

cap.release()
cv2.destroyAllWindows()

"""Desempenho do TLD em Diferentes Cenários"""

import cv2
from google.colab import files
from google.colab.patches import cv2_imshow

# Fazer upload de um vídeo
uploaded = files.upload()

# Obter o nome do vídeo carregado
video_path = next(iter(uploaded))

# Carregar o vídeo
cap = cv2.VideoCapture(video_path)

# Verificar se o vídeo foi carregado corretamente
if not cap.isOpened():
    print("Erro ao carregar o vídeo.")
else:
    print("Vídeo carregado com sucesso!")

# Ler o primeiro frame do vídeo
ret, frame = cap.read()

if not ret:
    print("Erro ao ler o primeiro frame.")
else:
    # Definir manualmente a ROI (Região de Interesse)
    # bbox = (x, y, largura, altura)
    bbox = (100, 100, 200, 200)  # Ajuste conforme necessário

    # Inicializar o rastreador TLD
    tracker = cv2.legacy.TrackerTLD_create()
    tracker.init(frame, bbox)

    print("Rastreador TLD inicializado com sucesso!")

# Loop para rastrear o objeto ao longo do vídeo
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Atualizar o rastreamento
    success, bbox = tracker.update(frame)

    if success:
        # Desenhar a caixa ao redor do objeto rastreado
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    else:
        cv2.putText(frame, "Rastreamento falhou", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Exibir o frame com a caixa delimitadora no Google Colab
    cv2_imshow(frame)

cap.release()
cv2.destroyAllWindows()