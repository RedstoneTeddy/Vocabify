import random
from time import time_ns

start_time = time_ns()
for _ in range(0,100000):
    r = random.randrange(0,1000000)
    r = random.randrange(0,1000000)
    r = random.randrange(0,1000000)
    r = random.randrange(0,1000000)
    r = random.randrange(0,1000000)
    r = random.randrange(0,1000000)
    r = random.randrange(0,1000000)
    r = random.randrange(0,1000000)
    r = random.randrange(0,1000000)
    r = random.randrange(0,1000000)
print(round((time_ns()-start_time)/1000000,3))