import copy
import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def add_round(seeds):
    out_seeds = []
    for i, seed in enumerate(seeds):
        out_seeds.extend([seed, 2*len(seeds) + 1 - seed])
    return out_seeds


def extra_credit(n=6):
    all_seeds = np.arange(1, 2**n + 1)
    starting_order = [1.]
    for i in range(1, n + 1):
        starting_order = add_round(starting_order)
    Bs = np.arange(2**n + 1) + .5
    winning_seeds = []
    for B in Bs:
        seeds = copy.deepcopy(starting_order)
        for _ in range(n):
            seeds = np.vstack([seeds[::2], seeds[1::2]])
            powers = 2**n + 1 - seeds
            bonus = np.argmax(seeds, axis=0)
            powers[bonus, np.arange(powers.shape[1])] += B
            seeds = seeds[np.argmax(powers, axis=0), np.arange(powers.shape[1])]
        winning_seeds.append(int(seeds[0]))

    unwinnable_seeds = [int(x) for x in set(all_seeds.flatten()).difference(winning_seeds)]

    return unwinnable_seeds


if __name__ == '__main__':
    print(f'unwinnable_seeds={extra_credit(6)}')