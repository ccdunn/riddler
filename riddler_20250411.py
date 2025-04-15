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



def j_of_k_checker(pattern, j_of_ks):
    pattern_len = len(pattern)
    for j_of_k in j_of_ks:
        j, k = j_of_k
        if pattern_len < k:
            if j - len(set(pattern)) > k - pattern_len:
                return False
        else:
            if len(set(pattern[-k:])) < j:
                return False
    return True


def rec_build_options(previous, l_remaining, n, j_of_ks):
    valids = []
    for i in range(n):
        test_pattern = previous + [i]
        if j_of_k_checker(test_pattern, j_of_ks):
            if l_remaining == 1:
                valids.append(test_pattern)
            else:
                test_valid = rec_build_options(test_pattern, l_remaining - 1, n, j_of_ks)
                if len(test_valid) > 0:
                   valids.extend(test_valid)
    return valids


def rec_gen_options_tree(options):
    tree = {}
    for option in options:
        if option[0] not in tree:
            tree[option[0]] = []
        if len(option) > 1:
            tree[option[0]].append(option[1:])
    for key, val in tree.items():
        tree[key] = rec_gen_options_tree(val)
    return tree


def rec_search_b(len, options_tree, history, full):
    max_len = len
    max_full = [full, ]
    if options_tree == {}:
        print(max_len)
        return max_len, max_full
    h_options_tree = copy.deepcopy(options_tree)
    for h in history:
        h_options_tree = h_options_tree[h]
    for choice in list(h_options_tree.keys()):
        new_options_tree = copy.deepcopy(options_tree)
        new_h_options_tree = new_options_tree
        for h in history:
            new_h_options_tree = new_h_options_tree[h]
        del new_h_options_tree[choice]
        choice_len, choice_full = rec_search_b(len + 1, new_options_tree, history[1:] + [choice], full + [choice])
        if choice_len > max_len:
            max_len = choice_len
            max_full = choice_full
        elif choice_len == max_len:
            max_full += choice_full
    print(max_len)
    return max_len, max_full


def rec_search_a(options_tree, history):
    h_options_tree = copy.deepcopy(options_tree)
    for h in history:
        h_options_tree = h_options_tree[h]
    if h_options_tree == {}:
        new_options_tree = copy.deepcopy(options_tree)
        new_h_options_tree = new_options_tree
        for h in history[:-1]:
            new_h_options_tree = new_h_options_tree[h]
        del new_h_options_tree[history[-1]]
        return rec_search_b(len(history), new_options_tree, history[1:], history)
    else:
        max_len = len(history)
        max_full = [history, ]
        for choice in list(h_options_tree.keys()):
            choice_len, choice_full = rec_search_a(options_tree, history + [choice])
            if choice_len > max_len:
                max_len = choice_len
                max_full = choice_full
            elif choice_len == max_len:
                max_full += choice_full
        return max_len, max_full


def classic():
    j_of_ks = [[2, 2]]
    l_unique = 3
    l_max = max([j_of_k[1] for j_of_k in j_of_ks] + [l_unique])
    options = rec_build_options([], l_max, n=3, j_of_ks=j_of_ks)
    options_tree = rec_gen_options_tree(options)
    max_length = rec_search_a(options_tree, [])
    return max_length


def extra_credit():
    j_of_ks = [[2, 2], [3, 4]]
    l_unique = 4
    l_max = max([j_of_k[1] for j_of_k in j_of_ks] + [l_unique])
    options = rec_build_options([], l_max, n=4, j_of_ks=j_of_ks)
    options_tree = rec_gen_options_tree(options)
    max_length = rec_search_a(options_tree, [])
    return max_length


if __name__ == '__main__':
    with timer('Classic'):
        max_len, max_full = classic()
        print(f'Longest hedge of 3: {max_len}')
        for mf in max_full:
            print(f'{mf}')
    with timer('Extra Credit'):
        print(f'Longest hedge of 4: {extra_credit()}')