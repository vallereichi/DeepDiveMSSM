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



def plot_hist(scans:list[Scan], obs:Observable) -> None:
    fig = plt.figure()
    gs = fig.add_gridspec(2, 1, height_ratios=(3,1), hspace=0.2)
    ax = fig.add_subplot(gs[0])
    labels = []

    # calculate the bin range
    bin_range = abs(scans[0].data[obs.key].max() - scans[0].data[obs.key].min())
    num_bins = 20
    step_size = int(bin_range // num_bins)
    bins = range(int(scans[0].data[obs.key].min()), int(scans[0].data[obs.key].max()), step_size)

    # choose to normalize the histogram for comparisons
    dens = False
    if len(scans) > 1:
        dens = True

    counts = []
    for scan in scans:
        labels.append(scan.name + ": $\\mathcal{L}_{max} = $" + str(scan.data[obs.key][scan.plr.idxmax()].round(2)))
        n, _,_ = ax.hist(scan.data[obs.key], bins=bins, density=dens, alpha=0.5)
        counts.append(n)

    ax.set_xlim(left=bins[0], right=bins[-1])
    ax.set_ylabel("counts")
    ax.legend(labels)

    # calculate the bin difference in case of comparison and plot it
    if len(scans) > 1:
        diff = counts[1] - counts[0]
        ax2 = fig.add_subplot(gs[1], sharex=ax)
        ax2.hlines(0, xmin=ax2.get_xlim()[0], xmax=ax2.get_xlim()[1], colors='grey', linestyles='--', linewidth=0.8)
        ax2.scatter(bins[:-1], diff, c='black', marker='.', alpha=0.8)
        ax2.set_xlabel(f'{obs.label} {obs.dimension}')
        ax2.set_ylabel("diff")
    else:
        ax.set_xlabel(f'{obs.label} {obs.dimension}')

    fig.tight_layout()
    plt.show()

    return
