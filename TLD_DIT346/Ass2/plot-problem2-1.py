import matplotlib.pyplot as plt

def read_data(file):
    average_steps = []
    workers = []

    with open(file, "r") as f:
        for line in f:
            splitted = line.split()
            average_steps.append(float(splitted[1]))
            workers.append(int(splitted[0]))

    return average_steps, workers

if __name__ == "__main__":
    average_steps, workers = read_data("problem2-1.out")

    relative_steps = [s / average_steps[0] for s in average_steps]

    plt.plot(workers, relative_steps, label = 'Actual')
    #plt.plot(workers, workers, label = 'Theoretical')
    plt.xlabel('Workers')
    plt.ylabel('SpeedUp')
    plt.title('Accuracy 1e-5')
    #plt.legend()
    plt.savefig('problem2-1.png')
