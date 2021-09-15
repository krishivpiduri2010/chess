import pygame

SQUARE_SIZE = 100
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


class Board:
    def __init__(self):
        self.images = {}
        self._load_imgs()
        self._make_board()

    def _load_imgs(self):
        for color in ['black', 'white']:
            for piece in ['rook', 'knight', 'bishop', 'king', 'queen', 'pawn']:
                self.images[color[0] + (piece[0] if piece != 'knight' else 'n')] = (
                    pygame.transform.scale(pygame.image.load('images/' + color + '_' + piece + '.png'), (100, 100)))

    def _make_board(self):
        self.board = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr'],
        ]

    def reset(self):
        self._make_board()

    def move(self, current_pos: [tuple[float], list[float], set[float]], new_pos: [type, list, set]):
        current_x, current_y = current_pos
        new_x, new_y = new_pos
        self.board[new_y][new_x] = self.board[current_y][current_x]
        self.board[current_y][current_x] = '--'

    def draw(self, win: pygame.Surface):
        for x in range(8):
            for y in range(8):
                if self.board[y][x] != '--':
                    win.blit(self.images[self.board[y][x]], (x * SQUARE_SIZE, y * SQUARE_SIZE))
                if y % 2 == 0:
                    if not x % 2 == 0:
                        pygame.draw.rect(win, (255, 255, 255),
                                         (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                        if self.board[y][x] != '--':
                            win.blit(self.images[self.board[y][x]], (x * SQUARE_SIZE, y * SQUARE_SIZE))

                else:
                    if x % 2 == 0:
                        pygame.draw.rect(win, (255, 255, 255),
                                         (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    if self.board[y][x] != '--':
                        win.blit(self.images[self.board[y][x]], (x * SQUARE_SIZE, y * SQUARE_SIZE))


BOARD = Board()


def draw(win: pygame.Surface):
    win.fill((128, 128, 128))
    BOARD.draw(win)
    pygame.display.update()


def main():
    selected_pos = []
    white_moves = True
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_pos = list(map(lambda x: x // 100, list(pygame.mouse.get_pos())))
                if len(selected_pos) == 2:
                    if white_moves:
                        if BOARD.board[selected_pos[1]][selected_pos[0]][0] == 'w':
                            print(BOARD.board[selected_pos[1]][selected_pos[0]][1])

                            # PAWN MOVEMENT CHECKING
                            if BOARD.board[selected_pos[1]][selected_pos[0]][1] == 'p':
                                if selected_pos[1] - 1 == clicked_pos[1]:
                                    if selected_pos[0] == clicked_pos[0]:
                                        BOARD.move(selected_pos, clicked_pos)
                                        white_moves = not white_moves
                                    else:
                                        if (selected_pos[0] + 1 == clicked_pos[0] or selected_pos[0] - 1 ==
                                            clicked_pos[0]) and selected_pos[1] - 1 == clicked_pos[1]:
                                            BOARD.move(selected_pos, clicked_pos)
                                            white_moves = not white_moves
                                else:
                                    if selected_pos[1] == 6:
                                        if selected_pos[1] - 2 == clicked_pos[1] and selected_pos[0] == \
                                                clicked_pos[0] and BOARD.board[clicked_pos[1]][clicked_pos[0]] \
                                                == '--':
                                            BOARD.move(selected_pos, clicked_pos)
                                            white_moves = not white_moves
                            # ROOK MOVEMENT CHECKING
                            elif BOARD.board[selected_pos[1]][selected_pos[0]][1] == 'r':
                                if (selected_pos[1] == clicked_pos[1]) and selected_pos != clicked_pos:
                                    print(selected_pos[0], clicked_pos[0])
                                    column = BOARD.board[selected_pos[1]]
                                    pieces = column[
                                             selected_pos[0]:clicked_pos[0]:1 if selected_pos[0] < clicked_pos[
                                                 0] else -1]
                                    print(pieces)
                                    pieces.pop(0)
                                    if all(ele == '--' for ele in pieces):
                                        BOARD.move(selected_pos, clicked_pos)
                                        white_moves = not white_moves
                                if selected_pos[0] == clicked_pos[0]:
                                    print(selected_pos[1], clicked_pos[1])
                                    column = []
                                    for row in BOARD.board:
                                        column.append(row[clicked_pos[0]])
                                    pieces = column[selected_pos[1]:clicked_pos[1]:1 if selected_pos[1] < clicked_pos[
                                        1] else -1]
                                    print(pieces)
                                    pieces.pop(0)
                                    print(pieces)
                                    try:
                                        pieces.pop(-1)
                                    except IndexError:
                                        pass
                                    print(pieces)
                                    if all(ele == '--' for ele in pieces):
                                        BOARD.move(selected_pos, clicked_pos)
                                        white_moves = not white_moves
                            # KING MOVEMENT
                            elif BOARD.board[selected_pos[1]][selected_pos[0]][1] == 'k':
                                for i in range(2):
                                    if abs(selected_pos[i] - clicked_pos[i]) != 1 and selected_pos[i] - clicked_pos[
                                        i] != 0:
                                        break
                                else:
                                    BOARD.move(selected_pos, clicked_pos)
                                    white_moves = not white_moves
                            # KNIGHT MOVEMENT
                            elif BOARD.board[selected_pos[1]][selected_pos[0]][1] == 'n':
                                print(abs(selected_pos[0] - clicked_pos[0]), abs(selected_pos[1] - clicked_pos[1]))
                                if (abs(selected_pos[0] - clicked_pos[0]) == 1 or abs(
                                        selected_pos[0] - clicked_pos[0]) == 2) and (
                                        abs(selected_pos[1] - clicked_pos[1]) == 1 or abs(
                                    selected_pos[1] - clicked_pos[1]) == 2):
                                    BOARD.move(selected_pos, clicked_pos)
                                    white_moves = not white_moves
                            else:
                                BOARD.move(selected_pos, clicked_pos)
                                white_moves = not white_moves

                    else:
                        if BOARD.board[selected_pos[1]][selected_pos[0]][0] == 'b':
                            print(BOARD.board[selected_pos[1]][selected_pos[0]][1])

                            # PAWN MOVEMENT CHECKING
                            if BOARD.board[selected_pos[1]][selected_pos[0]][1] == 'p':
                                if selected_pos[1] + 1 == clicked_pos[1] and selected_pos[0] == clicked_pos[0] \
                                        and BOARD.board[clicked_pos[1]][clicked_pos[0]] == '--':
                                    BOARD.move(selected_pos, clicked_pos)
                                    white_moves = not white_moves
                                else:
                                    if selected_pos[0] == clicked_pos[0]:
                                        if selected_pos[1] + 2 == clicked_pos[1] and selected_pos[0] == clicked_pos[
                                            0] and BOARD.board[clicked_pos[1]][clicked_pos[0]] == '--':
                                            BOARD.move(selected_pos, clicked_pos)
                                            white_moves = not white_moves
                                    else:
                                        if (selected_pos[0] + 1 == clicked_pos[0] or selected_pos[0] - 1 ==
                                            clicked_pos[0]) and selected_pos[1] + 1 == clicked_pos[1]:
                                            BOARD.move(selected_pos, clicked_pos)
                                            white_moves = not white_moves
                            # ROOK MOVEMENT
                            elif BOARD.board[selected_pos[1]][selected_pos[0]][1] == 'r':
                                if (selected_pos[1] == clicked_pos[1]) and selected_pos != clicked_pos:
                                    print(selected_pos[0], clicked_pos[0])
                                    column = BOARD.board[selected_pos[1]]
                                    pieces = column[
                                             selected_pos[0]:clicked_pos[0]:1 if selected_pos[0] < clicked_pos[
                                                 0] else -1]
                                    print(pieces)
                                    pieces.pop(0)
                                    if all(ele == '--' for ele in pieces):
                                        BOARD.move(selected_pos, clicked_pos)
                                        white_moves = not white_moves
                                if selected_pos[0] == clicked_pos[0]:
                                    print(selected_pos[1], clicked_pos[1])
                                    column = []
                                    for row in BOARD.board:
                                        column.append(row[clicked_pos[0]])
                                    pieces = column[
                                             selected_pos[1]:clicked_pos[1]:1 if selected_pos[1] < clicked_pos[
                                                 1] else -1]
                                    print(pieces)
                                    pieces.pop(0)
                                    print(pieces)
                                    try:
                                        pieces.pop(-1)
                                    except IndexError:
                                        pass
                                    print(pieces)
                                    if all(ele == '--' for ele in pieces):
                                        BOARD.move(selected_pos, clicked_pos)
                                        white_moves = not white_moves
                            # KING MOVEMENT
                            elif BOARD.board[selected_pos[1]][selected_pos[0]][1] == 'k':
                                for i in range(2):
                                    if abs(selected_pos[i] - clicked_pos[i]) != 1 and selected_pos[i] - clicked_pos[
                                        i] != 0:
                                        break
                                else:
                                    BOARD.move(selected_pos, clicked_pos)
                                    white_moves = not white_moves
                            # KNIGHT MOVEMENT
                            elif BOARD.board[selected_pos[1]][selected_pos[0]][1] == 'n':
                                print(abs(selected_pos[0] - clicked_pos[0]), abs(selected_pos[1] - clicked_pos[1]))
                                if (abs(selected_pos[0] - clicked_pos[0]) == 1 or abs(
                                        selected_pos[0] - clicked_pos[0]) == 3) and (
                                        abs(selected_pos[1] - clicked_pos[1]) == 1 or abs(
                                    selected_pos[1] - clicked_pos[1]) == 3):
                                    BOARD.move(selected_pos, clicked_pos)
                                    white_moves = not white_moves
                            else:
                                BOARD.move(selected_pos, clicked_pos)
                                white_moves = not white_moves

                    selected_pos = []
                else:
                    selected_pos = clicked_pos
                print(white_moves)

        draw(WIN)
    pygame.quit()


if __name__ == '__main__':
    main()
