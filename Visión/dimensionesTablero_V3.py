import cv2

def encontrar_esquinas_casillas(image):
    # Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar un desenfoque para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Aplicar un umbral para detectar las áreas negras
    _, thresholded = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)

    # Aplicar la detección de bordes con Canny
    edges = cv2.Canny(thresholded, 20, 80)

    # Encontrar contornos en los bordes detectados
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar el contorno más grande, que debería ser el contorno del tablero
    contorno_tablero = max(contours, key=cv2.contourArea)

    # Crear una lista para almacenar las coordenadas de las esquinas de cada casilla
    esquinas_casillas = []

    # Iterar sobre todos los contornos encontrados
    for contorno in contours:
        # Calcular las coordenadas del rectángulo delimitador
        x, y, w, h = cv2.boundingRect(contorno)
        
        # Calcular las coordenadas de las esquinas de la casilla
        esquina_superior_izquierda = (x, y)
        esquina_superior_derecha = (x + w, y)
        esquina_inferior_izquierda = (x, y + h)
        esquina_inferior_derecha = (x + w, y + h)
        """
        si por ejemplo mi tablero estuviese girado o con un poco torcido, se podría hacer un enderezado ?

        # Obtener las coordenadas de las esquinas del tablero en la imagen original
        esquinas_originales = encontrar_esquinas_casillas(image)

        # Definir las coordenadas de las esquinas en la imagen rectificada
        # Ajusta estas coordenadas según tu necesidad
        esquina_superior_izquierda_rect = (0, 0)
        esquina_superior_derecha_rect = (ancho_tablero_rectificado, 0)
        esquina_inferior_izquierda_rect = (0, alto_tablero_rectificado)
        esquina_inferior_derecha_rect = (ancho_tablero_rectificado, alto_tablero_rectificado)

        # Calcular la matriz de transformación
        matriz_transformacion = cv2.getPerspectiveTransform(np.array(esquinas_originales, dtype=np.float32), np.array([esquina_superior_izquierda_rect, esquina_superior_derecha_rect, esquina_inferior_izquierda_rect, esquina_inferior_derecha_rect], dtype=np.float32))

        # Aplicar la transformación para enderezar el tablero
        imagen_rectificada = cv2.warpPerspective(image, matriz_transformacion, (ancho_tablero_rectificado, alto_tablero_rectificado))
        """
        
        # Agregar las coordenadas de las esquinas a la lista
        esquinas_casillas.append((esquina_superior_izquierda, esquina_superior_derecha, esquina_inferior_izquierda, esquina_inferior_derecha))

    return esquinas_casillas

# Llamar a la función con la imagen y obtener las coordenadas de las esquinas
image = cv2.imread('Imagenes/tablero0.png')
coordenadas_esquinas = encontrar_esquinas_casillas(image)
print(coordenadas_esquinas)
# Ahora, coordenadas_esquinas contiene las coordenadas de las esquinas de todas las casillas encontradas en la imagen.
