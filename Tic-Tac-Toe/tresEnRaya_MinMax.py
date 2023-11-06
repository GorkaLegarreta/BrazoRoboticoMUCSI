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

def minimax(tablero, profundidad, es_maximizador):
    if jugador_gana(tablero, "O"):
        return 1
    if jugador_gana(tablero, "X"):
        return -1
    if es_empate(tablero):
        return 0

    if es_maximizador:
        mejor_valor = -float("inf")
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == " ":
                    tablero[i][j] = "O"
                    valor = minimax(tablero, profundidad + 1, False)
                    tablero[i][j] = " "
                    mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:
        mejor_valor = float("inf")
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == " ":
                    tablero[i][j] = "X"
                    valor = minimax(tablero, profundidad + 1, True)
                    tablero[i][j] = " "
                    mejor_valor = min(mejor_valor, valor)
        return mejor_valor

def movimiento_maquina_inteligente(tablero):
    mejor_valor = -float("inf")
    mejor_movimiento = None
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == " ":
                tablero[i][j] = "O"
                valor = minimax(tablero, 0, False)
                tablero[i][j] = " "
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = (i, j)
    return mejor_movimiento

def jugar_tres_en_raya():
    tablero = [[" " for _ in range(3)] for _ in range(3)]

    while True:
        mostrar_tablero(tablero)

        fila = int(input("Jugador X, elige una fila (0, 1, 2): "))
        columna = int(input("Jugador X, elige una columna (0, 1, 2): "))
        
        if tablero[fila][columna] == " ":
            tablero[fila][columna] = "X"
            if jugador_gana(tablero, "X"):
                mostrar_tablero(tablero)
                print("¡Jugador X ha ganado!")
                break

        if es_empate(tablero):
            mostrar_tablero(tablero)
            print("¡Es un empate!")
            break

        movimiento = movimiento_maquina_inteligente(tablero)
        tablero[movimiento[0]][movimiento[1]] = "O"
        
        if jugador_gana(tablero, "O"):
            mostrar_tablero(tablero)
            print("¡La máquina (O) ha ganado!")
            break

        if es_empate(tablero):
            mostrar_tablero(tablero)
            print("¡Es un empate!")
            break

jugar_tres_en_raya()
