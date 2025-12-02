using System;
using System.Collections.Generic;
using System.Threading;

namespace SnakeGameGDB
{
    class Program
    {
        static int width = 30;
        static int height = 15;

        static List<Position> snake;
        static Position food;
        static Direction dir;
        static Random rnd = new Random();
        static bool gameOver = false;
        static int score = 0;

        static void Main()
        {
            Console.CursorVisible = false;
            InitGame();

            while (!gameOver)
            {
                if (Console.KeyAvailable)
                {
                    ConsoleKeyInfo key = Console.ReadKey(true);
                    HandleInput(key.Key);
                }

                Update();
                Draw();

                Thread.Sleep(140);
            }

            GameOverScreen();
        }

        static void InitGame()
        {
            snake = new List<Position>();
            snake.Add(new Position(width / 2, height / 2));
            snake.Add(new Position(width / 2 - 1, height / 2));
            snake.Add(new Position(width / 2 - 2, height / 2));

            dir = Direction.Right;
            SpawnFood();
            score = 0;
        }

        static void SpawnFood()
        {
            while (true)
            {
                int x = rnd.Next(1, width - 1);
                int y = rnd.Next(1, height - 1);
                Position p = new Position(x, y);

                if (!snake.Contains(p))
                {
                    food = p;
                    break;
                }
            }
        }

        static void HandleInput(ConsoleKey key)
        {
            if (key == ConsoleKey.LeftArrow && dir != Direction.Right) dir = Direction.Left;
            if (key == ConsoleKey.RightArrow && dir != Direction.Left) dir = Direction.Right;
            if (key == ConsoleKey.UpArrow && dir != Direction.Down) dir = Direction.Up;
            if (key == ConsoleKey.DownArrow && dir != Direction.Up) dir = Direction.Down;

            if (key == ConsoleKey.Escape)
                gameOver = true;
        }

        static void Update()
        {
            Position head = snake[0];
            Position newHead = head;

            switch (dir)
            {
                case Direction.Left: newHead = new Position(head.X - 1, head.Y); break;
                case Direction.Right: newHead = new Position(head.X + 1, head.Y); break;
                case Direction.Up: newHead = new Position(head.X, head.Y - 1); break;
                case Direction.Down: newHead = new Position(head.X, head.Y + 1); break;
            }

            // choque con paredes
            if (newHead.X <= 0 || newHead.X >= width - 1 || newHead.Y <= 0 || newHead.Y >= height - 1)
            {
                gameOver = true;
                return;
            }

            // choque consigo mismo
            if (snake.Contains(newHead))
            {
                gameOver = true;
                return;
            }

            // comer
            if (newHead.Equals(food))
            {
                snake.Insert(0, newHead);
                score += 10;
                SpawnFood();
            }
            else
            {
                snake.Insert(0, newHead);
                snake.RemoveAt(snake.Count - 1);
            }
        }

        static void Draw()
        {
            Console.Clear();

            // bordes
            for (int x = 0; x < width; x++) Console.Write("-");
            Console.WriteLine();

            for (int y = 1; y < height - 1; y++)
            {
                Console.Write("|");
                for (int x = 1; x < width - 1; x++)
                {
                    Position p = new Position(x, y);

                    if (p.Equals(snake[0]))
                        Console.Write("O"); // cabeza
                    else if (snake.Contains(p))
                        Console.Write("o"); // cuerpo
                    else if (p.Equals(food))
                        Console.Write("X"); // comida
                    else
                        Console.Write(" ");
                }
                Console.WriteLine("|");
            }

            for (int x = 0; x < width; x++) Console.Write("-");
            Console.WriteLine();

            Console.WriteLine("Puntaje: " + score);
            Console.WriteLine("ESC para salir");
        }

        static void GameOverScreen()
        {
            Console.Clear();
            Console.WriteLine("--- GAME OVER ---");
            Console.WriteLine("Puntaje final: " + score);
            Console.WriteLine("Tamano del gusano: " + snake.Count);
            Console.WriteLine("Presiona una tecla para salir...");
            Console.ReadKey();
        }

        struct Position : IEquatable<Position>
        {
            public int X { get; }
            public int Y { get; }

            public Position(int x, int y)
            {
                X = x;
                Y = y;
            }

            public bool Equals(Position other) => X == other.X && Y == other.Y;
            public override bool Equals(object obj) => obj is Position p && Equals(p);
            public override int GetHashCode() => X * 397 ^ Y;
        }

        enum Direction { Left, Right, Up, Down }
    }
}
