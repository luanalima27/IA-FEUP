import time
import os
from datetime import datetime

class GameLogger:
    def __init__(self, game_mode, bot_configs, board_size):
        self.start_time = time.time()
        self.moves = []
        self.game_mode = game_mode
        self.bot_configs = bot_configs
        self.board_size = str(board_size)
        self.winner = None

    def log_move(self, time, player, move_type, cell_id, from_id=None):
        time = round(time, 2)

        if move_type == "placement":
            self.moves.append(f"Player {player + 1} placed at cell {cell_id}, took {time} seconds")
        elif move_type == "move":
            self.moves.append(f"Player {player + 1} moved from cell {from_id} to {cell_id}, took {time} seconds")

    def set_winner(self, winner):
        self.winner = winner

    def save_to_file(self):
        from board import SIZE, graph
        from pieces import stack

        total_time = round(time.time() - self.start_time, 2)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = "game_logs"
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, f"game_log_{timestamp}.txt")

        with open(filename, "w") as file:
            file.write(f"Game Mode: {self.game_mode}\n")
            if self.bot_configs:
                file.write(f"Bot Configs: {self.bot_configs}\n")
            file.write(f"Board Size: {self.board_size}\n")
            file.write(f"Winner: Player {self.winner + 1}\n")
            file.write(f"Total Time: {total_time} seconds\n")
            file.write("Moves:\n")
            for i, move in enumerate(self.moves):
                file.write(f"{i + 1}. {move}\n")

            # Add an empty line before board state
            file.write("\n")
            file.write(f"stack1: {stack.stack[0]}\n")
            file.write(f"stack2: {stack.stack[1]}\n")
            file.write("\n")

            # Write final board state as grid
            for row in range(SIZE):
                line = ""
                for col in range(SIZE):
                    cell = graph[row * SIZE + col]
                    if cell.piece is None:
                        line += "-"
                    else:
                        line += str(cell.piece.player + 1)
                file.write(line + "\n")
