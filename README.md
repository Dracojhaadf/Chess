# ♟️ Chess Game

A fully-featured chess game built with Python and Pygame, featuring Unicode chess pieces, all standard chess rules, and a clean visual interface.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- **Complete Chess Rules Implementation**
  - All piece movements (King, Queen, Rook, Bishop, Knight, Pawn)
  - Special moves: Castling (kingside and queenside)
  - En passant captures
  - Pawn promotion with piece selection UI
  - Check and checkmate detection
  - Stalemate detection

- **Visual Features**
  - Beautiful Unicode chess pieces (♔♕♖♗♘♙)
  - Highlighted valid moves
  - Check indicators (red highlights for king and attacking piece)
  - Selected piece highlighting
  - Smooth promotion interface

- **Game Management**
  - Turn-based gameplay
  - Move validation (prevents moves that leave king in check)
  - Game over detection
  - Restart functionality

## 🎮 How to Play

### Controls
- **Left Click**: Select and move pieces
- **R Key**: Restart game at any time
- **ESC**: Quit game

### Making Moves
1. Click on a piece of your color to select it
2. Valid moves will be highlighted in yellow-green
3. Click on a highlighted square to move
4. When a pawn reaches the opposite end, click on your desired promotion piece (Queen, Rook, Bishop, or Knight)

### Special Moves
- **Castling**: Move the king two squares toward a rook (kingside or queenside) when neither piece has moved, squares between are empty, and king is not in check
- **En Passant**: Available when an opponent's pawn moves two squares forward and lands beside your pawn
- **Promotion**: Occurs automatically when a pawn reaches the opposite end of the board

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Pygame library

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/chess-game.git
cd chess-game
```

2. **Install dependencies**
```bash
pip install pygame
```

3. **Run the game**
```bash
python chess.py
```

## 🎨 Screenshots

*Add screenshots of your game here*

## 🏗️ Project Structure

```
chess-game/
│
├── chess.py          # Main game file
└── README.md         # This file
```

## 🔧 Technical Details

### Board Representation
- 8x8 grid using a 2D list
- Each square contains either a `Piece` object or `None`
- Coordinates: (0,0) is top-left (black's back rank)

### Move Validation
- Generates pseudo-legal moves for each piece type
- Filters moves that would leave the king in check
- Simulates each move to verify legality

### Game States
- **Normal Play**: Players alternate turns
- **Check**: King is under attack (visual indicator shown)
- **Checkmate**: King in check with no legal moves (game over)
- **Stalemate**: No legal moves but king not in check (draw)
- **Promotion**: Player selects piece to promote pawn to

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

### Development Roadmap
- [ ] Move history display
- [ ] Captured pieces display
- [ ] Timer/clock for each player
- [ ] Save/load game functionality
- [ ] AI opponent
- [ ] Online multiplayer
- [ ] Opening book suggestions
- [ ] Move notation (algebraic notation)

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🐛 Known Issues

- None currently reported

## 💡 Tips for Players

- Plan your moves ahead
- Control the center of the board
- Protect your king (castle early!)
- Develop your pieces in the opening
- Look for checks and captures first
- The queen is powerful but can be trapped easily

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

## 🙏 Acknowledgments

- Built with [Pygame](https://www.pygame.org/)
- Chess rules reference: [FIDE Laws of Chess](https://www.fide.com/FIDE/handbook/LawsOfChess.pdf)
- Unicode chess symbols from Unicode Standard

---

**Enjoy the game! ♟️**
