import copy


class TravelingSalesmanProblem:
    """Representation of a traveling salesman optimization problem.  The goal
    is to find the shortest path that visits every city in a closed loop path.

    Students should only need to implement or modify the successors() and
    get_values() methods.

    Parameters
    ----------
    cities : list
        A list of cities specified by a tuple containing the name and the x, y
        location of the city on a grid. e.g., ("Atlanta", (585.6, 376.8))

    Attributes
    ----------
    names
    coords
    path : list
        The current path between cities as specified by the order of the city
        tuples in the list.
    """

    def __init__(self, cities):
        self.path = copy.deepcopy(cities)

    def copy(self):
        """Return a copy of the current board state."""
        new_tsp = TravelingSalesmanProblem(self.path)
        return new_tsp

    @property
    def names(self):
        """Strip and return only the city name from each element of the
        path list. For example,
            [("Atlanta", (585.6, 376.8)), ...] -> ["Atlanta", ...]
        """
        names, _ = zip(*self.path)
        return names

    @property
    def coords(self):
        """Strip the city name from each element of the path list and return
        a list of tuples containing only pairs of xy coordinates for the
        cities. For example,
            [("Atlanta", (585.6, 376.8)), ...] -> [(585.6, 376.8), ...]
        """
        _, coords = zip(*self.path)
        return coords

    def successors(self):
        """Return a list of states in the neighborhood of the current state by
        switching the order in which any adjacent pair of cities is visited.

        For example, if the current list of cities (i.e., the path) is [A, B, C, D]
        then the neighbors will include [A, B, D, C], [A, C, B, D], [B, A, C, D],
        and [D, B, C, A]. (The order of successors does not matter.)

        In general, a path of N cities will have N neighbors (note that path wraps
        around the end of the list between the first and last cities).

        Returns
        -------
        list<Problem>
            A list of TravelingSalesmanProblem instances initialized with their list
            of cities set to one of the neighboring permutations of cities in the
            present state
        """
        original = self.copy()
        successors = []

        for answer_pos in range(len(original.names) - 1, -1, -1):  # Create answers
            answer = []
            element_position = len(original.names) - 1
            while element_position >= 0:  # Create element each answer
                if element_position == answer_pos:
                    if element_position == 0:  #  Frontier inital case
                        answer[0] = original.path[0]
                        answer.append(original.path[len(original.names) - 1])
                    else:
                        answer.append(original.path[element_position - 1])
                        answer.append(original.path[element_position])
                        element_position -= 1
                else:
                    answer.append(original.path[element_position])
                element_position -= 1

            answer.reverse()
            successors.append(TravelingSalesmanProblem(answer))
        successors.reverse()
        return successors

    @staticmethod
    def _cities_distance(coord_city_1, coord_city_2):
        return ((coord_city_1[0] - coord_city_2[0]) ** 2 + (coord_city_1[1] - coord_city_2[1]) ** 2) ** (1 / 2)

    def get_value(self):
        """Calculate the total length of the closed-circuit path of the current
        state by summing the distance between every pair of adjacent cities.  Since
        the default simulated annealing algorithm seeks to maximize the objective
        function, return -1x the path length. (Multiplying by -1 makes the smallest
        path the smallest negative number, which is the maximum value.)

        Returns
        -------
        float
            A floating point value with the total cost of the path given by visiting
            the cities in the order according to the self.cities list

        Notes
        -----
            (1) Remember to include the edge from the last city back to the
            first city

            (2) Remember to multiply the path length by -1 so that simulated
            annealing finds the shortest path
        """
        distance_traveled = 0.0
        cities = self.coords
        origin = cities[0]

        for city in cities[1:]:
            distance_traveled += self._cities_distance(origin, city)
            origin = city

        distance_traveled += self._cities_distance(origin, cities[0])  # Back home

        return (distance_traveled) * -1.0