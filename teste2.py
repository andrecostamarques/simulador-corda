import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
from threading import Timer

# Global variable to control sound playback
playing = False
current_wave = None
slider_update_timer = None

def onda_sonora_corda(densidade, tensao, comprimento, tempo, amplitude_max=1):
    def calcular_frequencia(densidade, tensao, comprimento):
        frequencia = (1 / (2 * comprimento)) * np.sqrt(tensao / densidade)
        return frequencia

    frequencia = calcular_frequencia(densidade, tensao, comprimento)
    velocidade = np.sqrt(tensao / densidade)
    k = 2 * np.pi / (comprimento)
    amplitude = amplitude_max * (comprimento / np.pi)
    posicao = np.linspace(0, comprimento, 1000)
    t = np.linspace(0, tempo, 1000)
    onda = np.zeros((len(posicao), len(t)))

    for i in range(len(posicao)):
        for j in range(len(t)):
            onda[i, j] = amplitude * np.sin(k * posicao[i] - 2 * np.pi * frequencia * t[j])

    return posicao, t, onda, frequencia

def generate_wave(frequency, duration=1.0, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return wave, sample_rate

def play_frequency(frequency):
    global playing, current_wave
    current_wave, sample_rate = generate_wave(frequency)
    sd.play(current_wave, sample_rate, loop=True)

def stop_frequency():
    sd.stop()

def on_calculate():
    global playing
    try:
        comprimento = float(entry_comprimento.get())
        tensao = float(slider_tensao.get())
        tensao = tensao * 1000
        densidade = float(entry_densidade.get())

        posicao, t, onda, frequencia = onda_sonora_corda(densidade, tensao, comprimento, tempo)
        label_result.config(text=f"Frequência: {frequencia:.2f} Hz")

        if not playing:
            playing = True
            play_frequency(frequencia)
            button_calculate.config(text="Parar o Som", command=on_stop)
            plot_wave(posicao, t, onda, comprimento)
    except ValueError:
        messagebox.showerror("Input Error", "Por favor, insira valores numéricos válidos.")

def on_stop():
    global playing
    playing = False
    stop_frequency()
    button_calculate.config(text="Calcular e Tocar Frequência", command=on_calculate)

def plot_wave(posicao, t, onda, comprimento):
    fig, ax = plt.subplots()
    line, = ax.plot(posicao, onda[:, 0], lw=2)
    ax.set_ylim(-1.2 * amplitude_max, 1.2 * amplitude_max)
    ax.set_xlim(0, comprimento)
    ax.set_xlabel('Posição na Corda (m)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Onda Sonora da Corda')

    def animate(i):
        line.set_ydata(onda[:, i])
        return line,

    ani = FuncAnimation(fig, animate, frames=len(t), interval=50)
    plt.show()

def update_sound(val):
    global slider_update_timer
    if slider_update_timer is not None:
        slider_update_timer.cancel()
    slider_update_timer = Timer(0.1, apply_update_sound)
    slider_update_timer.start()

def apply_update_sound():
    global playing
    if playing:
        comprimento = float(entry_comprimento.get())
        tensao = slider_tensao.get() * 1000
        densidade = float(entry_densidade.get())
        _, _, _, frequencia = onda_sonora_corda(densidade, tensao, comprimento, tempo)
        play_frequency(frequencia)
        label_result.config(text=f"Frequência: {frequencia:.2f} Hz")

tempo = 1.0
amplitude_max = 1

# Create the main window
root = tk.Tk()
root.title("Calculadora de Frequência de Corda")

# Set the black background color
root.configure(bg="black")

# Set the window to be resizable and responsive
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a frame to hold the widgets with padding and background color
frame = tk.Frame(root, bg="black", padx=20, pady=20)
frame.grid(sticky='nsew')

# Create and place the widgets with larger font size for zoom effect
tk.Label(frame, text="Comprimento da Corda (m):", bg="black", fg="white", font=("Helvetica", 14)).grid(row=0, column=0, sticky='e', pady=10)
entry_comprimento = tk.Entry(frame, font=("Helvetica", 14))
entry_comprimento.grid(row=0, column=1, sticky='w', padx=20)
entry_comprimento.insert(0, "1.0")

tk.Label(frame, text="Tensão na Corda (KN):", bg="black", fg="white", font=("Helvetica", 14)).grid(row=1, column=0, sticky='e', pady=10)
slider_tensao = tk.Scale(frame, from_=450, to=1900, orient=tk.HORIZONTAL, length=300, bg="black", fg="white", font=("Helvetica", 14), command=update_sound)
slider_tensao.grid(row=1, column=1, sticky='w', padx=20)
slider_tensao.set(929)

tk.Label(frame, text="Densidade Linear da Corda (kg/m):", bg="black", fg="white", font=("Helvetica", 14)).grid(row=2, column=0, sticky='e', pady=10)
entry_densidade = tk.Entry(frame, font=("Helvetica", 14))
entry_densidade.grid(row=2, column=1, sticky='w', padx=20)
entry_densidade.insert(0, "1.2")

button_calculate = tk.Button(frame, text="Calcular e Tocar Frequência", command=on_calculate, font=("Helvetica", 14))
button_calculate.grid(row=3, column=0, columnspan=2, pady=20)

label_result = tk.Label(frame, text="", bg="black", fg="white", font=("Helvetica", 14))
label_result.grid(row=4, column=0, columnspan=2, pady=10)

# Set grid column weights to make the layout responsive
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Start the main loop
root.mainloop()
