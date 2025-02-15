import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms


if __name__ == '__main__':

    r2 = np.sqrt(2)

    R = (2 + 3*r2)/7
    print(f'{R=}')
    A = (0, - R)
    B = (0, 1/r2 - R)
    C = (1/(2*r2), 3/4*r2 - R)
    print(f'{C=}')

    fig, ax = plt.subplots(1)

    plt.scatter(A[0], A[1], c='r')
    plt.scatter(B[0], B[1], c='r')
    plt.scatter(C[0], C[1], c='r')

    # Define the center, radius, and angle range for the half-circle
    center = C
    radius = 1/2
    theta1 = -45
    theta2 = 135

    # Create an Arc patch to represent the half-circle
    arc = patches.Arc(center, radius * 2, radius * 2, theta1=theta1, theta2=theta2, edgecolor='red')

    # Add the patch to the axes
    ax.add_patch(arc)

    # Define the center, radius, and angle range for the half-circle
    center = (-C[0], C[1])
    radius = 1/2
    theta1 = -45 + 90
    theta2 = 135 + 90

    # Create an Arc patch to represent the half-circle
    arc = patches.Arc(center, radius * 2, radius * 2, theta1=theta1, theta2=theta2, edgecolor='red')

    # Add the patch to the axes
    ax.add_patch(arc)

    # Define circle parameters
    center_x = 0.
    center_y = 0.
    radius = R

    # Create a circle patch with fill set to False
    circle = patches.Circle((center_x, center_y), radius, fill=False, edgecolor='black', linewidth=2)

    # Add the circle to the axes
    ax.add_patch(circle)

    # Define square properties
    side_length = 1
    rotation_angle_deg = 45
    center_x, center_y = 0, -R + 1/r2
    rotation_angle_rad = np.deg2rad(rotation_angle_deg)

    # Create a rectangle patch (square)
    square = patches.Rectangle((center_x - side_length / 2, center_y - side_length / 2), side_length, side_length,
                               facecolor="pink", alpha=0.5, edgecolor="red")

    # Create a rotation transformation
    rotation = transforms.Affine2D().rotate_deg_around(center_x, center_y, rotation_angle_deg)

    # Add the rotation transformation to the square
    square.set_transform(rotation + ax.transData)

    # Add the square to the axes
    ax.add_patch(square)

    # Add the square to the axes
    ax.add_patch(square)



    ax.set_xlim([-R, R])

    ax.set_ylim([-R, R])
    ax.set_aspect('equal', adjustable='box')
    plt.show()
