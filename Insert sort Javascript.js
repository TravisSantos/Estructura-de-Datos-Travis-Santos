function insertionSort(arr) {
    let n = arr.length;

    // Recorremos el arreglo desde el segundo elemento
    for (let i = 1; i < n; i++) {
        let clave = arr[i];  // Guardamos el valor actual
        let j = i - 1;

        // Desplazamos los elementos mayores que la clave una posición a la derecha
        while (j >= 0 && arr[j] > clave) {
            arr[j + 1] = arr[j];
            j--;
        }

        // Insertamos la clave en la posición correcta
        arr[j + 1] = clave;
    }
    return arr;
}

// Ejemplo de uso
let numeros = [8, 3, 5, 4, 1];
console.log("Lista original:", numeros);
console.log("Lista ordenada:", insertionSort([...numeros]));