
class ChessError(Exception):
    pass


class InvalidMove(ChessError):
    '''Indicate an invalid move of a chess piece'''

    def __init__(self, piece, p0, p1):
        super().__init__()
        self.piece = piece
        self.p0 = p0
        self.p1 = p1

    def __str__(self) -> str:
        return f'cannot move {self.piece} from {self.p0} to {self.p1}'
