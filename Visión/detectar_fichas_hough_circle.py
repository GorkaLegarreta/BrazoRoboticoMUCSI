import cv2
import numpy as np

# Cargar una imagen o capturar desde la cámara
image = cv2.imread('Imagenes/tablero0.png')  # Cambia la ruta de la imagen según tus necesidades
image_original = image.copy()

def detectar_hough_circles(image, mask):
    fichas = cv2.bitwise_and(image, image, mask=mask)
    # Realizar la detección de círculos utilizando Hough Circles
    gray_img = cv2.cvtColor(fichas, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.medianBlur(gray_img, 5)
    circles = cv2.HoughCircles(
        gray_img, cv2.HOUGH_GRADIENT_ALT, 1, 20, param1=100, param2=0, minRadius=0, maxRadius=0)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        #cv2.line(image, (circles[0][0][0],circles[0][0][1]), (circles[0][1][0],circles[0][1][1]), (255, 255, 0), 2) 
        for i in circles[0, :]:
            # Dibujar los círculos detectados
            #cv2.circle(image, (i[0], i[1]), i[2], (255, 255, 0), 2)
            cv2.circle(image, (i[0], i[1]), 2, (255, 255, 0), 3)
    # Muestra el resultado en una ventana
    # cv2.imshow('Blue Detection', fichas)


# Definir los rangos de color para cada color
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([180, 255, 255])

# Convertir la imagen a espacio de color HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Crear máscaras para cada color
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask_red = mask_red1 + mask_red2
detectar_hough_circles(image, mask_blue)
detectar_hough_circles(image, mask_red)

# Encontrar los contornos de colores en la máscara combinada
#contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)        

# Dibujar los contornos de colores en la imagen original
#cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# Mostrar la imagen con los círculos y contornos de colores detectados
cv2.imshow('Detección de Fichas', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
