import pytest

from mutants import dna


@pytest.mark.parametrize(
    'y_index, x_index, max_starting_point, expected_result',
    [(0, 0, 2, True), (0, 1, 2, True), (0, 2, 2, True), (0, 3, 2, False)]
)
def test_horizontal_has_enough_length(y_index, x_index, max_starting_point, expected_result):
    result = dna.HorizontalChecker.has_enough_length(y_index, x_index, max_starting_point)
    assert result == expected_result


@pytest.mark.parametrize(
    'y_index, x_index, expected_result', [(0, 0, (0, 1)), (0, 1, (0, 2)), (0, 2, (0, 3))]
)
def test_horizontal_next_step(y_index, x_index, expected_result):
    result = dna.HorizontalChecker.next_step(y_index, x_index)
    assert result == expected_result


@pytest.mark.parametrize(
    'y_index, x_index, max_starting_point, expected_result',
    [(0, 0, 2, True), (1, 0, 2, True), (2, 0, 2, True), (3, 0, 2, False)]
)
def test_vertical_has_enough_length(y_index, x_index, max_starting_point, expected_result):
    result = dna.VerticalChecker.has_enough_length(y_index, x_index, max_starting_point)
    assert result == expected_result


@pytest.mark.parametrize(
    'y_index, x_index, expected_result', [(0, 0, (1, 0)), (1, 0, (2, 0)), (2, 0, (3, 0))]
)
def test_vertical_next_step(y_index, x_index, expected_result):
    result = dna.VerticalChecker.next_step(y_index, x_index)
    assert result == expected_result


@pytest.mark.parametrize(
    'y_index, x_index, max_starting_point, expected_result',
    [(0, 0, 2, True), (1, 1, 2, True), (2, 2, 2, True), (2, 3, 2, False), (3, 2, 2, False), (3, 3, 2, False)]
)
def test_diagonal_has_enough_length(y_index, x_index, max_starting_point, expected_result):
    result = dna.DiagonalChecker.has_enough_length(y_index, x_index, max_starting_point)
    assert result == expected_result


@pytest.mark.parametrize(
    'y_index, x_index, expected_result', [(0, 0, (1, 1)), (1, 1, (2, 2)), (2, 2, (3, 3))]
)
def test_diagonal_next_step(y_index, x_index, expected_result):
    result = dna.DiagonalChecker.next_step(y_index, x_index)
    assert result == expected_result


@pytest.mark.parametrize(
    'dna_sequence, expected_result',
    [(["ATGCGA", "CAGTGC", "TTATTT", "AGACGG", "GCGTCA", "TCACTG"], False),
     (["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"], True),
     (["ATGCGA", "CAGTGC", "TTATTT", "AGAAGG", "GCGTAA", "TCACTA"], False)]
)
def test_diagonal_border_reached(dna_sequence, expected_result):
    result = dna.identify(dna_sequence)
    assert result == expected_result


def test_abstract():
    try:
        dna.BaseChecker.has_enough_length(0, 0, 0)
    except NotImplementedError:
        pass

    try:
        dna.BaseChecker.next_step(0, 0)
    except NotImplementedError:
        pass
