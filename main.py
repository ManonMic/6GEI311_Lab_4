from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import numpy as np
import time
import matplotlib.pyplot as plt
import glob
from PIL import Image
import random
import string
import timeit


def visualize_runtimes(results, title):
    start,stop = np.array(results).T
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    fig, ax = plt.subplots()
    plt.barh(range(len(start)),stop-start,left=start)
    plt.grid(axis='x')
    plt.ylabel("Tasks")
    plt.xlabel("Seconds")
    plt.title(title)
    ax.text(0.05, 0.95, "Exec time: " + str(round(stop[-1]-start[0], 4)) + " seconds", transform=ax.transAxes, verticalalignment='top', bbox=props)
    plt.show()

def multithreading(func, iterations, workers):
    begin_time = time.time()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        res = executor.map(func, [begin_time for i in range(iterations)])
    return list(res)

def multiprocessing(func, iterations, workers):
    begin_time = time.time()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        res = executor.map(func, [begin_time for i in range(iterations)])
    return list(res)

def boucle(base=0):
    start = time.time() - base
    print("Boucle running")
    for i in (range(999999)):
        np.tanh(i)
    stop = time.time() - base
    return start, stop
    
if __name__ == "__main__":
    #print(timeit.timeit(boucle, number=1))
    N = 16

    # Multi threading
    #visualize_runtimes(multithreading(boucle, N, 1), "Python: Single Thread")
    #visualize_runtimes(multithreading(boucle, N, 4), "Python: Multi Thread")

    # Multiprocessing
    #visualize_runtimes(multiprocessing(boucle, N, 1), "Python: Single Process")
    #visualize_runtimes(multiprocessing(boucle, N, 4), "Python: Multi Process")

