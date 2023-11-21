import cv2

video_capture = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Selecciona el códec para el video
out = cv2.VideoWriter('Videos/javi_videos.avi', fourcc, 20.0, (640, 480))  # Nombre del archivo de video y configuración

while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    cv2.imshow("Camara Gorka", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):  # Si se pulsa 'r', graba el frame actual al video
        out.write(frame)
    elif key == ord('q'):
        cv2.destroyWindow("Camara Gorka")
        break

video_capture.release()
out.release()
cv2.waitKey()
cv2.destroyAllWindows()
