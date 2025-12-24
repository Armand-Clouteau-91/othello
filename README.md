# Projet Othello

A text-based implementation of the classic board game Othello (Reversi). This version runs entirely in the command line and serves as the logic core for future graphical versions.

## 📋 Features
- **Core Game Logic**: Full implementation of Othello rules (flanking, validity checks).
- **NumPy Grid**: Efficient 8x8 matrix representation of the board.
- **Local PvP**: Two-player turn-based gameplay in the terminal.
- **Score Tracking**: Real-time score updates after every move.

## 🛠️ Prerequisites
You will need Python installed along with the following libraries:
- `numpy` (for board management)
- `pygame` (used for game clock/timing)

```bash 
pip install numpy pygame
```

## 🚀 How to Run
Ensure board.py and game.py are in the same folder.
Run the game file:
```bash
python game.py
```

## 🎮 How to Play
1. The game starts with 2 Black and 2 White discs in the center.
2. The starting player is chosen randomly.
3. Input Coordinates: When prompted, enter the Row and Column as numbers between 1 and 8.
Example: Entering 3 for row and 4 for column places a piece at (3, 4).
4. The game will automatically flip opponent pieces.
5.The game ends when no moves are possible for either player.