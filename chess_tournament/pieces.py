
from abc import ABC, abstractmethod
from typing import Tuple

# ------------------------------------------------------------------------------
# Piere base class

class Piece(ABC):
    '''Base class for all chess pieces'''
    # TODO Piece class

    def __init__(self):
        self.is_empty = False
        self.is_black = False
        self.is_white = False
        self.image_filename = ''

    @abstractmethod
    def valid_move(self, delta: Tuple[int, int]) -> bool:
        pass


################################################################################
#                                                                              #
#  Piece implementations
#                                                                              #
################################################################################

class Empty(Piece):
    # TODO Empty piece

    def __init__(self):
        super().__init__()
        self.is_empty = True
        self.image_filename = './resources/blank.png'

    def valid_move(self, delta: Tuple[int, int]):
        return False


class WhiteBishop(Piece):
    # TODO WhiteBishop piece

    def __init__(self):
        super().__init__()
        self.is_white = True
        self.image_filename = './resources/bishopw.png'

    def valid_move(self, delta: Tuple[int, int]):
        return abs(delta[0]) == abs(delta[1])


class BlackBishop(Piece):
    # TODO BlackBishop piece

    def __init__(self):
        super().__init__()
        self.is_black = True
        self.image_filename = './resources/bishopb.png'

    def valid_move(self, delta: Tuple[int, int]):
        return abs(delta[0]) == abs(delta[1])


class WhiteKing(Piece):
    # TODO WhiteKing piece

    def __init__(self):
        super().__init__()
        self.is_white = True
        self.image_filename = './resources/kingw.png'

    def valid_move(self, delta: Tuple[int, int]):
        return abs(delta[0]) <= 1 and abs(delta[1]) <= 1


class BlackKing(Piece):
    # TODO BlackKing piece

    def __init__(self):
        super().__init__()
        self.is_black = True
        self.image_filename = './resources/kingb.png'

    def valid_move(self, delta: Tuple[int, int]):
        return abs(delta[0]) <= 1 and abs(delta[1]) <= 1


class WhiteKnight(Piece):
    # TODO WhiteKnight piece

    def __init__(self):
        super().__init__()
        self.is_white = True
        self.image_filename = './resources/knightw.png'

    def valid_move(self, delta: Tuple[int, int]):
        return (abs(delta[0]) == 2 and abs(delta[1]) == 1) or \
               (abs(delta[0]) == 1 and abs(delta[1]) == 2)


class BlackKnight(Piece):
    # TODO BlackKnight piece

    def __init__(self):
        super().__init__()
        self.is_black = True
        self.image_filename = './resources/knightb.png'

    def valid_move(self, delta: Tuple[int, int]):
        return (abs(delta[0]) == 2 and abs(delta[1]) == 1) or \
               (abs(delta[0]) == 1 and abs(delta[1]) == 2)


class WhitePawn(Piece):
    # TODO WhitePawn piece

    def __init__(self):
        super().__init__()
        self.is_white = True
        self.image_filename = './resources/pawnw.png'

    def valid_move(self, delta: Tuple[int, int]):
        return delta[1] == 0 and delta[0] in (1,2)


class BlackPawn(Piece):
    # TODO BlackPawn piece

    def __init__(self):
        super().__init__()
        self.is_black = True
        self.image_filename = './resources/pawnb.png'

    def valid_move(self, delta: Tuple[int, int]):
        return delta[1] == 0 and delta[0] in (-1,-2)


class WhiteQueen(Piece):
    # TODO WhiteQueen piece

    def __init__(self):
        super().__init__()
        self.is_white = True
        self.image_filename = './resources/queenw.png'

    def valid_move(self, delta: Tuple[int, int]):
        return delta[0] == 0 or delta[1] == 0 or (abs(delta[0]) == abs(delta[1]))


class BlackQueen(Piece):
    # TODO BlackQueen piece

    def __init__(self):
        super().__init__()
        self.is_black = True
        self.image_filename = './resources/queenb.png'

    def valid_move(self, delta: Tuple[int, int]):
        return delta[0] == 0 or delta[1] == 0 or (abs(delta[0]) == abs(delta[1]))


class WhiteRook(Piece):
    # TODO WhiteRook piece

    def __init__(self):
        super().__init__()
        self.is_white = True
        self.image_filename = './resources/rookw.png'

    def valid_move(self, delta: Tuple[int, int]):
        return delta[0] == 0 or delta[1] == 0


class BlackRook(Piece):
    # TODO BlackRook piece

    def __init__(self):
        super().__init__()
        self.is_black = True
        self.image_filename = './resources/rookb.png'

    def valid_move(self, delta: Tuple[int, int]):
        return delta[0] == 0 or delta[1] == 0
