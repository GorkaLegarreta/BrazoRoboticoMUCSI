import cv2
import numpy as np

# Cargar una imagen o capturar desde la cámara
image = cv2.imread('Imagenes/tablero3.png')  # O cambia a captura de cámara con cv2.VideoCapture

# Convertir la imagen a escala de grises
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar un filtro de suavizado para reducir el ruido
blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Aplicar un umbral para detectar las áreas negras
_, thresholded = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)

# Aplicar la detección de bordes con Canny
edges = cv2.Canny(thresholded, 20, 80)

# Encontrar los contornos en la imagen
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar los contornos en la imagen original
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# Mostrar la imagen con los contornos
cv2.imshow('Contornos', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
