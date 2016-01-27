import matplotlib.pyplot as plt
import itertools

def plot_antenna_array(points):
    for a, b in itertools.combinations(points, 2):
        plt.plot([a.x, b.x], [a.y, b.y])
        centre = a + (a.delta_to_other(b) * 0.5)
        plt.annotate(round(a.distance_to_other(b), 3),
                     xy = (centre.x, centre.y))
    for idx, point in enumerate(points):
        plt.plot([point.x], [point.y], 'ro', markersize=10)
        plt.annotate(idx, 
                     xy=(point.x, point.y))
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.title("Generated array geometry")
    plt.xlabel("x (metres)")
    plt.ylabel("y (metres)")
    plt.show()


