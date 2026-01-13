#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <string>

using namespace std;
using namespace chrono;

void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - i - 1; j++)
            if (arr[j] > arr[j + 1])
                swap(arr[j], arr[j + 1]);
}

void insertionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

void selectionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++)
            if (arr[j] < arr[minIdx])
                minIdx = j;
        swap(arr[i], arr[minIdx]);
    }
}

int partitionQS(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partitionQS(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

void merge(vector<int>& arr, int l, int m, int r) {
    vector<int> L(arr.begin() + l, arr.begin() + m + 1);
    vector<int> R(arr.begin() + m + 1, arr.begin() + r + 1);

    int i = 0, j = 0, k = l;
    while (i < L.size() && j < R.size()) {
        if (L[i] <= R[j]) arr[k++] = L[i++];
        else arr[k++] = R[j++];
    }
    while (i < L.size()) arr[k++] = L[i++];
    while (j < R.size()) arr[k++] = R[j++];
}

void mergeSort(vector<int>& arr, int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

int getMax(vector<int>& arr) {
    return *max_element(arr.begin(), arr.end());
}

void countingSort(vector<int>& arr, int exp) {
    int n = arr.size();
    vector<int> output(n);
    int count[10] = {0};

    for (int i = 0; i < n; i++)
        count[(arr[i] / exp) % 10]++;

    for (int i = 1; i < 10; i++)
        count[i] += count[i - 1];

    for (int i = n - 1; i >= 0; i--) {
        int idx = (arr[i] / exp) % 10;
        output[count[idx] - 1] = arr[i];
        count[idx]--;
    }

    arr = output;
}

void radixSort(vector<int>& arr) {
    int maxVal = getMax(arr);
    for (int exp = 1; maxVal / exp > 0; exp *= 10)
        countingSort(arr, exp);
}

vector<int> generarArreglo(int tamaño) {
    vector<int> arr(tamaño);
    for (int i = 0; i < tamaño; i++)
        arr[i] = rand() % 10000;
    return arr;
}

int main() {
    srand(time(0));

    vector<int> arr20 = generarArreglo(20);
    vector<int> arr100 = generarArreglo(100);
    vector<int> arr1000 = generarArreglo(1000);

    int opcion;
    cout << "Seleccione el tamaño del arreglo:\n";
    cout << "1. 20 elementos\n";
    cout << "2. 100 elementos\n";
    cout << "3. 1000 elementos\n";
    cout << "Opcion: ";
    cin >> opcion;

    vector<int> base;

    if (opcion == 1) base = arr20;
    else if (opcion == 2) base = arr100;
    else if (opcion == 3) base = arr1000;
    else {
        cout << "Opcion invalida\n";
        return 0;
    }

    vector<pair<string, double>> resultados;

    auto probar = [&](string nombre, auto funcion) {
        vector<int> copia = base;
        auto inicio = high_resolution_clock::now();
        funcion(copia);
        auto fin = high_resolution_clock::now();
        double tiempo = duration<double, milli>(fin - inicio).count();
        resultados.push_back({nombre, tiempo});
    };

    probar("Bubble Sort", [](vector<int>& a){ bubbleSort(a); });
    probar("Insertion Sort", [](vector<int>& a){ insertionSort(a); });
    probar("Selection Sort", [](vector<int>& a){ selectionSort(a); });
    probar("Quick Sort", [](vector<int>& a){ quickSort(a, 0, a.size() - 1); });
    probar("Merge Sort", [](vector<int>& a){ mergeSort(a, 0, a.size() - 1); });
    probar("Radix Sort", [](vector<int>& a){ radixSort(a); });

    sort(resultados.begin(), resultados.end(),
         [](auto& a, auto& b){ return a.second < b.second; });

    cout << "\nResultados (ordenados por rapidez):\n\n";
    for (auto& r : resultados)
        cout << r.first << ": " << r.second << " ms\n";

    cout << "\nMetodo mas rapido: " << resultados[0].first << endl;

    return 0;
}
