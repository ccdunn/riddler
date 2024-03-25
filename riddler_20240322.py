import numpy as np


def f(lut: np.ndarray, i: int, N: int):

    if N == 0:
        return 1

    opp = 2**N + 1 - i

    return opp*f(np.min([opp, i]), N - 1)


def grow_lut(lut: np.ndarray):
    # use dynamic programming to double number of teams to the lookup table
    N = lut.shape[1] + 1

    for i in range(2**(N - 1) + 1, 2**N + 1):
        lut = np.vstack([lut, lut[2**N - i, :]])

    lut = np.hstack([lut, np.arange(1, 2**N + 1)[::-1][:, np.newaxis]])

    return lut


def build_lut(N: int):
    # build a lookup table of strongest possible opponents for 2^N teams in a bracket-style knockout tournament
    if N < 0:
        raise ValueError(f'Negative N: {N}')
    if N == 0:
        return np.array([[]])

    lut = np.array([[2], [1]], dtype=int)

    for n in range(2, N+1):
        lut = grow_lut(lut)

    return lut


def main(N: int):

    lut = build_lut(N)

    opps = np.hstack([np.arange(1, 2**N+1)[:, np.newaxis], lut, np.prod(lut, axis=1, keepdims=True)**(1/N)])

    return opps


if __name__ == '__main__':
    N = 4
    opps = main(N)
    min_val = np.min(opps[:, -1])
    print(f'Seeds with hardest schedule out of {2**N}: {np.where(min_val == opps[:, -1])[0] + 1}')

    N = 10
    opps = main(N)
    # print(opps[:, [0, -1]])
    min_val = np.min(opps[:, -1])
    # print(np.where(min_val == opps[:, -1])[0] + 1)
    print(f'Seeds with hardest schedule relative to 2^N: {(np.where(min_val == opps[:, -1])[0] + 1)/(2**N)}')

    # print(opps[22 - 1, :])