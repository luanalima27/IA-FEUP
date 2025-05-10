# Yonmoque Hex

This project was developed as part of the Artificial Intelligence (IART) course – 3rd year of the Informatics and Computing Engineering degree (L.EIC) – 2024/2025.
Topic: Two-Player Board Games with Adversarial Search Methods.

## Objective

The goal of this project is to implement the board game Yonmoque Hex with support for multiple game modes (human vs. human, human vs. computer, computer vs. computer), using adversarial search algorithms like Minimax with Alpha-Beta Pruning and Monte Carlo Tree Search.

## Game Modes

- Human vs. Human
- Human vs. Computer
- Computer vs. Computer

Each bot can be individually configured with its own algorithm and difficulty level.

## Game Rules (Summary)

- The goal is to **make a line of exactly 4 pieces** to win.
- A line of 5 or more results in a **loss**.
- Winning lines only count if completed **via movement**, not by placement.
- Players can **flip enemy pieces** by surrounding them.
- Players can move in any of 6 directions.
- Tiles of the same color of the piece count as 1 tile for movement purposes.

## Requirements

- Python 3.8+
- Required library: pygame

Install dependecies

```
pip install pygame
```

## How to run

- Ensure all `.py` files are in the same folder.
- Run the main script

```
python main.py
```

- Use the graphical menu to select the game mode and needed configurations.

## Project Structure

### ./src
- `main.py` - Main game loop and screen flow
- `menu.py` - Game mode and bot configuration menus
- `board.py` - Board creation and drawing logic
- `pieces.py` - Piece and stack logic
- `handlers.py` - Interaction handling and move logic
- `algorithm.py` - Minimax and Monte Carlo algorithms and evaluation function
- `logger.py` - Logging results with `.txt` files

### ./game_logs
If this folder doesn't exist, finish a game and it will be created automatically. Stores the results of each game in a `.txt` file. **"game_log_{timestamp}"**

## Authors

Project developed by:

- Beatriz Pereira, up202207380
- João Silva, up202108713
- Luana Lima, up202206845
