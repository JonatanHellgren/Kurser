from mrjob.job import MRJob, MRStep
import time 
import sys


"""
Takes a file on the format <id>\t<group>\t<value> and computes the min, max,
mean and standard deviation for all of the valued as well as dividing the values
into bins where the integer value represents which bin it should be placed in.
The function does this using a mapper, combiner and reduer.
"""

class summary_statistics(MRJob):

    """
    A generator that yield the key 'value' and the value as a float
    """
    def mapper(self, _, line):
        splitted_line = line.split()
        yield ('value', float(splitted_line[2]))

    """
    A generator that summaries the output yielded from the mapper
    """
    def combiner(self, key, value):

        # stores the values in a list
        v = [val for val in value]
        length = len(v)

        # to compute the standard deviation we need the values squared
        v2 = [val*val for val in v]


        # initalizing and filling the the bins for the histogram
        bin_size = (7.2 - 3.1)/10
        bin_limits = [3.1 + bin_size * it for it in range(11)]
        bins = [0] * 10
        for val in v:
            for it in range(10):
                if bin_limits[it] < val and val < bin_limits[it+1]:
                    bins[it] += 1


        yield ('min', min(v))
        yield ('max', max(v))
        yield ('mean', sum(v)/length)
        yield ('std', (sum(v), sum(v2), length))
        yield ('hist', bins)
        
        #yield ('values', v)



    """
    The reducer summarieses the results yielded from the combiner and later
    yield each respective key summarised
    """
    def reducer(self, key, value):

        self.min_value = None
        self.max_value = None



        if key == 'min':
            self.min_value = min(value)
            yield ('min', self.min_value)

        elif key == 'max':
            self.max_value = max(value)
            yield ('max', self.max_value)

        elif key == 'mean':
            v = [val for val in value]
            yield ('mean', sum(v)/len(v))

        elif key == 'std':
            """
            To compute the standard deviation we summarize each value as well as
            summarizing each value squared. Then we compute E[v] and E[v^2] to be 
            able to use the formula:
            std(v) = sqrt(E[v^2] - E[v]^2),
            to compute the standard deviation.
            """
            sum_v = 0
            sum_v2 = 0
            length = 0

            for v in value:
                sum_v += v[0]
                sum_v2 += v[1]
                length += v[2]

            E_v = sum_v/length
            E_v2 = sum_v2/length

            yield('std', (E_v2 - E_v * E_v) ** (1/2))

        elif key == 'hist' :#and self.min_value != None and self.max_value != None:
            bins = [0] * 10
            for v in value:
                for it in range(10):
                    bins[it] += v[it]

            yield('hist', bins)





if __name__ == "__main__":
    start = time.time()
    summary_statistics.run()
    end = time.time()
    sys.stderr.write(f'time elapsed: {round(end-start, 2)}\n')


