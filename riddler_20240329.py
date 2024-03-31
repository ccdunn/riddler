import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def prop_states(states: np.ndarray, sizes: list):
    n = states.shape[1]
    new_states_fill_A = np.vstack([sizes[0]*np.ones([1, n]), states[1, :]])
    new_states_fill_B = np.vstack([states[0, :], sizes[1]*np.ones([1, n])])
    new_states_empty_A = states*np.array([[0], [1]])
    new_states_empty_B = states*np.array([[1], [0]])
    volumes = np.sum(states, axis=0)
    volumes_B_post_A2B = np.minimum(volumes, sizes[1])
    new_states_A2B = np.vstack([volumes - volumes_B_post_A2B, volumes_B_post_A2B])
    volumes_A_post_B2A = np.minimum(volumes, sizes[0])
    new_states_B2A = np.vstack([volumes_A_post_B2A, volumes - volumes_A_post_B2A])
    new_states = np.hstack([new_states_fill_A, 
                            new_states_fill_B, 
                            new_states_empty_A, 
                            new_states_empty_B, 
                            new_states_A2B, 
                            new_states_B2A])
    new_states = np.unique(new_states, axis=1)

    return new_states


def rec_prop_states(sizes):


    old_states = np.zeros([2, 1], dtype=int)
    n_steps = np.zeros([1, ], dtype=int)

    steps_req = -np.ones([np.max(sizes) + 1])
    steps_req[0] = 0

    i = 0
    while True:
        new_states = prop_states(old_states[:, n_steps == i], sizes)
        i += 1
        novel_states = np.array([new_states[:, i] for i in range(new_states.shape[1]) if not np.any(np.all(new_states[:, i:i+1] == old_states, axis=0))]).T
        if not len(novel_states):
            return old_states, n_steps
        n_steps = np.concatenate([n_steps, i*np.ones(novel_states.shape[1])])
        old_states = np.hstack([old_states, novel_states])


def min_steps_to_volume(states, n_steps):
    min_steps = -np.ones((int(np.max(states) + 1)), dtype=int)
    for i in range(len(min_steps)):
        find = np.where(np.any(states == i, axis=0))
        if len(find[0]):
            min_steps[i] = n_steps[find[0][0]]

    return min_steps



if __name__ == '__main__':
    sizes = np.array([[3], [10]], dtype=int)
    states, n_steps = rec_prop_states(sizes)
    print(states)
    print(n_steps)
    min_steps = min_steps_to_volume(states, n_steps)
    print(min_steps)
    print(np.argmax(min_steps))

    max_volume = 100
    min_stepss = np.zeros([max_volume + 1, max_volume + 1], dtype=int)
    for i in range(max_volume + 1):
        print(i)
        sizes = np.array([[i], [max_volume]], dtype=int)
        states, n_steps = rec_prop_states(sizes)
        min_stepss[i, :] = min_steps_to_volume(states, n_steps)

    print(min_stepss)
    min_stepss = min_stepss.astype(float)
    min_stepss[min_stepss == -1] = np.nan
    plt.figure(figsize=[16, 16])
    cmap = mpl.colormaps.get_cmap('viridis')  # viridis is the default colormap for imshow
    cmap.set_bad(color='white')
    plt.imshow(min_stepss, cmap=cmap)
    max_steps = np.nanmax(min_stepss, axis=1)
    global_max_steps = np.nanmax(max_steps)
    print(max_steps)
    new_global = True
    for i in range(len(max_steps)):
        if max_steps[i] < global_max_steps:
            x_coords = np.where(min_stepss[i, :] == max_steps[i])[0]
            plt.plot(x_coords, i*np.ones_like(x_coords), 'r.', markersize=4, label='Maximum per Configuration' if not i else None)
        else:
            x_coords = np.where(min_stepss[i, :] == global_max_steps)[0]
            plt.plot(x_coords, i*np.ones_like(x_coords), 'r*', markersize=8, label='Global Maximum' if new_global else None)
            new_global = False

    plt.gca().invert_yaxis()
    plt.xlabel('Target Volume', fontsize=16)
    plt.ylabel('Smaller Vessel Volume', fontsize=16)
    plt.title('Minimum Steps to Achieve a Volume', fontsize=24)
    cb = plt.colorbar()
    cb.set_label('Minimum # of Steps', fontsize=16)
    plt.legend(bbox_to_anchor=(1, -.1), loc='lower right', fontsize=12)
    plt.savefig('min_steps.png')
