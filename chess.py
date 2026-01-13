import pygame
import sys
import math
from typing import Optional, Tuple, List

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 750, 750
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)
SELECTED = (246, 246, 130)
CHECK = (255, 0, 0, 100)
PROMOTION_BG = (50, 50, 50, 180)

class Piece:
    def __init__(self, color: str, piece_type: str, row: int, col: int):
        self.color = color          # 'white' or 'black'
        self.piece_type = piece_type # 'K','Q','R','B','N','P'
        self.row = row
        self.col = col
        self.has_moved = False

class ChessGame:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = 'white'
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False
        self.winner = None
        self.move_history = []
        self.last_move = None  # for en passant

        # Promotion fields
        self.promotion_pending = False
        self.promotion_pawn = None
        self.promotion_row = None
        self.promotion_col = None

        self.setup_board()

    def setup_board(self):
        # Black back rank
        piece_order = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for col in range(COLS):
            self.board[0][col] = Piece('black', piece_order[col], 0, col)
            self.board[1][col] = Piece('black', 'P', 1, col)

        # White back rank
        for col in range(COLS):
            self.board[6][col] = Piece('white', 'P', 6, col)
            self.board[7][col] = Piece('white', piece_order[col], 7, col)

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < ROWS and 0 <= col < COLS

    def get_valid_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        if piece.piece_type == 'P':
            moves = self.get_pawn_moves(piece)
        elif piece.piece_type == 'R':
            moves = self.get_rook_moves(piece)
        elif piece.piece_type == 'N':
            moves = self.get_knight_moves(piece)
        elif piece.piece_type == 'B':
            moves = self.get_bishop_moves(piece)
        elif piece.piece_type == 'Q':
            moves = self.get_queen_moves(piece)
        elif piece.piece_type == 'K':
            moves = self.get_king_moves(piece)

        # Filter out moves that leave/put own king in check
        legal_moves = []
        for move in moves:
            if self.is_legal_move(piece, move):
                legal_moves.append(move)
        return legal_moves

    def get_pawn_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        direction = -1 if piece.color == 'white' else 1
        start_row = 6 if piece.color == 'white' else 1

        # Single step forward
        nr = piece.row + direction
        if self.is_valid_position(nr, piece.col) and not self.board[nr][piece.col]:
            moves.append((nr, piece.col))
            # Double step from starting position
            if piece.row == start_row:
                nr2 = piece.row + 2 * direction
                if self.is_valid_position(nr2, piece.col) and not self.board[nr2][piece.col]:
                    moves.append((nr2, piece.col))

        # Captures (normal + en passant)
        for dc in [-1, 1]:
            nr = piece.row + direction
            nc = piece.col + dc
            if self.is_valid_position(nr, nc):
                target = self.board[nr][nc]
                if target and target.color != piece.color:
                    moves.append((nr, nc))

        # En passant
        if self.last_move:
            last_piece, (orow, ocol), (nrow, ncol) = self.last_move
            if (last_piece.piece_type == 'P' and
                abs(nrow - orow) == 2 and
                nrow == piece.row and
                abs(ncol - piece.col) == 1):
                ep_row = piece.row + direction
                moves.append((ep_row, ncol))

        return moves

    def get_rook_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        for dr, dc in directions:
            for i in range(1, 8):
                nr = piece.row + dr * i
                nc = piece.col + dc * i
                if not self.is_valid_position(nr, nc):
                    break
                target = self.board[nr][nc]
                if target:
                    if target.color != piece.color:
                        moves.append((nr, nc))
                    break
                moves.append((nr, nc))
        return moves

    def get_knight_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        deltas = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        for dr, dc in deltas:
            nr = piece.row + dr
            nc = piece.col + dc
            if self.is_valid_position(nr, nc):
                target = self.board[nr][nc]
                if not target or target.color != piece.color:
                    moves.append((nr, nc))
        return moves

    def get_bishop_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        directions = [(1,1),(1,-1),(-1,1),(-1,-1)]
        for dr, dc in directions:
            for i in range(1, 8):
                nr = piece.row + dr * i
                nc = piece.col + dc * i
                if not self.is_valid_position(nr, nc):
                    break
                target = self.board[nr][nc]
                if target:
                    if target.color != piece.color:
                        moves.append((nr, nc))
                    break
                moves.append((nr, nc))
        return moves

    def get_queen_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        return self.get_rook_moves(piece) + self.get_bishop_moves(piece)

    def get_king_moves(self, piece: Piece, include_castling: bool = True) -> List[Tuple[int, int]]:
        moves = []
        directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
        for dr, dc in directions:
            nr = piece.row + dr
            nc = piece.col + dc
            if self.is_valid_position(nr, nc):
                target = self.board[nr][nc]
                if not target or target.color != piece.color:
                    moves.append((nr, nc))

        # Castling
        if include_castling and not piece.has_moved and not self.is_in_check(piece.color):
            opp = 'black' if piece.color == 'white' else 'white'
            # Kingside
            if (self.board[piece.row][7] and self.board[piece.row][7].piece_type == 'R' and
                not self.board[piece.row][7].has_moved and
                not self.board[piece.row][5] and not self.board[piece.row][6] and
                not self.is_under_attack(piece.row, 5, opp) and
                not self.is_under_attack(piece.row, 6, opp)):
                moves.append((piece.row, 6))
            # Queenside
            if (self.board[piece.row][0] and self.board[piece.row][0].piece_type == 'R' and
                not self.board[piece.row][0].has_moved and
                not self.board[piece.row][1] and not self.board[piece.row][2] and
                not self.board[piece.row][3] and
                not self.is_under_attack(piece.row, 3, opp) and
                not self.is_under_attack(piece.row, 2, opp)):
                moves.append((piece.row, 2))

        return moves

    def is_under_attack(self, row: int, col: int, by_color: str) -> bool:
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board[r][c]
                if p and p.color == by_color:
                    if p.piece_type == 'P':
                        dir = -1 if p.color == 'white' else 1
                        if (p.row + dir == row and abs(p.col - col) == 1):
                            return True
                    else:
                        moves_func = {
                            'R': self.get_rook_moves,
                            'N': self.get_knight_moves,
                            'B': self.get_bishop_moves,
                            'Q': self.get_queen_moves,
                            'K': lambda x: self.get_king_moves(x, include_castling=False)
                        }.get(p.piece_type)
                        if moves_func and (row, col) in moves_func(p):
                            return True
        return False

    def find_king(self, color: str) -> Optional[Tuple[int, int]]:
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board[r][c]
                if p and p.color == color and p.piece_type == 'K':
                    return (r, c)
        return None

    def is_in_check(self, color: str) -> bool:
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        opp = 'black' if color == 'white' else 'white'
        return self.is_under_attack(king_pos[0], king_pos[1], opp)

    def find_checking_piece(self, color: str) -> Optional[Piece]:
        """Find the piece that is checking the king of given color"""
        king_pos = self.find_king(color)
        if not king_pos:
            return None
        
        king_row, king_col = king_pos
        opp = 'black' if color == 'white' else 'white'
        
        # Check all opponent pieces to see if any is attacking the king
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board[r][c]
                if p and p.color == opp:
                    if p.piece_type == 'P':
                        dir = 1 if p.color == 'white' else -1
                        if (p.row + dir == king_row and abs(p.col - king_col) == 1):
                            return p
                    else:
                        moves_func = {
                            'R': self.get_rook_moves,
                            'N': self.get_knight_moves,
                            'B': self.get_bishop_moves,
                            'Q': self.get_queen_moves,
                            'K': lambda x: self.get_king_moves(x, include_castling=False)
                        }.get(p.piece_type)
                        if moves_func and (king_row, king_col) in moves_func(p):
                            return p
        return None

    def is_legal_move(self, piece: Piece, move: Tuple[int, int]) -> bool:
        orow, ocol = piece.row, piece.col
        nrow, ncol = move
        captured = self.board[nrow][ncol]

        # Simulate move
        self.board[nrow][ncol] = piece
        self.board[orow][ocol] = None
        piece.row, piece.col = nrow, ncol

        in_check = self.is_in_check(piece.color)

        # Undo
        self.board[orow][ocol] = piece
        self.board[nrow][ncol] = captured
        piece.row, piece.col = orow, ocol

        return not in_check

    def move_piece(self, piece: Piece, new_row: int, new_col: int):
        old_row, old_col = piece.row, piece.col

        # Castling
        if piece.piece_type == 'K' and abs(new_col - old_col) == 2:
            if new_col == 6:  # kingside
                rook = self.board[piece.row][7]
                self.board[piece.row][7] = None
                self.board[piece.row][5] = rook
                rook.col = 5
                rook.has_moved = True
            elif new_col == 2:  # queenside
                rook = self.board[piece.row][0]
                self.board[piece.row][0] = None
                self.board[piece.row][3] = rook
                rook.col = 3
                rook.has_moved = True

        # En passant capture
        if (piece.piece_type == 'P' and old_col != new_col and
            not self.board[new_row][new_col]):
            captured_row = old_row
            self.board[captured_row][new_col] = None

        # Perform move
        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.row = new_row
        piece.col = new_col
        piece.has_moved = True

        self.last_move = (piece, (old_row, old_col), (new_row, new_col))

        # Check for promotion
        promotion_row = 0 if piece.color == 'white' else 7
        if piece.piece_type == 'P' and new_row == promotion_row:
            self.promotion_pending = True
            self.promotion_pawn = piece
            self.promotion_row = new_row
            self.promotion_col = new_col
            return  # Do NOT switch turn yet

        # Normal move - switch player & check end
        self.current_player = 'black' if self.current_player == 'white' else 'white'

        if not self.has_legal_moves(self.current_player):
            self.game_over = True
            if self.is_in_check(self.current_player):
                self.winner = 'black' if self.current_player == 'white' else 'white'
            else:
                self.winner = 'Draw (Stalemate)'

    def promote_pawn(self, new_type: str):
        if not self.promotion_pending or not self.promotion_pawn:
            return
        self.promotion_pawn.piece_type = new_type.upper()
        self.promotion_pending = False
        self.promotion_pawn = None
        self.promotion_row = None
        self.promotion_col = None

        # Now switch turn & check game end
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        if not self.has_legal_moves(self.current_player):
            self.game_over = True
            if self.is_in_check(self.current_player):
                self.winner = 'black' if self.current_player == 'white' else 'white'
            else:
                self.winner = 'Draw (Stalemate)'

    def select_piece(self, row: int, col: int):
        if self.promotion_pending:
            return

        piece = self.get_piece(row, col)

        if self.selected_piece:
            if (row, col) in self.valid_moves:
                self.move_piece(self.selected_piece, row, col)
                self.selected_piece = None
                self.valid_moves = []
            elif piece and piece.color == self.current_player:
                self.selected_piece = piece
                self.valid_moves = self.get_valid_moves(piece)
            else:
                self.selected_piece = None
                self.valid_moves = []
        elif piece and piece.color == self.current_player:
            self.selected_piece = piece
            self.valid_moves = self.get_valid_moves(piece)

    def has_legal_moves(self, color: str) -> bool:
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board[r][c]
                if p and p.color == color:
                    if self.get_valid_moves(p):
                        return True
        return False

# ────────────────────────────────────────────────
#               DRAWING FUNCTIONS
# ────────────────────────────────────────────────

def draw_board(screen):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, game):
    font = pygame.font.SysFont("segoeuisymbol", 68)  # or "DejaVu Sans", "Arial Unicode MS", "Noto Sans"

    symbols = {
        ('white', 'K'): '♚', ('white', 'Q'): '♛', ('white', 'R'): '♜',
        ('white', 'B'): '♝', ('white', 'N'): '♞', ('white', 'P'): '♟',
        ('black', 'K'): '♔', ('black', 'Q'): '♕', ('black', 'R'): '♖',
        ('black', 'B'): '♗', ('black', 'N'): '♘', ('black', 'P'): '♙'
    }

    for r in range(ROWS):
        for c in range(COLS):
            piece = game.get_piece(r, c)
            if piece:
                symbol = symbols.get((piece.color, piece.piece_type), '?')
                color = (240, 240, 240) if piece.color == 'white' else (30, 30, 30)
                text = font.render(symbol, True, color)
                rect = text.get_rect(center=(c * SQUARE_SIZE + SQUARE_SIZE//2,
                                             r * SQUARE_SIZE + SQUARE_SIZE//2))
                screen.blit(text, rect)

def draw_highlights(screen, game):
    # Highlight king and checking piece in red if in check
    if game.is_in_check(game.current_player):
        king_pos = game.find_king(game.current_player)
        if king_pos:
            kr, kc = king_pos
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill((255, 0, 0, 150))  # Red for king in check
            screen.blit(s, (kc * SQUARE_SIZE, kr * SQUARE_SIZE))
        
        # Highlight the checking piece
        checking_piece = game.find_checking_piece(game.current_player)
        if checking_piece:
            cr, cc = checking_piece.row, checking_piece.col
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill((255, 0, 0, 150))  # Red for checking piece
            screen.blit(s, (cc * SQUARE_SIZE, cr * SQUARE_SIZE))
    
    if game.selected_piece:
        r, c = game.selected_piece.row, game.selected_piece.col
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(SELECTED)
        screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))

    for r, c in game.valid_moves:
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(HIGHLIGHT)
        screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))

def draw_promotion_choice(screen, game):
    if not game.promotion_pending:
        return

    row = game.promotion_row
    col_center = game.promotion_col

    # Semi-transparent dark bar
    overlay = pygame.Surface((SQUARE_SIZE * 4, SQUARE_SIZE), pygame.SRCALPHA)
    overlay.fill(PROMOTION_BG)
    start_x = max(0, (col_center - 1) * SQUARE_SIZE)
    screen.blit(overlay, (start_x, row * SQUARE_SIZE))

    font = pygame.font.SysFont("segoeuisymbol", 72)

    choices = ['Q','R','B','N']
    symbols = ['♛','♜','♝','♞'] if game.promotion_pawn.color == 'white' else ['♕','♖','♗','♘']

    for i, (choice, sym) in enumerate(zip(choices, symbols)):
        x = start_x + i * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        text = font.render(sym, True, (255, 255, 255))
        rect = text.get_rect(center=(x, y))
        screen.blit(text, rect)

def draw_info(screen, game):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Current: {game.current_player.capitalize()}", True, (255,255,255))
    screen.blit(text, (10, HEIGHT + 8))

    if game.is_in_check(game.current_player):
        check = font.render("CHECK!", True, (255, 80, 80))
        screen.blit(check, (WIDTH - 140, HEIGHT + 8))

def draw_game_over(screen, game):
    if not game.game_over:
        return
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,180))
    screen.blit(overlay, (0,0))

    font = pygame.font.Font(None, 80)
    if game.winner == 'Draw (Stalemate)':
        text = font.render("Stalemate", True, (220,220,220))
    else:
        text = font.render(f"{game.winner.capitalize()} wins!", True, (220,220,100))
    rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
    screen.blit(text, rect)

    small = pygame.font.Font(None, 40)
    restart = small.render("Press R to restart", True, (200,200,200))
    screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 50))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))
    pygame.display.set_caption("Chess - Promotion & Unicode Pieces")
    clock = pygame.time.Clock()
    game = ChessGame()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                x, y = event.pos
                if y >= HEIGHT:
                    continue
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE

                if game.promotion_pending:
                    prom_row = game.promotion_row
                    start_col = max(0, game.promotion_col - 1)
                    if row == prom_row and start_col <= col < start_col + 4:
                        idx = col - start_col
                        choice = ['Q','R','B','N'][idx]
                        game.promote_pawn(choice)
                else:
                    game.select_piece(row, col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = ChessGame()

        screen.fill((30, 30, 40))
        draw_board(screen)
        draw_highlights(screen, game)
        draw_pieces(screen, game)
        draw_promotion_choice(screen, game)
        draw_info(screen, game)
        draw_game_over(screen, game)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()