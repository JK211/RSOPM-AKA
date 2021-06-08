import time
# from pypuf.simulation import XORArbiterPUF
# from pypuf.simulation import LightweightSecurePUF
from pypuf.simulation import PermutationPUF
from pypuf.io import random_inputs

# puf = XORArbiterPUF(n=64, k=2, seed=1)
puf = PermutationPUF(n=128, k=8, seed=1)
challenges = random_inputs(n=128, N=1, seed=2)
sum=0
i=1
for i in range(1000):
    t1 = time.perf_counter()
    puf.eval(challenges)
    # print(puf.eval(challenges))
    t2 = time.perf_counter()
    sum=sum+t2-t1
print("Total time of 1000 times XORArbiterPUF operation:", sum, 's')
print("Average time of XORArbiterPUF operation:", (sum/1000) * 1000, 'ms')