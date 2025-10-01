function quickSort(arr) {
    if (arr.length <= 1) {
        return arr; // Caso base: ya está ordenado
    }

    const pivot = arr[arr.length - 1]; // Elegimos el último elemento como pivote
    const left = [];   // Elementos menores al pivote
    const right = [];  // Elementos mayores al pivote

    for (let i = 0; i < arr.length - 1; i++) {
        if (arr[i] < pivot) {
            left.push(arr[i]);
        } else {
            right.push(arr[i]);
        }
    }

    // Llamada recursiva
    return [...quickSort(left), pivot, ...quickSort(right)];
}

// Ejemplo de uso
const arr = [64, 34, 25, 12, 22, 11, 90];

console.log("Arreglo original:", arr);
const ordenado = quickSort(arr);
console.log("Arreglo ordenado:", ordenado);
