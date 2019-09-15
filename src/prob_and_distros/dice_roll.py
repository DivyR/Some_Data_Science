import random
import pylab
import math

DICE = [i for i in range(1, 7, 1)]


def roll_dice():
    """ returns a number between 1 and 6 inclusive."""
    return random.choice(DICE)


def sim_roll_dice(nTimes):
    """ outcomes of rolling a dice nTimes"""
    outcome = []
    for _ in range(nTimes):
        outcome.append(roll_dice())
    return outcome


def binomial_distribution(p, n, k):
    biCoeff = math.factorial(n) / (math.factorial(k) * (math.factorial(n - k)))
    part2 = (p ** k) * ((1 - p) ** (n - k))
    return biCoeff * part2


def run_bi_dist(p, ns, k):
    results = []
    for i in ns:
        results.append(binomial_distribution(p, i, k))
    pylab.figure()
    pylab.plot(ns, results, "ko")


if __name__ == "__main__":
    run_bi_dist(1 / 6, [i for i in range(2, 101)], 2)
    pylab.show()
