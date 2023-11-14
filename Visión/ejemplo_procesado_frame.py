import cv2
import numpy as np
import vision_tablero as vt

# Carga una imagen
image = cv2.imread('Imagenes/javi_14.png')

# Obtiene el estado del tablero
# Siempre se obtiene el estado del tablero antes de dibujar en el frame!
print(vt.obtener_estado_tablero(image))

# Dibuja sobre el frame las formas y contornos relevantes
vt.dibujar_sobre_frame(image)

# Muestra el frame sobredibujado
cv2.imshow('Fichas Libres', image)

# Guarda el frame sobredibujado
#cv2.imwrite('Imagenes/presentacion_4.png', image)

cv2.waitKey(0)
cv2.destroyAllWindows()
