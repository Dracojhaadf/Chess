♟️ Unicode Chess (Pygame)

A fully functional, lightweight Chess engine built in Python using Pygame, featuring a clean UI rendered entirely with Unicode chess symbols.
The game faithfully implements all standard chess rules, including advanced mechanics like Castling, En Passant, and Pawn Promotion, while maintaining smooth gameplay and clear visual feedback.

✨ Features
♜ Complete Move Logic

Supports all standard chess piece movements:

Pawn

Rook

Knight

Bishop

Queen

King

♞ Special Moves

Castling

King-side and Queen-side castling

Prevents illegal castling through or into check

En Passant

Correctly handles the special pawn capture after a double-step move

Pawn Promotion

Interactive UI popup when a pawn reaches the final rank

Choose between Queen, Rook, Bishop, or Knight

♚ Game State Detection

Check & Checkmate

Visual indication when a king is under attack

Stalemate

Automatically detects drawn positions when no legal moves remain

🎨 Visual Enhancements

Highlighted selected pieces

Highlighted valid moves

Clear check indicators for better readability and gameplay flow

🛠️ Installation & Requirements
Prerequisites

Python 3.x

Pygame

Install Pygame
pip install pygame

Unicode Font Support

The game uses Unicode chess symbols (♚ ♞ ♛ etc.).
Most modern operating systems already support these:

Windows: Segoe UI Symbol

Linux: DejaVu Sans

macOS: Default system fonts

⚠️ If pieces appear as empty squares or blocks, ensure a Unicode-compatible font is installed on your system.

🎮 How to Play
Run the Game
python chess_game.py

Controls

Left Click

Select a piece

Move a piece to a valid square

Pawn Promotion

Click one of the four piece symbols shown on the top/bottom bar

R Key

Reset the game at any time

Visual Cues
Color	Meaning
🟨 Yellow	Currently selected piece
🟩 Green	Valid moves for selected piece
🟥 Red	King in check or checking piece
