const SIZE = 20;

const EMPTY = ".";
const VIRUS = "V";
const BARRIER = "B";
const PLAYER = "P";
const EXIT = "E";

let board = [];
let player = { x: 0, y: 0 };
let exitPos = { x: SIZE - 1, y: SIZE - 1 };

let inventory = { barriers: 25 };
let gameOver = false;
let win = false;
let turn = 0;
let waitingBarrierDir = false;

function createBoard() {
    board = Array.from({ length: SIZE }, () =>
        Array.from({ length: SIZE }, () => EMPTY)
    );

    board[player.y][player.x] = PLAYER;
    board[exitPos.y][exitPos.x] = EXIT;
    placeVirus(12);
}

function placeVirus(count) {
    let placed = 0;
    while (placed < count) {
        let x = Math.floor(Math.random() * SIZE);
        let y = Math.floor(Math.random() * SIZE);
        if (board[y][x] === EMPTY) {
            board[y][x] = VIRUS;
            placed++;
        }
    }
}

function drawBoard() {
    console.clear();
    console.log("=== VIRUS OUTBREAK ===");
    console.log("Turno:", turn);
    console.log("Barreras:", inventory.barriers);
    console.log("Objetivo: llegar a E o contener el virus");
    console.log("");

    for (let y = 0; y < SIZE; y++) {
        let row = "";
        for (let x = 0; x < SIZE; x++) {
            row += board[y][x] + " ";
        }
        console.log(row);
    }

    console.log("");
    console.log("Mover: W A S D | B = colocar barrera | X = salir");
    if (waitingBarrierDir) {
        console.log("Direccion barrera: W A S D");
    }
}

function movePlayer(dx, dy) {
    let nx = player.x + dx;
    let ny = player.y + dy;

    if (nx < 0 || ny < 0 || nx >= SIZE || ny >= SIZE) return;
    if (board[ny][nx] === BARRIER || board[ny][nx] === VIRUS) return;

    board[player.y][player.x] = EMPTY;
    player.x = nx;
    player.y = ny;

    if (board[ny][nx] === EXIT) {
        win = true;
        gameOver = true;
        return;
    }

    board[player.y][player.x] = PLAYER;
}

function placeBarrier(dir) {
    if (inventory.barriers <= 0) return;

    let dx = 0, dy = 0;
    if (dir === "W") dy = -1;
    if (dir === "S") dy = 1;
    if (dir === "A") dx = -1;
    if (dir === "D") dx = 1;

    let x = player.x + dx;
    let y = player.y + dy;

    if (
        x >= 0 && y >= 0 &&
        x < SIZE && y < SIZE &&
        board[y][x] === EMPTY
    ) {
        board[y][x] = BARRIER;
        inventory.barriers--;
    }
}

function spreadVirus() {
    let newVirus = [];

    for (let y = 0; y < SIZE; y++) {
        for (let x = 0; x < SIZE; x++) {
            if (board[y][x] === VIRUS) {
                [[1,0],[-1,0],[0,1],[0,-1]].forEach(([dx,dy]) => {
                    let nx = x + dx;
                    let ny = y + dy;
                    if (
                        nx >= 0 && ny >= 0 &&
                        nx < SIZE && ny < SIZE &&
                        board[ny][nx] === EMPTY
                    ) {
                        newVirus.push([nx, ny]);
                    }
                });
            }
        }
    }

    newVirus.forEach(([x,y]) => board[y][x] = VIRUS);

    if (board[player.y][player.x] === VIRUS) {
        gameOver = true;
        win = false;
    }
}

function checkLose() {
    let free = false;
    for (let y = 0; y < SIZE; y++) {
        for (let x = 0; x < SIZE; x++) {
            if (board[y][x] === EMPTY) free = true;
        }
    }
    if (!free) {
        gameOver = true;
        win = false;
    }
}

function gameTurn(input) {
    input = input.trim().toUpperCase();

    if (waitingBarrierDir) {
        placeBarrier(input);
        waitingBarrierDir = false;
    } else {
        if (input === "W") movePlayer(0, -1);
        if (input === "S") movePlayer(0, 1);
        if (input === "A") movePlayer(-1, 0);
        if (input === "D") movePlayer(1, 0);
        if (input === "B") waitingBarrierDir = true;
        if (input === "X") process.exit();
    }

    spreadVirus();
    checkLose();
    turn++;

    if (gameOver) {
        drawBoard();
        console.log(win ? "GANASTE 🎉" : "PERDISTE ☠️");
        process.exit();
    }

    drawBoard();
}

process.stdin.setEncoding("utf8");
process.stdin.on("data", gameTurn);

createBoard();
drawBoard();
