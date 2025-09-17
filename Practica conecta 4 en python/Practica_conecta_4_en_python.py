# -*- coding: utf-8 -*-
FILAS = 6
COLUMNAS = 7

# --- Crear tablero vacío ---
def crear_tablero():
    return [[" " for _ in range(COLUMNAS)] for _ in range(FILAS)]

# --- Mostrar tablero en consola ---
def mostrar_tablero(tablero):
    for fila in tablero:
        print("|" + "|".join(fila) + "|")
    print(" " + " ".join(str(i) for i in range(COLUMNAS)))

# --- Colocar ficha en la columna seleccionada ---
def soltar_ficha(tablero, col, ficha):
    for fila in range(FILAS - 1, -1, -1):
        if tablero[fila][col] == " ":
            tablero[fila][col] = ficha
            return True
    return False  # columna llena

# --- Detectar 4 fichas consecutivas horizontal ---
def hay_ganador_horizontal(tablero, ficha):
    for fila in range(FILAS):
        for col in range(COLUMNAS - 3):
            if (tablero[fila][col] == ficha and
                tablero[fila][col+1] == ficha and
                tablero[fila][col+2] == ficha and
                tablero[fila][col+3] == ficha):
                return True
    return False

# --- Detectar 4 fichas consecutivas vertical ---
def hay_ganador_vertical(tablero, ficha):
    for col in range(COLUMNAS):
        for fila in range(FILAS - 3):
            if (tablero[fila][col] == ficha and
                tablero[fila+1][col] == ficha and
                tablero[fila+2][col] == ficha and
                tablero[fila+3][col] == ficha):
                return True
    return False

# --- Detectar 4 fichas consecutivas diagonal descendente (\) ---
def hay_ganador_diagonal_desc(tablero, ficha):
    for fila in range(FILAS - 3):
        for col in range(COLUMNAS - 3):
            if (tablero[fila][col] == ficha and
                tablero[fila+1][col+1] == ficha and
                tablero[fila+2][col+2] == ficha and
                tablero[fila+3][col+3] == ficha):
                return True
    return False

# --- Detectar 4 fichas consecutivas diagonal ascendente (/) ---
def hay_ganador_diagonal_asc(tablero, ficha):
    for fila in range(3, FILAS):
        for col in range(COLUMNAS - 3):
            if (tablero[fila][col] == ficha and
                tablero[fila-1][col+1] == ficha and
                tablero[fila-2][col+2] == ficha and
                tablero[fila-3][col+3] == ficha):
                return True
    return False

# --- Comprobar todas las formas de ganar ---
def hay_ganador(tablero, ficha):
    return (hay_ganador_horizontal(tablero, ficha) or
            hay_ganador_vertical(tablero, ficha) or
            hay_ganador_diagonal_desc(tablero, ficha) or
            hay_ganador_diagonal_asc(tablero, ficha))

# --- Comprobar si el tablero está lleno ---
def tablero_lleno(tablero):
    return all(tablero[0][col] != " " for col in range(COLUMNAS))

# --- Lógica principal del juego ---
def jugar():
    tablero = crear_tablero()
    jugador_actual = "X"

    while True:
        mostrar_tablero(tablero)
        print(f"Turno del jugador {jugador_actual}")

        # Pedir columna
        try:
            col = int(input("Elige una columna (0-6): "))
            if col < 0 or col >= COLUMNAS:
                print("Columna invalida.")
                continue
        except ValueError:
            print("Debes escribir un numero.")
            continue

        # Colocar ficha
        if not soltar_ficha(tablero, col, jugador_actual):
            print("Columna llena.")
            continue

        # Comprobar ganador
        if hay_ganador(tablero, jugador_actual):
            mostrar_tablero(tablero)
            print(f"Jugador {jugador_actual} gana!")
            break
        elif tablero_lleno(tablero):
            mostrar_tablero(tablero)
            print("Empate.")
            break
        else:
            # Cambiar de jugador
            jugador_actual = "O" if jugador_actual == "X" else "X"

# --- Ejecutar juego ---
if __name__ == "__main__":
    jugar()
