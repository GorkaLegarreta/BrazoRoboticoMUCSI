import cv2
import numpy as np

# Umbral superior e inferior para cada color
umbral_inferior_azul = np.array([90, 50, 50])
umbral_superior_azul = np.array([130, 255, 255])
umbral_inferior_rojo1 = np.array([0, 100, 100])
umbral_superior_rojo1 = np.array([10, 255, 255])
umbral_inferior_rojo2 = np.array([160, 100, 100])
umbral_superior_rojo2 = np.array([180, 255, 255])
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([40, 255, 255])

# Devuelve máscaras para cada color
def obtener_mascaras_colores(imagen):
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    mascara_azul = cv2.inRange(hsv, umbral_inferior_azul, umbral_superior_azul)
    mascara_rojo1 = cv2.inRange(hsv, umbral_inferior_rojo1, umbral_superior_rojo1)
    mascara_rojo2 = cv2.inRange(hsv, umbral_inferior_rojo2, umbral_superior_rojo2)
    #mascara_rojo = mascara_rojo1 + mascara_rojo2
    mascara_rojo = cv2.inRange(hsv, lower_yellow, upper_yellow)

    return mascara_azul, mascara_rojo

# Devuelve un array de fichas (circulares) detectadas en 'imagen' de un color contenido en 'mascara'
def obtener_fichas_color(imagen, mascara) -> []:
    fichas = cv2.bitwise_and(imagen, imagen, mask = mascara)
    imagen_gris = cv2.cvtColor(fichas, cv2.COLOR_BGR2GRAY)
    imagen_gris = cv2.medianBlur(imagen_gris, 5)
    fichas = cv2.HoughCircles(imagen_gris, cv2.HOUGH_GRADIENT_ALT, 1, 40, param1=100, param2=0, minRadius=0, maxRadius=0)

    if fichas is not None:
        fichas = np.uint16(np.around(fichas))

    return fichas

# Devuelve los parámetros x, y, w, h que delimitan el rectángulo del tablero
def obtener_rectangulo_tablero(imagen):
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    imagen_desenfocada = cv2.GaussianBlur(imagen_gris, (5, 5), 0)
    _, imagen_umbralizada = cv2.threshold(imagen_desenfocada, 50, 255, cv2.THRESH_BINARY)
    imagen_bordes = cv2.Canny(imagen_umbralizada, 20, 80)
    
    contornos, _ = cv2.findContours(imagen_bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contorno_tablero = max(contornos, key=cv2.contourArea)

    return cv2.boundingRect(contorno_tablero)

# Devuelve las casillas con los parámetros x, y, w, h que delimitan el rectángulo del tablero
def obtener_rectangulos_casillas(rectangulo_tablero):
    ancho_casilla = int(rectangulo_tablero[2]/3)
    alto_casilla = int(rectangulo_tablero[3]/3)
    rectangulos_casillas = []

    for i in range(3):
        for j in range(3):
            rectangulos_casillas.append((rectangulo_tablero[0] + j*ancho_casilla, 
                                         rectangulo_tablero[1] + i*alto_casilla, ancho_casilla, alto_casilla))

    return rectangulos_casillas

# Devuelve True si el centro de 'ficha' está dentro de 'rectangulo' (x, y, w, h)
def dentro(ficha, rectangulo) -> bool:
    centro_ficha_x = ficha[0]
    centro_ficha_y = ficha[1]
    #radio_ficha = ficha[2]-5
    radio_ficha = 5

    if  rectangulo[0] < (centro_ficha_x-radio_ficha) and (centro_ficha_x+radio_ficha) < (rectangulo[0]+rectangulo[2]) and \
        rectangulo[1] < (centro_ficha_y-radio_ficha) and (centro_ficha_y+radio_ficha) < (rectangulo[1]+rectangulo[3]):
        return True
    else: 
        return False

# Devuelve la primera 'ficha' que no está dentro de 'rectangulo_tablero'
def obtener_ficha_libre(fichas, rectangulo_tablero):
    for i in fichas[0, :]:
        if not dentro(i, rectangulo_tablero):
            return i

# Devuelve un entero que transformado a base 3 representa el estado del tablero
def obtener_estado_tablero(imagen) -> int:
    
    rectangulo_tablero = obtener_rectangulo_tablero(imagen)
    rectangulos_casillas = obtener_rectangulos_casillas(rectangulo_tablero)
    mascara_azul, mascara_rojo = obtener_mascaras_colores(imagen)
    fichas_azules = obtener_fichas_color(imagen, mascara_azul)
    fichas_rojas = obtener_fichas_color(imagen, mascara_rojo)

    estado = 0

    for i in range(9):
        print("i: ", i)
        for j in fichas_azules[0, :]:            
            if dentro(j, rectangulos_casillas[i]):
                print("azul", j)
                estado += 1*(3**i)
        for k in fichas_rojas[0, :]:            
            if dentro(k, rectangulos_casillas[i]):
                print("amarillo: ",k)
                estado += 2*(3**i)
                
    return estado
