def load_svg(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def load_board_assets():
    boards = {
        '3x3': load_svg('src/assets/board_3x3.svg'),
        '5x5': load_svg('src/assets/board_5x5.svg'),
        '7x7': load_svg('src/assets/board_7x7.svg')
    }
    return boards

def load_stone_assets():
    stones = {
        'big': load_svg('src/assets/stone_big.svg'),
        'small': load_svg('src/assets/stone_small.svg')
    }
    return stones

def get_asset(asset_type, size=None):
    if asset_type == 'board':
        if size in ['3x3', '5x5', '7x7']:
            return load_board_assets()[size]
    elif asset_type == 'stone':
        if size in ['big', 'small']:
            return load_stone_assets()[size]
    return None