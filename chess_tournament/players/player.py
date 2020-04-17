
import asyncio
import threading

from abc import ABC, abstractmethod
from chess_tournament.board import Board
from chess_tournament.moves import Move
from typing import Callable, Optional


class Player(ABC):
    '''Base class for all AI players providing a common interface'''

    turn_thrd: threading.Thread
    next_move: Optional[Move] # Is None before first move

    def __init__(self, name: str, is_white: bool, initial_board: Board, time_remaining: Callable[[], int]):
        # TODO
        self.name = name
        self.is_white = is_white
        self.is_black = not is_white
        self.time_remaining = time_remaining
        self.next_move = None
        if is_white:
            self.start_turn(
                board=initial_board,
                last_move=None,
            )


    @abstractmethod
    def kill(self):
        '''Stop any processing done and threads owned by the player'''
        pass #TODO


    @abstractmethod
    def move(self, board: Board, last_move: Optional[Move]) -> Move:
        '''Perform the next move'''
        pass


    def start_turn(self, board: Board, last_move: Optional[Move]):
        def turn_thrd():
            self.next_move = self.move(board, last_move)

        thrd = threading.Thread(target=turn_thrd)
        thrd.start()
        self.turn_thrd = thrd


    def turn_done(self) -> bool:
        '''Return True if the player is done with their turn'''
        if self.turn_thrd is None:
            return False
        return not self.turn_thrd.is_alive()
