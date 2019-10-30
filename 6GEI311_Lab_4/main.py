from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import numpy as np
import time
import matplotlib.pyplot as plt
import glob
from PIL import Image
import random
import string
import timeit
import sys
import tkinter as tk
from tkinter import ttk


sys.path.append(".\\x64\\Release")
import exec_time

def boucle(base=0):
    start = time.time() - base
    for i in (range(999999)):
        np.tanh(i)
    stop = time.time() - base
    return start, stop

def interface_gui():

    def visualize_runtimes(results, title):
        start,stop = np.array(results).T
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        fig, ax = plt.subplots()
        plt.barh(range(len(start)),stop-start,left=start)
        plt.grid(axis='x')
        plt.ylabel("Tasks")
        plt.xlabel("Seconds")
        plt.title(title)
        ax.text(0.05, 0.95, "Exec time: " + str(round(stop[-1]-start[0], 4)) + " seconds", transform=ax.transAxes, 
                verticalalignment='top', bbox=props)
        plt.show()


    def boucle_simple(base=0):
        start = time.time() - base
        for i in (range(999999)):
            np.tanh(i)
        stop = time.time() - base
        res = "Temps d'exécution : " + str(stop-start)
        label_time.configure(text=res)


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


    window = tk.Tk()
    window.title("Les boucles d'exécution")

    label_choice = tk.Label(window, text="Entrez le nombre de processus/threads à lancer :", font="Arial, 12", bd=20)
    label_choice.grid(column=0, row=4)
    choice = tk.Spinbox(window, from_=0, to=100, font="Arial, 12")
    choice.grid(column=1, row=4)


    button_simpleloop_python = tk.Button(window, text="Boucle simple (python)", font="Arial, 12", bg="#e77f67", command=boucle_simple)
    button_simpleloop_python.grid(column=0, row=1)
    button_multiprocess_python = tk.Button(window, text="Boucle découpée en x processus (python)", 
                                           font="Arial, 12", bg="#e77f67", 
                                           command= lambda: visualize_runtimes(multiprocessing(boucle, 16, int(choice.get())), "Python: multiprocessing"))
    button_multiprocess_python.grid(column=0, row=2)
    button_multithreads_python = tk.Button(window, text="Boucle découpée en x threads (python)", 
                                           font="Arial, 12", bg="#e77f67", 
                                           command= lambda: visualize_runtimes(multithreading(boucle, 16, int(choice.get())), "Python: multithreading"))
    button_multithreads_python.grid(column=0, row=3)

    button_simpleloop_cpp = tk.Button(window, text="Boucle simple (C++)", font="Arial, 12", bg="#786fa6")
    button_simpleloop_cpp.grid(column=1, row=1)
    button_multiprocess_cpp = tk.Button(window, text="Boucle découpée en x processus (C++)", font="Arial, 12", bg="#786fa6")
    button_multiprocess_cpp.grid(column=1, row=2)
    button_multithreads_cpp = tk.Button(window, text="Boucle découpée en x threads (C++)", font="Arial, 12", bg="#786fa6")
    button_multithreads_cpp.grid(column=1, row=3)


    label_time = tk.Label(window, text="Cliquez sur une des stratégies pour afficher son temps d'exécution ici", 
                          font="Arial, 12", bg="white", relief="ridge", padx=5, pady=5, bd=5)
    label_time.grid(column=0, row=5)

    window.mainloop()


if __name__ == "__main__":
    interface_gui()
	#print(timeit.timeit(boucle, number=1))
	N = 16

	# Multi threading
	#visualize_runtimes(multithreading(boucle, 1, 1), "Python: Single Thread")
	#visualize_runtimes(multithreading(boucle, 16, 4), "Python: Multi Thread")
	visualize_runtimes(exec_time.thread_exec_time(1), "C++: Multi Thread")
	#exec_time.thread_exec_time(16,1)

	# Multiprocessing
	#visualize_runtimes(multiprocessing(boucle, N, 1), "Python: Single Process")
	#visualize_runtimes(multiprocessing(boucle, N, 4), "Python: Multi Process")