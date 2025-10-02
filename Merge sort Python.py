def merge_sort(arr):
    if len(arr) > 1:
        # Encontrar el punto medio
        mid = len(arr) // 2

        # Dividir en dos mitades
        izquierda = arr[:mid]
        derecha = arr[mid:]

        # Llamadas recursivas para ordenar ambas mitades
        merge_sort(izquierda)
        merge_sort(derecha)

        # Índices iniciales para recorrer las mitades
        i = j = k = 0

        # Mezclar los datos en arr[]
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i] < derecha[j]:
                arr[k] = izquierda[i]
                i += 1
            else:
                arr[k] = derecha[j]
                j += 1
            k += 1

        # Copiar los elementos restantes de izquierda[]
        while i < len(izquierda):
            arr[k] = izquierda[i]
            i += 1
            k += 1

        # Copiar los elementos restantes de derecha[]
        while j < len(derecha):
            arr[k] = derecha[j]
            j += 1
            k += 1


arr = [64, 34, 25, 12, 22, 11, 90]
print("Arreglo original:", arr)

merge_sort(arr)

print("Arreglo ordenado:", arr)
