# Last Move Game Visualization

This project is a graphical representation of the Last Move game, which allows players to interact with the game visually using a GUI. The game features a customizable board size of 3x3, 5x5, or 7x7, and players can move their big stones and place small stones on the board.

## Project Structure

The project is organized as follows:

```
last-move-visualization
├── src
│   ├── main.py          # Main game logic and loop
│   ├── gui.py           # Graphical user interface
│   ├── assets           # Contains SVG graphics for boards and stones
│   │   ├── board_3x3.svg
│   │   ├── board_5x5.svg
│   │   ├── board_7x7.svg
│   │   ├── stone_big.svg
│   │   └── stone_small.svg
│   └── utils.py         # Utility functions for the project
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd last-move-visualization
   ```

2. **Install dependencies**:
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   Execute the main script to start the game:
   ```bash
   python src/main.py
   ```

## Usage Guidelines

- Upon starting the game, you will be prompted to select the board size (3, 5, or 7).
- Players will take turns moving their big stones and placing small stones on the board.
- The game ends when a player can no longer make a valid move.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.