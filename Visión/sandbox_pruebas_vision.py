import cv2
import numpy as np
import vision_tablero as vt

# Cargar una imagen o capturar desde la cámara
image = cv2.imread('Imagenes/tablero.png')  # Cambia la ruta de la imagen según tus necesidades

# Obtiene el estado del tablero codificado en un entero decimal
estado = vt.obtener_estado_tablero(image)
print(estado)

rectangulo_tablero = vt.obtener_rectangulo_tablero(image)
_, mascara_a, mascara_r = vt.obtener_mascaras_colores(image)

# Bloque que obtiene las fichas azules
fichas_azules = vt.obtener_fichas_color(image, mascara_a)
if fichas_azules is not None:
    for i in fichas_azules[0, :]:
        # dibuja en rosa la circunferencia de todas las fichas azules
        cv2.circle(image, (i[0], i[1]), i[2], (255, 0, 255), 2)
        # si la ficha esta dentro del tablero marca el centro en amarillo
        if vt.dentro(i, rectangulo_tablero):
            cv2.circle(image, (i[0], i[1]), 2, (0, 255, 255), 3)

    ficha_libre = vt.obtener_ficha_libre(fichas_azules, rectangulo_tablero)
    # si hay una ficha libre marca el centro en verde
    if ficha_libre is not None:
        cv2.circle(image, (ficha_libre[0], ficha_libre[1]), 2, (0, 255, 0), 3)

# Bloque que contiene las fichas rojas
fichas_rojas = vt.obtener_fichas_color(image, mascara_r)
if fichas_rojas is not None:
    for i in fichas_rojas[0, :]:
        # dibuja en negro la circunferencia de todas las fichas rojas
        cv2.circle(image, (i[0], i[1]), i[2], (0, 0, 0), 2)
        # si la ficha está dentro del tablero, marca el centro en amarillo
        if vt.dentro(i, rectangulo_tablero):
            cv2.circle(image, (i[0], i[1]), 2, (0, 255, 255), 3)

    ficha_libre = vt.obtener_ficha_libre(fichas_rojas, rectangulo_tablero)
    # si hay una ficha libre, marca el centro en verde
    if ficha_libre is not None:
        cv2.circle(image, (ficha_libre[0], ficha_libre[1]), 2, (0, 255, 0), 3)

cv2.imshow('Sandbox de Pruebas de Vision', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
