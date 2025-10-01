class QuickSort {
    // Método para intercambiar dos elementos
    static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    // Partición del arreglo (método Lomuto)
    static int partition(int[] arr, int low, int high) {
        int pivot = arr[high]; // último elemento como pivote
        int i = (low - 1); // índice de menor elemento
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, high);
        return i + 1;
    }

    // QuickSort recursivo
    static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);

            // Ordenar los elementos antes y después de la partición
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    // Programa principal
    public static void main(String[] args) {
        int[] arr = {64, 34, 25, 12, 22, 11, 90};
        int n = arr.length;

        System.out.println("Arreglo original:");
        for (int num : arr) {
            System.out.print(num + " ");
        }

        quickSort(arr, 0, n - 1);

        System.out.println("\n\nArreglo ordenado:");
        for (int num : arr) {
            System.out.print(num + " ");
        }
        System.out.println(); // salto de línea final
    }
}
