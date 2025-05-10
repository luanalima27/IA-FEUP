import copy
import random
import math
from board import graph, SIZE, NEUTRAL, WHITE, BLUE, DIRECTIONS
from pieces import stack, Piece
from handlers import check_flip


# ------------------ GAME STATE CLASS ------------------
class GameState:
    def __init__(self, cells, pieces, stack):
        self.cells = cells          # List of cells on the board
        self.pieces = pieces        # All placed pieces
        self.stack = stack          # Piece stock for each player
        self.last_action = {        # Information about the last move
            "player": None,
            "type": None,
            "cell_id": None
        }

    def clone(self):
        return copy.deepcopy(self)


# ------------------ LIST POSSIBLE MOVES ------------------
def list_possible_moves(state: GameState, player: int, is_first_move=None):
    if is_first_move is None:
        is_first_move = not any(p.player == player and p.cell is not None for p in state.pieces)

    moves = []

    # Placement moves: if there are pieces left in the stack
    if state.stack.stack[player] > 0:
        for cell in state.cells:
            if cell.piece is None:
                # Do not allow placement on corner cells on the first move
                if is_first_move and cell.id in [0, SIZE - 1, SIZE * SIZE - SIZE, SIZE * SIZE - 1]:
                    continue
                moves.append(("placement", cell))

    # Movement moves: for each piece of the player on the board
    for piece in state.pieces:
        if piece.player == player and piece.cell is not None:
            destinations = get_valid_moves(piece)
            for dest in destinations:
                moves.append(("move", piece.cell, dest))

    return moves


# ------------------ GET VALID MOVES ------------------
def get_valid_moves(piece: Piece):
    moves = []
    for direction in DIRECTIONS:
        moves.extend(validate_direction(piece.cell, piece, False, direction))
    return moves

def validate_direction(current_cell, piece: Piece, color_switched, direction):
    moves = []
    next_cell = current_cell.neighbors.get(direction)
    
    # Stop if there is no neighbor or it is occupied
    if next_cell is None or next_cell.piece is not None:
        return moves

    # Determine if the next cell is of the "correct" color based on the player's color
    correct_color = (piece.player == 0 and next_cell.type == BLUE) or (piece.player == 1 and next_cell.type == WHITE)

    if current_cell.type == next_cell.type:
        moves.append(next_cell)
        if correct_color:
            moves.extend(validate_direction(next_cell, piece, color_switched, direction))
    elif not color_switched:
        moves.append(next_cell)
        if correct_color:
            moves.extend(validate_direction(next_cell, piece, True, direction))

    return moves


# ------------------ APPLY MOVE ------------------
def apply_move(state: GameState, move, player: int):
    new_state = state.clone()

    if move[0] == "placement":
        cell = move[1]
        target_cell = next(c for c in new_state.cells if c.id == cell.id)
        if new_state.stack.stack[player] > 0 and target_cell.piece is None:
            new_state.stack.stack[player] -= 1
            piece = Piece(player)
            piece.insert_piece(target_cell)
            new_state.pieces.append(piece)
            new_state.last_action = {"player": player, "type": "placement", "cell_id": target_cell.id}

    elif move[0] == "move":
        origin, destination = move[1], move[2]
        new_origin = next(c for c in new_state.cells if c.id == origin.id)
        new_dest = next(c for c in new_state.cells if c.id == destination.id)
        piece = new_origin.piece
        if piece:
            piece.move_to(new_dest)
            check_flip(new_dest)
            new_state.last_action = {"player": player, "type": "move", "cell_id": new_dest.id}

    return new_state


# ------------------ HEURISTIC EVALUATION ------------------
def count_in_line(cell, player, dir1, dir2):
    count = 1
    next_cell = cell.neighbors.get(dir1)
    while next_cell and next_cell.piece and next_cell.piece.player == player:
        count += 1
        next_cell = next_cell.neighbors.get(dir1)
    next_cell = cell.neighbors.get(dir2)
    while next_cell and next_cell.piece and next_cell.piece.player == player:
        count += 1
        next_cell = next_cell.neighbors.get(dir2)
    return count


def evaluate_state(state: GameState, player: int):
    score = 0
    values = {1: 1, 2: 10, 3: 100, 4: 1000, 5: -10000}

    for cell in state.cells:
        if cell.piece:
            p = cell.piece.player
            max_line = max(
                count_in_line(cell, p, "UP", "DOWN"),
                count_in_line(cell, p, "UP_RIGHT", "DOWN_LEFT"),
                count_in_line(cell, p, "UP_LEFT", "DOWN_RIGHT")
            )
            if p == player:
                score += values.get(max_line, 0)
            else:
                score -= values.get(max_line, 0)

    player_pieces = sum(1 for p in state.pieces if p.player == player)
    opponent_pieces = sum(1 for p in state.pieces if p.player != player)
    score += (player_pieces - opponent_pieces)

    action = state.last_action
    if action["player"] == player:
        score += 0.5 if action["type"] == "move" else -0.2
    else:
        score -= 0.5 if action["type"] == "move" else -0.2

    return score


# ------------------ CHECK IF GAME OVER ------------------
def is_terminal_state(state: GameState, player: int):
    action = state.last_action
    if action["player"] is None:
        return False, evaluate_state(state, player)

    last_cell = next((c for c in state.cells if c.id == action["cell_id"]), None)
    if not last_cell or not last_cell.piece:
        return False, evaluate_state(state, player)

    player_turn = action["player"]
    longest = max(
        count_in_line(last_cell, player_turn, "UP", "DOWN"),
        count_in_line(last_cell, player_turn, "UP_RIGHT", "DOWN_LEFT"),
        count_in_line(last_cell, player_turn, "UP_LEFT", "DOWN_RIGHT")
    )

    if longest >= 5:
        return True, -100000 if player_turn == player else 100000
    if longest == 4 and action["type"] == "move":
        return True, 100000 if player_turn == player else -100000

    return False, evaluate_state(state, player)


# ------------------ MINIMAX WITH ALPHA-BETA PRUNING ------------------
def minimax(state: GameState, depth: int, alpha: float, beta: float, maximizing: bool, player: int):
    terminal, score = is_terminal_state(state, player)
    if depth == 0 or terminal:
        return score

    if maximizing:
        max_eval = -float('inf')
        for move in list_possible_moves(state, player):
            new_state = apply_move(state, move, player)
            eval = minimax(new_state, depth - 1, alpha, beta, False, player)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        opponent = 1 - player
        for move in list_possible_moves(state, opponent):
            new_state = apply_move(state, move, opponent)
            eval = minimax(new_state, depth - 1, alpha, beta, True, player)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# ------------------ FIND BEST MOVE USING MINIMAX ------------------
def best_move(state: GameState, player: int, depth: int):
    first_turn = not any(p.player == player and p.cell is not None for p in state.pieces)
    winning = []

    # Check for immediate winning moves
    for move in list_possible_moves(state, player, first_turn):
        new_state = apply_move(state, move, player)
        is_term, score = is_terminal_state(new_state, player)
        if is_term and score > 0:
            winning.append(move)
    if winning:
        return random.choice(winning)

    best_value = -float('inf')
    best_moves = []

    for move in list_possible_moves(state, player, first_turn):
        new_state = apply_move(state, move, player)
        value = minimax(new_state, depth - 1, -float('inf'), float('inf'), False, player)
        if value > best_value:
            best_value = value
            best_moves = [move]
        elif value == best_value:
            best_moves.append(move)

    return random.choice(best_moves) if best_moves else None


# ------------------ MCTS NODE CLASS ------------------
class MCTSNode:
    def __init__(self, state, parent, move, player_just_moved, next_player):
        self.state = state              # Game state at this node
        self.parent = parent            # Parent node
        self.move = move                # Move that led to this node (None for root)
        self.player_just_moved = player_just_moved  # Player who made the move
        self.next_player = next_player  # Player whose turn is next
        self.wins = 0                 # Number of wins (from the perspective of the root player)
        self.visits = 0               # Number of visits to this node
        self.untried_moves = list_possible_moves(state, next_player) # List of moves not yet explored from this state for next_player
        self.children = []            # List of child nodes

    # Select child with highest UCT value
    def uct_select_child(self, exploration=math.sqrt(2)):
        return max(
            self.children,
            key=lambda child: child.wins / child.visits + exploration * math.sqrt(math.log(self.visits) / child.visits)
        )

    # Expand node by trying one of the untried moves
    def add_child(self, move, state):
        child = MCTSNode(state, parent=self, move=move, player_just_moved=self.next_player, next_player=1 - self.next_player)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    # Update node's statistics with simulation result
    def update(self, simulation_winner):
        self.visits += 1
        if self.player_just_moved is not None and self.player_just_moved == simulation_winner:
            self.wins += 1


# ------------------ ENHANCED ROLLOUT (SIMULATION) FUNCTION ------------------
def rollout(state, current_turn, root_player, max_rollout_steps=100, epsilon=0.3):
    state_sim = copy.deepcopy(state)
    turn = current_turn
    for _ in range(max_rollout_steps):
        moves = list_possible_moves(state_sim, turn)
        if not moves:
            break

        # Check for immediate win moves for the current player
        immediate_win_moves = []
        for move in moves:
            next_state = apply_move(state_sim, move, turn)
            is_term, score = is_terminal_state(next_state, root_player)
            # If current player's move leads to immediate win for root or prevents opponent win
            if is_term and ((turn == root_player and score > 0) or (turn != root_player and score < 0)):
                immediate_win_moves.append(move)
        if immediate_win_moves:
            chosen_move = random.choice(immediate_win_moves)
        else:
            # Epsilon-greedy: with probability epsilon choose random, else choose best move by evaluation
            if random.random() < epsilon:
                chosen_move = random.choice(moves)
            else:
                best_eval = -float('inf')
                best_moves = []
                for move in moves:
                    next_state = apply_move(state_sim, move, turn)
                    eval_score = evaluate_state(next_state, root_player)
                    if eval_score > best_eval:
                        best_eval = eval_score
                        best_moves = [move]
                    elif eval_score == best_eval:
                        best_moves.append(move)
                chosen_move = random.choice(best_moves) if best_moves else random.choice(moves)
        
        state_sim = apply_move(state_sim, chosen_move, turn)
        turn = 1 - turn
        terminal, _ = is_terminal_state(state_sim, root_player)
        if terminal:
            break

    final_score = evaluate_state(state_sim, root_player)
    return root_player if final_score > 0 else 1 - root_player


# ------------------ FIND BEST MOVE USING MCTS ------------------
def best_move_mcts(state: GameState, player: int, iterations: int):
    # Check for any immediate winning move
    possible_moves = list_possible_moves(state, player)
    immediate_wins = []
    for move in possible_moves:
        new_state = apply_move(state, move, player)
        is_term, score = is_terminal_state(new_state, player)
        if is_term and score > 0:
            immediate_wins.append(move)
    if immediate_wins:
        return random.choice(immediate_wins)

    # Create the root node for MCTS
    root = MCTSNode(state, parent=None, move=None, player_just_moved=None, next_player=player)

    for _ in range(iterations):
        node = root
        state_sim = copy.deepcopy(state)
        current_turn = player

        # 1. Selection: traverse the tree using UCT until a node with untried moves is found
        while node.untried_moves == [] and node.children:
            node = node.uct_select_child()
            state_sim = apply_move(state_sim, node.move, current_turn)
            current_turn = 1 - current_turn

        # 2. Expansion: expand one untried move
        if node.untried_moves:
            move = random.choice(node.untried_moves)
            state_sim = apply_move(state_sim, move, current_turn)
            node = node.add_child(move, state_sim)
            current_turn = 1 - current_turn

        # 3. Simulation (Rollout) using the enhanced policy
        simulation_winner = rollout(state_sim, current_turn, player)

        # 4. Backpropagation: update nodes along the path
        while node is not None:
            node.update(simulation_winner)
            node = node.parent

    # Choose the child with the highest visit count
    best_child = max(root.children, key=lambda child: child.visits)
    return best_child.move