#include <iostream>
using namespace std;

// Función para mezclar dos mitades del arreglo
void merge(int arr[], int izquierda, int medio, int derecha) {
    int n1 = medio - izquierda + 1;
    int n2 = derecha - medio;

    // Arreglos temporales
    int* L = new int[n1];
    int* R = new int[n2];

    // Copiar datos a arreglos temporales
    for (int i = 0; i < n1; i++)
        L[i] = arr[izquierda + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[medio + 1 + j];

    // Mezclar los arreglos temporales
    int i = 0, j = 0, k = izquierda;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    // Copiar los elementos restantes de L[]
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    // Copiar los elementos restantes de R[]
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }

    // Liberar memoria dinámica
    delete[] L;
    delete[] R;
}

// Función principal de Merge Sort
void mergeSort(int arr[], int izquierda, int derecha) {
    if (izquierda < derecha) {
        int medio = izquierda + (derecha - izquierda) / 2;

        // Ordenar la primera y segunda mitad
        mergeSort(arr, izquierda, medio);
        mergeSort(arr, medio + 1, derecha);

        // Mezclar ambas mitades
        merge(arr, izquierda, medio, derecha);
    }
}

// Función para imprimir un arreglo
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++)
        cout << arr[i] << " ";
    cout << endl;
}

// Programa principal
int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int size = sizeof(arr) / sizeof(arr[0]);

    cout << "Arreglo original: ";
    printArray(arr, size);

    mergeSort(arr, 0, size - 1);

    cout << "Arreglo ordenado: ";
    printArray(arr, size);

    return 0;
}
