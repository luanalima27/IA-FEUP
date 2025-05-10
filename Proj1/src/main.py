import pygame
import time
from board import *
from pieces import *
from handlers import *
from menu import *
import algorithm as alg
from logger import GameLogger


# Initialize Pygame
pygame.init()

def game_loop():
    start_game = main_menu()
    
    # Quit game
    if not start_game:
        pygame.quit()
        quit()

    # Determine game mode and bot configs
    if start_game[0] == "human_vs_computer":
        bot_configs = [start_game[1]]
    elif start_game[0] == "computer_vs_computer":
        bot_configs = [start_game[1], start_game[2]]
    else:
        bot_configs = []

    game_mode = start_game[0]
    logger = GameLogger(game_mode, bot_configs, get_size())
    
    running = True
    turn = 0
    winner = None
    setup_game()
    graph = create_graph()
    reset_handlers(graph)
    stack.__init__()
    human_start_time = None

    while running:
        screen.fill(BG_COLOR)
        draw_graph()
        stack.draw_stack_and_pieces(screen, turn)
        
        # Show current turn
        font = pygame.font.Font(None, 36)
        turn_text = f"Player {turn + 1}'s Turn"
        turn_surface = font.render(turn_text, True, (0, 0, 0))
        screen.blit(turn_surface, (WIDTH // 2 - turn_surface.get_width() // 2, 20))
        
        
        # Human Player
        if game_mode == "human_vs_human" or (game_mode == "human_vs_computer" and turn == 0):
            if human_start_time is None:
                human_start_time = time.time()
            if winner is None:
                hint_message = "Press 'M' for a hint using Minimax or 'C' for a hint using Monte Carlo"
                hint_font = pygame.font.Font(None, 28)
                hint_surface = hint_font.render(hint_message, True, (0, 0, 0))
                screen.blit(hint_surface, (WIDTH // 2 - hint_surface.get_width() // 2, HEIGHT - 50))

                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    current_state = alg.GameState(graph, stack.pieces, stack)
                    depth = 3
                    hint_move = alg.best_move(current_state, turn, depth)
                    if hint_move[0] == "placement":
                        hint_cell = next(c for c in graph if c.id == hint_move[1].id)
                        hint_cell.hint = True
                    elif hint_move[0] == "move":
                        origin_cell = next(c for c in graph if c.id == hint_move[1].id)
                        destination_cell = next(c for c in graph if c.id == hint_move[2].id)
                        origin_cell.hint = True
                        destination_cell.hint = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    current_state = alg.GameState(graph, stack.pieces, stack)
                    iterations = 50
                    hint_move = alg.best_move_mcts(current_state, turn, iterations) 
                    if hint_move[0] == "placement":
                        hint_cell = next(c for c in graph if c.id == hint_move[1].id)
                        hint_cell.hint = True
                    elif hint_move[0] == "move":
                        origin_cell = next(c for c in graph if c.id == hint_move[1].id)
                        destination_cell = next(c for c in graph if c.id == hint_move[2].id)
                        origin_cell.hint = True
                        destination_cell.hint = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clear_hints()
                    x, y = pygame.mouse.get_pos()
                    result = handle_click(x, y, turn)
                    
                    if isinstance(result, tuple):
                        new_turn, move_cell, move_type, from_id = result
                        move_time = time.time() - human_start_time
                        logger.log_move(move_time, turn, move_type, move_cell.id, from_id)
                        turn = new_turn
                        human_start_time = None
                        
                        if turn >= 2:
                            winner = turn - 2
                            logger.set_winner(winner)
                            logger.save_to_file()
                            choice = show_final_state(winner, move_cell, turn, stack)
                            if choice == "restart":
                                return True
                            running = False
                            break
                    else:
                        turn = result

        # AI logic
        else:
            algorithm_name, difficulty = bot_configs[turn if game_mode == "computer_vs_computer" else 0]
            pygame.display.flip()

            current_state = alg.GameState(graph, stack.pieces, stack)
            
            if algorithm_name == "MonteCarlo":
                iterations_map = {"Easy": 25, "Medium": 50, "Hard": 100}
                difficulty_str = "Easy Medium Hard".split()[difficulty - 1]
                iterations = iterations_map[difficulty_str]
                start_time = time.time()
                move = alg.best_move_mcts(current_state, turn, iterations)
                move_time = time.time() - start_time

            else:
                depth_map = {"Easy": 1, "Medium": 2, "Hard": 3}
                difficulty_str = "Easy Medium Hard".split()[difficulty - 1]
                depth = depth_map[difficulty_str]
                start_time = time.time()
                move = alg.best_move(current_state, turn, depth)
                move_time = time.time() - start_time

            if move[0] == "placement":
                selected_cell = next(c for c in graph if c.id == move[1].id)
                stack.place_piece(selected_cell, turn)
                move_cell = selected_cell
                logger.log_move(move_time, turn, "placement", selected_cell.id)
                
            elif move[0] == "move":
                origin = next(c for c in graph if c.id == move[1].id)
                destination = next(c for c in graph if c.id == move[2].id)
                if origin.piece:
                    origin.piece.move_to(destination)
                    check_flip(destination)
                    move_cell = destination
                    logger.log_move(move_time, turn, "move", destination.id, origin.id)

                if check_conditions(move_cell):
                    winner = turn
                    logger.set_winner(winner)
                    logger.save_to_file()
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    choice = show_final_state(winner, move_cell, turn, stack)
                    if choice == "restart":
                        return True
                    running = False
                    break

            pygame.time.wait(1000)
            turn = 1 - turn

        if turn >= 2:
            winner = turn - 1
            break

        pygame.display.flip()

    return False


# End screen after game over
while True:
    if not game_loop():
        break

pygame.quit()