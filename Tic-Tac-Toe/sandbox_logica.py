import logica as lg

def jugar_partida(t:lg.Tablero, j1:lg.Jugador, j2:lg.Jugador) -> None:
    while True:
        if not t.es_victoria() and not t.es_empate():
            t.colocar_ficha(j1.ficha, j1.seleccionar_casilla(t))
            print(t.estado)
        else: 
            break
        if not t.es_victoria() and not t.es_empate():
            t.colocar_ficha(j2.ficha, j2.seleccionar_casilla(t))
            print(t.estado)
        else: 
            break
    if t.es_ganador('1'):
        print('Ha ganado el jugador 1! :)')
    elif t.es_ganador('2'):
        print('Ha ganado el jugador 2! :)')
    elif t.es_empate():
        print('Empate! :)')

t = lg.Tablero()
j1 = lg.JugadorMinMax('1')
j2 = lg.JugadorMinMax('2')

jugar_partida(t, j1, j2)
            
        
