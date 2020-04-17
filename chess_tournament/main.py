# Copyright 2020, Magnus Hirth. All rights reserved

import argparse
import PySimpleGUI as sg
import threading
import time

from .board import Board
from .players import players, Player
from datetime import datetime
from typing import List, Optional

# ------------------------------------------------------------------------------
# UI texts

start_game_txt = 'Start game!'
end_game_txt = 'End game'
exit_txt = 'Exit'
black_name = 'Barack Obama'
white_name = 'Donald Trump'

# Game type lengths in seconds
game_types = {
    'Flash (10 sec)' :       10,
    'Bullet (1 min)' :   1 * 60,
    'Blitz (5 min)'  :   5 * 60,
    'Rapid (15 min)' :  15 * 60,
    'Long (120 min)' : 120 * 60,
}

# Start board layouts
start_boards = {
    'Normal' : Board.default,
}

# Bonus times to be added after a move
time_bonuses = [1, 5, 10, 0]

# ------------------------------------------------------------------------------


def render_square(image, key, location):
    '''Render a chess square, setting appropriate background color'''
    if (location[0] + location[1]) % 2:
        color =  '#B58863'
    else:
        color = '#F0D9B5'
    return sg.RButton('', image_filename=image, size=(1, 1), button_color=('white', color), pad=(0, 0), key=key)


################################################################################
#                                                                              #
#  Game state
#                                                                              #
################################################################################

class GameState:

    started: datetime
    started_ns: int
    board: Board
    cur_player: int
    game_lock: threading.Lock
    ended: False

    # Player instances, 0-White 1-Black
    players: List[Player]

    # Player times, 0-White 1-Black
    times: List[int]
    time_bonus: int
    time_thread: threading.Thread

    def __init__(self, white_player, black_player, game_length: int, initial_board: Board,
                 time_bonus: int = 10):
        '''Create and start a new game, specifying game length (per player) in seconds'''
        self.started = datetime.now()
        self.started_ns = time.time_ns()
        self.game_lock = threading.Lock()
        self.board = initial_board
        self.ended = False

        # Players
        self.players = [
            white_player(white_name, is_white=True, initial_board=initial_board, time_remaining=lambda: self.times[0]),
            black_player(black_name, is_white=False, initial_board=initial_board, time_remaining=lambda: self.times[1])
        ]
        self.cur_player = 0

        # Time counting
        self.times = [game_length]*2
        self.time_bonus = time_bonus
        self.start_countdown()


    def end(self):
        '''End the game'''
        self.ended = True


    def check(self) -> bool:
        '''Check the state of the game, returning True of it the game requires
        an update of the board.
        '''
        # TODO implement move waiting with threading.Event
        with self.game_lock:
            done = self.players[self.cur_player].turn_done()
        return done or 0 in self.times


    def update(self) -> bool:
        '''Perform updates of the board, returning True of the game is finished
        after the update is performed, either by timeout or checkmate
        '''

        # Handle timeout
        if 0 in self.times:
            return True

        cp = self.cur_player
        np = cp ^ 1
        player = self.players[cp]

        # Perform move
        move = player.next_move
        # if move is None:
        #     raise ValueError(f'invalid move value: {move} (by {player.name})')
        self.board.move(move)

        # Add bonus time
        self.times[cp] += self.time_bonus

        # Start next players turn
        np = self.cur_player ^ 1
        self.players[np].start_turn(
            board=self.board,
            last_move=move,
        )
        self.cur_player = np


    # --------------------------------------------------------------------------
    # Time

    def start_countdown(self):
        '''Start countdown thread'''

        # TODO rewrite with threading.Timer

        def counter():

            # Store last diff to find amount to reduce player time
            last = 0

            while not self.ended:
                # Don't be too active
                time.sleep(0.1)

                # Count down using difference from game start
                diff = (time.time_ns() - self.started_ns) // 1_000_000_000
                # print(f'{last=}, {diff=}')

                if diff > last:

                    with self.game_lock:
                        val = self.times[self.cur_player] - (diff - last)
                        if val < 0:
                            val = 0
                        self.times[self.cur_player] = val

                    last = diff

        thrd = threading.Thread(target=counter, name='counter_thread')
        thrd.start()
        self.time_thread = thrd

    def white_time(self) -> str:
        '''Get string representation of remaining play time for white player'''
        with self.game_lock:
            time = self.times[0]
        m, s = divmod(time, 60)
        return f'{m:02}:{s:02}'

    def black_time(self) -> str:
        '''Get string representation of remaining play time for black player'''
        with self.game_lock:
            time = self.times[1]
        m, s = divmod(time, 60)
        return f'{m:02}:{s:02}'


################################################################################
#                                                                              #
#  Game flow
#                                                                              #
################################################################################

def run(*args, **kwargs):

    # Top menu line
    menu_def = [
        ['File', ['Foo', exit_txt ]],
        ['Help', 'About...'],
    ]

    player_names = list(players.keys())
    type_names = list(game_types.keys())
    start_board_names = list(start_boards.keys())

    # Game controls
    board_controls = [
        [sg.Text('The artificial chess tournament!', pad=(1, 5), font=('', 20))],
        [sg.Text('AI players personality:')],
        [sg.Drop(player_names, default_value=player_names[0], key='BLACK_PLAYER'), sg.Text('Black')],
        [sg.Drop(player_names, default_value=player_names[0], key='WHITE_PLAYER'), sg.Text('White')],
        [sg.Text('Game type (duration):')],
        [sg.Drop(type_names, default_value=type_names[0], key='GAME_TYPE'), sg.Text('+'), sg.Drop(time_bonuses, default_value=time_bonuses[0], key='TIME_BONUS'), sg.Text('bonus seconds')],
        [sg.Text('Start board layout:')],
        [sg.Drop(start_board_names, default_value=start_board_names[0], key='START_BOARD')],
        [sg.RButton(start_game_txt, pad=((5, 5), (10, 0))), sg.RButton(end_game_txt, pad=((5, 5), (10, 0)))],
        [sg.Text('\u2015'*32)],
        [sg.Text(f'Time {black_name}:'), sg.Text(f'-           ', key='BLACK_TIME')],
        [sg.Text(f'Time {white_name}:'), sg.Text(f'-           ', key='WHITE_TIME')],
    ]

    # Setup board
    board = Board.default()
    board_layout = board.layout(renderer=render_square)

    # Main layout of application window
    layout = [
        [sg.Menu(menu_def, tearoff=False)],
        [sg.Column(board_layout, key='BOARD_LAYOUT'), sg.Column(board_controls)],
    ]

    window = sg.Window(
        'Chess',
        default_button_element_size=(12,1),
        auto_size_buttons=False,
        icon='resources/kingb.ico',
        resizable=True,
    ).Layout(layout)


    # --------------------------------------------------------------------------
    # Loop taking in user input
    game = None

    while True:
        button, value = window.Read(timeout=100)

        if button in (None, exit_txt):
            break  # Quit program

        # Game running handling
        if game is not None:
            done = False

            # Update game times
            window['BLACK_TIME'].update(game.black_time())
            window['WHITE_TIME'].update(game.white_time())
            # Check of game should be updated
            if game.check():
                done = game.update()
                window['BOARD_LAYOUT'].update(game.board.layout(renderer=render_square))

            # Handle end game
            if done or button == end_game_txt:
                game.end()
                game = None
                sg.popup('Game finished!')

        # Out-of-game handling
        else:

            # Run game
            if button == start_game_txt:

                # Get and verify game parameters
                white = value['WHITE_PLAYER']
                black = value['BLACK_PLAYER']
                game_type = value['GAME_TYPE']
                start_board = value['START_BOARD']
                try:
                    time_bonus = int(value['TIME_BONUS'])
                except ValueError:
                    time_bonus = None

                if white not in players or \
                   black not in players or \
                   game_type not in game_types or \
                   start_board not in start_boards or \
                   time_bonus is None:
                    # Informative popup error message
                    txt = 'Some game parameters have invalid values'
                    if white not in players: txt += f'\n  - Unknown white player "{white}"'
                    if black not in players: txt += f'\n  - Unknown black player "{black}"'
                    if game_type not in game_types: txt += f'\n  - Unknown game type "{game_type}"'
                    if start_board not in start_boards: txt += f'\n  - Unknown start board "{start_board}"'
                    if time_bonus is None: txt += f'\n  - Invalid time bonus value "{value["TIME_BONUS"]}"'
                    sg.popup(txt, title='Bad game parameter(s)')

                # Start new game
                else:
                    game = GameState(
                        white_player=players[white],
                        black_player=players[black],
                        game_length=game_types[game_type],
                        initial_board=start_boards[start_board](),
                        time_bonus=time_bonus,
                    )

    if game is not None:
        game.end()
    print('Goodbye')
