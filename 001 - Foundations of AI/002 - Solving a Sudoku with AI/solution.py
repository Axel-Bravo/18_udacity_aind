from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_desc_units = [sum([cross(rows[i], cols[i]) for i in range(0, 9)], [])]
diagonal_asc_units = [sum([cross(rows[8 - i], cols[i]) for i in range(0, 9)], [])]
unitlist = row_units + column_units + square_units + diagonal_desc_units + diagonal_asc_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

letter_translator = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8}


def remove_from_line(values, candidate, candidate_twin):
    """
    Remove twin_pair values from all of their peers
    :param values: with the form {'box_name': '123456789', ...}
    :type values: dict
    :param candidate: candidate position
    :type candidate: str
    :param candidate_twin: candidate_twin position
    :type candidate_twin: str
    :return: values
    """
    if [x for x in square_units if candidate in x and candidate_twin in x]:  # Square elimination
        elements_aligned = set([x for x in square_units if candidate in x][0]) - {candidate} - {candidate_twin}
    elif candidate[0] == candidate_twin[0]:  # Row elimination
        elements_aligned = set(row_units[letter_translator[candidate[0]]]) - {candidate} - {candidate_twin}
    elif candidate[1] == candidate_twin[1]:  # Column elimination
        elements_aligned = set(column_units[int(candidate[1]) - 1]) - {candidate} - {candidate_twin}
    elif (letter_translator[candidate[0]] + 1 == int(candidate[1])) and \
            (letter_translator[candidate_twin[0]] + 1 == int(candidate_twin[1])):  # Diagonal descending elimination
        elements_aligned = set(diagonal_desc_units) - {candidate} - {candidate_twin}
    elif (letter_translator[candidate[0]] + 1 + int(candidate[1]) == 10) and \
            (letter_translator[candidate_twin[0]] + 1 + int(candidate_twin[1]) == 10):  # Diagonal ascending elimination
        elements_aligned = set(diagonal_asc_units) - {candidate} - {candidate_twin}
    else:  # Dummy case
        elements_aligned = []

    for element_aligned in elements_aligned:
        values[element_aligned] = values[element_aligned].replace(values[candidate][0], '')
        values[element_aligned] = values[element_aligned].replace(values[candidate][1], '')

    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    candidates = [x for x in values if len(values[x]) == 2]
    candidates_comparable = set(candidates)

    for candidate in candidates:
        candidate_twins = [x for x in peers[candidate] if x in (candidates_comparable - {candidate})]
        if candidate_twins:
            for candidate_twin in candidate_twins:
                if values[candidate] == values[candidate_twin]:
                    values = remove_from_line(values=values, candidate=candidate, candidate_twin=candidate_twin)
        candidates_comparable.remove(candidate)
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    for box in values:
        if len(values[box]) == 1:
            for peer in peers[box]:
                values[peer] = values[peer].replace(values[box], '')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in '123456789':
            digit_position = [box for box in unit if digit in values[box]]
            if len(digit_position) == 1:
                values[digit_position[0]] = digit
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Your code here: Use the Only Choice Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    # Return if arrived to end condition
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    _, candidate = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recursion to solve each one of the resulting Sudokus, and if one returns a value (not False),
    # return that answer!
    for case in values[candidate]:
        values_case = values.copy()
        values_case[candidate] = case
        attempt = search(values_case)
        if attempt:
            return attempt
    return False


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku

        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
