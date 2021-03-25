# Scaffold for solution to DIT873 / DAT346, Programming task 1


def fib (limit) :
    # Given an input limit, calculate the Fibonacci series within [0,limit]
    # The first two numbers of the series are always equal to 1,
    # and each consecutive number returned is the sum of the last two numbers.
    # You should use generators for implementing this function
    # See https://docs.python.org/3/howto/functional.html#generator-expressions-and-list-comprehensions
    # Your code below
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b

    return

def list_fib(limit) :
    # Construct a list of Fibonacci series
    list = []
    for i in fib(limit):
        list.append(i)
    # Your code below
    return list

# The following is called if you execute the script from the commandline
# e.g. with python solution.py
if __name__ == "__main__":
    limit = 20
    print(list_fib(limit))
    assert list_fib(limit) == [0, 1, 1, 2, 3, 5, 8, 13]

