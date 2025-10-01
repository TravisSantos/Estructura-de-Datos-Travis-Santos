using System;

class QuickSortProgram
{
    static void Swap(ref int a, ref int b)
    {
        int temp = a;
        a = b;
        b = temp;
    }

    // Método para particionar el arreglo
    static int Partition(int[] arr, int low, int high)
    {
        int pivot = arr[high]; // Se elige el último elemento como pivote
        int i = (low - 1);

        for (int j = low; j < high; j++)
        {
            if (arr[j] < pivot)
            {
                i++;
                Swap(ref arr[i], ref arr[j]);
            }
        }
        Swap(ref arr[i + 1], ref arr[high]);
        return i + 1;
    }
    static void QuickSort(int[] arr, int low, int high)
    {
        if (low < high)
        {
            int pi = Partition(arr, low, high);

          
            QuickSort(arr, low, pi - 1);
            QuickSort(arr, pi + 1, high);
        }
    }

    static void Main()
    {
        int[] arr = { 64, 34, 25, 12, 22, 11, 90 };

        Console.WriteLine("Arreglo original:");
        foreach (int num in arr)
            Console.Write(num + " ");

        QuickSort(arr, 0, arr.Length - 1);

        Console.WriteLine("\n\nArreglo ordenado con Quick Sort:");
        foreach (int num in arr)
            Console.Write(num + " ");
    }
}