matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("Matriz completa:")
for fila in matriz:
    print(fila)

print("\nBarrido elemento por elemento:")
for i in range(len(matriz)):         # Recorre filas
    for j in range(len(matriz[i])):  # Recorre columnas
        print(f"Elemento en [{i}][{j}] = {matriz[i][j]}")
