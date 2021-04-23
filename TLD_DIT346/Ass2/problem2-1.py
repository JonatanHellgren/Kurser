import numpy as np
import multiprocessing # See https://docs.python.org/3/library/multiprocessing.html
from multiprocessing import Value
import argparse # See https://docs.python.org/3/library/argparse.html
import random
import time
from math import pi


def sample_pi(MyQueue, n):
    """ Perform n steps of Monte Carlo simulation for estimating Pi/4.
        Returns the number of sucesses."""
    random.seed()
    s = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            s += 1

    MyQueue.put(s)



def compute_pi(args):
    random.seed(1)
    error = 1
    n = 1
    s_total = 0
    n_total = 0
    pi_est = 0


    Queue_ = multiprocessing.Queue()

    while error > args.accuracy:

        Processes_ = [multiprocessing.Process(target=sample_pi,
                                                args=(Queue_, n))
                      for _ in range(args.workers)]

        for p in Processes_:
            p.start()

        for p in Processes_:
            p.join()

        s = [Queue_.get() for _ in Processes_]
        s_total += np.sum(s)
        n_total += n * args.workers

        pi_est = (4.0*s_total)/n_total
        error = np.abs(pi - pi_est)

    """
    print(" Steps\tSuccess\tPi est.\tError")
    print("%6d\t%7d\t%1.5f\t%1.5f" % (n_total, s_total, pi_est, pi-pi_est))
    """

    return n_total


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute Pi using Monte Carlo simulation.')
    parser.add_argument('--workers', '-w',
                        default='1',
                        type = int,
                        help='Number of parallel processes')
    parser.add_argument('--accuracy', '-a',
                        default='1e-4',
                        type = float,
                        help='When estimate is with in the range of the accuracy to the real value of pi the simulation will stop')
    args = parser.parse_args()
    start_time = time.time()
    n_total = compute_pi(args)
    end_time = time.time()
    time = end_time - start_time 

    print(args.workers, n_total / time)
