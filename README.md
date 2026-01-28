# Othello V0 - Console Version

## Description
Minimal viable product with core game logic. Console-based interaction.

## Features
- Complete Othello rules
- Move validation and disc flipping
- Turn management
- Score tracking

## How to Run
--> python game.py

## How to Play
Enter row and column numbers (1-8) when prompted.

Example: 
Enter the row you want to put your piece in: 3
Enter the column you want to put your piece in: 4


# Othello V1 - Graphical Interface

## Description
Adds complete Pygame interface with visual board and controls.

## New Features
- Interactive graphical board
- Mouse click controls
- Visual move highlighting
- Score panels and timer
- Undo/Restart/Pass buttons
- End game screen

## How to Run
```bash
python interface.py
```

## Controls
- **Click**: Place disc on highlighted square
- **Undo button**: Revert last move
- **Restart button**: New game
- **Pass button**: Skip turn


# Othello V2 - Final Version with greedy AI

## Description
Final version with AI opponent and complete feature set.

## New Features
- Main menu with game mode selection
- AI opponent (greedy algorithm)
- Player vs Player mode
- Player vs Bot mode
- Smart undo (reverts 2 moves in bot games)
- Menu button to return to main screen

## How to Run
```bash
python interface.py
```
## Game Modes
1. **Player vs Player**: Two humans play locally
2. **Player vs Bot**: Play against AI (bot plays as White)

## AI Behavior
- Evaluates all valid moves
- Chooses move that maximizes immediate score
- Plays automatically with 2000ms delay


