import java.util.*;
import java.io.*;

public class Main {
    static int[][] board = new int[9][9];
    static boolean[][] fixed = new boolean[9][9];
    static int lives = 3;
    static Scanner sc = new Scanner(System.in);
    static String saveFile = "sudoku_save.txt";

    public static void main(String[] args) {
        System.out.println("=== Sudoku Game ===");
        System.out.println("1. Nuevo juego");
        System.out.println("2. Cargar juego guardado");
        int option = sc.nextInt();

        if (option == 2 && loadGame()) {
            System.out.println("Progreso cargado exitosamente!");
        } else {
            System.out.println("Selecciona dificultad: 1 (Facil), 2 (Medio), 3 (Dificil)");
            int difficulty = sc.nextInt();
            generateBoard(difficulty);
        }

        playGame();
    }

    // Generar tablero inicial según la dificultad
    public static void generateBoard(int difficulty) {
        // Tablero base solucionado
        int[][] solved = {
            {5,3,4,6,7,8,9,1,2},
            {6,7,2,1,9,5,3,4,8},
            {1,9,8,3,4,2,5,6,7},
            {8,5,9,7,6,1,4,2,3},
            {4,2,6,8,5,3,7,9,1},
            {7,1,3,9,2,4,8,5,6},
            {9,6,1,5,3,7,2,8,4},
            {2,8,7,4,1,9,6,3,5},
            {3,4,5,2,8,6,1,7,9}
        };

        // Copiamos la solucion al tablero
        for (int i = 0; i < 9; i++)
            for (int j = 0; j < 9; j++)
                board[i][j] = solved[i][j];

        // Determinar cuántos espacios vaciar según la dificultad
        int blanks = switch (difficulty) {
            case 1 -> 30;  // fácil
            case 2 -> 45;  // medio
            default -> 60; // difícil
        };

        Random rand = new Random();
        while (blanks > 0) {
            int i = rand.nextInt(9);
            int j = rand.nextInt(9);
            if (board[i][j] != 0) {
                board[i][j] = 0;
                blanks--;
            }
        }

        // Marcamos las celdas fijas
        for (int i = 0; i < 9; i++)
            for (int j = 0; j < 9; j++)
                fixed[i][j] = (board[i][j] != 0);
    }

    // Mostrar el tablero
    public static void printBoard() {
        System.out.println("\nVidas restantes: " + lives);
        System.out.println("  0 1 2 3 4 5 6 7 8");
        for (int i = 0; i < 9; i++) {
            System.out.print(i + " ");
            for (int j = 0; j < 9; j++) {
                if (board[i][j] == 0)
                    System.out.print(". ");
                else
                    System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
    }

    // Verificar si se puede colocar un número
    public static boolean isValid(int row, int col, int num) {
        for (int x = 0; x < 9; x++) {
            if (board[row][x] == num || board[x][col] == num)
                return false;
        }

        int startRow = row - row % 3;
        int startCol = col - col % 3;
        for (int i = startRow; i < startRow + 3; i++)
            for (int j = startCol; j < startCol + 3; j++)
                if (board[i][j] == num)
                    return false;

        return true;
    }

    // Guardar progreso en archivo
    public static void saveGame() {
        try (PrintWriter writer = new PrintWriter(new FileWriter(saveFile))) {
            writer.println(lives);
            for (int i = 0; i < 9; i++) {
                for (int j = 0; j < 9; j++) {
                    writer.print(board[i][j] + " ");
                }
                writer.println();
            }
            writer.close();
            System.out.println("Juego guardado exitosamente!");
        } catch (IOException e) {
            System.out.println("Error al guardar el juego: " + e.getMessage());
        }
    }

    // Cargar progreso desde archivo
    public static boolean loadGame() {
        try (Scanner file = new Scanner(new File(saveFile))) {
            lives = file.nextInt();
            for (int i = 0; i < 9; i++)
                for (int j = 0; j < 9; j++) {
                    board[i][j] = file.nextInt();
                    fixed[i][j] = (board[i][j] != 0);
                }
            return true;
        } catch (Exception e) {
            System.out.println("No hay partida guardada.");
            return false;
        }
    }

    // Lógica principal del juego
    public static void playGame() {
        while (true) {
            printBoard();

            if (isComplete()) {
                System.out.println("¡Felicidades! Has completado el Sudoku.");
                return;
            }

            System.out.println("\nElige una acción:");
            System.out.println("1. Ingresar número");
            System.out.println("2. Guardar y salir");
            int choice = sc.nextInt();

            if (choice == 2) {
                saveGame();
                break;
            }

            System.out.print("Fila (0-8): ");
            int row = sc.nextInt();
            System.out.print("Columna (0-8): ");
            int col = sc.nextInt();

            if (fixed[row][col]) {
                System.out.println("No puedes modificar esta celda.");
                continue;
            }

            System.out.print("Número (1-9): ");
            int num = sc.nextInt();

            if (isValid(row, col, num)) {
                board[row][col] = num;
                System.out.println("Número colocado correctamente!");
            } else {
                lives--;
                System.out.println("Número incorrecto! Te quedan " + lives + " vidas.");
                if (lives == 0) {
                    System.out.println("Has perdido el juego. Fin de la partida.");
                    break;
                }
            }
        }
    }

    // Verificar si el sudoku está completo
    public static boolean isComplete() {
        for (int i = 0; i < 9; i++)
            for (int j = 0; j < 9; j++)
                if (board[i][j] == 0)
                    return false;
        return true;
    }
}
