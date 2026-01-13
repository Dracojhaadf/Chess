Unicode Chess with Pygame
This is a fully functional, lightweight Chess engine written in Python using the pygame library. It features a clean UI using Unicode character symbols for pieces and supports advanced chess rules like Castling, En Passant, and Pawn Promotion.

🚀 Features
Complete Move Logic: Supports all standard moves for Pawns, Rooks, Knights, Bishops, Queens, and Kings.

Special Moves:

Castling: King and Queen-side castling logic (ensures king doesn't move through check).

En Passant: Allows pawn capture on the special diagonal move following an opponent's double-step.

Pawn Promotion: Interactive UI popup to choose between Queen, Rook, Bishop, or Knight when a pawn reaches the final rank.

Game State Detection:

Check/Checkmate: Visual indicators for when a king is under attack.

Stalemate: Automatic detection of draws when no legal moves remain.

Visual Highlights: Selected pieces and valid target squares are highlighted for better playability.

🛠️ Installation & Requirements
Prerequisites
Python 3.x

Pygame: The library used for rendering and event handling.

Setup
Install Pygame:

Bash

pip install pygame
Ensure Font Support: The game uses Unicode symbols (♚, ♞, etc.). Most modern OS fonts (like Segoe UI Symbol on Windows or DejaVu Sans on Linux) support these. If pieces appear as blocks, ensure your system has a Unicode-compatible font installed.

🎮 How to Play
Run the Game:

Bash

python chess_game.py
Controls:

Left Click: Select a piece or a destination square.

Promotion: Click one of the four symbols that appear on the top/bottom bar when a pawn reaches the end.

R Key: Reset the game at any time.

Visual Cues:

Yellow: Currently selected piece.

Green: Valid moves for the selected piece.

Red: The King is in check, or the piece that is delivering the check.

📂 Code Structure
Piece Class: Manages individual piece data (color, type, position, and movement history).

ChessGame Class: The "Brain" of the application. It manages the board state, move validation (including "move simulation" to prevent moving into check), and turn logic.

Drawing Functions: Modular functions to render the board, pieces, and UI overlays independently.

Main Loop: Handles the 60 FPS update cycle and event processing.

🧪 Implementation Notes: Move Validation
The engine uses a simulation-based approach to validate legal moves. When you click a piece:

It calculates all "pseudo-legal" moves based on the piece type.

It temporarily "executes" the move on a ghost board.

It checks if the friendly King is under attack in that new state.

If the King is safe, the move is added to the final valid_moves list.
