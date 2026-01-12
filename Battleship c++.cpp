#include <iostream>
#include <vector>
#include <string>

using namespace std;

const int SIZE = 10;

// Tipos de casillas
const char WATER = '~';
const char SHIP  = 'B';
const char HIT   = 'X';
const char MISS  = 'O';

// Barcos (nombre, tamaño)
vector<pair<string, int>> ships = {
    {"Portaaviones", 5},
    {"Acorazado",    4},
    {"Crucero",      3},
    {"Submarino",    3},
    {"Destructor",   2}
};

void initBoard(vector<vector<char>>& board) {
    board.assign(SIZE, vector<char>(SIZE, WATER));
}

// Mostrar tablero completo (solo para dueño del tablero)
void showBoard(const vector<vector<char>>& board) {
    cout << "  ";
    for (int i = 0; i < SIZE; i++) cout << i << " ";
    cout << "\n";

    for (int i = 0; i < SIZE; i++) {
        cout << i << " ";
        for (int j = 0; j < SIZE; j++)
            cout << board[i][j] << " ";
        cout << "\n";
    }
}

// Mostrar tablero para el enemigo (oculta barcos)
void showFogBoard(const vector<vector<char>>& board) {
    cout << "  ";
    for (int i = 0; i < SIZE; i++) cout << i << " ";
    cout << "\n";

    for (int i = 0; i < SIZE; i++) {
        cout << i << " ";
        for (int j = 0; j < SIZE; j++) {
            if (board[i][j] == SHIP)
                cout << WATER << " ";  // Ocultar barcos
            else
                cout << board[i][j] << " ";
        }
        cout << "\n";
    }
}

// Verifica que un barco pueda colocarse
bool canPlace(const vector<vector<char>>& board, int r, int c, int size, char dir) {
    if (dir == 'H') {
        if (c + size > SIZE) return false;
        for (int j = 0; j < size; j++)
            if (board[r][c + j] != WATER) return false;
    }
    else {
        if (r + size > SIZE) return false;
        for (int j = 0; j < size; j++)
            if (board[r + j][c] != WATER) return false;
    }
    return true;
}

// Coloca el barco
void placeShip(vector<vector<char>>& board, int r, int c, int size, char dir) {
    if (dir == 'H') {
        for (int j = 0; j < size; j++)
            board[r][c + j] = SHIP;
    } else {
        for (int j = 0; j < size; j++)
            board[r + j][c] = SHIP;
    }
}

// Disparo
bool shoot(vector<vector<char>>& board, int r, int c) {
    if (board[r][c] == SHIP) {
        board[r][c] = HIT;
        return true;
    }
    if (board[r][c] == WATER) {
        board[r][c] = MISS;
    }
    return false;
}

// Revisar si quedan barcos
bool hasShips(const vector<vector<char>>& board) {
    for (auto& row : board)
        for (char cell : row)
            if (cell == SHIP)
                return true;
    return false;
}

int main() {
    vector<vector<char>> board1, board2;
    initBoard(board1);
    initBoard(board2);

    cout << "===== BATTLESHIP =====\n";

    // ==================== COLOCAR BARCOS =======================
    for (int player = 1; player <= 2; player++) {
        vector<vector<char>>& board = (player == 1 ? board1 : board2);

        cout << "\n=== Jugador " << player << ": Coloca tus barcos ===\n";

        for (auto& ship : ships) {
            string name = ship.first;
            int size = ship.second;

            cout << "\nColocando " << name << " (tamano " << size << ")\n";

            while (true) {
                int r, c;
                char dir;

                cout << "Fila: ";
                cin >> r;
                cout << "Columna: ";
                cin >> c;

                cout << "Direccion (H = horizontal, V = vertical): ";
                cin >> dir;
                dir = toupper(dir);

                if (r < 0 || r >= SIZE || c < 0 || c >= SIZE ||
                    (dir != 'H' && dir != 'V')) {
                    cout << "Entrada invalida, intenta de nuevo.\n";
                    continue;
                }

                if (canPlace(board, r, c, size, dir)) {
                    placeShip(board, r, c, size, dir);
                    showBoard(board);
                    break;
                } else {
                    cout << "No se puede colocar ahi. Intenta de nuevo.\n";
                }
            }
        }

        cout << "\nListo jugador " << player << "! Presiona ENTER para continuar...";
        cin.ignore();
        cin.get();
        system("clear"); // Limpia pantalla en OnlineGDB (Linux)
    }

    // ==================== JUEGO ======================
    int turn = 1;

    while (true) {
        vector<vector<char>>& enemyBoard = (turn == 1 ? board2 : board1);
        vector<vector<char>>& myBoard    = (turn == 1 ? board1 : board2);

        cout << "\n===== TURNO DEL JUGADOR " << turn << " =====\n";

        cout << "\nTu tablero:\n";
        showBoard(myBoard);

        cout << "\nTablero enemigo:\n";
        showFogBoard(enemyBoard);

        int r, c;
        cout << "\nIngresa fila del disparo: ";
        cin >> r;
        cout << "Ingresa columna del disparo: ";
        cin >> c;

        if (r < 0 || r >= SIZE || c < 0 || c >= SIZE) {
            cout << "Coordenadas invalidas, pierdes el turno.\n";
        } else {
            bool hit = shoot(enemyBoard, r, c);
            cout << (hit ? "¡Impacto!" : "Agua...") << "\n";
        }

        if (!hasShips(enemyBoard)) {
            cout << "\n\n===== ¡EL JUGADOR " << turn << " HA GANADO! =====\n";
            break;
        }

        cout << "\nPresiona ENTER para cambiar de jugador...";
        cin.ignore();
        cin.get();
        system("clear");

        turn = (turn == 1 ? 2 : 1);
    }

    return 0;
}
