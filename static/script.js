let currentPlayer = null;
let sessionId = null;
let gameOver = false;
let qrCodeVisible = false;
let homeQrCodeVisible = false;

function updateBoard(board) {
    const table = document.getElementById('board');
    table.innerHTML = '';

    // Create column headers for clicking
    const headerRow = document.createElement('tr');
    for (let col = 0; col < board[0].length; col++) {
        const th = document.createElement('th');
        th.textContent = col;
        th.addEventListener('click', () => makeMove(col));
        headerRow.appendChild(th);
    }
    table.appendChild(headerRow);

    // Create the board cells
    for (let row of board) {
        const tr = document.createElement('tr');
        for (let cell of row) {
            const td = document.createElement('td');
            if (cell === " ") {
                td.className = 'empty';
            } else if (cell === "X") {
                td.className = 'playerX';
                td.textContent = 'X';
            } else if (cell === "O") {
                td.className = 'playerO';
                td.textContent = 'O';
            }
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }
}

async function fetchBoard() {
    if (gameOver) return;
    const response = await fetch(`/board/${sessionId}`);
    const board = await response.json();
    updateBoard(board);
    checkWin();
}

async function checkWin() {
    const response = await fetch(`/check_win/${sessionId}`);
    const result = await response.json();
    const messageDiv = document.getElementById('message');
    if (result.winner) {
        messageDiv.textContent = `Player ${result.winner} wins!`;
        document.getElementById('currentTurn').style.display = 'none';
        document.getElementById('resetBtn').style.display = 'block';
        gameOver = true;
    } else {
        messageDiv.textContent = '';
    }
}

async function makeMove(column) {
    if (gameOver) return;
    const response = await fetch(`/move/${sessionId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ column, player: currentPlayer })
    });

    if (response.ok) {
        fetchBoard();
    } else {
        const error = await response.json();
        alert(error.detail);
    }
}

async function createSession() {
    const response = await fetch('/create_session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})  // Sending an empty JSON object
    });
    const result = await response.json();
    sessionId = result.session_id;
    currentPlayer = result.player;
    document.getElementById('currentTurn').textContent = `Player ${currentPlayer}'s turn`;
    document.getElementById('currentTurn').style.display = 'block';
    document.getElementById('showQRCodeBtn').textContent = 'Show Session QR Code';
    document.getElementById('showQRCodeBtn').style.display = 'inline';
    document.getElementById('resetBtn').style.display = 'none';
    document.getElementById('sessionIdInput').value = sessionId;
    document.getElementById('joinSessionDiv').style.display = 'none'; // Hide join session form
    gameOver = false;
    window.history.pushState({}, '', `/${sessionId}`);
    fetchBoard();
}

async function joinSession() {
    const inputSessionId = document.getElementById('sessionIdInput').value;
    if (!inputSessionId) {
        alert('Please enter a session ID.');
        return;
    }
    joinExistingSession(inputSessionId);
}

async function joinExistingSession(sessionIdToJoin) {
    try {
        const response = await fetch(`/join_session/${sessionIdToJoin}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})  // Sending an empty JSON object if no additional data is needed
        });
        if (!response.ok) {
            throw new Error(`Session ${sessionIdToJoin} not found`);
        }
        const result = await response.json();
        sessionId = result.session_id;
        currentPlayer = result.player;
        document.getElementById('currentTurn').textContent = `Player ${currentPlayer}'s turn`;
        document.getElementById('currentTurn').style.display = 'block';
        document.getElementById('showQRCodeBtn').textContent = 'Show Session QR Code';
        document.getElementById('showQRCodeBtn').style.display = 'inline';
        document.getElementById('resetBtn').style.display = 'none';
        document.getElementById('joinSessionDiv').style.display = 'none'; // Hide join session form
        gameOver = false;
        window.history.pushState({}, '', `/${sessionId}`);
        fetchBoard();
    } catch (error) {
        alert(error.message);
    }
}

function toggleQRCode() {
    const qrCodeContainer = document.getElementById('qrCodeContainer');
    if (qrCodeVisible) {
        qrCodeContainer.style.display = 'none';
        qrCodeContainer.innerHTML = '';
        document.getElementById('showQRCodeBtn').textContent = 'Show Session QR Code';
    } else {
        new QRCode(qrCodeContainer, {
            text: window.location.href,
            width: 128,
            height: 128
        });
        qrCodeContainer.style.display = 'flex';
        document.getElementById('showQRCodeBtn').textContent = 'Hide Session QR Code';
    }
    qrCodeVisible = !qrCodeVisible;
}

function toggleHomeQRCode() {
    const qrCodeContainer = document.getElementById('qrCodeContainer');
    if (homeQrCodeVisible) {
        qrCodeContainer.style.display = 'none';
        qrCodeContainer.innerHTML = '';
        document.getElementById('showHomeQRCodeBtn').textContent = 'Show Home QR Code';
    } else {
        new QRCode(qrCodeContainer, {
            text: window.location.origin,
            width: 128,
            height: 128
        });
        qrCodeContainer.style.display = 'flex';
        document.getElementById('showHomeQRCodeBtn').textContent = 'Hide Home QR Code';
    }
    homeQrCodeVisible = !homeQrCodeVisible;
}

function resetGame() {
    createSession();
}

// Check if there's a session ID in the URL and join that session automatically
window.onload = () => {
    const urlSessionId = window.location.pathname.substring(1);
    if (urlSessionId) {
        joinExistingSession(urlSessionId);
    }
};

setInterval(fetchBoard, 250); // Fetch board every 250 ms
