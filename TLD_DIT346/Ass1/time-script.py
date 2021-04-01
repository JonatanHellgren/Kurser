import argparse
import os
import time
import matplotlib.pyplot as plt


'''
This function executes a script i times with a specified number of workers. It
returns the average time taken to ececute the script. We are using the os module
in python so that we can makie it possible to run this script on all fututre
scripts.
'''

def time_script(script, k, i):
    tot_time = 0
    for _ in range(i):
        start = time.time()
        os.system(f"python3 {script} -w {k}")
        end = time.time()
        tot_time += end - start
    return tot_time / i


'''
This function uses time_script but executes it with different a different
number of workes each time. It return a list containing the average time taken
to execute the script for each amount of workers.
'''

def time_scripts(args, ks):
    times = []
    for k in ks:
        times.append(time_script(args.script, k, args.iterations))
    return times

'''
In the main function we make it possible to execute different scripts with
an parser, we also make it possible to choose how many times we want to run the
scrips, this is nice since the time it takes to execute a script can have
different variations. The main function then goes on to plotting the measured
and the theoretical time for the script. 
'''

if __name__ == "__main__":
    # number of workers (cores)
    ks = [1, 2, 4, 8, 16, 32]

    # here we handle the arguments that can be passed to the script
    parser = argparse.ArgumentParser(description='Plots the sppedup for a script when increasing the number of threads')
    parser.add_argument('--script', '-s',
                        type = str,
                        help='Script that we want to run')
    parser.add_argument('--iterations', '-i',
                        default='10',
                        type = int,
                        help='Number of iterations performed for the script for every number of threads')
    args = parser.parse_args()

    # plot the measured time for the script
    times = time_scripts(args, ks)
    one_core = times[0]
    times = [one_core/time for time in times]
    plt.plot(ks, times, label = 'Measured')

    # compute and plot the theoretical time for the script
    seq = range(1, 33)
    f = 0.6
    theoretical = [1 / ( (1 - f) + (f / s)) for s in seq]
    plt.plot(seq, theoretical, label = f'Theoretical, f = {f}')

    # making the plot look a bit nices by adding titles and such 
    plt.title('10 million iterations')
    plt.xlabel('Number of Processors')
    plt.ylabel('SpeedUP')
    plt.legend()
    plt.xticks(ks)
    print(times)
    plt.savefig('speedup1_bayes_1e7.png')
