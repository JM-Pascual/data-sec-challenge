from minesweeper_mapper import map_board_to_neighbouring_mines

if __name__ == '__main__':
    board = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 1, 0, 0]
    ]

    mapped_board = map_board_to_neighbouring_mines(board)

    for row in mapped_board:
        print(row)