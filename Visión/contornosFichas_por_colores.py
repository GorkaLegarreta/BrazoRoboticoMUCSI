import cv2
import numpy as np

"""
Define la funcion que detecta los contornos de las fichas y nos diferencia en base a la mascara que lo ha detectado
"""
def detectar_contornos_colores(image):
    # Definir los rangos de color para cada ficha
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
    mask_red = mask_red1 + mask_red2
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Encontrar los contornos en las máscaras de los colores
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours_blue, contours_red, contours_green, contours_yellow

# Ejemplo de uso:
"""
# Ejemplo de uso con una imagen
image = cv2.imread('Imagenes/tablero10.png')  # Reemplaza 'tu_imagen.png' con la ruta de tu imagen
contornos_azules, contornos_rojos, contornos_verdes, contornos_amarillos = detectar_contornos_colores(image)

# Dibujar los contornos en la imagen original y mostrarla
image_contornos = image.copy()

# Dibujar los contornos de color azul en la imagen
cv2.drawContours(image_contornos, contornos_azules, -1, (0, 0, 0), 2)

# Dibujar los contornos de color rojo en la imagen
cv2.drawContours(image_contornos, contornos_rojos, -1, (0, 0, 0), 2)

# Dibujar los contornos de color verde en la imagen
cv2.drawContours(image_contornos, contornos_verdes, -1, (0, 0, 0), 2)

# Dibujar los contornos de color amarillo en la imagen
cv2.drawContours(image_contornos, contornos_amarillos, -1, (0, 0, 0), 2)

# Mostrar la imagen con los contornos
cv2.imshow('Imagen con Contornos', image_contornos)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""