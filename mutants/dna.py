import abc
from typing import List, Tuple


class BaseChecker(metaclass=abc.ABCMeta):
    """Base class for checking for repeated sequences of letters in a string.
    """
    @staticmethod
    @abc.abstractmethod
    def has_enough_length(y_index: int, x_index: int, max_starting_point: int) -> bool:
        """Checks if there are enough elements to form a full sequence

        :param y_index: Horizontal position
        :param x_index: Vertical position
        :param max_starting_point: Farthest position where a search can be initiated
        :return: True if there are enough elements to form a full sequence. False otherwise.
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def next_step(y_index: int, x_index: int) -> Tuple[int, int]:
        """Takes current y/x position and calculates next search step

        :param y_index: Horizontal position
        :param x_index: Vertical position
        :return: y/x position for the next search step
        """
        raise NotImplementedError


class HorizontalChecker(BaseChecker):
    """Subclass for searching horizontal sequences.
    """
    @staticmethod
    def has_enough_length(y_index: int, x_index: int, max_starting_point: int) -> bool:
        return x_index <= max_starting_point

    @staticmethod
    def next_step(y_index: int, x_index: int) -> Tuple[int, int]:
        return y_index + 0, x_index + 1


class VerticalChecker(BaseChecker):
    """Subclass for searching vertical sequences.
    """
    @staticmethod
    def has_enough_length(y_index: int, x_index: int, max_starting_point: int) -> bool:
        return y_index <= max_starting_point

    @staticmethod
    def next_step(y_index: int, x_index: int) -> Tuple[int, int]:
        return y_index + 1, x_index + 0


class DiagonalChecker(BaseChecker):
    """Subclass for searching diagonal sequences
    """
    @staticmethod
    def has_enough_length(y_index: int, x_index: int, max_starting_point: int) -> bool:
        return x_index <= max_starting_point and y_index <= max_starting_point

    @staticmethod
    def next_step(y_index: int, x_index: int) -> Tuple[int, int]:
        return y_index + 1, x_index + 1


def identify(dna: List) -> bool:
    """Looks up for sequences of repeated letters in a DNA string.

    New search methods can be added by creating a corresponding class
    and registering such method in 'search_methods' variable.

    :param dna: Matrix consisting of a list of strings.
    :return: True if DNA string is verified as mutant's. False otherwise.
    """

    matrix_size = len(dna)
    mutant_sequence_length = 4
    max_starting_point = matrix_size - mutant_sequence_length
    # letters_checked = 0
    mutant_sequences_required = 2
    mutant_sequences_found = 0
    search_methods = (HorizontalChecker, VerticalChecker, DiagonalChecker)
    verified_starting_points = {}

    for y_index, sequence in enumerate(dna):
        # Quits as soon as required number of sequences is found
        if mutant_sequences_found >= mutant_sequences_required:
            break
        for x_index, starting_letter in enumerate(sequence):
            # letters_checked += 1

            for search_method in search_methods:
                # Quits as soon as required number of sequences is found
                if mutant_sequences_found >= mutant_sequences_required:
                    break

                # Avoids taking starting points for previously mapped sequences
                # Otherwise, the following string would result in 2 sequences found: 'A A A A A T' (0 to 3 and 1 to 4)
                # Using a dict has the advantage of keeping time complexity in O(1) when compared to a list/tuple
                if verified_starting_points.get(f'{y_index}{x_index}'):
                    continue

                # Only starts a new search if there's enough length in a string
                if search_method.has_enough_length(y_index, x_index, max_starting_point):
                    adjancency_length = 1
                    next_y_index, next_x_index = y_index, x_index

                    while True:
                        next_y_index, next_x_index = search_method.next_step(next_y_index, next_x_index)

                        # letters_checked += 1
                        if dna[next_y_index][next_x_index] != starting_letter:
                            break
                        else:
                            verified_starting_points[f'{next_y_index}{next_x_index}'] = 1
                            adjancency_length += 1

                        # print(f'{search_method.__name__} adjancency of length [{adjancency_length}] '
                        #       f'found for [{starting_letter}] at [{next_y_index}][{next_x_index}]')
                        if adjancency_length >= mutant_sequence_length:
                            mutant_sequences_found += 1
                            break

    # print(f"letters checked: {letters_checked}")
    return True if mutant_sequences_found >= mutant_sequences_required else False
