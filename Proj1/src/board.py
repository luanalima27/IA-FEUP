import pygame
import math


# Screen settings
WIDTH, HEIGHT = 800, 800
graph = None
SIZE = 5 # SIZE of the board
HEX_RADIUS = (WIDTH - 200) // (SIZE + (SIZE - 1 // 2)) / 2
BG_COLOR = (255, 255, 255) # Background Color
NEUTRAL, WHITE, BLUE = 0, 1, 2 # Types of cells
COLORS = [(255, 165, 0), (255, 255, 255), (173, 216, 230)] # Colors of the cells
DIRECTIONS = ["UP", "UP_RIGHT", "DOWN_RIGHT", "DOWN", "DOWN_LEFT", "UP_LEFT"] # Possible directions of movement

# Screen with title
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yonmoque Hex")

# Class that represents each cell in the board
class Cell:
    def __init__(self, id):
        self.id = id
        self.type = None # Type of cell (neutral, white, blue)
        self.piece = None  # None means empty cell
        self.pos = None
        self.highlighted = False
        self.hint = False
        self.neighbors : Cell = {dir: None for dir in DIRECTIONS} # None means no neighbor

    def set_neighbor(self, direction, node):
        self.neighbors[direction] = node
        
    def has_piece(self):
        return self.piece != None
    
    def has_neighbor(self, direction):
        return self.neighbors[direction] != None


# Create a graph (list) with all the cells
def create_graph():
    global SIZE, graph

    # Create all the default cells
    cells = [Cell(i) for i in range(SIZE * SIZE)]

    # Set the neighbors for each cell
    for i in range(SIZE * SIZE):
        cell = cells[i]
        cell.type = WHITE
        
        if i % SIZE != 0:  # Not first column
            cells[i - 1]. set_neighbor("DOWN_RIGHT", cell)
            cell.set_neighbor("UP_LEFT", cells[i - 1])

        if i >= SIZE:  # Not first row
            cells[i - SIZE].set_neighbor("DOWN_LEFT", cell)
            cell.set_neighbor("UP_RIGHT", cells[i - SIZE])

        if i >= SIZE + 1 and (i % SIZE) != 0:  # Not first column and not first row
            cells[i - SIZE - 1].set_neighbor("DOWN", cell)
            cell.set_neighbor("UP", cells[i - SIZE - 1])
        
    # Set the blue cells    
    for i in range(SIZE):
        cells[i].type = BLUE
        cells[SIZE * SIZE - i - 1].type = BLUE
        cells[i * SIZE - 1].type = BLUE
        cells[i * SIZE].type = BLUE
        
    # Set the neutral cells
    cells[0].type = NEUTRAL
    cells[SIZE - 1].type = NEUTRAL
    cells[SIZE * SIZE - SIZE].type = NEUTRAL
    cells[SIZE * SIZE - 1].type = NEUTRAL
    cells[SIZE * SIZE // 2].type = NEUTRAL
    
    
    # Set the positions of the cells
    row_pos = [400, 200]
    
    for i in range(SIZE):
        col_pos = row_pos.copy()
        for d in range(SIZE):
            cells[i * SIZE + d].pos = (col_pos[0], col_pos[1])
            col_pos[0] += HEX_RADIUS * 1.5
            col_pos[1] += HEX_RADIUS * math.sqrt(3) / 2
        row_pos[0] -= HEX_RADIUS * 1.5
        row_pos[1] += HEX_RADIUS * math.sqrt(3) / 2
        
    graph = cells

    return cells
        


# Draws an hexagon
def draw_hexagon(x, y, type, HEX_RADIUS, highlighted, hint=False):
    points = []
    for i in range(6):
        angle = math.pi / 3 * i
        px = x + HEX_RADIUS * math.cos(angle)
        py = y + HEX_RADIUS * math.sin(angle)
        points.append((px, py))
    
    # Draw an hexagon with a black outline
    pygame.draw.polygon(screen, COLORS[type], points, 0)
    # If a hint is active, draw a red border; else if highlighted, draw cyan; else black
    if hint:
        pygame.draw.polygon(screen, (255, 0, 0), points, 3)
    elif highlighted:
        pygame.draw.polygon(screen, (0, 255, 255), points, 2)
    else:
        pygame.draw.polygon(screen, (0, 0, 0), points, 2)
    
    if type == NEUTRAL:
        font = pygame.font.Font(None, 24)
        text_surface = font.render("N", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x, y))

        screen.blit(text_surface, text_rect)


# Draw the board (highlighted cells last)
def draw_graph():
    
    for cell in graph:
        if cell.highlighted == False:
            x, y = cell.pos
            draw_hexagon(x, y, cell.type, HEX_RADIUS, cell.highlighted, cell.hint)
            
    for cell in graph:
        if cell.highlighted == True:
            x, y = cell.pos
            draw_hexagon(x, y, cell.type, HEX_RADIUS, cell.highlighted, cell.hint)


def clear_hints():
    for cell in graph:
        cell.hint = False


def increase_size():
    global SIZE
    if SIZE < 9:
        SIZE += 2
    
def decrease_size():
    global SIZE
    if SIZE > 5:
        SIZE -= 2
        
def get_size():
    global SIZE
    return SIZE
