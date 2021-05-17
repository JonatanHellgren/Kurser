import argparse
import time
import pyspark 

def sort_to_bins(bins, value):
    for it in range(10):
        if bins[it] < value and value < bins[it+1]:
            yield (it, value)

def spark_summary_statistics(text_file, workers):
    sc = pyspark.SparkContext(master = f'local[{workers}]')

    values = sc.textFile(text_file).map(lambda l: ('value', float(l.split()[2])))

    min_value = values.min()[1]
    max_value = values.max()[1]
    length = values.count()

    sum_values = values.map(lambda x: x[1]).sum()
    sum_squared_values = values.map(lambda x: x[1]*x[1]).sum()

    E_v = sum_values/length
    E_v2 = sum_squared_values/length

    mean = sum_values/length
    std = (E_v2 - E_v*E_v) ** (1/2)

    # bins
    bin_size = (max_value - min_value)/10
    bins = [min_value + it * bin_size for it in range(11)]

    bin_counts = values.flatMap(lambda l: sort_to_bins(bins, l[1])).countByKey()

    print(f' Min\t{min_value}\n Max\t{max_value}\n mean\t {mean}\n std\t {std}')
    print(f'Bin counts:\n{bin_counts}')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Select file and amount of workers')
    parser.add_argument('--file', '-f', type = str,
                        help = 'Which file one would like to compute summary statistict for')
    parser.add_argument('--workers', '-w', type = int,
                        help = 'How many workers should be utalized in pyspark')

    args = parser.parse_args() 

    start_time = time.time()
    spark_summary_statistics(args.file, args.workers)
    end_time = time.time()

    print(f'Time elapsed: {round(end_time - start_time, 2)}')

