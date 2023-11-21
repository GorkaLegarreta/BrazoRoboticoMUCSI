import rospy
from geometry_msgs.msg import PoseArray, Pose
import random
from abc import abstractmethod

class NodoLogica:
    def __init__(self) -> None:
        rospy.init_node("nodo_logica",anonymous=True)
        self.flag_adquisicion = True
        self.t = Tablero()
        self.j1 = JugadorMinMax('1')
        self.j2 = JugadorMinMax('2')
        # Además del suscriptor_estado también serán necesarios:
        # - suscriptor_coordenadas_casillas Float32MultiArray de 9 (único mensaje al inicio)
        # - suscriptoror_fichas_libres Float32MultiArray de 2 (10 Hz al igual que publicador_estado)
        self.suscriptor_frame = rospy.Subscriber("topic_estado", PoseArray, self.estado_callback)
        
        rospy.wait_for_message("topic_estado", PoseArray)
    
    def estado_callback(self, data: PoseArray) -> None:
        if self.flag_adquisicion:
            self.t.estado = self.decodificar_estado(data.header.frame_id)
            print(self.t.estado)
            self.flag_adquisicion = False
    
    # Bucle del juego de Tres en Raya
    def jugar_partida(self) -> None:
        while not rospy.is_shutdown():
            self.t.estado = None
            self.flag_adquisicion = True
            while self.t.estado is None:
                rospy.sleep(0.1)
            if not self.t.es_victoria() and not self.t.es_empate():
                self.t.colocar_ficha(self.j1.ficha, self.j1.seleccionar_casilla(self.t))
                print(self.t.estado)
            else: 
                break
            if not self.t.es_victoria() and not self.t.es_empate():
                self.t.colocar_ficha(self.j2.ficha, self.j2.seleccionar_casilla(self.t))
                print(self.t.estado)
            else: 
                break
        if self.t.es_ganador('1'):
            print('Ha ganado el jugador 1! :)')
        elif self.t.es_ganador('2'):
            print('Ha ganado el jugador 2! :)')
        elif self.t.es_empate():
            print('Empate! :)')
    
    # Método que decodifica la situación del tablero de un estado entero decimal a un string
    # Devuelve una cadena de 9 caracteres (0, 1, 2) representando el estado del tablero
    def decodificar_estado(self, numero) -> str:
        resto = ''
        for i in range(9):
            if numero != 0:
                cociente = int(numero / 3)
                resto += str(numero % 3)
                numero = cociente
            else:
                resto += '0'
        return resto

class Tablero:
    def __init__(self) -> None:
        self.estado = '000000000'

    # Método encargado de comunicarse con el nodo de visión
    # Solicita al nodo de visión el estado actual del tablero que recibe como entero D
    # Decodifica dicho entero y lo convierte a string
    def actualizar_estado(self) -> str:
        pass

    # Método encargado de comunicarse con los nodos de visión y robótica
    # Solicita al nodo de vision la ubicación de una ficha libre (TOPIC)
    # Solicita al nodo de robótica colocar la ficha en dicha ubicación(casilla) (TOPIC)
    def colocar_ficha(self, ficha, casilla) -> None:
        #self.estado = self.estado[:casilla] + ficha + self.estado[casilla+1:]
        pass
    
    # Comprueba si el tablero se encuentra en estado de victoria
    def es_victoria(self) -> bool:
        if  self.estado[0] == self.estado[1] == self.estado[2] != '0' or \
            self.estado[3] == self.estado[4] == self.estado[5] != '0' or \
            self.estado[6] == self.estado[7] == self.estado[8] != '0' or \
            self.estado[0] == self.estado[3] == self.estado[6] != '0' or \
            self.estado[1] == self.estado[4] == self.estado[7] != '0' or \
            self.estado[2] == self.estado[5] == self.estado[8] != '0' or \
            self.estado[0] == self.estado[4] == self.estado[8] != '0' or \
            self.estado[2] == self.estado[4] == self.estado[6] != '0':
            return True
        else:
            return False

    # Comprueba si el jugador 'ficha' ha ganado 
    def es_ganador(self, ficha) -> bool:
        if  self.estado[0] == self.estado[1] == self.estado[2] == ficha or \
            self.estado[3] == self.estado[4] == self.estado[5] == ficha or \
            self.estado[6] == self.estado[7] == self.estado[8] == ficha or \
            self.estado[0] == self.estado[3] == self.estado[6] == ficha or \
            self.estado[1] == self.estado[4] == self.estado[7] == ficha or \
            self.estado[2] == self.estado[5] == self.estado[8] == ficha or \
            self.estado[0] == self.estado[4] == self.estado[8] == ficha or \
            self.estado[2] == self.estado[4] == self.estado[6] == ficha:
            return True
        else:
            return False
        
    # Comprueba si el jugador 'ficha' ha ganado 
    def es_empate(self) -> bool:
        if  not self.es_victoria() and self.estado.count('0') == 0:
            #print("empaterrrr")
            return True
        else:
            return False

class Jugador:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def seleccionar_casilla(self, t:Tablero) -> int:
        pass

#Clase que hereda de la clase base Jugador e implementa el método seleccionar_casilla con minimax
class JugadorMinMax(Jugador):
    def __init__(self, ficha: str) -> None:
        super().__init__()
        self.cache = {}
        self.ficha = ficha
        if self.ficha == '1':
            self.otra_ficha = '2'
        else: self.otra_ficha = '1'

    def seleccionar_casilla(self, t:Tablero) -> int:
        if self.ficha == '1' and t.estado == '000000000':
            return random.choice([x for x in range(9) if x % 2 == 0])

        _, accion = self.minimax(t, 0, True)

        return accion

    def minimax(self, t:Tablero, profundidad:int, es_maximizador:bool) -> tuple:
        if t.estado in self.cache:
            return random.choice(self.cache[t.estado])
        
        if t.es_ganador(self.ficha): 
            return 1, -1
        if t.es_ganador(self.otra_ficha): 
            return -1, -1
        if t.es_empate():
            return 0, -1

        if es_maximizador:
            mejores_valores = {}
            mejor_valor = -100
            for i in range(9):
                if t.estado[i] == '0':
                    t.estado = t.estado[:i] + self.ficha + t.estado[i+1:]
                    valor, _ = self.minimax(t, profundidad+1, False)
                    t.estado = t.estado[:i] + '0' + t.estado[i+1:]
                    if valor > mejor_valor:
                        mejor_valor = valor
                        mejores_valores = {(mejor_valor, i)}
                    elif valor == mejor_valor:
                        mejores_valores.add((valor, i))
            mejores_valores = tuple(mejores_valores) 
            self.cache[t.estado] = mejores_valores  
            return random.choice(mejores_valores)
        else:
            mejores_valores = {}
            mejor_valor = 100
            for i in range(9):
                if t.estado[i] == '0':
                    t.estado = t.estado[:i] + self.otra_ficha + t.estado[i+1:]
                    valor, _ = self.minimax(t, profundidad+1, True)
                    t.estado = t.estado[:i] + '0' + t.estado[i+1:]
                    if valor < mejor_valor:
                        mejor_valor = valor
                        mejores_valores = {(mejor_valor, i)}
                    elif valor == mejor_valor:
                        mejores_valores.add((valor, i))
            mejores_valores = tuple(mejores_valores) 
            self.cache[t.estado] = mejores_valores  
            return random.choice(mejores_valores)
        
if __name__ == '__main__':
        nodo = NodoLogica()
        nodo.jugar_partida()