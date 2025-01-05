"""
This is the main game entry file for the game.
This file contains the main gameloop and functions
that help initialize the module classes.

__AUTHOR__ = "Kriti Bhatnagar" and "Anand Maurya"
"""

import pygame

from sys import exit, path
from os import listdir
from os.path import join, isfile
from typing import Literal
from math import ceil, sqrt

import pygame.macosx
from WordHandler import Words
from random import choice


pygame.init()


SCREEN_SIZE = 1200, 800
window = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Crossword")


def convert_mouse_pos_to_grid(
    mouse_pos: tuple[int, int], block_size: tuple[int, int]
) -> tuple[int, int]:
    """
    This converts the mouse click to a grid_pos.

    @param: mouse_pos : tuple[int, int]
        The position of the mouse click.
    @param: block_size : tuple[int, int]
        The size of an individual grid square.

    @returns: tuple[int, int]
        The grid coords of the mouse.
    """
    x_pos = (mouse_pos[0] - mouse_pos[0] % block_size[0]) // block_size[0]
    y_pos = (mouse_pos[1] - mouse_pos[1] % block_size[1]) // block_size[1]
    return x_pos, y_pos


def load_alphabets(block_size: tuple[int, int]) -> dict[str, pygame.Surface]:
    """
    This loads all the alphabet tiles from the Assets\\Alphabets directory.

    @param: block_size : tuple[int, int]
        The size of an individual alphabet tile.

    @returns: dict[str, pygame.Surface]
        The alphabet character mapped to its image tile.
    """
    alphabets_path = join("Assets", "Alphabets")
    letters = [
        char.removesuffix(".png")
        for char in listdir(alphabets_path)
        if isfile(join(alphabets_path, char))
    ]
    return {
        name: pygame.transform.scale(
            pygame.image.load(join(alphabets_path, name + ".png")).convert_alpha(),
            block_size,
        )
        for name in letters
    }


def fill_grid(func):

    def wrapper(
        alphabets: dict[str, pygame.Surface],
        word_data: dict[tuple[str, str], list[tuple[int, int]]],
        block_size: tuple[int, int],
        grid_square_number: int,
    ) -> list[tuple[pygame.Surface, tuple[int, int]]]:
        """
        This updates the grid to fill all the empty squares with random letters.

        @param: alphabets : dict[str, pygame.Surface]
            The letter of the word mapped to its image.
        @param: word_data : dict[tuple[str, str], list[tuple[int, int]]]
            The tuple of the word, its orientation mapped to the pos of its letters.
        @param: block_size : tuple[int, int]
            The size of the individual grid square.
        @param: grid_square_number : int
            The number of squares in the grid

        @returns: list[tuple[pygame.Surface, tuple[int, int]]]
            The list of all the alphabet surfaces and their pos.
        """
        original_result = func(alphabets, word_data, block_size)
        grid_dimension = int(sqrt(grid_square_number))
        letters = "A B C D E F G H I J K L M N O P Q R S U V W X Y Z"
        letters = letters.split(" ")
        for i in range(grid_dimension):
            for j in range(grid_dimension):
                pos = i * block_size[0], j * block_size[1]
                if any(pos == data[1] for data in original_result):
                    continue
                random_alphabet = choice(letters)
                original_result.append((alphabets[random_alphabet], pos))
        return original_result

    return wrapper


@fill_grid
def get_word_data(
    alphabets: dict[str, pygame.Surface],
    word_data: dict[tuple[str, str], list[tuple[int, int]]],
    block_size: tuple[int, int],
) -> list[tuple[pygame.Surface, tuple[int, int]]]:
    """
    This gets the data of the words to be displayed.

    @param: alphabets : dict[str, pygame.Surface]
        The letter of the word mapped to its image.
    @param: word_data : dict[tuple[str, str], list[tuple[int, int]]]
        The tuple of the word, its orientation mapped to the pos of its letters.

    @returns: list[tuple[pygame.Surface, tuple[int, int]]]
        The list of the tuple of the alphabet image mapped to its pos in pixels.
    """
    surface_list = []
    for (word, orientation), pos_list in word_data.items():
        if orientation[1] in "RD":
            word = word[::-1]
        for i, pos in enumerate(pos_list):
            char_surface = alphabets[word[i]]
            surface_list.append(
                (char_surface, (pos[0] * block_size[0], pos[1] * block_size[1]))
            )
    return surface_list


def bg_assets_loader(
    screen_size: tuple[int, int]
) -> dict[pygame.Surface, tuple[int, int]]:
    """
    This loads all the bg elements on the screen.

    @param: screen_size : tuple[int, int]
        The size of the screen that hosts the game.

    @returns: dict[pygame.Surface, tuple[int, int]]
        The surface that is to be displayed mapped to its position.
    """
    BG_IMAGE = join("Assets", "BgImage.png")
    bg_image = pygame.image.load(BG_IMAGE).convert()
    bg_image = pygame.transform.scale(bg_image, screen_size)

    BG_WORD_LIST_PATH = join("Assets", "BgWordList.png")
    BG_WORD_LIST_SIZE = screen_size[0], 200
    bg_word_list = pygame.image.load(BG_WORD_LIST_PATH).convert()
    bg_word_list = pygame.transform.scale(bg_word_list, BG_WORD_LIST_SIZE)

    assets_dict = {bg_image: (0, 0), bg_word_list: (0, 600)}
    return assets_dict


def get_grid_pos(
    block_size: tuple[int, int],
    grid_size: tuple[int, int],
    grid_offset: tuple[int, int] = (0, 0),
) -> list[tuple[int, int]]:
    """
    This gets all the pos that the grid squares need to go to.

    @param: block_size : tuple[int, int]
        The size of an individual block of the grid.
    @param: grid_size : tuple[int, int]
        The size of the complete grid.
    @param: grid_offset : tuple[int, int]
        The place where the grid has to be placed.
        This can be used to move the grid on the board.

    @returns: list[tuple[int, int]]
        The list of all the pos of the grid blocks.
    """
    return [
        (
            (i * block_size[0] + grid_offset[0]) // block_size[0],
            (j * block_size[1] + grid_offset[1]) // block_size[1],
        )
        for i in range(ceil(grid_size[0] // block_size[0]))
        for j in range(ceil(grid_size[1] // block_size[0]))
    ]


def draw(
    screen: pygame.Surface,
    assets_data: dict[pygame.Surface, tuple[int, int]],
    grid_data: dict[tuple[int, int], list[tuple[int, int]]],
    block_size: tuple[int, int],
    alphabet_data: list[tuple[pygame.Surface, tuple[int, int]]],
    words: dict[tuple[str, str], tuple[int, int]],
    alphabet_tiles: dict[str, pygame.Surface],
) -> None:
    GRAY = (75, 75, 75)
    for image, pos in assets_data.items():
        screen.blit(image, pos)
    for size, pos_list in grid_data.items():
        for pos in pos_list:
            # ? This converts the square index of the square pos to the position in pixels.
            rect = pygame.Rect((pos[0] * block_size[0], pos[1] * block_size[1]), size)
            # ? This draws the border of the grid from the rect.
            pygame.draw.rect(screen, GRAY, rect, 1)
    screen.blits(alphabet_data)
    char_pos = (0, 650)
    for (word, _), pos in words.items():
        word = " " + word
        for char in word:
            if char == " ":
                char_pos = char_pos[0] + block_size[0] - 15, char_pos[1]
                continue
            screen.blit(
                pygame.transform.scale(alphabet_tiles[char], (35, 35)),
                (char_pos[0], char_pos[1]),
            )
            char_pos = char_pos[0] + block_size[0] - 15, char_pos[1]
            if char_pos[0] > 1100:
                char_pos = 35, char_pos[1] + 75
    pygame.display.update()


def main(screen: pygame.Surface) -> None:
    """
    This is the main gameloop of the game.

    @param: screen : pygame.Surface
        The screen that hosts the game.
    """
    screen_size = screen.get_size()

    grid_size = 600, 600
    block_size = 50, 50
    grid_pos = get_grid_pos(block_size, grid_size)
    grid_data = {block_size: grid_pos}

    timer = pygame.time.Clock()
    fps = 60

    assets_data = bg_assets_loader(screen_size)
    alphabet_tiles = load_alphabets(block_size)
    difficulty = "Medium"
    words = Words(difficulty, len(grid_pos)).final_words
    alphabet_data = get_word_data(
        alphabet_tiles,
        words,
        block_size,
        len(grid_pos),
    )

    running = True
    mouse_drag_pos = []
    drag_event = False
    while running:
        timer.tick(fps)
        if not drag_event:
            mouse_drag_pos = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # ? This tells when the user starts/stops selecting the squares
            if event.type == pygame.MOUSEBUTTONDOWN:
                drag_event = True
            elif event.type == pygame.MOUSEBUTTONUP:
                drag_event = False
        # ? This records all the position where the mouse is selecting.
        if drag_event:
            mouse_grid_pos = convert_mouse_pos_to_grid(
                pygame.mouse.get_pos(), block_size
            )
            if mouse_grid_pos not in mouse_drag_pos:
                mouse_drag_pos.append(mouse_grid_pos)
            # ? This helps us check for if a valid word is selected.
            mouse_drag_pos.sort()
        # There will a short window where drag event is false but mouse_drag_pos is not empty. We need to check for the word there.
        if not drag_event and mouse_drag_pos:
            if any(mouse_drag_pos == word_data for word_data in words.values()):
                words = {
                    word_data: pos
                    for word_data, pos in words.items()
                    if pos != mouse_drag_pos
                }
                for mouse_pos in mouse_drag_pos:
                    for i, (_, pos) in enumerate(alphabet_data):
                        if mouse_pos == (
                            pos[0] // block_size[0],
                            pos[1] // block_size[1],
                        ):
                            alphabet_data.pop(i)
        if not words:
            print("Congrats")
        draw(screen, assets_data, grid_data, block_size, alphabet_data, words, alphabet_tiles)  # type: ignore
    pygame.quit()
    exit()


if __name__ == "__main__":
    main(window)
