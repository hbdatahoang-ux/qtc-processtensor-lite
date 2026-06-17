import numpy as np

def test_markov_limit():

    params = {
        "dt": 0.1,
        "seed": 42,
        "eps": 0.0,
        "mem_strength": 0.0,
    }

    _, err1 = bm1_wrapper(**params)
    _, err2 = bm2_wrapper(**params)

    diff = np.linalg.norm(err1 - err2)

    print("Markov limit diff = - test_markov_limit.py:17", diff)

    assert diff < 1e-12