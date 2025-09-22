def insertion_sort(lista):
    # Recorremos la lista desde el segundo elemento
    for i in range(1, len(lista)):
        clave = lista[i]        # Guardamos el valor actual
        j = i - 1               # Empezamos a comparar con el anterior

        # Desplazamos los elementos mayores que la clave una posición a la derecha
        while j >= 0 and lista[j] > clave:
            lista[j + 1] = lista[j]
            j -= 1

        # Insertamos la clave en la posición correcta
        lista[j + 1] = clave
    
    return lista


# Ejemplo de uso
numeros = [8, 3, 5, 4, 1]
print("Lista original:", numeros)
print("Lista ordenada:", insertion_sort(numeros))