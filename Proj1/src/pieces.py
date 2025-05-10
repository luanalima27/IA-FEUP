import pygame
import math
from board import *

COLORS = [(255, 0, 0), (0, 255, 0)]

class Piece:
    def __init__(self, player):
        self.player = player
        self.cell : Cell = None  # The Cell object this piece belongs to
        self.highlighted = False # Flag to check if the piece was selected
        self.original_cell = None

    def move_to(self, new_cell):
        if new_cell.piece is not None:
            print("Invalid move! Cell is already occupied.")
            return False

        self.original_cell = self.cell
        self.cell.piece = None  # Remove from the current cell
        new_cell.piece = self  # Place in the new cell
        self.cell = new_cell  # Update the piece's position
        return True

    # Draw a piece (highlighted when selected to be moved)
    def draw(self, screen):
        if self.cell:
            x, y = self.cell.pos  # Get the cell's pixel position
            pygame.draw.circle(screen, COLORS[self.player], (x, y), HEX_RADIUS * 2 // 3)  # Draw piece
            if self.cell.hint:
                pygame.draw.circle(screen, (255, 255, 255), (x, y), HEX_RADIUS * 2 // 3, 3)
            elif self.highlighted:
                pygame.draw.circle(screen, (255, 255, 0), (x, y), HEX_RADIUS * 2 // 3, 3)  # Draw highlighted outline
            else:
                pygame.draw.circle(screen, (0, 0, 0), (x, y), HEX_RADIUS * 2 // 3, 3)  # Draw outline
            return True
        return False
                
    def insert_piece(self, cell):
        if cell.piece is None:
            cell.piece = self
            self.cell = cell
        else:
            print("Cell already occupied.")
            
    def flip(self):
        self.player = abs(self.player - 1)


# Stack class to manage available pieces per player
class Stack:
    def __init__(self):
        self.stack = [6, 6]
        self.highlighted = False
        self.pieces = []
        
    def place_piece(self, cell, player):
        if self.stack[player] <= 0:
            return
        self.stack[player] -= 1
        piece = Piece(player)
        self.pieces.append(piece)
        piece.insert_piece(cell)
                
    # Draw a stack of available pieces for a player (highlighted when selected to place)
    def draw_available(self, screen, player, turn):
        if self.stack[player] <= 0:
            return

        x = 250 + 300 * player
        y = 600
        
        pygame.draw.circle(screen, COLORS[player], (x, y), HEX_RADIUS * 2 // 3)
        if self.highlighted and player == turn:
            pygame.draw.circle(screen, (255, 255, 0), (x, y), HEX_RADIUS * 2 // 3, 3)
        else:
            pygame.draw.circle(screen, (0, 0, 0), (x, y), HEX_RADIUS * 2 // 3, 3)
        
        # Write the number of pieces left
        font = pygame.font.Font(None, 24)
        text_surface = font.render("x" + str(self.stack[player]), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x, y))
        
        screen.blit(text_surface, text_rect)
        
    def draw_stack(self, screen, turn):
        self.draw_available(screen, 0, turn)
        self.draw_available(screen, 1, turn)
        
    # only for development
    def init_pieces(self):
        piece = Piece(0)
        self.pieces.append(piece)
        piece = Piece(1)
        self.pieces.append(piece)
            
        
    # Draw all pieces and stacks
    def draw_stack_and_pieces(self, screen, turn):
        for piece in self.pieces:
            piece.draw(screen)
        self.draw_stack(screen, turn)
            
stack = Stack()