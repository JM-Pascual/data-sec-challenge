import pytest
from minesweeper_mapper import map_board_to_neighbouring_mines

# Tableros para los tests

EMPTY_BOARD = []
EMPTY_BOARD_EXPECTED = []

EMPTY_BOARD_NESTED = [[], [], [], []]
EMPTY_BOARD_NESTED_EXPECTED = [[], [], [], []]

SINGLE_ELEMENT_BOARD = [[0]]
SINGLE_ELEMENT_BOARD_EXPECTED = [[0]]

SINGLE_MINE_BOARD = [[1]]
SINGLE_MINE_BOARD_EXPECTED = [[9]]

BASE_EXAMPLE = [
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 1, 0, 0]
]
BASE_EXAMPLE_EXPECTED = [
    [1, 9, 2, 1],
    [2, 3, 9, 2],
    [3, 9, 4, 9],
    [9, 9, 3, 1]
]

NON_SQUARE_BOARD = [
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 1]
]
NON_SQUARE_BOARD_EXPECTED = [
    [1, 9, 2, 1],
    [2, 3, 9, 2],
    [1, 9, 3, 9]
]

LINEAR_BOARD = [[0, 0, 1, 0, 0, 1, 0, 0, 0, 0]]
LINEAR_BOARD_EXPECTED = [[0, 1, 9, 1, 1, 9, 1, 0, 0, 0]]

VERTICAL_BOARD = [
    [0],
    [0],
    [1],
    [0],
    [0],
    [1],
    [0],
    [0],
    [0],
    [0]
]
VERTICAL_BOARD_EXPECTED = [
    [0],
    [1],
    [9],
    [1],
    [1],
    [9],
    [1],
    [0],
    [0],
    [0]
]

ALL_BOMBS_BOARD = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]

ALL_BOMBS_BOARD_EXPECTED = [
    [9, 9, 9],
    [9, 9, 9],
    [9, 9, 9]
]

ALL_EMPTY_SQUARES_BOARD = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

ALL_EMPTY_SQUARES_BOARD_EXPECTED = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

BORDERS_BOARD = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]
BORDERS_BOARD_EXPECTED = [
    [9, 9, 9, 9, 9],
    [9, 5, 3, 5, 9],
    [9, 3, 0, 3, 9],
    [9, 5, 3, 5, 9],
    [9, 9, 9, 9, 9]
]

INVERTED_BORDERS_BOARD = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]
INVERTED_BORDERS_BOARD_EXPECTED = [
    [1, 2, 3, 2, 1],
    [2, 9, 9, 9, 2],
    [3, 9, 9, 9, 3],
    [2, 9, 9, 9, 2],
    [1, 2, 3, 2, 1]
]

ALL_AREAS_COVERED_BOARD = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]
ALL_AREAS_COVERED_BOARD_EXPECTED = [
    [9, 9, 9],
    [9, 8, 9],
    [9, 9, 9]
]

INVERTED_ALL_AREAS_COVERED_BOARD = [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
]
INVERTED_ALL_AREAS_COVERED_BOARD_EXPECTED = [
    [1, 1, 1],
    [1, 9, 1],
    [1, 1, 1]
]

# Funcion de assertion
def assert_expected_mapped_board_result(board, expected):
    assert map_board_to_neighbouring_mines(board) == expected

# Suite de tests
def test_empty_board():
    assert_expected_mapped_board_result(EMPTY_BOARD, EMPTY_BOARD_EXPECTED)

def test_empty_board_nested():
    assert_expected_mapped_board_result(EMPTY_BOARD_NESTED, EMPTY_BOARD_NESTED_EXPECTED)

def test_single_element_board():
    assert_expected_mapped_board_result(SINGLE_ELEMENT_BOARD, SINGLE_ELEMENT_BOARD_EXPECTED)

def test_single_mine_board():
    assert_expected_mapped_board_result(SINGLE_MINE_BOARD, SINGLE_MINE_BOARD_EXPECTED)

def test_linear_board():
    assert_expected_mapped_board_result(LINEAR_BOARD, LINEAR_BOARD_EXPECTED)

def test_vertical_board():
    assert_expected_mapped_board_result(VERTICAL_BOARD, VERTICAL_BOARD_EXPECTED)

def test_base_example():
    assert_expected_mapped_board_result(BASE_EXAMPLE, BASE_EXAMPLE_EXPECTED)

def test_non_square_board():
    assert_expected_mapped_board_result(NON_SQUARE_BOARD, NON_SQUARE_BOARD_EXPECTED)

def test_all_bombs_board():
    assert_expected_mapped_board_result(ALL_BOMBS_BOARD, ALL_BOMBS_BOARD_EXPECTED)

def test_all_empty_squares_board():
    assert_expected_mapped_board_result(ALL_EMPTY_SQUARES_BOARD, ALL_EMPTY_SQUARES_BOARD_EXPECTED)

def test_borders_board():
    assert_expected_mapped_board_result(BORDERS_BOARD, BORDERS_BOARD_EXPECTED)

def test_inverted_borders_board():
    assert_expected_mapped_board_result(INVERTED_BORDERS_BOARD, INVERTED_BORDERS_BOARD_EXPECTED)

def test_all_areas_covered_board():
    assert_expected_mapped_board_result(ALL_AREAS_COVERED_BOARD, ALL_AREAS_COVERED_BOARD_EXPECTED)

def test_inverted_all_areas_covered_board():
    assert_expected_mapped_board_result(INVERTED_ALL_AREAS_COVERED_BOARD, INVERTED_ALL_AREAS_COVERED_BOARD_EXPECTED)