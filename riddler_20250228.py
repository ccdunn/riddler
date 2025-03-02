import unittest
from typing import Dict, List, Tuple
import copy

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def rec_expected_points(dist: List[int], dists: Dict[Tuple[int], float]):
    """
    :param dist: List[int]
        Sorted list in ascending order of current type counts
    :param dists: Dict[Tuple[int], float]
        Dictionary mapping sorted tuples in ascending order of type counts to expected score
    :return: float
        Expected score using optimal policy from the current type counts
    """
    if tuple(dist) in dists:
        return dists[tuple(dist)]

    next_dists = {}
    n_cards = 0
    max_count = dist[-1]
    key = ()
    for d in range(len(dist)):
        if dist[d] == 0:
            continue
        n_cards += dist[d]

        if d > 0 and dist[d] == dist[d-1]:
            next_dists[key] += dist[d]
            continue

        if dist[d] > max_count:
            max_count = dist[d]

        key = copy.deepcopy(dist)
        key[d] -= 1
        key = tuple(key)
        if key in next_dists:
            next_dists[key] += dist[d]
        else:
            next_dists[key] = dist[d]

    score = max_count/n_cards  # probability of getting a point this round
    for key, prob in next_dists.items():
        prob /= n_cards
        dists[key] = rec_expected_points(list(key), dists)
        score += prob*dists[key]

    # print(f'{dist}:\t{score}')
    return score


def expected_points(n_cards: int = 2, n_colors: int = 3):
    dists = {tuple([0, ]*(n_colors - 1) + [1, ]): 1.}
    dist = [n_cards, ]*n_colors
    exp_points = rec_expected_points(dist, dists)
    return exp_points


def classic():
    exp_points = expected_points(2, 3)
    return exp_points


def extra_credit():
    exp_points = expected_points(10, 3)
    return exp_points


def extra_extra_credit():
    ns_cards = range(1, 2**3 + 1)
    ns_colors = range(1, 2**4 + 1)
    exp_points = np.zeros((len(ns_cards), len(ns_colors)))
    for i, n_cards in enumerate(ns_cards):
        for j, n_colors in enumerate(ns_colors):
            exp_points[i, j] = expected_points(n_cards, n_colors)/(n_cards * n_colors)

    fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    image = ax.matshow(exp_points, extent=[ns_colors[0] - .5, ns_colors[-1] + .5, ns_cards[0] - .5, ns_cards[-1] + .5], norm=LogNorm(vmin=np.min(exp_points), vmax=1))
    fig.colorbar(image)
    ax.set_xticks(np.arange(ns_colors[0], ns_colors[-1] + 1., 1.))
    ax.set_yticks(np.arange(ns_cards[0], ns_cards[-1] + 1., 1.))
    ax.xaxis.set_ticks_position('bottom')
    plt.ylabel(f'Number of Rabbits per Color')
    plt.xlabel(f'Number of Colors')
    plt.title('Maximum Expected Points per Card')
    plt.savefig('riddler_20250228_extraextracredit.png')

    return exp_points


class TestExpectedPoint(unittest.TestCase):
    def test_1(self):
        self.assertAlmostEqual(expected_points(n_cards=1, n_colors=3), 1/3 + .5 + 1, places=6)
        return

    def test_2(self):
        self.assertAlmostEqual(expected_points(n_cards=1, n_colors=2), 1/2 + 1, places=6)
        return

    def test_100(self):
        self.assertAlmostEqual(expected_points(n_cards=1, n_colors=100), sum([1/x for x in range(1, 101)]), places=6)
        return

    def test_100cards(self):
        self.assertAlmostEqual(expected_points(n_cards=100, n_colors=1), 100, places=6)
        return

    def test_2_2(self):
        self.assertAlmostEqual(expected_points(n_cards=2, n_colors=2), 1/2 + 2/3 + 2/3*(1.5) + 1/3*(2), places=6)
        return


if __name__ == '__main__':
    print(f'classic: {classic()}')
    print(f'extra credit: {extra_credit()}')
    extra_extra_credit()