import matplotlib.pyplot as plt
import itertools

def plot_antenna_array(points):
    for idx, point in enumerate(points):
        plt.plot([point.x], [point.y], 'ro')
        plt.annotate(idx, 
                     xy=(point.x, point.y))
    for a, b in itertools.combinations(points, 2):
        plt.plot([a.x, b.x], [a.y, b.y])
        centre = a + (a.delta_to_other(b) * 0.5)
        plt.annotate(round(a.distance_to_other(b), 3),
                     xy = (centre.x, centre.y))
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.show()


