import os
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, messagebox

def load_data(filename):
    data = np.genfromtxt(filename, delimiter=',')
    return data

def save_data(filename, data):
    np.savetxt(filename, data, delimiter=',')

def plot_data(signals, titles):
    num_signals = len(signals)
    fig, axs = plt.subplots(1, num_signals, figsize=(15, 5))

    for i in range(num_signals):
        axs[i].plot(signals[i])
        axs[i].set_title(titles[i])
        axs[i].set_xlabel('Czas [s]')
        axs[i].set_ylabel('Amplituda')
        axs[i].grid(True)

    plt.tight_layout()
    plt.show()

def select_files():
    root = Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(initialdir="./dane", title="Wybierz pliki",
                                        filetypes=(("Pliki CSV", "*.csv"), ("Wszystkie pliki", "*.*")))
    if len(files) == 2:
        return files
    elif len(files) == 0:
        messagebox.showinfo("Info", "Nie wybrano żadnych plików. Program zostanie zakończony.")
        exit()
    else:
        messagebox.showerror("Błąd", "Proszę wybrać dokładnie dwa pliki.")
        return select_files()


def convolution(signal1, signal2):
    n1 = len(signal1)
    n2 = len(signal2)
    result_length = n1 + n2 - 1
    result = np.zeros(result_length)

    for i in range(n1):
        for j in range(n2):
            result[i + j] += signal1[i] * signal2[j]

    start = (result_length - n1) // 2
    return result[start:start + n1]

files = select_files()
signals = [load_data(file) for file in files]

convolved_signal = convolution(signals[0], signals[1])

titles = [os.path.basename(file) for file in files]
titles.append('Splot Sygnałów')
signals.append(convolved_signal)
plot_data(signals, titles)

save_data('convolved_signal.csv', convolved_signal)
