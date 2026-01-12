using System;

class RadixSort
{
    static int GetMax(int[] arr)
    {
        int max = arr[0];
        for (int i = 1; i < arr.Length; i++)
            if (arr[i] > max)
                max = arr[i];
        return max;
    }

    static void CountingSort(int[] arr, int exp)
    {
        int n = arr.Length;
        int[] output = new int[n];
        int[] count = new int[10];

        for (int i = 0; i < n; i++)
            count[(arr[i] / exp) % 10]++;

        for (int i = 1; i < 10; i++)
            count[i] += count[i - 1];

        for (int i = n - 1; i >= 0; i--)
        {
            int digit = (arr[i] / exp) % 10;
            output[count[digit] - 1] = arr[i];
            count[digit]--;
        }

        for (int i = 0; i < n; i++)
            arr[i] = output[i];
    }

    static void RadixSortMethod(int[] arr)
    {
        int max = GetMax(arr);

        for (int exp = 1; max / exp > 0; exp *= 10)
            CountingSort(arr, exp);
    }

    static void PrintArray(int[] arr)
    {
        foreach (int num in arr)
            Console.Write(num + " ");
        Console.WriteLine();
    }

    static void Main()
    {
        int[] arr = { 170, 45, 75, 90, 802, 24, 2, 66 };

        Console.WriteLine("Arreglo original:");
        PrintArray(arr);

        RadixSortMethod(arr);

        Console.WriteLine("\nArreglo ordenado:");
        PrintArray(arr);
    }
}
