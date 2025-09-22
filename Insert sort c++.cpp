#include <iostream>
#include <vector>
using namespace std;

void insertionSort(vector<int>& arr) {
    int n = arr.size();

    // Recorremos el arreglo desde el segundo elemento
    for (int i = 1; i < n; i++) {
        int clave = arr[i];  
        int j = i - 1;

        while (j >= 0 && arr[j] > clave) {
            arr[j + 1] = arr[j];
            j--;
        }

        // Insertamos la clave en la posición correcta
        arr[j + 1] = clave;
    }
}

int main() {
    vector<int> numeros = {8, 3, 5, 4, 1};

    cout << "Lista original: ";
    for (int num : numeros) cout << num << " ";
    cout << endl;

    insertionSort(numeros);

    cout << "Lista ordenada: ";
    for (int num : numeros) cout << num << " ";
    cout << endl;

    return 0;
}