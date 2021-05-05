import matplotlib.pyplot as plt
import argparse

def read_data(file):
    time = []
    workers = []

    with open(file, "r") as f:
        for line in f:
            splitted = line.split()
            time.append(float(splitted[1]))
            workers.append(int(splitted[0]))

    return time, workers

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Which output one would like to visualize')
    parser.add_argument('--file', '-f', type = str)
    args = parser.parse_args() 

    time, workers = read_data(args.file)

    relative_time = [time[0] / s for s in time]

    plt.plot(workers, relative_time, label = 'Actual')
    #plt.plot(workers, workers, label = 'Theoretical')
    plt.xlabel('Workers')
    plt.ylabel('SpeedUp')
    #plt.legend()
    fig_name = args.file.split('.')[0]

    plt.savefig(f'{fig_name}.png')
