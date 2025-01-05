"""
This module handles the words of the crossword puzzle.
Like loading the word, selecting orientation and pos.

__AUTHOR__ = "Kriti Bhatnagar" and "Anand Maurya"
"""

from pickle import load
from typing import Literal
from os.path import join
from random import choice, randrange
from math import sqrt


"""
All the methods are anonymous and in a class
to avoid assigning and 
calling each function for all the 3 difficulties.
"""


class Words:
    def __init__(
        self, difficulty: Literal["Easy", "Medium", "Hard"], grid_size: int
    ) -> None:
        """
        This initializes words for a particular difficulty.

        @param: difficulty : Literal["Easy", "Medium", "Hard"]
            The difficulty of the words.
        """
        self.words = self.__get_words(difficulty)
        self.words = self.__select_orientation(self.words)
        self.final_words = self.__select_pos(self.words, grid_size)

    def __get_words(self, difficulty: Literal["Easy", "Medium", "Hard"]) -> list[str]:
        """
        This gets the words based on the difficulty given.

        @param: difficulty : Literal["Easy", "Medium", "Hard"]
            The difficulty of words to get.

        @returns: list[str]
            The list of the words of the particular difficulty.
        """
        words_path = join("Assets", "WordData.dat")
        with open(words_path, "rb") as words:
            words = load(words)
            return words[difficulty]

    def __select_orientation(self, word_list: list[str]) -> dict[str, str]:
        """
        This selects the orientation for each word in a word list.

        @param: word_list : list[str]
            The list of the words.

        @returns: dict[str, str]
            The dict of the word mapped with its orientation.
        """
        # ? Here:
        # ? HL: Horizontal staring from left.
        # ? HR: Horizontal starting from right.
        # ? VU: Vertical starting from up.
        # ? VD: Vertical staring from down.
        ORIENTATIONS = [
            "HL",
            "HR",
            "VU",
            "VD",
        ]
        return {word: choice(ORIENTATIONS) for word in word_list}

    def __select_random_pos(
        self, orientation: str, grid_dimension: int, word_len: int
    ) -> list[tuple[int, int]]:
        """
        This selects the random position for a word.

        @param: orientation : str
            The orientation of the word.
        @param: grid_dimension : int
            The no of squares in 1 row/col.
            Assuming the grid is square.
        @param: word_len : int
            The len of the word for which the pos is to be made.

        @returns: list[tuple[int, int]]
            The list of all the positions.
        """
        positions = []
        if orientation[0] == "H":  # Horizontal placement
            y_pos = randrange(grid_dimension)
            x_pos = randrange(grid_dimension - word_len + 1)
            positions = [(x_pos + i, y_pos) for i in range(word_len)]
        elif orientation[0] == "V":  # Vertical placement
            x_pos = randrange(grid_dimension)
            y_pos = randrange(grid_dimension - word_len + 1)
            positions = [(x_pos, y_pos + i) for i in range(word_len)]
        return positions

    def __select_pos(
        self, word_list: dict[str, str], grid_square_number: int
    ) -> dict[tuple[str, str], list[tuple[int, int]]]:
        """
        Assigns positions on the grid for each word based on its orientation.

        @param: word_list : dict[str, str]
            Dictionary mapping each word to its orientation ("H" for horizontal, "V" for vertical).
        @param: grid_size: int
            Total number of squares in the grid.

        @returns: dict[tuple[str, str], list[tuple[int, int]]]
            Dictionary mapping each (word, orientation) pair to a list of positions (x, y) on the grid.
        """
        pos_dict = {}
        grid_dimension = int(sqrt(grid_square_number))
        # ? Track occupied positions on the grid
        occupied_positions = set()
        for word, orientation in word_list.items():
            word_len = len(word)
            pos = []
            positions = self.__select_random_pos(orientation, grid_dimension, word_len)
            # ? Check for overlap and ensure unique positions
            while any(pos in occupied_positions for pos in positions):
                positions = self.__select_random_pos(
                    orientation, grid_dimension, word_len
                )
            occupied_positions.update(positions)
            pos.extend(positions)
            pos_dict[(word, orientation)] = pos
        return pos_dict
