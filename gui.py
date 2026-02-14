import tkinter as tk
from tkinter import PhotoImage, Canvas
import os

class LastMoveGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Last Move Game")
        
        self.canvas = Canvas(master)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.board_size = 3  # Default size
        self.board_image = None
        self.big_stone_image = None
        self.small_stone_image = None

        self.load_assets()
        self.draw_board()

    def load_assets(self):
        asset_path = os.path.join(os.path.dirname(__file__), 'assets')
        self.board_images = {
            3: PhotoImage(file=os.path.join(asset_path, 'board_3x3.svg')),
            5: PhotoImage(file=os.path.join(asset_path, 'board_5x5.svg')),
            7: PhotoImage(file=os.path.join(asset_path, 'board_7x7.svg')),
        }
        self.big_stone_image = PhotoImage(file=os.path.join(asset_path, 'stone_big.svg'))
        self.small_stone_image = PhotoImage(file=os.path.join(asset_path, 'stone_small.svg'))

    def draw_board(self):
        self.canvas.delete("all")
        self.board_image = self.board_images[self.board_size]
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.board_image)

    def update_board(self, board):
        # Logic to update the board with stones based on the game state
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] == "O":
                    self.canvas.create_image(col * 100, row * 100, anchor=tk.NW, image=self.small_stone_image)
                elif board[row][col] != "":
                    self.canvas.create_image(col * 100, row * 100, anchor=tk.NW, image=self.big_stone_image)

    def set_board_size(self, size):
        self.board_size = size
        self.draw_board()

def main():
    root = tk.Tk()
    game_gui = LastMoveGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()