"""
test_distance.py
----------------

Test distance algorithms.

"""

import networkx as nx
from netrd import distance
from netrd.distance import BaseDistance


def test_same_graph():
    """The distance between two equal graphs must be zero."""
    G = nx.karate_club_graph()

    for obj in distance.__dict__.values():
        if isinstance(obj, type) and BaseDistance in obj.__bases__:
            dist = obj().dist(G, G)
            assert dist == 0.0


def test_different_graphs():
    """ The distance between two different graphs must be nonzero."""
    G1 = nx.fast_gnp_random_graph(100, 0.1)
    G2 = nx.barabasi_albert_graph(100, 5)

    for obj in distance.__dict__.values():
        if isinstance(obj, type) and BaseDistance in obj.__bases__:
            dist = obj().dist(G1, G2)
            assert dist != 0.0

