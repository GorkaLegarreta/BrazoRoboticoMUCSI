import cv2

video_capture =  cv2.VideoCapture(0)
count = 0

while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    cv2.imshow("Camara Gorka", frame)
    # Espera la pulsación de una tecla
    key = cv2.waitKey(1) & 0xFF    
    if key == ord('s'): # Si se pulsa 's', guarda la imagen actual
        count += 1
        image_name = f'Imagenes/gorka_{count}.png'  # Nombre del archivo de imagen
        cv2.imwrite(image_name, frame)  # Guarda la imagen en un archivo    
    elif key == ord('q'): # Si se pulsa 'q', sale del bucle        
        cv2.destroyWindow("Camara con filtro")
        break

video_capture.release()
cv2.waitKey()
cv2.destroyAllWindows()