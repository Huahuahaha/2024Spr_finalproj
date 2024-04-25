import re
import copy
import random

EMPTY = '　'
WALL = '##'
DEPTH = 4


class Piece():
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __str__(self):
        if self.color == 'R':
            return '\033[31m' + self.name + '\033[0m'
        else:
            return self.name


class Gamestate():
    def __init__(self):
        self.board = [
            [WALL, WALL, Piece(u'車', 'B'), Piece(u'馬', 'B'), Piece(u'象', 'B'), Piece(u'士', 'B'), Piece(u'将', 'B'),
             Piece(u'士', 'B'), Piece(u'象', 'B'), Piece(u'馬', 'B'), Piece(u'車', 'B'), WALL, WALL],
            [WALL, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL],
            [WALL, WALL, EMPTY, Piece(u'砲', 'B'), EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, Piece(u'砲', 'B'), EMPTY, WALL,
             WALL],
            [WALL, WALL, Piece(u'卒', 'B'), EMPTY, Piece(u'卒', 'B'), EMPTY, Piece(u'卒', 'B'), EMPTY,
             Piece(u'卒', 'B'), EMPTY, Piece(u'卒', 'B'), WALL, WALL],
            [Piece(u'「', 'B'), Piece(u'巨', 'B'), EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
             Piece(u'「', 'R'), Piece(u'巨', 'R')],
            [Piece(u'将', 'B'), Piece(u'」', 'B'), EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
             Piece(u'帅', 'R'), Piece(u'」', 'R')],
            # [WALL, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL],
            # [WALL, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL],
            [WALL, WALL, Piece(u'兵', 'R'), EMPTY, Piece(u'兵', 'R'), EMPTY, Piece(u'兵', 'R'), EMPTY,
             Piece(u'兵', 'R'), EMPTY, Piece(u'兵', 'R'), WALL, WALL],
            [WALL, WALL, EMPTY, Piece(u'炮', 'R'), EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, Piece(u'炮', 'R'), EMPTY, WALL,
             WALL],
            [WALL, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL],
            [WALL, WALL, Piece(u'俥', 'R'), Piece(u'傌', 'R'), Piece(u'相', 'R'), Piece(u'仕', 'R'), Piece(u'帅', 'R'),
             Piece(u'仕', 'R'), Piece(u'相', 'R'), Piece(u'傌', 'R'), Piece(u'俥', 'R'), WALL, WALL],
        ]
        self.redMove = True
        self.history = []

    def is_valid_move(self, start, end):
        return True

    def are_you_winner(self):
        pos1 = [(0, 5), (0, 6), (0, 7), (1, 5), (1, 6),
                (1, 7), (2, 5), (2, 6), (2, 7)]
        pos2 = [(9, 5), (9, 6), (9, 7), (8, 5), (8, 6),
                (8, 7), (7, 5), (7, 6), (7, 7)]
        hasJiang = False
        for pos in pos1:
            if self.board[pos[0]][pos[1]] != EMPTY and self.board[pos[0]][pos[1]].name == u'将':
                if (self.board[pos[0]][pos[1] + 1] != EMPTY and self.board[pos[0]][pos[1] + 1].name == u'」'):
                    pass
                else:
                    hasJiang = True
                    break
        if not hasJiang:
            return True

        hasShuai = False
        for pos in pos2:
            if self.board[pos[0]][pos[1]] != EMPTY and self.board[pos[0]][pos[1]].name == u'帅':
                if (self.board[pos[0]][pos[1] + 1] != EMPTY and self.board[pos[0]][pos[1] + 1].name == u'」'):
                    pass
                else:
                    hasShuai = True
                    break
        if not hasShuai:
            return False

        return None

    def move(self, start, end):
        current = copy.deepcopy(self.board)
        self.history.append(current)
        start_piece = self.board[start[0]][start[1]]
        end_piece = self.board[end[0]][end[1]]

        start_is_jujiang = False
        end_is_jujiang = False
        end_jujiang_pos = None
        if start_piece.name == u'「':
            start_is_jujiang = True
        if end_piece not in [EMPTY, WALL] and end_piece.color != start_piece.color:
            if end_piece.name == u'「':
                end_is_jujiang = True
                end_jujiang_pos = end
            elif end_piece.name == u'巨':
                end_is_jujiang = True
                end_jujiang_pos = (end[0], end[1] - 1)
            elif end_piece.name == u'」':
                end_is_jujiang = True
                end_jujiang_pos = (end[0] - 1, end[1] - 1)
            elif end_piece.name in [u'将', u'帅'] and (
                    self.board[end[0]][end[1] + 1] not in [EMPTY, WALL] and self.board[end[0]][
                end[1] + 1].name == u'」'):
                end_is_jujiang = True
                end_jujiang_pos = (end[0] - 1, end[1])

        if not start_is_jujiang and not end_is_jujiang:
            self.board[start[0]][start[1]] = EMPTY
            self.board[end[0]][end[1]] = start_piece
        elif start_is_jujiang and end_is_jujiang:
            temp = (
            self.board[start[0]][start[1]], self.board[start[0]][start[1] + 1], self.board[start[0] + 1][start[1]],
            self.board[start[0] + 1][start[1] + 1])
            self.board[end_jujiang_pos[0]][end_jujiang_pos[1]] = EMPTY
            self.board[end_jujiang_pos[0] + 1][end_jujiang_pos[1]] = EMPTY
            self.board[end_jujiang_pos[0]][end_jujiang_pos[1] + 1] = EMPTY
            self.board[end_jujiang_pos[0] + 1][end_jujiang_pos[1] + 1] = EMPTY
            self.board[start[0]][start[1]] = EMPTY
            self.board[start[0]][start[1] + 1] = EMPTY
            self.board[start[0] + 1][start[1]] = EMPTY
            self.board[start[0] + 1][start[1] + 1] = EMPTY
            self.board[end[0]][end[1]] = temp[0]
            self.board[end[0]][end[1] + 1] = temp[1]
            self.board[end[0] + 1][end[1]] = temp[2]
            self.board[end[0] + 1][end[1] + 1] = temp[3]
        elif start_is_jujiang:
            temp = (
            self.board[start[0]][start[1]], self.board[start[0]][start[1] + 1], self.board[start[0] + 1][start[1]],
            self.board[start[0] + 1][start[1] + 1])
            self.board[start[0]][start[1]] = EMPTY
            self.board[start[0]][start[1] + 1] = EMPTY
            self.board[start[0] + 1][start[1]] = EMPTY
            self.board[start[0] + 1][start[1] + 1] = EMPTY
            self.board[end[0]][end[1]] = temp[0]
            self.board[end[0]][end[1] + 1] = temp[1]
            self.board[end[0] + 1][end[1]] = temp[2]
            self.board[end[0] + 1][end[1] + 1] = temp[3]
        elif end_is_jujiang:
            self.board[end_jujiang_pos[0]][end_jujiang_pos[1]] = EMPTY
            self.board[end_jujiang_pos[0] + 1][end_jujiang_pos[1]] = EMPTY
            self.board[end_jujiang_pos[0]][end_jujiang_pos[1] + 1] = EMPTY
            self.board[end_jujiang_pos[0] + 1][end_jujiang_pos[1] + 1] = EMPTY
            self.board[start[0]][start[1]] = EMPTY
            self.board[end[0]][end[1]] = start_piece

        self.redMove = not self.redMove

    def unmove(self):
        if self.history:
            self.board = self.history.pop()
            self.redMove = not self.redMove

    def get_all_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] in [EMPTY, WALL]:
                    continue
                if self.redMove and self.board[r][c].color == 'B':
                    continue
                elif not self.redMove and self.board[r][c].color == 'R':
                    continue

                if self.board[r][c].name in [u'車', u'俥']:
                    moves.extend(self.get_ju_move((r, c)))
                elif self.board[r][c].name in [u'馬', u'傌']:
                    moves.extend(self.get_ma_move((r, c)))
                elif self.board[r][c].name in [u'象', u'相']:
                    moves.extend(self.get_xiang_move((r, c)))
                elif self.board[r][c].name in [u'士', u'仕']:
                    moves.extend(self.get_shi_move((r, c)))
                elif self.board[r][c].name in [u'将', u'帅'] and (
                        self.board[r][c + 1] not in [EMPTY, WALL] and self.board[r][c + 1].name != u'」'):
                    moves.extend(self.get_jiang_move((r, c)))
                elif self.board[r][c].name in [u'砲', u'炮']:
                    moves.extend(self.get_pao_move((r, c)))
                elif self.board[r][c].name in [u'卒', u'兵']:
                    moves.extend(self.get_zu_move((r, c)))
                elif self.board[r][c].name in [u'「']:
                    moves.extend(self.get_jujiang_move((r, c)))
        random.shuffle(moves)
        return moves

    def get_ju_move(self, start):
        ''' Ma, 車 or 俥, is chinese rook.
        Rules like the chess rook.
        '''
        moves = []
        i = 1
        end = (start[0] - i, start[1])
        while end[0] >= 0:
            if self.board[end[0]][end[1]] == EMPTY:
                moves.append((start, end))
            elif self.board[end[0]][end[1]] == WALL:
                break
            elif self.board[end[0]][end[1]].color != self.board[start[0]][start[1]].color:
                moves.append((start, end))
                break
            else:
                break
            i += 1
            end = (start[0] - i, start[1])

        i = 1
        end = (start[0], start[1] - i)
        while end[1] >= 0:
            if self.board[end[0]][end[1]] == EMPTY:
                moves.append((start, end))
            elif self.board[end[0]][end[1]] == WALL:
                break
            elif self.board[end[0]][end[1]].color != self.board[start[0]][start[1]].color:
                moves.append((start, end))
                break
            else:
                break
            i += 1
            end = (start[0], start[1] - i)

        i = 1
        end = (start[0] + i, start[1])
        while end[0] < len(self.board):
            if self.board[end[0]][end[1]] == EMPTY:
                moves.append((start, end))
            elif self.board[end[0]][end[1]] == WALL:
                break
            elif self.board[end[0]][end[1]].color != self.board[start[0]][start[1]].color:
                moves.append((start, end))
                break
            else:
                break
            i += 1
            end = (start[0] + i, start[1])

        i = 1
        end = (start[0], start[1] + i)
        while end[1] < len(self.board[start[0]]):
            if self.board[end[0]][end[1]] == EMPTY:
                moves.append((start, end))
            elif self.board[end[0]][end[1]] == WALL:
                break
            elif self.board[end[0]][end[1]].color != self.board[start[0]][start[1]].color:
                moves.append((start, end))
                break
            else:
                break
            i += 1
            end = (start[0], start[1] + i)
        return moves

    def get_ma_move(self, start):
        ''' Ma, 馬 or 傌, is chinese horse.
        Rules like the chess horse.
        Except some piece may block the horse leg.
        '''
        moves = []
        offset = [(-1, -2, 0, -1), (-2, -1, -1, 0), (1, -2, 0, -1), (-2, 1, -1, 0), (1, 2, 0, 1), (2, 1, 1, 0),
                  (-1, 2, 0, 1), (2, -1, 1, 0)]
        for off in offset:
            end = (start[0] + off[0], start[1] + off[1])
            if end[0] >= 0 and end[0] < len(self.board) and end[1] >= 0 and end[1] < len(self.board[0]):
                if self.board[start[0] + off[2]][start[1] + off[3]] != EMPTY:  # blocked leg
                    continue
                if self.board[end[0]][end[1]] == EMPTY:
                    moves.append((start, end))
                elif self.board[end[0]][end[1]] == WALL:
                    continue
                elif self.board[end[0]][end[1]].color != self.board[start[0]][start[1]].color:
                    moves.append((start, end))
                else:
                    continue
        return moves

    def get_xiang_move(self, start):
        ''' Xiang, 象 or 相, is chinese bishop.

        '''
        moves = []
        pos1 = [(0, 4), (0, 8), (2, 2), (2, 6), (2, 10), (4, 4), (4, 8)]
        pos2 = [(9, 4), (9, 8), (7, 2), (7, 6), (7, 10), (5, 4), (5, 8)]
        end_pos = list(pos1)
        end_pos.extend(pos2)
        for end in end_pos:
            if (start in pos1 and end in pos1) or (start in pos2 and end in pos2):
                if abs(end[0] - start[0]) == 2 and abs(end[1] - start[1]) == 2:
                    if self.board[(start[0] + end[0]) // 2][(start[1] + end[1]) // 2] != EMPTY:  # blocked leg
                        continue
                    if self.board[end[0]][end[1]] == EMPTY:
                        moves.append((start, end))
                    elif self.board[end[0]][end[1]] == WALL:
                        continue
                    elif self.board[end[0]][end[1]].color != self.board[start[0]][start[1]].color:
                        moves.append((start, end))
                    else:
                        continue
        return moves

    def get_shi_move(self, start):
        ''' Shi, 士 or 仕.

        '''
        moves = []
        pos1 = [(0, 5), (0, 7), (1, 6), (2, 5), (2, 7)]
        pos2 = [(9, 5), (9, 7), (8, 6), (7, 5), (7, 7)]
        end_pos = list(pos1)
        end_pos.extend(pos2)
        for end in end_pos:
            if (start in pos1 and end in pos1) or (start in pos2 and end in pos2):
                if abs(end[0] - start[0]) == 1 and abs(end[1] - start[1]) == 1:
                    if self.board[end[0]][end[1]] == EMPTY:
                        moves.append((start, end))
                    elif self.board[end[0]][end[1]] == WALL:
                        continue
                    elif self.board[end[0]][end[1]].color != self.board[start[0]][start[1]].color:
                        moves.append((start, end))
                    else:
                        continue
        return moves

    def get_jiang_move(self, start):
        ''' Jiang, 将 or 帅.

        '''
        moves = []
        pos1 = [(0, 5), (0, 6), (0, 7), (1, 5), (1, 6),
                (1, 7), (2, 5), (2, 6), (2, 7)]
        pos2 = [(9, 5), (9, 6), (9, 7), (8, 5), (8, 6),
                (8, 7), (7, 5), (7, 6), (7, 7)]
        end_pos = list(pos1)
        end_pos.extend(pos2)
        for end in end_pos:
            if (start in pos1 and end in pos1) or (start in pos2 and end in pos2):
                if abs(end[0] - start[0]) in [0, 1] and abs(end[1] - start[1]) in [0, 1] and (
                        abs(end[0] - start[0]) + abs(end[1] - start[1]) == 1):
                    if self.board[end[0]][end[1]] == EMPTY:
                        moves.append((start, end))
                    elif self.board[end[0]][end[1]] == WALL:
                        continue
                    elif self.board[end[0]][end[1]].color != self.board[start[0]][start[1]].color:
                        moves.append((start, end))
                    else:
                        continue
        return moves

    def get_pao_move(self, start):
        ''' Pao 砲 or 炮'.

        '''
        moves = []
        i = 1
        can_capture = False
        end = (start[0] - i, start[1])
        while end[0] >= 0:
            if self.board[end[0]][end[1]] == EMPTY:
                if not can_capture:
                    moves.append((start, end))
            elif self.board[end[0]][end[1]] == WALL:
                break
            else:
                if not can_capture:
                    can_capture = True
                    if self.board[end[0]][end[1]].name in [u'「', u'巨', u'」']:
                        i += 1
                    elif self.board[end[0]][end[1]].name in [u'将', u'帅'] and (
                            self.board[end[0]][end[1] + 1] not in [EMPTY, WALL] and self.board[end[0]][
                        end[1] + 1].name == u'」'):
                        i += 1
                elif self.board[end[0]][end[1]].color != self.board[start[0]][start[1]].color:
                    moves.append((start, end))
                    break
                else:
                    break
            i += 1
            end = (start[0] - i, start[1])

        i = 1
        can_capture = False
        end = (start[0], start[1] - i)
        while end[1] >= 0:
            if self.board[end[0]][end[1]] == EMPTY:
                if not can_capture:
                    moves.append((start, end))
            elif self.board[end[0]][end[1]] == WALL:
                break
            else:
                if not can_capture:
                    can_capture = True
                    if self.board[end[0]][end[1]].name in [u'「', u'巨', u'」']:
                        i += 1
                    elif self.board[end[0]][end[1]].name in [u'将', u'帅'] and (
                            self.board[end[0]][end[1] + 1] not in [EMPTY, WALL] and self.board[end[0]][
                        end[1] + 1].name == u'」'):
                        i += 1
                elif self.board[end[0]][end[1]].color != self.board[start[0]][start[1]].color:
                    moves.append((start, end))
                    break
                else:
                    break
            i += 1
            end = (start[0], start[1] - i)

        i = 1
        can_capture = False
        end = (start[0] + i, start[1])
        while end[0] < len(self.board):
            if self.board[end[0]][end[1]] == EMPTY:
                if not can_capture:
                    moves.append((start, end))
            elif self.board[end[0]][end[1]] == WALL:
                break
            else:
                if not can_capture:
                    can_capture = True
                    if self.board[end[0]][end[1]].name in [u'「', u'巨', u'」']:
                        i += 1
                    elif self.board[end[0]][end[1]].name in [u'将', u'帅'] and (
                            self.board[end[0]][end[1] + 1] not in [EMPTY, WALL] and self.board[end[0]][
                        end[1] + 1].name == u'」'):
                        i += 1
                elif self.board[end[0]][end[1]].color != self.board[start[0]][start[1]].color:
                    moves.append((start, end))
                    break
                else:
                    break
            i += 1
            end = (start[0] + i, start[1])

        i = 1
        can_capture = False
        end = (start[0], start[1] + i)
        while end[1] < len(self.board[start[0]]):
            if self.board[end[0]][end[1]] == EMPTY:
                if not can_capture:
                    moves.append((start, end))
            elif self.board[end[0]][end[1]] == WALL:
                break
            else:
                if not can_capture:
                    can_capture = True
                    if self.board[end[0]][end[1]].name in [u'「', u'巨', u'」']:
                        i += 1
                    elif self.board[end[0]][end[1]].name in [u'将', u'帅'] and (
                            self.board[end[0]][end[1] + 1] not in [EMPTY, WALL] and self.board[end[0]][
                        end[1] + 1].name == u'」'):
                        i += 1
                elif self.board[end[0]][end[1]].color != self.board[start[0]][start[1]].color:
                    moves.append((start, end))
                    break
                else:
                    break
            i += 1
            end = (start[0], start[1] + i)
        return moves

    def get_zu_move(self, start):
        ''' Zu 卒 or 兵.
        '''
        moves = []
        ends = []
        if self.board[start[0]][start[1]].name == u'卒':
            ends.append((start[0] + 1, start[1]))
            if start[0] >= 5:
                ends.append((start[0], start[1] - 1))
                ends.append((start[0], start[1] + 1))
        else:
            ends.append((start[0] - 1, start[1]))
            if start[0] <= 4:
                ends.append((start[0], start[1] - 1))
                ends.append((start[0], start[1] + 1))
        for end in ends:
            if self.board[end[0]][end[1]] == EMPTY:
                moves.append((start, end))
            elif self.board[end[0]][end[1]] == WALL:
                continue
            elif self.board[end[0]][end[1]].color != self.board[start[0]][start[1]].color:
                moves.append((start, end))
            else:
                continue
        return moves

    def get_jujiang_move(self, start):
        ''' JuJiang 巨将 or 巨帅.
        '''
        moves = []
        offset = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for off in offset:
            end = (start[0] + off[0], start[1] + off[1])
            pieces = [end, (end[0] + 1, end[1]), (end[0], end[1] + 1), (end[0] + 1, end[1] + 1)]
            valid = True
            for piece in pieces:
                if piece[0] >= 0 and piece[0] < len(self.board) and piece[1] >= 0 and piece[1] < len(self.board[0]):
                    if self.board[piece[0]][piece[1]] == EMPTY:
                        continue
                    elif self.board[piece[0]][piece[1]] == WALL:
                        valid = False
                        break
                    elif self.board[piece[0]][piece[1]].color != self.board[start[0]][start[1]].color:
                        continue
                    elif piece not in pieces:
                        valid = False
                        break
                else:
                    valid = False
                    break
            if valid:
                moves.append((start, end))
        return moves

    def __str__(self):
        s = '\n'
        for r in range(len(self.board)):
            s += str(r)
            for c in range(len(self.board[r])):
                s += ' ' + str(self.board[r][c])
            s += '\n'
        for c in range(len(self.board[0])):
            if c < 11:
                s += EMPTY + str(c)
            else:
                s += ' ' + str(c)
        return s + '\n'


def get_start_location(game):
    while True:
        line = input('Please input [row column] of your piece: ')
        fields = re.split('\s+', line)
        if len(fields) == 2:
            try:
                r = int(fields[0])
                c = int(fields[1])
                return (r, c)
            except:
                pass
        print('Invalid location. Try again!')


def get_end_location(game):
    while True:
        line = input('Please input [row column] to put your piece: ')
        fields = re.split('\s+', line)
        if len(fields) == 2:
            try:
                r = int(fields[0])
                c = int(fields[1])
                if r >= 0 and r <= 9 and c >= 0 and c <= 12 and game.board[r][c] not in [WALL]:
                    return (r, c)
            except:
                pass
        print('Invalid location. Try again!')


def calculate(game):
    score = 0
    total_piece = 0
    for r in range(len(game.board)):
        for c in range(len(game.board[r])):
            if game.board[r][c] in [EMPTY, WALL]:
                continue
            total_piece += 1

    for r in range(len(game.board)):
        for c in range(len(game.board[r])):
            if game.board[r][c] in [EMPTY, WALL]:
                continue
            sign = 1
            if game.board[r][c].color == 'B':
                sign = -1

            if game.board[r][c].name in [u'車', u'俥']:
                score += 9 * sign
            elif game.board[r][c].name in [u'馬', u'傌']:
                if total_piece >= 17:
                    score += 4 * sign
                else:
                    score += 5 * sign
            elif game.board[r][c].name in [u'象', u'相']:
                score += 2 * sign
            elif game.board[r][c].name in [u'士', u'仕']:
                score += 2 * sign
            elif game.board[r][c].name in [u'将', u'帅']:
                score += 100 * sign
            elif game.board[r][c].name in [u'砲', u'炮']:
                score += 4.5 * sign
            elif game.board[r][c].name in [u'卒', u'兵']:
                if game.board[r][c].name == u'卒':
                    if r >= 5:
                        score += 2 * sign
                    else:
                        score += 1 * sign
                else:
                    if r <= 4:
                        score += 2 * sign
                    else:
                        score += 1 * sign
            elif game.board[r][c].name in [u'巨']:
                score += 14 * sign
    return score


def max(game, depth, alpha, beta):
    if depth == 0:
        score = calculate(game)
        return score, None
    moves = game.get_all_moves()
    candidate_move = None
    candidate_score = None
    for move in moves:
        game.move(move[0], move[1])
        score, _ = min(game, depth - 1, alpha, beta)
        game.unmove()
        if candidate_move == None or score > candidate_score:
            candidate_move = move
            candidate_score = score
        if score >= beta:
            return candidate_score, candidate_move
        elif score > alpha:
            alpha = score
    return candidate_score, candidate_move


def min(game, depth, alpha, beta):
    if depth == 0:
        score = calculate(game)
        return score, None
    moves = game.get_all_moves()
    candidate_move = None
    candidate_score = None
    for move in moves:
        game.move(move[0], move[1])
        score, _ = max(game, depth - 1, alpha, beta)
        game.unmove()
        if candidate_move == None or score < candidate_score:
            candidate_move = move
            candidate_score = score
        if score <= alpha:
            return candidate_score, candidate_move
        elif score < beta:
            beta = score
    return candidate_score, candidate_move


def alpha_beta_algo(game, depth):
    _, move = min(game, depth, -100, 100)
    return move


if __name__ == '__main__':
    while True:
        print('Welcome to the Chinese Chess!')
        print('1. Player vs AI')
        print('2. Player vs Player')
        ai = input('Please select: ')
        if ai == '1' or ai == '2':
            break

    game = Gamestate()
    while True:
        print(game)
        winner = game.are_you_winner()
        if winner != None:
            if winner == True:
                print('You win!')
            else:
                print('You lose!')
            break
        print('--------------- Red Turn ---------------')
        start = get_start_location(game)
        end = get_end_location(game)
        while (start, end) not in game.get_all_moves():
            print('Invalid move. Try again!')
            start = get_start_location(game)
            end = get_end_location(game)
        game.move(start, end)

        print(game)
        winner = game.are_you_winner()
        if winner != None:
            if winner == True:
                print('You win!')
            else:
                print('You lose!')
            break
        if ai == '1':
            move = alpha_beta_algo(game, DEPTH)
            game.move(move[0], move[1])
        else:
            print('-------------- Black Turn --------------')
            start = get_start_location(game)
            end = get_end_location(game)
            while (start, end) not in game.get_all_moves():
                print('Invalid move. Try again!')
                start = get_start_location(game)
                end = get_end_location(game)
            game.move(start, end)