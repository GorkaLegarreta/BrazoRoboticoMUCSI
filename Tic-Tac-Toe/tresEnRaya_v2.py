import random

def mostrar_tablero(tablero):
    for fila in tablero:
        print(" | ".join(fila))
        print("---------")

def es_empate(tablero):
    for fila in tablero:
        if " " in fila:
            return False
    return True

def jugador_gana(tablero, jugador):
    for i in range(3):
        if all(casilla == jugador for casilla in tablero[i]) or \
           all(tablero[j][i] == jugador for j in range(3)):
            return True
    if all(tablero[i][i] == jugador for i in range(3)) or \
       all(tablero[i][2 - i] == jugador for i in range(3)):
        return True
    return False

def movimiento_maquina(tablero):
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == " ":
                return i, j
    return None

def jugar_tres_en_raya():
    tablero = [[" " for _ in range(3)] for _ in range(3)]
    jugador_humano = "X"
    jugador_maquina = "O"

    while True:
        mostrar_tablero(tablero)

        if jugador_humano == "X":
            fila = int(input(f"Jugador {jugador_humano}, elige una fila (0, 1, 2): "))
            columna = int(input(f"Jugador {jugador_humano}, elige una columna (0, 1, 2): "))
        else:
            print("Turno de la máquina (O)...")
            fila, columna = movimiento_maquina(tablero)
            if fila is None:
                print("¡Es un empate!")
                break

        if tablero[fila][columna] == " ":
            tablero[fila][columna] = jugador_humano
            if jugador_gana(tablero, jugador_humano):
                mostrar_tablero(tablero)
                print(f"¡Jugador {jugador_humano} ha ganado!")
                break

        if es_empate(tablero):
            mostrar_tablero(tablero)
            print("¡Es un empate!")
            break

        jugador_humano, jugador_maquina = jugador_maquina, jugador_humano

jugar_tres_en_raya()
