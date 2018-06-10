import json
import copy

import numpy as np  # contains helpful math functions like numpy.exp()
import numpy.random as random  # see numpy.random module
# import random  # alternative to numpy.random module

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from  traveling_salesman_problem import *

"""Read input data and define helper functions for visualization."""

# Map services and data available from U.S. Geological Survey, National Geospatial Program.
# Please go to http://www.usgs.gov/visual-id/credit_usgs.html for further information
map = mpimg.imread("map.png")  # US States & Capitals map

# List of 30 US state capitals and corresponding coordinates on the map
with open('capitals.json', 'r') as capitals_file:
    capitals = json.load(capitals_file)
capitals_list = list(capitals.items())


def show_path(path, starting_city, w=12, h=8):
    """Plot a TSP path overlaid on a map of the US States & their capitals."""
    x, y = list(zip(*path))
    _, (x0, y0) = starting_city
    plt.imshow(map)
    plt.plot(x0, y0, 'y*', markersize=15)  # y* = yellow star for starting point
    plt.plot(x + x[:1], y + y[:1])  # include the starting point at the end of path
    plt.axis("off")
    fig = plt.gcf()
    fig.set_size_inches([w, h])


def simulated_annealing(problem, schedule):
    """The simulated annealing algorithm, a version of stochastic hill climbing
    where some downhill moves are allowed. Downhill moves are accepted readily
    early in the annealing schedule and then less often as time goes on. The
    schedule input determines the value of the temperature T as a function of
    time. [Norvig, AIMA Chapter 3]

    Parameters
    ----------
    problem : Problem
        An optimization problem, already initialized to a random starting state.
        The Problem class interface must implement a callable method
        "successors()" which returns states in the neighborhood of the current
        state, and a callable function "get_value()" which returns a fitness
        score for the state. (See the `TravelingSalesmanProblem` class below
        for details.)

    schedule : callable
        A function mapping time to "temperature". "Time" is equivalent in this
        case to the number of loop iterations.

    Returns
    -------
    Problem
        An approximate solution state of the optimization problem

    Notes
    -----
        (1) DO NOT include the MAKE-NODE line from the AIMA pseudocode

        (2) Modify the termination condition to return when the temperature
        falls below some reasonable minimum value (e.g., 1e-10) rather than
        testing for exact equality to zero

    See Also
    --------
    AIMA simulated_annealing() pseudocode
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Simulated-Annealing.md
    """
    current_value = problem.get_value()
    for time in range(1, int(1e100)):
        temperature = schedule(time)
        if temperature <= 1e-10:
            return problem
        next = random.choice(problem.successors())
        next_value = next.get_value()
        delta_e = next_value - current_value
        if delta_e >= 0:
            current_value = next_value
            problem = next
        else:
            success_probab = np.exp(delta_e / temperature)
            if random.choice([1, 0], p=[success_probab, 1 - success_probab]):
                current_value = next_value
                problem = next

# These are presented as globals so that the signature of schedule()
# matches what is shown in the AIMA textbook; you could alternatively
# define them within the schedule function, use a closure to limit
# their scope, or define an object if you would prefer not to use
# global variables
alpha = 0.95
temperature=1e4


def schedule(time):
    return ((alpha**time)*temperature)


if __name__ == '__main__':
    # Construct an instance of the TravelingSalesmanProblem
    test_cities = [('DC', (11, 1)), ('SF', (0, 0)), ('PHX', (2, -3)), ('LA', (0, -4))]
    tsp = TravelingSalesmanProblem(test_cities)
    assert (tsp.path == test_cities)

    # Test the successors() method -- no output means the test passed
    successor_paths = [x.path for x in tsp.successors()]
    assert (all(x in [[('LA', (0, -4)), ('SF', (0, 0)), ('PHX', (2, -3)), ('DC', (11, 1))],
                      [('SF', (0, 0)), ('DC', (11, 1)), ('PHX', (2, -3)), ('LA', (0, -4))],
                      [('DC', (11, 1)), ('PHX', (2, -3)), ('SF', (0, 0)), ('LA', (0, -4))],
                      [('DC', (11, 1)), ('SF', (0, 0)), ('LA', (0, -4)), ('PHX', (2, -3))]]
                for x in successor_paths))

    # test the schedule() function -- no output means that the tests passed
    assert (np.allclose(alpha, 0.95, atol=1e-3))
    assert (np.allclose(schedule(0), temperature, atol=1e-3))
    assert (np.allclose(schedule(10), 5987.3694, atol=1e-3))

    # Failure implies that the initial path of the test case has been changed
    assert (tsp.path == [('DC', (11, 1)), ('SF', (0, 0)), ('PHX', (2, -3)), ('LA', (0, -4))])
    result = simulated_annealing(tsp, schedule)
    print("Initial score: {}\nStarting Path: {!s}".format(tsp.get_value(), tsp.path))
    print("Final score: {}\nFinal Path: {!s}".format(result.get_value(), result.path))
    assert (tsp.path != result.path)
    assert (result.get_value() > tsp.get_value())