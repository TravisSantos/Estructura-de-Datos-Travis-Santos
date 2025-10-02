def buscar_elemento(matriz, objetivo):
    for i in range(len(matriz)):              
        for j in range(len(matriz[i])):       
            if matriz[i][j] == objetivo:      
                return (i, j)                 
    return None                               

# Ejemplo de uso
matriz = [
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
]

print("Matriz:")
for fila in matriz:
    print(fila)

objetivo = int(input("Ingresa el numero que quieres buscar: "))
resultado = buscar_elemento(matriz, objetivo)

if resultado:
    print(f"Elemento {objetivo} encontrado en la posicion (fila={resultado[0]}, columna={resultado[1]})")
else:
    print(f"Elemento {objetivo} no se encontro en la matriz.")
