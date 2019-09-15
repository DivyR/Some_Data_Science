###########################
# 6.0002 Problem Set 1a: Space Cows

from ps1_partition import get_partitions
import time

# ================================
# Part A: Transporting Space Cows
# ================================


# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # read file
    file = open(filename, "r")
    # {cowname: weight} dict
    cowMap = dict()
    # read each line: name,weight
    for line in file:
        # parse and add to dict
        info = line.split(",")
        cowMap[info[0]] = int(info[1].replace("\n", ""))
    # close file
    file.close()
    # return generated dict
    return cowMap


# Problem 2
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # cows sorted in descending weight
    cowList = sorted(cows.items(), key=lambda kv: kv[1], reverse=True)
    trips = list()
    while len(cowList):
        # set limit for each trip
        remainingLimit = limit
        trip = list()
        # tracks which cows to remove
        remove = list()
        # check each remaining cow for a trip
        for cow in cowList:
            # add cow to the trip if it is within limit
            if cow[1] <= remainingLimit:
                trip.append(cow[0])
                # remove cow from being transported again
                remove.append(cow)
                # update limit
                remainingLimit -= cow[1]
            # break if limit is zero
            elif not remainingLimit:
                break
        # remove from cowList
        for cow in remove:
            cowList.remove(cow)
        # remaining cows are all too heavy to ever be transported
        if not len(trip):
            # set to empty list in order to break the loop
            cowList = list()
        # append a trip
        trips.append(trip)
    # return trips
    return trips


# Problem 3
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # list of cow names
    cowList = list(cows)
    bestTrips = list()
    # using the generator to get bruteforce trips
    for trips in get_partitions(cowList):
        # see if subtrips are within limit
        for trip in trips:
            tripLimit = limit
            for cow in trip:
                tripLimit -= cows[cow]
            # if the subtrip is out of limit move onto the next trip
            if tripLimit < 0:
                break
        if tripLimit >= 0:
            bestTrips = trips
            break
    # return the best possible trip-setup
    return bestTrips


# Problem 4
def compare_cow_transport_algorithms(filename):
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cowMap = load_cows(filename)
    startTime = time.time()
    greedyTrips = greedy_cow_transport(cowMap)
    greedyTime = time.time() - startTime
    bruteTrips = brute_force_cow_transport(cowMap)
    bruteTime = time.time() - startTime

    print("Greedy took: {} and Brute took: {}.".format(greedyTime, bruteTime))
    longerBy = bruteTime / greedyTime
    print("Brute ran {} times longer than Greedy.".format(longerBy))
    return (greedyTrips, bruteTrips)


if __name__ == "__main__":
    # file-path assuming the file is ran from the top directory
    filename = "src/ps/ps1/ps1_cow_data.txt"
    compare_cow_transport_algorithms(filename)
