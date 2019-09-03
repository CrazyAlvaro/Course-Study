import numpy as np
import time

# nd[row, col]
# nd[3,2]
# nd[0:3, 1:3]
# nd[:, 3]

def test_run():
    # uniformly sample [0.0, 1.0]
    print np.random.random(4,5)
    print np.random.normal(5,4)

    # numpy.ndarray
    a = np.random.random(5,4)
    a.dtype
    a.shape[0]
    a.shape[1]

    mean = a.mean()

    a[a<mean] = mean
