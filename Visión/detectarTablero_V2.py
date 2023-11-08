import cv2
import numpy as np

# Cargar una imagen o capturar desde la cámara
image = cv2.imread('Imagenes/tablero10.png')  # O cambia a captura de cámara con cv2.VideoCapture
def encontrar_esquinas_tablero(image):
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

    # Crear una lista para almacenar las coordenadas de las esquinas de cada casilla
    esquinas_casillas = []
    # Iterar sobre todos los contornos encontrados
    for contorno in contours:
        # Calcular las coordenadas del rectángulo delimitador
        x, y, w, h = cv2.boundingRect(contorno)
        
        # Calcular las coordenadas de las esquinas de la casilla
        esquina_superior_izquierda = (x, y)
        esquina_superior_derecha = (x + w, y)
        esquina_inferior_izquierda = (x, y + h)
        esquina_inferior_derecha = (x + w, y + h)
        
        # Agregar las coordenadas de las esquinas a la lista
        esquinas_casillas.append((esquina_superior_izquierda, esquina_superior_derecha, esquina_inferior_izquierda, esquina_inferior_derecha))
    # Dibujar los contornos en la imagen original
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    print(esquinas_casillas)
    return esquinas_casillas





encontrar_esquinas_tablero(image)

# Mostrar la imagen con los contornos
cv2.imshow('Contornos', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
