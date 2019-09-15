import random
import pylab

random.seed(0)

# for testing purposes

HEADS = 1
TAILS = 2


def flip_coin():
    """returns heads or tails"""
    return random.choice([HEADS, TAILS])


def simulate_flips(nFlips):
    """returns a tuple: (numHeads, numTails, nFlips)"""
    numHeads = 0
    numTails = 0
    for i in range(abs(nFlips)):
        if flip_coin() == HEADS:
            numHeads += 1
        else:
            numTails += 1
    headsRatio = numHeads / nFlips
    tailsRatio = numTails / nFlips
    outcome = (numHeads, numTails, headsRatio, tailsRatio, nFlips)
    return outcome


def plot_simulated_flips(
    ratios, flips, title, yLabel, xLabel, leftY, rightY, leftX, expected=0
):
    """plot the flips"""
    pylab.figure()
    pylab.plot(flips, ratios, "ko")
    pylab.ylim(leftY, rightY)
    pylab.xlim(left=leftX)
    pylab.axhline(expected)
    pylab.ylabel(yLabel)
    pylab.xlabel(xLabel)
    pylab.title(title)


def law_of_large_nums(factor=1, amount=1000):
    flips = [factor * i for i in range(1, amount + 1)]
    flipsTracker = []
    hRatios = []
    hOverT = []
    # gather data
    for i in flips:
        outcome = simulate_flips(i)
        try:
            hOverT.append(outcome[0] / outcome[1])
        except ZeroDivisionError:
            continue
        hRatios.append(outcome[2])
        flipsTracker.append(i)
    # plot
    plot_simulated_flips(
        hRatios,
        flipsTracker,
        "Heads/TotalFlips vs TotalFlips",
        "Heads/TotalFlips",
        "TotalFlips",
        -0.1,
        1.1,
        -1,
        1 / 2,
    )
    plot_simulated_flips(
        hOverT,
        flipsTracker,
        "Heads/Tails vs TotalFlips",
        "Heads/Tails",
        "TotalFlips",
        -0.1,
        2.1,
        -1,
        1,
    )


if __name__ == "__main__":
    law_of_large_nums()
    pylab.show()
