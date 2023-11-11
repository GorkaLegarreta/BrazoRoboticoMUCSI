import cv2
import numpy as np
import vision_tablero as vt

# Cargar una imagen o capturar desde la cámara
image = cv2.imread('Imagenes/tablero.png')  # Cambia la ruta de la imagen según tus necesidades
rectangulo_tablero = vt.obtener_rectangulo_tablero(image)
mascara_a, mascara_r = vt.obtener_mascaras_colores(image)

x, y, w, h = vt.obtener_rectangulo_tablero(image)
cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 1)
cv2.imshow('Tablero', image)
cv2.imwrite('Imagenes/presentacion_0.png', image)

fichas_azules = vt.obtener_fichas_color(image, mascara_a)
if fichas_azules is not None:
    for i in fichas_azules[0, :]:
        cv2.circle(image, (i[0], i[1]), 2, (255, 255, 200), 3)
cv2.imshow('Fichas Azules', image)
cv2.imwrite('Imagenes/presentacion_1.png', image)


fichas_rojas = vt.obtener_fichas_color(image, mascara_r)
if fichas_rojas is not None:
    for i in fichas_rojas[0, :]:
        cv2.circle(image, (i[0], i[1]), 2, (255, 200, 255), 3)
cv2.imshow('Fichas Rojas', image)
cv2.imwrite('Imagenes/presentacion_2.png', image)

if fichas_azules is not None:
    for i in fichas_azules[0, :]:
        if vt.dentro(i, rectangulo_tablero):
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 3)

if fichas_rojas is not None:
    for i in fichas_rojas[0, :]:
        if vt.dentro(i, rectangulo_tablero):
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 3)
cv2.imshow('Fichas en Juego', image)
cv2.imwrite('Imagenes/presentacion_3.png', image)

if fichas_azules is not None:
    f = vt.obtener_ficha_libre(fichas_azules, rectangulo_tablero)
    print("hola1")
    if f is not None:
        cv2.circle(image, (f[0], f[1]), f[2], (0, 255, 255), 3)
        print("hola2")

if fichas_rojas is not None:
    f = vt.obtener_ficha_libre(fichas_rojas, rectangulo_tablero)
    if f is not None:
        cv2.circle(image, (f[0], f[1]), f[2], (0, 255, 255), 3)
cv2.imshow('Fichas Libres', image)
cv2.imwrite('Imagenes/presentacion_4.png', image)


# Obtiene el estado del tablero codificado en un entero decimal
estado = vt.obtener_estado_tablero(image)
print(estado)

#obtiene el estado real del tablero como una secuencia de ceros, unos y doses
estado_descodificado = vt.base3(estado)
print(estado_descodificado)

#cv2.imshow('Sandbox de Pruebas de Vision', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
