import java.util.*;
import java.io.*;

class Main {
    private static final int SIZE = 9;
    private static final int SUBGRID = 3;
    private static int[][] board = new int[SIZE][SIZE];
    private static boolean[][] fixed = new boolean[SIZE][SIZE];
    private static int lives = 3;

    // Variables para cronómetro
    private static long startTime = 0;
    private static long elapsedTime = 0;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Random rand = new Random();

        System.out.println("=== SUDOKU ===");
        System.out.println("1. Nuevo juego");
        System.out.println("2. Cargar progreso");
        System.out.print("Selecciona opcion: ");
        int opcion = sc.nextInt();

        if (opcion == 2 && new File("sudoku_save.txt").exists()) {
            cargarProgreso();
        } else {
            System.out.println("\nSelecciona dificultad:");
            System.out.println("1. Muy facil");
            System.out.println("2. Facil");
            System.out.println("3. Media");
            System.out.println("4. Dificil");
            System.out.println("5. Muy dificil");
            System.out.print("Opcion: ");
            int dificultad = sc.nextInt();

            int minPistas = 0, maxPistas = 0;
            switch (dificultad) {
                case 1: minPistas = 36; maxPistas = 49; break;
                case 2: minPistas = 32; maxPistas = 35; break;
                case 3: minPistas = 28; maxPistas = 31; break;
                case 4: minPistas = 24; maxPistas = 27; break;
                case 5: minPistas = 17; maxPistas = 23; break;
                default: minPistas = 28; maxPistas = 31; break;
            }

            generateFullBoard();
            removeCells(rand.nextInt(maxPistas - minPistas + 1) + minPistas);
            System.out.println("\nTablero generado!\n");
        }

        startTime = System.currentTimeMillis(); // ⏱️ Comienza a contar tiempo
        playGame(sc);
        sc.close();
    }

    // ---------- GENERADOR DE TABLERO ----------
    private static boolean generateFullBoard() {
        return fillBoard(0, 0);
    }

    private static boolean fillBoard(int row, int col) {
        if (row == SIZE) return true;
        int nextRow = (col == SIZE - 1) ? row + 1 : row;
        int nextCol = (col + 1) % SIZE;

        List<Integer> nums = new ArrayList<>();
        for (int i = 1; i <= SIZE; i++) nums.add(i);
        Collections.shuffle(nums);

        for (int num : nums) {
            if (isValidPlacement(row, col, num)) {
                board[row][col] = num;
                if (fillBoard(nextRow, nextCol)) return true;
                board[row][col] = 0;
            }
        }
        return false;
    }

    private static void removeCells(int clues) {
        Random rand = new Random();
        int cellsToRemove = SIZE * SIZE - clues;

        // Inicialmente marcar todo como fijo; luego liberamos los removidos.
        for (int i = 0; i < SIZE; i++) {
            Arrays.fill(fixed[i], true);
        }

        while (cellsToRemove > 0) {
            int row = rand.nextInt(SIZE);
            int col = rand.nextInt(SIZE);
            if (board[row][col] != 0) {
                board[row][col] = 0;
                fixed[row][col] = false;
                cellsToRemove--;
            }
        }
    }

    private static boolean isValidPlacement(int row, int col, int num) {
        for (int i = 0; i < SIZE; i++) {
            if (board[row][i] == num || board[i][col] == num) return false;
        }
        int startRow = row - row % SUBGRID;
        int startCol = col - col % SUBGRID;
        for (int i = 0; i < SUBGRID; i++) {
            for (int j = 0; j < SUBGRID; j++) {
                if (board[startRow + i][startCol + j] == num) return false;
            }
        }
        return true;
    }

    // ---------- JUEGO ----------
    private static void playGame(Scanner sc) {
        while (true) {
            printBoard();
            showElapsedTime(); // mostrar tiempo actual

            if (isSolved()) {
                elapsedTime += System.currentTimeMillis() - startTime;
                System.out.println("\n¡Felicidades! Has completado el Sudoku!");
                showFinalTime();
                new File("sudoku_save.txt").delete(); // eliminar guardado
                break;
            }
            if (lives <= 0) {
                elapsedTime += System.currentTimeMillis() - startTime;
                System.out.println("\nPerdiste todas tus vidas. Fin del juego.");
                showFinalTime();
                new File("sudoku_save.txt").delete(); // eliminar guardado
                break;
            }

            System.out.println("\nOpciones:");
            System.out.println("1. Ingresar numero");
            System.out.println("2. Guardar progreso");
            System.out.println("3. Salir sin guardar");
            System.out.print("Opcion: ");
            int opcion = safeNextInt(sc);

            if (opcion == 2) {
                elapsedTime += System.currentTimeMillis() - startTime;
                guardarProgreso();
                System.out.println("Progreso guardado correctamente.");
                startTime = System.currentTimeMillis();
                continue;
            } else if (opcion == 3) {
                System.out.println("Saliendo sin guardar...");
                break;
            }

            System.out.print("Fila (1-9): ");
            int row = safeNextInt(sc) - 1;
            System.out.print("Columna (1-9): ");
            int col = safeNextInt(sc) - 1;

            if (row < 0 || row >= SIZE || col < 0 || col >= SIZE) {
                System.out.println("Posicion invalida.");
                continue;
            }

            if (fixed[row][col]) {
                System.out.println("Esa celda no se puede modificar.");
                continue;
            }

            System.out.print("Numero (1-9): ");
            int num = safeNextInt(sc);

            if (num < 1 || num > 9) {
                System.out.println("Numero invalido.");
                continue;
            }

            if (isValidPlacementWithCurrentBoard(row, col, num)) {
                board[row][col] = num;
                System.out.println("Numero colocado correctamente!");
            } else {
                System.out.println("Numero incorrecto. Pierdes una vida.");
                lives--;
                System.out.println("Vidas restantes: " + lives);
            }
        }
    }

    // valida teniendo en cuenta la posicion vacia (no comprueba board[row][col])
    private static boolean isValidPlacementWithCurrentBoard(int row, int col, int num) {
        // comprobar fila y columna (ignorando la celda actual que es 0)
        for (int i = 0; i < SIZE; i++) {
            if (board[row][i] == num) return false;
            if (board[i][col] == num) return false;
        }
        int startRow = row - row % SUBGRID;
        int startCol = col - col % SUBGRID;
        for (int i = 0; i < SUBGRID; i++)
            for (int j = 0; j < SUBGRID; j++)
                if (board[startRow + i][startCol + j] == num)
                    return false;
        return true;
    }

    private static void printBoard() {
        System.out.println("\nVidas restantes: " + lives);
        System.out.println("-------------------------");
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (j % 3 == 0) System.out.print("| ");
                System.out.print((board[i][j] == 0 ? "." : board[i][j]) + " ");
            }
            System.out.println("|");
            if ((i + 1) % 3 == 0) System.out.println("-------------------------");
        }
    }

    private static boolean isSolved() {
        for (int i = 0; i < SIZE; i++)
            for (int j = 0; j < SIZE; j++)
                if (board[i][j] == 0)
                    return false;
        return true;
    }

    // ---------- TIEMPO ----------
    private static void showElapsedTime() {
        long currentElapsed = elapsedTime + (System.currentTimeMillis() - startTime);
        long seconds = currentElapsed / 1000;
        long minutes = seconds / 60;
        seconds %= 60;
        System.out.printf("⏱ Tiempo: %02d:%02d\n", minutes, seconds);
    }

    private static void showFinalTime() {
        long seconds = elapsedTime / 1000;
        long minutes = seconds / 60;
        seconds %= 60;
        System.out.printf("⏱ Tiempo total: %02d:%02d\n", minutes, seconds);
    }

    // ---------- GUARDAR Y CARGAR ----------
    private static void guardarProgreso() {
        try (PrintWriter pw = new PrintWriter(new FileWriter("sudoku_save.txt"))) {
            pw.println(lives);
            pw.println(elapsedTime); // guardar tiempo acumulado en ms
            for (int i = 0; i < SIZE; i++) {
                for (int j = 0; j < SIZE; j++) {
                    pw.print(board[i][j] + " ");
                }
                pw.println();
            }
            for (int i = 0; i < SIZE; i++) {
                for (int j = 0; j < SIZE; j++) {
                    pw.print((fixed[i][j] ? 1 : 0) + " ");
                }
                pw.println();
            }
        } catch (IOException e) {
            System.out.println("Error al guardar el progreso: " + e.getMessage());
        }
    }

    private static void cargarProgreso() {
        try (Scanner file = new Scanner(new File("sudoku_save.txt"))) {
            lives = file.nextInt();
            elapsedTime = file.nextLong();
            for (int i = 0; i < SIZE; i++) {
                for (int j = 0; j < SIZE; j++) {
                    board[i][j] = file.nextInt();
                }
            }
            for (int i = 0; i < SIZE; i++) {
                for (int j = 0; j < SIZE; j++) {
                    fixed[i][j] = (file.nextInt() == 1);
                }
            }
            System.out.println("Progreso cargado correctamente.");
        } catch (IOException e) {
            System.out.println("No se pudo cargar el progreso: " + e.getMessage());
        }
    }

    // Lee int de forma segura (evita excepciones si el usuario mete otra cosa)
    private static int safeNextInt(Scanner sc) {
        while (!sc.hasNextInt()) {
            sc.next(); // descartar token inválido
            System.out.print("Entrada invalida. Intenta de nuevo: ");
        }
        return sc.nextInt();
    }
}
