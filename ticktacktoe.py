#!/usr/bin/python

import itertools
import re
import sys

class Painter(object):
    def __init__(self, board):
        self.board = board
        pass

    def __call__(self):
        self.paint_board()

    def paint_board(self):
        print '\n    A | B | C'
        print '  ------------'
        for i, r in enumerate(self.board.data):
            print '%s | %s | %s | %s' % (i+1, r[0] or ' ', r[1] or ' ', r[2] or ' ')
            print '  |---|---|---'


class Prompter(object):
    def __init__(self):
        pass

    def get_input(self, player):
        return raw_input('\n%s, enter square: ' % player.name)

    def validate_input(self, val):
        # Should be in the format A1
        rgx = re.compile('([Aa|Bb|Cc])([123])')
        match = re.match(rgx, val)
        if not match:
            return None
        col, row = match.groups()
        cols = ['A','B','C']
        return cols.index(col.upper()), int(row) - 1

    def prompt(self, player):
        resp = self.get_input(player)
        resp = self.validate_input(resp)
        while resp is None:
            resp = self.get_input(player)
            resp = self.validate_input(resp)
        return resp

class Board(object):
    def __init__(self):
        self.data = None

    def reset(self):
        self.data = []
        for i in range(3):
            self.data.append([None, None, None])

    def set_cell(self, col, row, token):
        self.data[row][col] = token

    def find_winner(self):
        # search horizontally
        for row in self.data:
            res = set(row)
            if len(res) == 1 and None not in res:
                return res.pop()

        # search vertically
        for i in range(3):
            res = set([x[i] for x in self.data])
            if len(res) == 1 and None not in res:
                return res.pop()

        #diagonally
        lr = []
        rl = []
        for i in range(3):
           lr.append(self.data[i][i])
           rl.append(self.data[i][-i-1])
        if len(set(lr)) == 1 and None not in lr:
            return lr.pop()
        if len(set(rl)) == 1 and None not in rl:
            return rl.pop()

        return None


class Player(object):
    def __init__(self, name, token):
        self.name = name
        self.token = token

def winner_name_from_token(players, token):
    for player in players:
        if player.token == token:
            return player.name

def main():
    board = Board()
    board.reset()
    paint = Painter(board)
    prompter = Prompter()
    paint()

    players = itertools.cycle([
        Player('Evsobabso', 'X'),
        Player('Daddy', 'O'),
        ])

    while True:
        player = players.next()
        col, row = prompter.prompt(player)
        board.set_cell(col, row, player.token)
        paint()
        winner_token = board.find_winner()
        if winner_token:
            print '%s wins!' % winner_name_from_token(players, winner_token)
            break


if __name__ == '__main__':
    main()

# TODO:  need to check that we are not setting a cell that is already set
# TODO:  need to check when the board is full and there is no winner
# TODO:  need to provide user input for name and token
# TODO:  need to provide a nice welome title and message
# TODO:  make nice pretty winner announcement
