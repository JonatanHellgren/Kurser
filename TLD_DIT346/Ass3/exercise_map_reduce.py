from mrjob.job import MRJob, MRStep
from operator import itemgetter
import time

class FindDublicates(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_max_word)
        ]
    
    def mapper(self, _, line):
        words = line.split()
        for w in words:
            yield (w, 1)

    def combiner(self, key, counts):
        yield (key, sum(counts))

    def reducer(self, key, counts):
        s = sum(counts)
        yield None, (s, key)

    def reducer_find_max_word(self, _, count_word_tuples): 
        # takes the max of the first element in the tuple
        # yield max(count_word_tuples)
        
        # To specify which key that should be used
        yield max(count_word_tuples, key=itemgetter(0))





if __name__ == "__main__":
    #start = time.time()
    FindDublicates.run()
    #end = time.time()
    #print(end - start)
