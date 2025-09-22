using System;

class Program
{
    static void InsertionSort(int[] arr)
    {
        int n = arr.Length;

        // Recorremos el arreglo desde el segundo elemento
        for (int i = 1; i < n; i++)
        {
            int clave = arr[i]; 
            int j = i - 1;

            while (j >= 0 && arr[j] > clave)
            {
                arr[j + 1] = arr[j];
                j--;
            }

            // Insertamos la clave en la posición correcta
            arr[j + 1] = clave;
        }
    }

    static void Main()
    {
        int[] numeros = { 8, 3, 5, 4, 1 };

        Console.WriteLine("Lista original: " + string.Join(" ", numeros));

        InsertionSort(numeros);

        Console.WriteLine("Lista ordenada: " + string.Join(" ", numeros));
    }
}