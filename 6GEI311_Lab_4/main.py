from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import numpy as np
import time
import matplotlib.pyplot as plt
import sys
import tkinter as tk

sys.path.append(".\\x64\\Release")
import exec_time


def boucle(base=0):
    start = time.time() - base
    for i in (range(999999)):
        np.tanh(i)
    stop = time.time() - base
    return start, stop


def boucle_cpp(base=0):
    start = time.time() - base
    exec_time.boucle()
    stop = time.time() - base
    return start, stop


def interface_gui():
    def visualize_runtimes(results, title):
        print(results)
        start, stop = np.array(results).T
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        fig, ax = plt.subplots()
        plt.barh(range(len(start)), stop - start, left=start)
        plt.grid(axis='x')
        plt.ylabel("Tasks")
        plt.xlabel("Seconds")
        plt.title(title)
        ax.text(0.05, 0.95, "Exec time: " + str(round(stop[-1] - start[0], 4)) + " seconds", transform=ax.transAxes,
                verticalalignment='top', bbox=props)
        plt.show()

    def boucle_simple(base=0):
        start = time.time() - base
        for i in (range(999999)):
            np.tanh(i)
        stop = time.time() - base
        res = "Temps d'exécution : " + str(stop - start) + " secondes"
        label_time.configure(text=res)

    def show_simple_loop(delta):
        res = "Temps d'exécution : " + str(delta) + " microsecondes"
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

    label_choice = tk.Label(window, text="Nombre de processus/threads à lancer (N) : ", font="Arial, 12", bd=20)
    label_choice.grid(column=0, row=4)
    nb_workers = tk.Spinbox(window, from_=1, to=100, font="Arial, 12")
    nb_workers.grid(column=1, row=4)

    button_simpleloop_python = tk.Button(window, text="Boucle simple (python)", font="Arial, 12", bg="#e77f67",
                                         command=boucle_simple)
    button_simpleloop_python.grid(column=0, row=1)
    button_multiprocess_python = tk.Button(window, text="Boucle découpée en N processus (Python)",
                                           font="Arial, 12", bg="#e77f67",
                                           command=lambda: visualize_runtimes(
                                               multiprocessing(boucle, 16, int(nb_workers.get())),
                                               "Python: multiprocessing"))
    button_multiprocess_python.grid(column=0, row=2)
    button_multithreads_python = tk.Button(window, text="Boucle découpée en N threads (Python)",
                                           font="Arial, 12", bg="#e77f67",
                                           command=lambda: visualize_runtimes(
                                               multithreading(boucle, 16, int(nb_workers.get())),
                                               "Python: multithreading"))
    button_multithreads_python.grid(column=0, row=3)

    button_simpleloop_cpp = tk.Button(window, text="Boucle simple (C++)", font="Arial, 12", bg="#786fa6",
                                      command=lambda: show_simple_loop(exec_time.simple_loop()))
    button_simpleloop_cpp.grid(column=1, row=1)
    button_multiprocess_cpp = tk.Button(window, text="Boucle découpée en N processus (C++)", font="Arial, 12",
                                        bg="#786fa6",
                                        command=lambda: visualize_runtimes(
                                            exec_time.process_exec_time(int(nb_workers.get())), "C++: multiprocessing"))
    button_multiprocess_cpp.grid(column=1, row=2)
    button_multithreads_cpp = tk.Button(window, text="Boucle découpée en N threads (C++)",
                                        font="Arial, 12", bg="#786fa6",
                                        command=lambda: visualize_runtimes(
                                            exec_time.thread_exec_time(int(nb_workers.get())), "C++: multithreading"))
    button_multithreads_cpp.grid(column=1, row=3)

    label_time = tk.Label(window,
                          text="Cliquez sur une des stratégies pour afficher son temps d'exécution pour 16 itérations",
                          font="Arial, 12", bg="white", relief="ridge", padx=5, pady=5, bd=5)
    label_time.grid(column=0, row=5)

    window.mainloop()


if __name__ == "__main__":
    interface_gui()
