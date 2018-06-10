import copy


class GameState:
    """
    Considerations:
        - Board coordinates are situated at the top - left corner
        - Position structure is based on tuples (x: columns,y: rows)
        - Movements are numbered starting from: 'upwards' till: 'diagonal upwards - left', clockwise
    """

    def __init__(self, dim_x=3, dim_y=2):
        board = [[0] * dim_y for _ in range(dim_x)]
        board[dim_x - 1][dim_y - 1] = '/'
        self._board = board
        self._player_1_position = tuple()  # Player position marked by a 1 (int)
        self._player_2_position = tuple()  # Player position marked by a 2 (int)
        self._initiative = 1
        self._movements = dict([(1, (0, -1)), (2, (1, -1)), (3, (1, 0)), (4, (1, 1)), (5, (0, 1)), (6, (-1, 1)),
                                (7, (-1, 0)), (8, (-1, -1))])

    def forecast_move(self, move):
        """
        Return a new board object with the specified move applied to the current game state.
        :param move: position selected to go, by current player
        :type move: tuple (x,y)
        :return: a GameState object with the active player occupying the given move
        """
        future_board = copy.deepcopy(self)
        if self._initiative == 1:
            future_board._board[move[0]][move[1]] = 1
            future_board._player_1_position = move
            future_board._initiative = 2
        else:  # Second player moves
            future_board._board[move[0]][move[1]] = 2
            future_board._player_2_position = move
            future_board._initiative = 1
        return future_board

    def player_current_position(self) -> tuple:
        """
        Gives current position of player with initiative
        :return: tuple
        """
        if self._initiative == 1:
            return self._player_1_position
        else:
            return self._player_2_position

    def in_game_board(self, move: tuple) -> bool:
        """
        Given a move, indicates if it falls inside the game board
        :param move: indicates desired position to be occupied by player
        :type move: tuple(int,int)
        :return: bool
        """
        if move[0] < 0 or move[1] < 0:
            return False
        try:
            self._board[move[0]][move[1]]
        except:
            return False
        return True

    def free_position(self, move: tuple) -> bool:
        """
        Given a move, indicates if the position is available
        :param move: indicates desired position to be occupied by player
        :type move: tuple(int,int)
        :return: bool
        """
        return self._board[move[0]][move[1]] == 0

    def expand_movement_direction(self, movements, movement_restriction, relative_position):
        """
        Expands the movement of the player in a given direction up to the end of the board or collision with
        an occupied position
        :param movements: possible valid movements for the active player
        :type movements: list of move, tuple (x,y)
        :param movement_restriction: INTERNAL, do not modify. Restricts the direction of expansion
        :type movement_restriction: int, see movements (parameter)
        :param relative_position: INTERNAL, do not modify. Informs of the last valid position from the expansion
        :type relative_position: tuple (x,y)
        :return: list of moves, or False if none valid found
        """

        x_variation = self._movements[movement_restriction][0]
        y_variation = self._movements[movement_restriction][1]
        current_position = self.player_current_position()

        if relative_position:
            move = (relative_position[0] + x_variation, relative_position[1] + y_variation)
        else:
            move = (current_position[0] + x_variation, current_position[1] + y_variation)

        if self.in_game_board(move) and self.free_position(move):
            movements.append(move)
            further_movements = self.get_legal_moves(movement_restriction=movement_restriction,
                                                     relative_position=move)
            if further_movements:
                [movements.append(x) for x in further_movements]
            return movements
        else:
            return False

    def get_legal_moves(self, movement_restriction=0, relative_position=None):
        """
        Return a list of all legal moves available to the active player.
        :param movement_restriction: INTERNAL, do not modify. Restricts the direction of expansion
        :type movement_restriction: int, see movements (parameter)
        :param relative_position: INTERNAL, do not modify. Informs of the last valid position from the expansion
        :type relative_position: tuple (x,y)
        :return: list of moves
        """
        movements = []

        if movement_restriction == 0:  # If not restricted, initial movement, search in all directions
            # First move
            if self.player_current_position() == ():
                moves = [(pos_x, y) for pos_x, x in enumerate(self._board) for y in range(len(x)) if
                         self._board[pos_x][y] == 0]
                return moves
            # Other moves
            for movement in range(1, 9):
                self.expand_movement_direction(movements=movements, movement_restriction=movement,
                                               relative_position=relative_position)

        else:
            self.expand_movement_direction(movements=movements, movement_restriction=movement_restriction,
                                           relative_position=relative_position)

        return movements
