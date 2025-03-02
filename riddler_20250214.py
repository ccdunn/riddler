import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms

R2 = np.sqrt(2)


def draw_circumscribing_circle(ax, R, x=0., y=0.):
    # Create a circle patch with fill set to False
    circle = patches.Circle((x, y), R, fill=False, edgecolor='black', linewidth=2)

    # Add the circle to the axes
    ax.add_patch(circle)
    return


def draw_heart_patch(ax, x, y, theta_deg, scale=1.):
    # Create a rectangle patch (square)
    square = patches.Rectangle((-scale/2, -scale/2), scale, scale,
                               facecolor="pink", alpha=0.5, edgecolor="red")

    left_arc_center_x = 0.
    left_arc_center_y = scale/2
    right_arc_center_x = scale/2
    right_arc_center_y = 0.

    # Define the center, radius, and angle range for the half-circle
    radius = scale/2

    # Create an Arc patch to represent the half-circle
    left_arc = patches.Arc((left_arc_center_x, left_arc_center_y), 2*radius, 2*radius, theta1=0, theta2=180, edgecolor='red')

    # Create an Arc patch to represent the half-circle
    right_arc = patches.Arc((right_arc_center_x, right_arc_center_y), radius * 2, radius * 2, theta1=-90, theta2=90, edgecolor='red')

    # Create a rotation and shift transformation
    rotation = transforms.Affine2D().rotate_deg_around(0, 0, 45 + theta_deg)
    shift = transforms.Affine2D().translate(x, y)
    transform = rotation + shift + ax.transData

    for patch in [square, left_arc, right_arc]:
        patch.set_transform(transform)
        ax.add_patch(patch)

    return


def extra_credit():

    # find shortest cross dimension of the heart shape

    Rs = [2**0 + 2**-1, 2**0 + 2**-1 + 2**-4 - 2**-6, 2**0 + 2**-1 + 2**-5, 2**0 + 2**-1 + 2**-5 + 2**-7, 1.5]
    # Rs = Rs[4:5]
    max_R = np.max(Rs)

    fig, axs = plt.subplots(1, len(Rs), figsize=(8*len(Rs), 8))

    for i, R in enumerate(Rs):
        if len(Rs) > 1:
            ax = axs[i]
        else:
            ax = axs
        if i == 0:
            draw_heart_patch(ax, R2/2 - 1/(2*R2), 1/(2*R2), 0.)
            draw_heart_patch(ax, - R2/2 + 1/(2*R2), - 1/(2*R2), 180.)
            draw_circumscribing_circle(ax, R)
        elif i == 1:
            y_offset = 2**-1 + 2**-2 + 2**-4 + 2**-7
            x_offset = 2**-2 - 2**-3 + 2**-4 - 2**-6 + 2**-7 - 2**-9 - 2**-10
            draw_heart_patch(ax, x_offset, -y_offset, 0.)
            draw_heart_patch(ax, -x_offset, y_offset, 180.)
        elif i == 2:
            y_offset_0 = 2**-1 + 2**-2 + 2**-4 + 2**-7
            y_offset_1 = 2**-1 + 2**-4 + 2**-5 + 2**-7
            draw_heart_patch(ax, 0, -y_offset_0, 0.)
            draw_heart_patch(ax, 0, y_offset_1, 0.)
        elif i == 3:
            y_offset_0 = 2**-1 + 2**-2 + 2**-4 + 2**-6
            y_offset_1 = 2**-1 + 2**-5 + 2**-8
            draw_heart_patch(ax, 0., -y_offset_0, 0.)
            draw_heart_patch(ax, 0., y_offset_1, -45.)
        elif i == 4:
            y_offset_0 = 2**-1 + 2**-2 + 2**-3 + 2**-6
            y_offset_1 = 2**-1 + 2**-5 + 2**-8
            draw_heart_patch(ax, 2**-5 + 2**-6, -y_offset_0, 45.)
            draw_heart_patch(ax, 0., y_offset_1, -180.)



        draw_circumscribing_circle(ax, Rs[i])
        ax.set_xlim([-max_R, max_R])
        ax.set_ylim([-max_R, max_R])
        ax.set_aspect('equal', adjustable='box')


    plt.savefig('riddler_20250214_2_heart.png')


def classic():

    R = (2 + 3*R2)/7
    print(f'{R=}')
    A = (0, - R)
    B = (0, 1/R2 - R)
    C = (1/(2*R2), 3/4*R2 - R)
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
    center_x, center_y = 0, -R + 1/R2
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

    plt.savefig('riddler_20250214_1_heart.png')


if __name__ == '__main__':
    # classic()
    extra_credit()