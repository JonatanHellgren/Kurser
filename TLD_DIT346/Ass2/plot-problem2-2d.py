import matplotlib.pyplot as plt

def read_data(file):
    time  = []
    workers = []

    with open(file, "r") as f:
        for line in f:
            splitted = line.split()
            print(splitted)
            time.append(float(splitted[1]))
            workers.append(int(splitted[0]))

    return time, workers

def amdahls_speedup(p, s):
    return 1 / ((1-p) + p/s)

if __name__ == "__main__":
    time, workers = read_data("problem2-2d_1e6.out")

    relative_time = [time[0] / t for t in time]

    thoretical = [amdahls_speedup(0.912, w) for w in workers]


    plt.plot(workers, relative_time, label = 'Actual')
    plt.plot(workers, thoretical, label = 'Theoretical')
    plt.title('10 iterations, 1 000 000 samples')
    plt.xlabel('Workers')
    plt.ylabel('SpeedUp')
    plt.legend()
    plt.savefig('problem2-2d_1e6.png')
