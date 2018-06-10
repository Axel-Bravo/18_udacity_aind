
def terminal_test(gameState):
    """ Return True if the game is over for the active player
    and False otherwise.
    """
    if gameState.get_legal_moves() == []:
        return  True
    else:
        return False


def min_value(gameState):
    """ Return the value for a win (+1) if the game is over,
    otherwise return the minimum value over all legal child
    nodes.
    """
    if terminal_test(gameState=gameState):
        return 1
    else:
       return min([max_value(gameState.forecast_move(legal_move)) for legal_move in gameState.get_legal_moves()])


def max_value(gameState):
    """ Return the value for a loss (-1) if the game is over,
    otherwise return the maximum value over all legal child
    nodes.
    """
    if terminal_test(gameState=gameState):
        return -1
    else:
       return max([min_value(gameState.forecast_move(legal_move)) for legal_move in gameState.get_legal_moves()])