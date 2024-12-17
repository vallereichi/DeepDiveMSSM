from classes import Scan, Observable
import matplotlib.pyplot as plt


def plot_plr(scans:list[Scan], obs:Observable) -> None:
    nrows = 1
    ncols = 1
    index = 1

    fig = plt.figure()
    ax = fig.add_subplot(nrows, ncols, index)
    labels = []

    for scan in scans:
        ax.scatter(scan.data[obs.key], scan.plr, marker='.', alpha=0.5)
        labels.append(scan.name + ": $\\mathcal{L}_{max} = $" + str(scan.data[obs.key][scan.plr.idxmax()].round(2)))
        

    ax.set_xlabel(f'{obs.label} {obs.dimension}')
    ax.set_ylabel("Profile Likelihood Ratio")
    ax.legend(labels)

    fig.tight_layout()
    plt.show()

    return