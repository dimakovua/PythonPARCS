import random
from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Initialized")

    def solve(self):
        print("Job Started")
        k = len(self.workers)
        print("Workers: %d" % k)

        # Reading input
        N1, x1, x2, y1, y2 = self.read_input()

        # Map phase
        mapped = []
        for i in range(k):
            print("Mapping %d" % i)
            mapped.append(self.workers[i].mymap(N1 // k + (N1 % k > i), x1, x2, y1, y2))

        # Reduce phase
        num = self.myreduce(mapped)

        integral = num * (x2 - x1) * (y2 - y1) / N1

        # Writing output
        self.write_output(integral)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(N1, x1, x2, y1, y2):
        num = 0
        for _ in range(N1):
            x = random.uniform(x1, x2)
            y = random.uniform(y1, y2)
            fun = foo(x)
            if 0 <= y <= fun:
                num += 1
            elif 0 >= y >= fun:
                num -= 1
        return num

    @staticmethod
    @expose
    def myreduce(mapped):
        return sum(item.value for item in mapped)

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            lines = f.readlines()
            N = int(lines[0].strip())
            x1, x2, y1, y2 = map(float, lines[1].strip().split())
            return N, x1, x2, y1, y2

    def write_output(self, output):
        with open(self.output_file_name, 'w') as f:
            f.write(str(output))
        print("Output written")

def foo(x):
    return 1 / (x ** 5 + 1)

