import cv2
import numpy as np
import dimensionesTablero_V3
import contornosFichas_por_colores

# Cargar la imagen
image = cv2.imread('Imagenes/tablero6.png')

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
tablero = np.zeros((3, 3), dtype=bool)

# Relacionar los colores con los jugadores
colores_jugadores = {
    (0, 0, 255): 1,  # Rojo
    (255, 0, 0): 2,  # Azul
    (0, 255, 0): 3,  # Verde
    (0, 255, 255): 4  # Amarillo
}

contours = contours_blue + contours_red + contours_green + contours_yellow

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
        # Variables para almacenar el color dominante en cada casilla
        color_dominante = 0

        for contorno in contours:
            momentos = cv2.moments(contorno)
            if momentos["m00"] != 0:
                x = int(momentos["m10"] / momentos["m00"])
                y = int(momentos["m01"] / momentos["m00"])
                if x1 - margen_x <= x <= x2 + margen_x and y1 - margen_y <= y <= y2 + margen_y:
                    # Obtener el color dominante del contorno
                    if contorno in contours_red:
                        color_dominante = 1  # Jugador 1 (Rojo)
                        tablero[fila][columna] = color_dominante
                        break
                    elif contorno in contours_blue:
                        color_dominante = 2  # Jugador 2 (Azul)
                        tablero[fila][columna] = color_dominante
                        break
                    elif contorno in contours_green:
                        color_dominante = 3  # Jugador 3 (Verde)
                        tablero[fila][columna] = color_dominante
                        break
                    elif contorno in contours_yellow:
                        color_dominante = 4  # Jugador 4 (Amarillo)
                        tablero[fila][columna] = color_dominante
                        break
        

# En este punto, la matriz 'tablero' contiene información sobre si cada casilla está ocupada o no.
print(tablero)
