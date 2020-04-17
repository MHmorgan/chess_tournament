
import time

from chess_tournament.players import Player
from chess_tournament.moves import Move
from chess_tournament.board import Board
from typing import Optional

class Simpleton(Player):
    '''Simple chess AI'''

    def kill(self):
        '''Stop any processing done and threads owned by the player'''
        pass #TODO


    def move(self, board: Board, last_move: Optional[Move]) -> Move:
        '''Do a move'''
        print(f'{self.name} moving...')
        time.sleep(2.0)
        return None