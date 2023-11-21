import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseArray, Pose
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
from typing import Any

class NodoVisionTablero:
    def __init__(self) -> None:
        rospy.init_node("nodo_vision_tablero",anonymous=True)
        self.publicador_estado = rospy.Publisher("topic_estado", PoseArray)
        self.publicador_coord_casillas = rospy.Publisher("topic_coord_casillas", PoseArray)
        self.suscriptor_frame = rospy.Subscriber("/usb_cam/image_raw", Image, self.frame_callback)
        self.tiempo_ciclo = rospy.Rate(10)
        
        # Instanciamos CvBridge para convertir los frames de ROS a OpenCV
        self.bridge = CvBridge()
        
        self.flag_adquisicion = True
        
        # Umbral superior e inferior para cada color
        self.umbral_inferior_azul = np.array([90, 50, 50])
        self.umbral_superior_azul = np.array([130, 255, 255])
        self.umbral_inferior_rojo1 = np.array([0, 100, 100])
        self.umbral_superior_rojo1 = np.array([10, 255, 255])
        self.umbral_inferior_rojo2 = np.array([160, 100, 100])
        self.umbral_superior_rojo2 = np.array([180, 255, 255])
        self.umbral_inferior_amarillo = np.array([20, 100, 100])
        self.umbral_superior_amarillo = np.array([40, 255, 255])
        
        self.pose_array_estado = PoseArray()
        self.coord_fichas_libres = PoseArray()
        self.coord_fichas_libres_enviadas = False
        
        rospy.wait_for_message("/usb_cam/image_raw", Image)

    def rutina(self) -> None:
        self.publicador_estado.publish(self.obtener_estado_tablero(self.frame))
        self.tiempo_ciclo.sleep()
    
    def frame_callback(self, msg: Image):
        if self.flag_adquisicion:
            print("frame recibido")
            try:
                # Convertimos el frame capturado por ROS a OpenCV
                self.frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                cv2.imshow('frame', self.frame)
                cv2.waitKey(1)
            except CvBridgeError as e:
                print(e)
            
            self.flag_adquisicion = False
        
    def start(self) -> None:
        while not rospy.is_shutdown():
            self.frame = None
            self.flag_adquisicion = True
            while self.frame is None:
                rospy.sleep(0.1)
            if not self.coord_fichas_libres_enviadas:
                # TO DO
                #self.publicador_coord_casillas.publish(self.obtener_poses_casillas)
                self.coord_fichas_libres_enviadas = True  
            #cv2.imshow('frame', self.frame)
            #cv2.waitKey(0)
            self.rutina()

    # Devuelve máscaras para cada color
    def obtener_mascaras_colores(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mascara_amarillo = cv2.inRange(hsv, self.umbral_inferior_amarillo, self.umbral_superior_amarillo)
        mascara_azul = cv2.inRange(hsv, self.umbral_inferior_azul, self.umbral_superior_azul)
        mascara_rojo1 = cv2.inRange(hsv, self.umbral_inferior_rojo1, self.umbral_superior_rojo1)
        mascara_rojo2 = cv2.inRange(hsv, self.umbral_inferior_rojo2, self.umbral_superior_rojo2)
        mascara_rojo = mascara_rojo1 + mascara_rojo2
        
        return mascara_amarillo, mascara_azul, mascara_rojo

    # Devuelve un array de fichas (circulares) detectadas en 'frame' de un color contenido en 'mascara'
    def obtener_fichas_color(self, frame, mascara) -> []:
        fichas = cv2.bitwise_and(frame, frame, mask = mascara)
        frame_gris = cv2.cvtColor(fichas, cv2.COLOR_BGR2GRAY)
        frame_gris = cv2.medianBlur(frame_gris, 5)
        fichas = cv2.HoughCircles(frame_gris, cv2.HOUGH_GRADIENT_ALT, 1, 20, param1=100, param2=0, minRadius=24, maxRadius=0)

        if fichas is not None:
            fichas = np.uint16(np.around(fichas))

        return fichas

    # Devuelve los parámetros x, y, w, h que delimitan el rectángulo del tablero
    def obtener_rectangulo_tablero(self, frame) -> Any:
        frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_desenfocado = cv2.GaussianBlur(frame_gris, (5, 5), 0)
        _, frame_umbralizado = cv2.threshold(frame_desenfocado, 50, 255, cv2.THRESH_BINARY)
        frame_bordes = cv2.Canny(frame_umbralizado, 20, 80)
        contornos, _ = cv2.findContours(frame_bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contorno_tablero = None
        if contornos:
            contorno_tablero = max(contornos, key=cv2.contourArea)

        return cv2.boundingRect(contorno_tablero)

    # Devuelve las casillas con los parámetros x, y, w, h que delimitan el rectángulo del tablero
    def obtener_rectangulos_casillas(self, rectangulo_tablero: list) -> list:
        ancho_casilla = int(rectangulo_tablero[2]/3)
        alto_casilla = int(rectangulo_tablero[3]/3)
        rectangulos_casillas = []

        for i in range(3):
            for j in range(3):
                rectangulos_casillas.append((rectangulo_tablero[0] + j*ancho_casilla, 
                                            rectangulo_tablero[1] + i*alto_casilla, ancho_casilla, alto_casilla))

        return rectangulos_casillas
    
    def obtener_poses_casillas():
        # TO DO
        pass

    # Devuelve True si el centro de 'ficha' está dentro de 'rectangulo' (x, y, w, h)
    def dentro(self, ficha, rectangulo) -> bool:
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
    def obtener_ficha_libre(self, fichas, rectangulo_tablero) -> Any:
        for i in fichas[0, :]:
            if not self.dentro(i, rectangulo_tablero):
                return i

    # Devuelve un entero que transformado a base 3 representa el estado del tablero
    def obtener_estado_tablero(self, frame) -> PoseArray:
        rect_tablero = self.obtener_rectangulo_tablero(frame)
        rect_casillas = self.obtener_rectangulos_casillas(rect_tablero)
        mascara_2, mascara_1, _ = self.obtener_mascaras_colores(frame)
        fichas_1 = self.obtener_fichas_color(frame, mascara_1)
        fichas_2 = self.obtener_fichas_color(frame, mascara_2)
        header = []

        for i in range(9):
            header[i] = '0'
            print("i: ", i)
            if fichas_1 is not None:
                for j in fichas_1[0, :]:            
                    if self.dentro(j, rect_casillas[i]):
                        print("azul: ", j)
                        header[i] = '1'                        
            if fichas_2 is not None:
                for k in fichas_2[0, :]:            
                    if self.dentro(k, rect_casillas[i]):
                        print("amarillo: ",k)
                        header[i] = '2'
        
        #ficha_libre_1 = self.obtener_ficha_libre(self, fichas_1, rect_tablero)
        #ficha_libre_2 = self.obtener_ficha_libre(self, fichas_2, rect_tablero)
        
        self.pose_array_estado.header.frame_id = str(header)
        
        pose_ficha_libre_1 = Pose()
        pose_ficha_libre_2 = Pose()
        
        # TO DO
        #pose_ficha_libre_1.position.x, pose_ficha_libre_1.position.y, pose_ficha_libre_1.position.z = x,y,z
        #pose_ficha_libre_1.orientation.x, pose_ficha_libre_1.orientation.y, pose_ficha_libre_1.orientation.z, pose_ficha_libre_1.orientation.w = qx, qy, qz, qw
        #pose_array.poses.append(pose_ficha_libre_1) 
        
        return self.pose_array_estado

    # Dibuja contornos y formas sobre el frame
    def dibujar_sobre_frame(self, frame):
        rect_tablero = self.obtener_rectangulo_tablero(frame)
        rect_casillas = self.obtener_rectangulos_casillas(rect_tablero)
        mascara_2, mascara_1, _ = self.obtener_mascaras_colores(frame)

        # Dibuja el rectángulo del tablero y las casillas
        cv2.rectangle(frame, (rect_tablero[0],rect_tablero[1]),
                    (rect_tablero[0]+rect_tablero[2], rect_tablero[1]+rect_tablero[3]), (0, 255, 0), 1)
        for casilla in rect_casillas:
            cv2.rectangle(frame, (casilla[0],casilla[1]), (casilla[0]+casilla[2], casilla[1]+casilla[3]), (0, 255, 0), 1)

        # Dibuja sobre el frame el centro de las fichas del jugador 1 y su circunferencia
        fichas_1 = self.obtener_fichas_color(frame, mascara_1)
        if fichas_1 is not None:
            for i in fichas_1[0, :]:
                cv2.circle(frame, (i[0], i[1]), 2, (255, 255, 200), 3)
                if self.dentro(i, rect_tablero):
                    cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 3)
                else:
                    cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 255), 3)
            ficha_libre = self.obtener_ficha_libre(fichas_1, rect_tablero)
            if ficha_libre is not None:
                print('Ficha libre 1, X: ', ficha_libre[0])
                print('Ficha libre 1, Y: ',ficha_libre[1])

        # Dibuja sobre el frame el centro de las fichas del jugador 2 y su circunferencia
        fichas_2 = self.obtener_fichas_color(frame, mascara_2)
        if fichas_2 is not None:
            for i in fichas_2[0, :]:
                cv2.circle(frame, (i[0], i[1]), 2, (0, 150, 255), 3)
                if self.dentro(i, rect_tablero):
                    cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 3)
                else:
                    cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 255), 3)
            ficha_libre = self.obtener_ficha_libre(fichas_2, rect_tablero)
            if ficha_libre is not None:
                print('Ficha libre 2, X: ', ficha_libre[0])
                print('Ficha libre 2, Y: ',ficha_libre[1])
        
        return frame

if __name__ == '__main__':
    nodo = NodoVisionTablero()
    nodo.start()
