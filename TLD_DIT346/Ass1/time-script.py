import argparse
import os
import time
import matplotlib.pyplot as plt

def time_script(script, k, i):
    tot_time = 0
    for _ in range(i):
        start = time.time()
        os.system(f"python3 {script} -w {k}")
        end = time.time()
        tot_time += end - start
    return tot_time / i

def time_scripts(args, ks):
    times = []
    for k in ks:
        times.append(time_script(args.script, k, args.iterations))
    return times


if __name__ == "__main__":
    ks = [1, 2, 3, 4, 5, 6, 7, 8] #[1, 2, 4, 8, 16, 32]

    parser = argparse.ArgumentParser(description='Plots the sppedup for a script when increasing the number of threads')
    parser.add_argument('--script', '-s',
                        type = str,
                        help='Script that we want to run')
    parser.add_argument('--iterations', '-i',
                        default='10',
                        type = int,
                        help='Number of iterations performed for the script for every number of threads')
    args = parser.parse_args()

    times = time_scripts(args, ks)
    plt.plot(ks, times)
    plt.show()
