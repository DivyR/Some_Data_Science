import coin_flip as cf
import pylab


def calculate_sd(results):
    """ calculates the standard deviation of a set of data"""
    cardinality = len(results)
    if not cardinality:
        raise ValueError
    mean = sum(results) / cardinality
    variance = 0.0
    for i in results:
        variance += (i - mean) ** 2
    variance /= cardinality
    return variance ** 0.5


def coin_flip_sd(nTrials, nFlips):
    """ generate stardard deviation for nTrials with nFlips each"""
    heads, means = [], []
    for i in range(nTrials):
        outcome = cf.simulate_flips(nFlips)
        heads.append(outcome[0])
        means.append(outcome[2])
    mean = sum(means) / len(means)
    return (calculate_sd(heads), mean)


def generate_coin_flip_sds(xAxis, nTrials):
    sds, means = [], []
    for i in xAxis:
        sd, mean = coin_flip_sd(nTrials, i)
        sds.append(sd)
        means.append(mean)
    return (sds, means)


def plot_sds(xAxis, sds, nTrials):
    pylab.figure()
    pylab.plot(xAxis, sds, "ko")
    pylab.title("Stan.Deviations of " + str(nTrials) + " vs nFlips per Trial")
    pylab.semilogx()
    pylab.semilogy()
    pylab.xlabel("nFlips")
    pylab.ylabel("SD of nTrials")


if __name__ == "__main__":
    xAxis = [2 ** i for i in range(1, 15, 1)]
    nTrials = 10
    sds, hMeans = generate_coin_flip_sds(xAxis, nTrials)
    print(sds)
