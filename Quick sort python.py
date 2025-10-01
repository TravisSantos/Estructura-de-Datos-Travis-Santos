def quick_sort(arr):
    if len(arr) <= 1:
        return arr  # Caso base: ya está ordenado
    else:
        pivote = arr[len(arr) // 2]  # Elegimos el pivote (mitad del arreglo)
        menores = [x for x in arr if x < pivote]     # Elementos menores al pivote
        iguales = [x for x in arr if x == pivote]    # Elementos iguales al pivote
        mayores = [x for x in arr if x > pivote]     # Elementos mayores al pivote
        return quick_sort(menores) + iguales + quick_sort(mayores)

nums = [64, 34, 25, 12, 22, 11, 90]
print("Arreglo original:", nums)
ordenado = quick_sort(nums)
print("Arreglo ordenado:", ordenado)