def mostrar_tablero(tablero):
    for fila in tablero:
        print(" | ".join(fila))
        print("---------")

def es_empate(tablero):
    for fila in tablero:
        if " " in fila:
            return False
    return True

def jugar_tres_en_raya():
    tablero = [[" " for _ in range(3)] for _ in range(3)]
    jugador = "X"

    while True:
        mostrar_tablero(tablero)
        fila = int(input(f"Jugador {jugador}, elige una fila (0, 1, 2): "))
        columna = int(input(f"Jugador {jugador}, elige una columna (0, 1, 2): "))

        if tablero[fila][columna] == " ":
            tablero[fila][columna] = jugador
        else:
            print("Casilla ocupada. Intenta de nuevo.")
            continue

        # Verificar si alguien ganó
        for i in range(3):
            if tablero[i][0] == tablero[i][1] == tablero[i][2] != " " or \
               tablero[0][i] == tablero[1][i] == tablero[2][i] != " ":
                mostrar_tablero(tablero)
                print(f"¡Jugador {jugador} ha ganado!")
                return

        if tablero[0][0] == tablero[1][1] == tablero[2][2] != " " or \
           tablero[0][2] == tablero[1][1] == tablero[2][0] != " ":
            mostrar_tablero(tablero)
            print(f"¡Jugador {jugador} ha ganado!")
            return
        
        # Verificar si hay un empate
        if es_empate(tablero):
            mostrar_tablero(tablero)
            print("¡Es un empate!")
            return

        # Si no hay ganador, alternar jugadores
        jugador = "O" if jugador == "X" else "X"

jugar_tres_en_raya()
