# Valores de las areas del tablero
EMPTY_BOARD_AREA = 0
MINE_AREA = 1

# Valores de las areas mapeadas
MAPPED_MINE_AREA = 9

# Funcion de mapeo
def get_neighbouring_mines_in_area(board: list[list[int]], row_index: int, column_index: int) -> int:
    rows, cols = len(board), len(board[0])
    neighbouring_mines = 0

    # Es importante asegurarse que no se hagan lecturas de valores fuera de la tabla.
    # Es decir, validar para los siguientes casos:
    # i_inicial < 0 or i_max >= rows
    # j_inicial < 0 or j_max >= cols

    # Estas lineas generan los limites de ambos ciclos, evitando las condiciones anteriormente mencionadas
    # Si (index - 1) < 0, entonces nuestra cota inferior es 0
    # Si (index + 2) > rows || columns (segun corresponda), entonces nuestra cota superior es la que limita la matriz
    row_lower_bound, row_upper_bound = max(0, row_index - 1), min(rows, row_index + 2)
    col_lower_bound, col_upper_bound = max(0, column_index - 1), min(cols, column_index + 2)

    for i in range(row_lower_bound, row_upper_bound):
        for j in range(col_lower_bound, col_upper_bound):
            if board[i][j] == MINE_AREA:
                neighbouring_mines += 1

    return neighbouring_mines

# Funcion principal
def map_board_to_neighbouring_mines(board: list[list[int]]) -> list[list[int]]:
    # Como se aclaro en las observaciones, se entiende que la matriz puede no ser cuadrada pero si rectangular
    # Es decir, los valores de m y n pueden ser distintos pero no cambiar segun la fila o la columna

    # Se valida si la matriz esta vacia
    # En caso de estarlo, se retorna la misma matriz sin llamar a la funcion de mapeo
    if len(board) == 0 or len(board[0]) == 0:
        return board

    rows, cols = len(board), len(board[0])
    mapped_board = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == MINE_AREA:
                mapped_board[i][j] = MAPPED_MINE_AREA
                continue
            mapped_board[i][j] = get_neighbouring_mines_in_area(board, i, j)

    return mapped_board
