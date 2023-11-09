import cv2
import numpy as np
import dimensionesTablero_V3
import contornosFichas_por_colores

# Cargar la imagen
image = cv2.imread('Imagenes/tablero8.png')

# Detectar la dimensión del tablero y los contornos de las fichas
dimensionesTablero = dimensionesTablero_V3.encontrar_esquinas_casillas(image)
contours_blue, contours_red, contours_green, contours_yellow = contornosFichas_por_colores.detectar_contornos_colores(image)

# Calcular las dimensiones de las casillas
esquinas_tablero = dimensionesTablero[0]  # Accedemos a la única tupla en la lista

# Extraer las coordenadas de las esquinas
esquina_superior_izquierda = esquinas_tablero[0]
esquina_superior_derecha = esquinas_tablero[1]
esquina_inferior_izquierda = esquinas_tablero[2]
esquina_inferior_derecha = esquinas_tablero[3]

x_min, y_min = esquina_superior_izquierda
x_max, y_max = esquina_inferior_derecha

# Ahora tienes las coordenadas de las esquinas del tablero.

ancho_casilla = (x_max - x_min) // 3
alto_casilla = (y_max - y_min) // 3

# Crear una matriz para representar el tablero con información sobre si está ocupada
tablero = np.zeros((3, 3), dtype=int)

# Recorrer cada casilla del tablero
for fila in range(3):
    for columna in range(3):
        # Coordenadas de la esquina superior izquierda e inferior derecha de la casilla
        x1 = x_min + columna * ancho_casilla
        y1 = y_min + fila * alto_casilla
        x2 = x1 + ancho_casilla
        y2 = y1 + alto_casilla

        # Margen fijo en función del tamaño de la casilla
        margen_x = ancho_casilla // 10  # Ajusta este valor según tus necesidades
        margen_y = alto_casilla // 10  # Ajusta este valor según tus necesidades

        # Verificar si algún contorno está dentro de la casilla o dentro del margen
        for contorno in contours_red:
            momentos = cv2.moments(contorno)
            if momentos["m00"] != 0:
                x = int(momentos["m10"] / momentos["m00"])
                y = int(momentos["m01"] / momentos["m00"])
                if x1 - margen_x <= x <= x2 + margen_x and y1 - margen_y <= y <= y2 + margen_y:
                    tablero[fila, columna] = 1 # Jugador 1 (Rojo)
                    break  # Puedes detener la búsqueda si se encuentra un contorno en la casilla

        for contorno in contours_blue:
            momentos = cv2.moments(contorno)
            if momentos["m00"] != 0:
                x = int(momentos["m10"] / momentos["m00"])
                y = int(momentos["m01"] / momentos["m00"])
                if x1 - margen_x <= x <= x2 + margen_x and y1 - margen_y <= y <= y2 + margen_y:
                    tablero[fila, columna] = 2  # Jugador 2 (Azul)
                    break  # Puedes detener la búsqueda si se encuentra un contorno en la casilla

# En este punto, la matriz 'tablero' contiene información sobre si cada casilla está ocupada o no.

print(tablero)

