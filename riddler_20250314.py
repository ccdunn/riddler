import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def draw_island():
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    thetas = np.linspace(0, np.pi, 2**8, endpoint=True)
    R = 1.
    plt.plot(R*np.cos(thetas), R*np.sin(thetas), c='gold', linewidth=3, label='Semicircular Beach')
    plt.plot([-R, R], [0, 0], c='darkorange', linewidth=3, label='Diametric Beach')

    xs = np.linspace(-R, R, 2**8, endpoint=True)
    plt.plot(xs, (R**2 - xs**2)/(2*R), c='k', linewidth=2, label='Equidistant Boundary')

    ex_x = .4
    ex_y = (R**2 - ex_x**2)/(2*R)
    plt.plot([0, ex_x], [0, ex_y], c='grey', linestyle=':')
    plt.scatter(ex_x, ex_y, s=2**5, c='k')
    plt.plot([ex_x, R*ex_x/np.sqrt(ex_x**2 + ex_y**2)], [ex_y, R*ex_y/np.sqrt(ex_x**2 + ex_y**2)], c='k', linestyle='--')
    plt.plot([ex_x, ex_x], [0, ex_y], c='k', linestyle='--')

    plt.axis('equal')
    plt.legend(loc='upper left')
    lim_buffer = 1.1
    plt.xlim([-lim_buffer*R, lim_buffer*R])
    plt.ylim([-(lim_buffer - 1)*R, lim_buffer*R])
    plt.savefig('riddler_20250314.png')


def extra_credit():

    n = 2**26
    xys = np.random.rand(2, n)
    xys = xys[:, np.linalg.norm(xys, axis=0) <= 1]
    ds = np.copy(xys)
    ds[0, :] = 1 - np.linalg.norm(xys, axis=0)
    dbar = np.mean(np.min(ds, axis=0))

    return dbar


if __name__ == '__main__':
    draw_island()
    print(f'dbar={extra_credit()}')