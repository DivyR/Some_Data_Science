import scipy
from scipy import integrate
import random
import pylab


def gaus(x, mu, sigma):
    part1 = 1 / (sigma * (2 * scipy.pi) ** 0.5)
    ePower = (-(x - mu) ** 2) / (2 * (sigma) ** 2)
    part2 = scipy.e ** ePower
    return part1 * part2


def normal_distibution(mean=0, sigma=1, nPoints=1000000, bins=1000):
    """plots a bell curve with n points"""
    points = [random.gauss(mean, sigma) for _ in range(nPoints)]
    pylab.figure()
    pylab.hist(points, bins=bins)


def empirical_rule(fnc, mu, sigma):
    """integrates provided function over 1, 2, and 3 SD intervals"""
    fncArgs = (mu, sigma)
    results = []
    for iSigma in range(1, 4, 1):
        delta = iSigma * sigma
        a, b = mu - delta, mu + delta
        results.append(scipy.integrate.quad(fnc, a, b, fncArgs))
    print(*results, sep="\n")
    print("Expected: 68-95-99.7")


if __name__ == "__main__":
    empirical_rule(gaus, 0, 10)
    pylab.show()
