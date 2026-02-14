import sys
import copy
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit,
    QComboBox, QPushButton, QStackedWidget, QHBoxLayout, QMessageBox, QFrame
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

ASSET_PATH = os.path.join(os.path.dirname(__file__), "assets")

class StartScreen(QWidget):
    def __init__(self, on_start):
        super().__init__()
        self.on_start = on_start
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name1_label = QLabel("1. Oyuncu ismi:")
        layout.addWidget(self.name1_label)
        self.name1_input = QLineEdit()
        layout.addWidget(self.name1_input)

        self.name2_label = QLabel("2. Oyuncu ismi:")
        layout.addWidget(self.name2_label)
        self.name2_input = QLineEdit()
        layout.addWidget(self.name2_input)

        self.size_label = QLabel("Tahta boyutu:")
        layout.addWidget(self.size_label)
        self.size_combo = QComboBox()
        self.size_combo.addItems(["3x3", "5x5", "7x7"])
        layout.addWidget(self.size_combo)

        # Tahta renkleri seçimi
        self.board_color_label = QLabel("Tahta renkleri:")
        layout.addWidget(self.board_color_label)
        self.board_color_combo = QComboBox()
        self.board_color_combo.addItems([
            "Siyah-Beyaz", "Kahverengi-Bej", "Mavi-Beyaz", "Yeşil-Beyaz", "Gri-Beyaz", "Kırmızı-Beyaz"
        ])
        layout.addWidget(self.board_color_combo)

        self.start_button = QPushButton("Başla")
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button)

    def start_game(self):
        name1 = self.name1_input.text().strip() or "P1"
        name2 = self.name2_input.text().strip() or "P2"
        size = int(self.size_combo.currentText().split("x")[0])
        board_color = self.board_color_combo.currentText()
        self.on_start(name1, name2, size, board_color)

class GameWindow(QWidget):
    def __init__(self, player1, player2, board_size, board_color):
        super().__init__()
        self.player_names = [player1, player2]
        self.board_size = board_size
        self.turn = 0
        self.positions = [(0, board_size // 2), (board_size - 1, board_size // 2)]
        self.board_color = board_color
        self.init_game()

    def get_board_colors(self):
        # Renk çiftlerini döndürür
        color_map = {
            "Siyah-Beyaz": ("#222", "#fff"),
            "Kahverengi-Bej": ("#8B5A2B", "#F5DEB3"),
            "Mavi-Beyaz": ("#3399ff", "#fff"),
            "Yeşil-Beyaz": ("#228B22", "#fff"),
            "Gri-Beyaz": ("#888", "#fff"),
            "Kırmızı-Beyaz": ("#cc2222", "#fff"),
        }
        return color_map.get(self.board_color, ("#222", "#fff"))

    def init_game(self):
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.board[self.positions[0][0]][self.positions[0][1]] = "P1_BIG"
        self.board[self.positions[1][0]][self.positions[1][1]] = "P2_BIG"

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.board_widget = QFrame(self)
        kare_boyutu = 60
        self.board_widget.setFixedSize(kare_boyutu*self.board_size, kare_boyutu*self.board_size)
        self.layout.addWidget(self.board_widget, alignment=Qt.AlignCenter)

        board_svg = f"board_{self.board_size}x{self.board_size}.svg"
        board_svg_path = os.path.join(ASSET_PATH, board_svg)
        self.board_bg = QLabel(self.board_widget)
        self.board_bg.setPixmap(QPixmap(board_svg_path).scaled(kare_boyutu*self.board_size, kare_boyutu*self.board_size, Qt.KeepAspectRatio))
        self.board_bg.setGeometry(0, 0, kare_boyutu*self.board_size, kare_boyutu*self.board_size)

        self.stone_pixmaps = {
            "P1_BIG": QPixmap(os.path.join(ASSET_PATH, "P1stone_big.svg")).scaled(50, 50, Qt.KeepAspectRatio),
            "P2_BIG": QPixmap(os.path.join(ASSET_PATH, "P2stone_big.svg")).scaled(50, 50, Qt.KeepAspectRatio),
            "P1_SMALL": QPixmap(os.path.join(ASSET_PATH, "P1stone_small.svg")).scaled(40, 40, Qt.KeepAspectRatio),
            "P2_SMALL": QPixmap(os.path.join(ASSET_PATH, "P2stone_small.svg")).scaled(40, 40, Qt.KeepAspectRatio),
        }

        # Hamle tipi: önce büyük taş, sonra küçük taş
        self.move_phase = "big"  # "big" veya "small"

        # Kareler için QLabel ve tıklama
        color1, color2 = self.get_board_colors()
        self.cell_labels = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        for i in range(self.board_size):
            for j in range(self.board_size):
                lbl = ClickableLabel(i, j, self.board_widget)
                lbl.setGeometry(j*kare_boyutu, i*kare_boyutu, kare_boyutu, kare_boyutu)
                # Alternatif renkli kareler (dama tahtası gibi)
                if (i + j) % 2 == 0:
                    lbl.setStyleSheet(f"background: {color1};")
                else:
                    lbl.setStyleSheet(f"background: {color2};")
                lbl.setScaledContents(True)
                lbl.clicked.connect(self.handle_cell_click)
                self.cell_labels[i][j] = lbl

        self.status_label = QLabel()
        self.layout.addWidget(self.status_label)
        self.update_board()
        self.update_status()

    def update_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell = self.board[i][j]
                lbl = self.cell_labels[i][j]
                if cell == "P1_BIG":
                    lbl.setPixmap(self.stone_pixmaps["P1_BIG"])
                elif cell == "P2_BIG":
                    lbl.setPixmap(self.stone_pixmaps["P2_BIG"])
                elif cell == "P1_SMALL":
                    lbl.setPixmap(self.stone_pixmaps["P1_SMALL"])
                elif cell == "P2_SMALL":
                    lbl.setPixmap(self.stone_pixmaps["P2_SMALL"])
                else:
                    lbl.clear()

    def update_status(self):
        idx = self.turn % 2
        if self.move_phase == "big":
            self.status_label.setText(f"{self.player_names[idx]} ({'P1' if idx==0 else 'P2'}) büyük taşını hareket ettir.")
        else:
            self.status_label.setText(f"{self.player_names[idx]} ({'P1' if idx==0 else 'P2'}) küçük taşını yerleştir.")

    def handle_cell_click(self, row, col):
        idx = self.turn % 2
        if self.move_phase == "big":
            if self.positions[idx] == (row, col):
                moves = self.get_valid_moves(row, col)
                self.highlight_moves(moves)
                self.selected_big = (row, col)
            elif hasattr(self, "selected_big") and (row, col) in self.get_valid_moves(*self.selected_big):
                self.board[self.selected_big[0]][self.selected_big[1]] = ""
                self.board[row][col] = f"P{idx+1}_BIG"
                self.positions[idx] = (row, col)
                self.move_phase = "small"
                self.update_board()
                self.highlight_moves([])  # Yeşil çerçeveyi temizle
                self.update_status()
                del self.selected_big
        elif self.move_phase == "small":
            if self.board[row][col] == "":
                self.board[row][col] = f"P{idx+1}_SMALL"
                self.update_board()  # Taş hemen görünsün
                next_idx = (self.turn + 1) % 2
                next_player = {"symbol": f"P{next_idx+1}_BIG", "position": self.positions[next_idx]}
                if not check_winner(self.board, next_player, self.board_size):
                    # 1 saniye gecikmeli kazanan mesajı
                    QTimer.singleShot(1000, lambda: QMessageBox.information(self, "Oyun Bitti", f"{self.player_names[idx]} kazandı!"))
                    return
                self.turn += 1
                self.move_phase = "big"
                self.update_board()
                self.update_status()

    def get_valid_moves(self, row, col):
        # Büyük taş için geçerli hamleleri döndürür
        directions = [(-1,0),(1,0),(0,1),(0,-1),(-1,1),(-1,-1),(1,1),(1,-1)]
        moves = []
        for dr, dc in directions:
            nr, nc = row+dr, col+dc
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size and self.board[nr][nc] == "":
                moves.append((nr, nc))
        return moves

    def highlight_moves(self, moves):
        color1, color2 = self.get_board_colors()
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (i + j) % 2 == 0:
                    self.cell_labels[i][j].setStyleSheet(f"background: {color1};")
                else:
                    self.cell_labels[i][j].setStyleSheet(f"background: {color2};")
        for r, c in moves:
            self.cell_labels[r][c].setStyleSheet("background: #aaffaa; border: 2px solid #33cc33;")

# Yardımcı: Tıklanabilir QLabel
from PyQt5.QtCore import pyqtSignal

class ClickableLabel(QLabel):
    clicked = pyqtSignal(int, int)
    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col

    def mousePressEvent(self, event):
        self.clicked.emit(self.row, self.col)

def check_winner(board, player, size):
    row, col = player["position"]
    directions = [(-1,0),(1,0),(0,1),(0,-1),(-1,1),(-1,-1),(1,1),(1,-1)]
    for dr, dc in directions:
        nr, nc = row+dr, col+dc
        if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == "":
            return True
    return False

class WelcomeScreen(QWidget):
    def __init__(self, on_new_game, on_how_to_play):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        logo_label = QLabel()
        logo_pixmap = QPixmap(logo_path).scaled(200, 200, Qt.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Başlık
        title = QLabel("Last Move Game")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # Yeni Oyun Butonu
        new_game_btn = QPushButton("Yeni Oyun")
        new_game_btn.setStyleSheet("font-size: 18px; padding: 10px;")
        new_game_btn.clicked.connect(on_new_game)
        layout.addWidget(new_game_btn)

        # Nasıl Oynanır Butonu
        how_to_play_btn = QPushButton("Nasıl Oynanır?")
        how_to_play_btn.setStyleSheet("font-size: 18px; padding: 10px;")
        how_to_play_btn.clicked.connect(on_how_to_play)
        layout.addWidget(how_to_play_btn)

        layout.addStretch()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Last Move Game")
        self.setGeometry(100, 100, 600, 700)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # WelcomeScreen ekle
        self.welcome_screen = WelcomeScreen(self.show_start_screen, self.show_how_to_play)
        self.stack.addWidget(self.welcome_screen)

        self.start_screen = StartScreen(self.start_game)
        self.stack.addWidget(self.start_screen)

    def show_start_screen(self):
        self.stack.setCurrentWidget(self.start_screen)

    def show_how_to_play(self):
        QMessageBox.information(
            self,
            "Nasıl Oynanır?",
            "Oyunun amacı rakibin büyük taşını hareket ettiremeyeceği bir konuma getirmektir.\n"
            "Her turda önce büyük taşınızı bir yöne hareket ettirebilirsiniz,(eğer ihtiyacınız varsa) ardından küçük taşınızı yerleştirin.\n"
            "Büyük taşlar çapraz ve düz hareket edebilir. Küçük taşlar engel olarak kullanılır.\n"
            "Taşlar boş karelere yerleştirilebilir."
        )

    def start_game(self, name1, name2, size, board_color):
        self.game_window = GameWindow(name1, name2, size, board_color)
        self.stack.addWidget(self.game_window)
        self.stack.setCurrentWidget(self.game_window)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    print(os.path.exists(os.path.join(ASSET_PATH, "P1stone_big.svg")))  # True olmalı
    sys.exit(app.exec_())