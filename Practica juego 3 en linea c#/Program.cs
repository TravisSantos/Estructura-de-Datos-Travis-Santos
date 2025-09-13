using System;

class Program
{
    static char[,] tablero = new char[3, 3]; // tablero 3x3
    static char jugadorActual = 'X';

    static void Main()
    {
        InicializarTablero();

        int movimientos = 0;
        bool juegoTerminado = false;

        while (!juegoTerminado && movimientos < 9)
        {
            Console.Clear();
            MostrarTablero();
            Console.WriteLine($"Turno del jugador {jugadorActual}");
            Console.Write("Fila (0-2): ");
            int fila = int.Parse(Console.ReadLine());
            Console.Write("Columna (0-2): ");
            int col = int.Parse(Console.ReadLine());

            if (tablero[fila, col] == ' ')
            {
                tablero[fila, col] = jugadorActual;
                movimientos++;

                if (HayGanador())
                {
                    Console.Clear();
                    MostrarTablero();
                    Console.WriteLine($"¡Jugador {jugadorActual} ha ganado!");
                    juegoTerminado = true;
                }
                else
                {
                    jugadorActual = (jugadorActual == 'X') ? 'O' : 'X';
                }
            }
            else
            {
                Console.WriteLine("Esa casilla ya está ocupada. Presiona Enter para intentar de nuevo.");
                Console.ReadLine();
            }
        }

        if (!juegoTerminado)
        {
            Console.Clear();
            MostrarTablero();
            Console.WriteLine("¡Empate!");
        }
    }

    static void InicializarTablero()
    {
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++)
                tablero[i, j] = ' ';
    }

    static void MostrarTablero()
    {
        Console.WriteLine("  0 1 2");
        for (int i = 0; i < 3; i++)
        {
            Console.Write(i + " ");
            for (int j = 0; j < 3; j++)
            {
                Console.Write(tablero[i, j]);
                if (j < 2) Console.Write("|");
            }
            Console.WriteLine();
            if (i < 2) Console.WriteLine("  -----");
        }
    }

    static bool HayGanador()
    {
        // Revisar filas y columnas
        for (int i = 0; i < 3; i++)
        {
            if (tablero[i, 0] != ' ' && tablero[i, 0] == tablero[i, 1] && tablero[i, 1] == tablero[i, 2])
                return true;
            if (tablero[0, i] != ' ' && tablero[0, i] == tablero[1, i] && tablero[1, i] == tablero[2, i])
                return true;
        }

        // Revisar diagonales
        if (tablero[0, 0] != ' ' && tablero[0, 0] == tablero[1, 1] && tablero[1, 1] == tablero[2, 2])
            return true;
        if (tablero[0, 2] != ' ' && tablero[0, 2] == tablero[1, 1] && tablero[1, 1] == tablero[2, 0])
            return true;

        return false;
    }
}