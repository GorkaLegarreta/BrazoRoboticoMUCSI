import cv2
import numpy as np

# Umbral superior e inferior para cada color
umbral_inferior_azul = np.array([90, 50, 50])
umbral_superior_azul = np.array([130, 255, 255])
umbral_inferior_rojo1 = np.array([0, 100, 100])
umbral_superior_rojo1 = np.array([10, 255, 255])
umbral_inferior_rojo2 = np.array([160, 100, 100])
umbral_superior_rojo2 = np.array([180, 255, 255])
umbral_inferior_amarillo = np.array([20, 100, 100])
umbral_superior_amarillo = np.array([40, 255, 255])

# Devuelve máscaras para cada color
def obtener_mascaras_colores(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mascara_amarillo = cv2.inRange(hsv, umbral_inferior_amarillo, umbral_superior_amarillo)
    mascara_azul = cv2.inRange(hsv, umbral_inferior_azul, umbral_superior_azul)
    mascara_rojo1 = cv2.inRange(hsv, umbral_inferior_rojo1, umbral_superior_rojo1)
    mascara_rojo2 = cv2.inRange(hsv, umbral_inferior_rojo2, umbral_superior_rojo2)
    mascara_rojo = mascara_rojo1 + mascara_rojo2
    
    return mascara_amarillo, mascara_azul, mascara_rojo

# Devuelve un array de fichas (circulares) detectadas en 'frame' de un color contenido en 'mascara'
def obtener_fichas_color(frame, mascara) -> []:
    fichas = cv2.bitwise_and(frame, frame, mask = mascara)
    frame_gris = cv2.cvtColor(fichas, cv2.COLOR_BGR2GRAY)
    frame_gris = cv2.medianBlur(frame_gris, 5)
    fichas = cv2.HoughCircles(frame_gris, cv2.HOUGH_GRADIENT_ALT, 1, 20, param1=100, param2=0, minRadius=24, maxRadius=0)

    if fichas is not None:
        fichas = np.uint16(np.around(fichas))

    return fichas

# Devuelve los parámetros x, y, w, h que delimitan el rectángulo del tablero
def obtener_rectangulo_tablero(frame):
    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_desenfocado = cv2.GaussianBlur(frame_gris, (5, 5), 0)
    _, frame_umbralizado = cv2.threshold(frame_desenfocado, 50, 255, cv2.THRESH_BINARY)
    frame_bordes = cv2.Canny(frame_umbralizado, 20, 80)
    contornos, _ = cv2.findContours(frame_bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
    radio_ficha = ficha[2]-5
    #radio_ficha = 5
    if  (rectangulo[0] < (centro_ficha_x-radio_ficha)) and ((centro_ficha_x+radio_ficha) < (rectangulo[0]+rectangulo[2])) and \
        (rectangulo[1] < (centro_ficha_y-radio_ficha)) and ((centro_ficha_y+radio_ficha) < (rectangulo[1]+rectangulo[3])):
        return True
    else: 
        return False

# Devuelve la primera 'ficha' que no está dentro de 'rectangulo_tablero'
def obtener_ficha_libre(fichas, rectangulo_tablero):
    for i in fichas[0, :]:
        if not dentro(i, rectangulo_tablero):
            return i

# Devuelve un entero que transformado a base 3 representa el estado del tablero
def obtener_estado_tablero(frame) -> int:
    rect_tablero = obtener_rectangulo_tablero(frame)
    rect_casillas = obtener_rectangulos_casillas(rect_tablero)
    mascara_2, mascara_1, _ = obtener_mascaras_colores(frame)
    fichas_1 = obtener_fichas_color(frame, mascara_1)
    fichas_2 = obtener_fichas_color(frame, mascara_2)
    estado = 0

    for i in range(9):
        print("i: ", i)
        if fichas_1 is not None:
            for j in fichas_1[0, :]:            
                if dentro(j, rect_casillas[i]):
                    print("azul: ", j)
                    estado += 1*(3**i)
        if fichas_2 is not None:
            for k in fichas_2[0, :]:            
                if dentro(k, rect_casillas[i]):
                    print("amarillo: ",k)
                    estado += 2*(3**i)
                
    return estado

# Dibuja contornos y formas sobre el frame
def dibujar_sobre_frame(frame):
    rect_tablero = obtener_rectangulo_tablero(frame)
    rect_casillas = obtener_rectangulos_casillas(rect_tablero)
    mascara_2, mascara_1, _ = obtener_mascaras_colores(frame)

    # Dibuja el rectángulo del tablero y las casillas
    cv2.rectangle(frame, (rect_tablero[0],rect_tablero[1]),
                (rect_tablero[0]+rect_tablero[2], rect_tablero[1]+rect_tablero[3]), (0, 255, 0), 1)
    for casilla in rect_casillas:
        cv2.rectangle(frame, (casilla[0],casilla[1]), (casilla[0]+casilla[2], casilla[1]+casilla[3]), (0, 255, 0), 1)

    # Dibuja sobre el frame el centro de las fichas del jugador 1 y su circunferencia
    fichas_1 = obtener_fichas_color(frame, mascara_1)
    if fichas_1 is not None:
        for i in fichas_1[0, :]:
            cv2.circle(frame, (i[0], i[1]), 2, (255, 255, 200), 3)
            if dentro(i, rect_tablero):
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 3)
            else:
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 255), 3)
        ficha_libre = obtener_ficha_libre(fichas_1, rect_tablero)
        if ficha_libre is not None:
            print('Ficha libre 1, X: ', ficha_libre[0])
            print('Ficha libre 1, Y: ',ficha_libre[1])

    # Dibuja sobre el frame el centro de las fichas del jugador 2 y su circunferencia
    fichas_2 = obtener_fichas_color(frame, mascara_2)
    if fichas_2 is not None:
        for i in fichas_2[0, :]:
            cv2.circle(frame, (i[0], i[1]), 2, (0, 150, 255), 3)
            if dentro(i, rect_tablero):
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 3)
            else:
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 255), 3)
        ficha_libre = obtener_ficha_libre(fichas_2, rect_tablero)
        if ficha_libre is not None:
            print('Ficha libre 2, X: ', ficha_libre[0])
            print('Ficha libre 2, Y: ',ficha_libre[1])
    
    return frame