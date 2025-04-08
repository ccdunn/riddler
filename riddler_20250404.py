import copy
import math
import itertools as itr
import time
from contextlib import contextmanager

from scipy.special import comb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

@contextmanager
def timer(name='Elapsed time'):
    start_time = time.perf_counter()
    yield
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"{name}: {elapsed_time:.4f} seconds")


def add_round(seeds):
    out_seeds = []
    for i, seed in enumerate(seeds):
        out_seeds.extend([seed, 2*len(seeds) + 1 - seed])
    return out_seeds


def must_take_ids(rem_combs):
    u_ids, counts = np.unique(np.array(rem_combs).flatten(), return_counts=True)
    return u_ids[counts == len(rem_combs)//2 + 1], u_ids[np.argsort(counts)[::-1]]



def is_valid_comb(new_comb, combs, last_comb, musts):
    if any([id not in new_comb for id in musts]):
        return False
    if combs[new_comb]:
        return False
    for id in new_comb:
        if id in last_comb:
            return False
    return True


def rec_test(combs, rem_combs, prev_comb):
    if not len(rem_combs):
        return True, []
    musts, ranked = must_take_ids(rem_combs)
    if len(musts) > len(rem_combs[0]):
        return False, []
    for j in range(len(rem_combs)):
        if is_valid_comb(rem_combs[j], combs, prev_comb, musts):
            rem_combs_j = copy.deepcopy(rem_combs)
            del rem_combs_j[j]
            combs_j = copy.deepcopy(combs)
            combs_j[rem_combs[j]] = True
            valid, order = rec_test(combs_j, rem_combs_j, rem_combs[j])
            if valid:
                return True, [[int(id) for id in rem_combs[j]], ] + order

    return False, []


def min_class_search(m=3, min_class_size=1):
    class_size = min_class_size
    while True:
        ids = np.arange(class_size) + 1
        rem_combs = list(itr.combinations(ids, m))
        combs = {}
        for c in rem_combs:
            combs[c] = False
        prev_comb = []
        found, order = rec_test(combs, rem_combs, prev_comb)
        if found:
            return class_size, order


if __name__ == '__main__':
    with timer('Classic'):
        m = 3
        class_size, order = min_class_search(m, min_class_size=2*m + 1)
        print(f'Minimum group required for sets of {m}={class_size}')
    with timer('Extra Credit'):
        m = 10
        class_size, order = min_class_search(m, min_class_size=2*m + 7)
        print(f'Minimum group required for sets of {m}={class_size}')