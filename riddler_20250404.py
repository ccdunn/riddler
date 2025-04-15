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


def rec_sort_by_desired(rem_combs, desired):
    if len(rem_combs) == 1:
        return [0]
    inds_with = [i for i, comb in enumerate(rem_combs) if desired[0] in comb]
    inds_without = list(range(len(rem_combs)))
    for i in inds_with[::-1]:
        del inds_without[i]
    if len(desired) <= 1:
        return inds_with + inds_without
    sorted_with = rec_sort_by_desired([rem_combs[i] for i in inds_with], desired[1:])
    sorted_without = rec_sort_by_desired([rem_combs[i] for i in inds_without], desired[1:])
    return sorted_with + [i + len(sorted_with) for i in sorted_without]


def rec_test(combs, rem_combs, prev_comb, interchangeables):
    if not len(rem_combs):
        return True, []
    musts, ranked = must_take_ids(rem_combs)
    if len(musts) > len(rem_combs[0]):
        return False, []
    search_order = rec_sort_by_desired(rem_combs, ranked)
    rem_combs = [rem_combs[i] for i in search_order]  # reorder to explore most promising options first
    for j in range(len(rem_combs)):
        if is_valid_comb(rem_combs[j], combs, prev_comb, musts):
            rem_combs_j = copy.deepcopy(rem_combs)
            del rem_combs_j[j]
            combs_j = copy.deepcopy(combs)
            combs_j[rem_combs[j]] = True
            valid, order = rec_test(combs_j, rem_combs_j, rem_combs[j], interchangeables)
            if valid:
                return True, [[int(id) for id in rem_combs[j]], ] + order

    return False, []


def min_class_search(m=3, min_class_size=1):
    class_size = min_class_size
    while True:
        ids = tuple([id + 1 for id in range(class_size)])
        rem_combs = list(itr.combinations(ids, m))
        combs = {}
        for c in rem_combs:
            combs[c] = False
        prev_comb = []
        order = [ids[:m], ids[m:2*m]]
        combs[order[0]] = True
        combs[order[1]] = True
        interchangeables = [order[0], order[1], ids[2*m:]]
        rem_combs.remove(order[0])
        rem_combs.remove(order[1])
        found, rem_order = rec_test(combs, rem_combs, prev_comb, interchangeables)
        if found:
            return class_size, order + rem_order
        else:
            print(f'{class_size} failed')
            class_size += 1


if __name__ == '__main__':
    with timer('Classic'):
        m = 3
        class_size, order = min_class_search(m, min_class_size=2*m + 2)
        print(f'Minimum group required for sets of {m}={class_size}')
    with timer('Extra Credit'):
        m = 10
        class_size, order = min_class_search(m, min_class_size=2*m + 1)
        print(f'Minimum group required for sets of {m}={class_size}')