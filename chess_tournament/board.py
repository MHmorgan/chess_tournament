
import PySimpleGUI as sg

from chess_tournament.errors import ChessError, InvalidMove
from chess_tournament.pieces import Piece, Empty, BlackBishop, BlackKing, BlackKnight, BlackPawn, BlackQueen, BlackRook, WhiteBishop, WhiteKing, WhiteKnight, WhitePawn, WhiteQueen, WhiteRook
from chess_tournament.moves import Move
from typing import List, Tuple

Matrix = List[List[Piece]]
Position = Tuple[int,int]

class Board:
    pieces: Matrix

    def __init__(self, pieces: Matrix):
        self.pieces = pieces


    @classmethod
    def default(cls) -> 'Board':
        return cls([
            [BlackRook(), BlackKnight(), BlackBishop(), BlackKing(), BlackQueen(), BlackBishop(), BlackKnight(), BlackRook()],
            [BlackPawn(),   BlackPawn(),   BlackPawn(), BlackPawn(),  BlackPawn(),   BlackPawn(),   BlackPawn(), BlackPawn()],
            [    Empty(),       Empty(),       Empty(),     Empty(),      Empty(),       Empty(),       Empty(),     Empty()],
            [    Empty(),       Empty(),       Empty(),     Empty(),      Empty(),       Empty(),       Empty(),     Empty()],
            [    Empty(),       Empty(),       Empty(),     Empty(),      Empty(),       Empty(),       Empty(),     Empty()],
            [    Empty(),       Empty(),       Empty(),     Empty(),      Empty(),       Empty(),       Empty(),     Empty()],
            [WhitePawn(),   WhitePawn(),   WhitePawn(), WhitePawn(),  WhitePawn(),   WhitePawn(),   WhitePawn(), WhitePawn()],
            [WhiteRook(), WhiteKnight(), WhiteBishop(), WhiteKing(), WhiteQueen(), WhiteBishop(), WhiteKnight(), WhiteRook()],
        ])


    def layout(self, renderer) -> list:

        # the main board display layout
        board_layout = [[sg.T('     ')] + [sg.T(f'{a}', pad=((23,27),0), font='Any 13') for a in 'abcdefgh']]

        # loop though board and create buttons with images
        for i in range(8):
            row = [sg.T(str(8-i)+'   ', font='Any 13')]
            for j in range(8):
                # piece_image = images[board[i][j]]
                piece_image = self.pieces[i][j].image_filename
                row.append(renderer(piece_image, key=(i,j), location=(i,j)))
            row.append(sg.T(str(8-i)+'   ', font='Any 13'))
            board_layout.append(row)

        # add the labels across bottom of board
        board_layout.append([sg.T('     ')] + [sg.T('{}'.format(a), pad=((23,27),0), font='Any 13') for a in 'abcdefgh'])

        return board_layout


    
    def at(self, p: Position) -> Piece:
        return self.pieces[p[1]][p[0]]


    def move(self, move: Move):
        # piece = self.at(p0)
        # if not piece.valid_move((p1[0] - p0[0], p1[1] - p0[1])):
        #     raise InvalidMove(piece, p0, p1)
        pass #TODO
