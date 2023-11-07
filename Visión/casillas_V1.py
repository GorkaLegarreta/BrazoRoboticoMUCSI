import cv2
import numpy as np
import dimensionesTablero_V3
import contornosFichas_V3

# Cargar la imagen
image = cv2.imread('Imagenes/tablero9.png')

# Detectar la dimensión del tablero y los contornos de las fichas
dimensionesTablero = dimensionesTablero_V3.encontrar_esquinas_casillas(image)
contornosFichas = contornosFichas_V3.detectar_contornos_fichas(image)

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

# Recorrer cada casilla del tablero
for fila in range(3):
    for columna in range(3):
        # Coordenadas de la esquina superior izquierda e inferior derecha de la casilla
        x1 = x_min + columna * ancho_casilla
        y1 = y_min + fila * alto_casilla
        x2 = x1 + ancho_casilla
        y2 = y1 + alto_casilla

        # Margen de tolerancia para considerar que un contorno está dentro de una casilla
        margen = 5 # Ajusta este valor según tus necesidades

        # Verificar si algún contorno está dentro de la casilla
        for contorno in contornosFichas:
            for punto in contorno:
                x, y = punto[0]
                if x1 - margen <= x <= x2 + margen and y1 - margen <= y <= y2 + margen:
                    tablero[fila, columna] = True
                    break  # Puedes detener la búsqueda si se encuentra un contorno en la casilla

# En este punto, la matriz 'tablero' contiene información sobre si cada casilla está ocupada o no.
print(tablero)