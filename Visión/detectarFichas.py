"""
Este código detectará contornos en colores azul, rojo, verde, amarillo y otros que puedas definir. 
Asegúrate de ajustar los valores lower_color y upper_color según los rangos de color que deseas detectar. 
También puedes añadir más rangos de color si es necesario para tu aplicación.
"""
import cv2
import numpy as np

# Cargar una imagen o capturar desde la cámara
image = cv2.imread('Imagenes/gorka_1.png')  # O cambia a captura de cámara con cv2.VideoCapture

# Definir los rangos de color para cada color
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([180, 255, 255])

lower_green = np.array([40, 100, 100])
upper_green = np.array([80, 255, 255])

lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([40, 255, 255])

# Convertir la imagen a espacio de color HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Crear máscaras para cada color
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask_green = cv2.inRange(hsv, lower_green, upper_green)
mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

# Combinar las máscaras para todos los colores
combined_mask = mask_blue + mask_red1 + mask_red2 + mask_green + mask_yellow

# Encontrar los contornos en la máscara combinada
contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar los contornos en la imagen original
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# Mostrar la imagen con los contornos de colores detectados
cv2.imshow('Contornos de Colores', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
