import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Configuração da GUI
root = tk.Tk()
root.title("Calculadora de Frequência de Corda")
root.configure(bg='black')
root.geometry("500x400")  # Define o tamanho da janela

# Variável para controlar o estado de reprodução do som
is_playing = False
current_wave = None
fs = 44100  # Frequência de amostragem

# Função para calcular a frequência
def calcular_frequencia(densidade, tensao, comprimento):
    frequencia = (1 / (2 * comprimento)) * np.sqrt(tensao / densidade)
    return frequencia

# Função para gerar a onda da frequência
def gerar_onda(frequencia):
    global current_wave
    t = np.linspace(0, 1, fs, endpoint=False)
    current_wave = 0.5 * np.sin(2 * np.pi * frequencia * t)

# Função para tocar ou parar a frequência
def tocar_ou_parar_frequencia():
    global is_playing
    if is_playing:
        sd.stop()
        button_calcular.config(text="Calcular e Tocar Frequência")
        is_playing = False
    else:
        try:
            densidade = float(entry_densidade.get())
            tensao = float(entry_tensao.get())
            comprimento = float(entry_comprimento.get())
            frequencia = calcular_frequencia(densidade, tensao, comprimento)
            gerar_onda(frequencia)
            sd.play(current_wave, fs, loop=True)
            messagebox.showinfo("Frequência Calculada", f"A frequência é {frequencia:.2f} Hz")
            button_calcular.config(text="Parar Frequência")
            is_playing = True
            # Chamar a função para animar a corda
            animar_corda(frequencia, comprimento)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos")

# Função para animar a corda vibrando
def animar_corda(frequencia, comprimento):
    fig, ax = plt.subplots()
    x = np.linspace(0, comprimento, 500)
    line, = ax.plot(x, np.zeros_like(x))
    
    def update(frame):
        y = np.sin(2 * np.pi * frequencia * (x / comprimento) - frame / fs)
        line.set_ydata(y)
        return line,
    
    # Ajuste dos limites dos eixos para melhor visualização
    ax.set_ylim(-1, 1)
    ax.set_xlim(0, comprimento)
    ani = FuncAnimation(fig, update, frames=np.arange(0, fs), blit=True, interval=20)
    plt.xlabel('Comprimento da Corda (m)')
    plt.ylabel('Deslocamento (m)')
    plt.title('Animação da Corda Vibrando')
    plt.show()

# Criação dos campos de entrada
tk.Label(root, text="Comprimento da Corda (m):", bg='black', fg='white', font=("Helvetica", 14)).pack(pady=10)
entry_comprimento = tk.Entry(root, bg='lightgray', fg='black', font=("Helvetica", 14), width=20)
entry_comprimento.pack(pady=10)

tk.Label(root, text="Tensão na Corda (N):", bg='black', fg='white', font=("Helvetica", 14)).pack(pady=10)
entry_tensao = tk.Entry(root, bg='lightgray', fg='black', font=("Helvetica", 14), width=20)
entry_tensao.pack(pady=10)

tk.Label(root, text="Densidade Linear da Corda (kg/m):", bg='black', fg='white', font=("Helvetica", 14)).pack(pady=10)
entry_densidade = tk.Entry(root, bg='lightgray', fg='black', font=("Helvetica", 14), width=20)
entry_densidade.pack(pady=10)

# Definir valores padrão nos campos de entrada
entry_densidade.insert(0, "1.2")  # Densidade em kg/m
entry_comprimento.insert(0, "1.0")  # Comprimento em m

button_calcular = tk.Button(root, text="Calcular e Tocar Frequência", command=tocar_ou_parar_frequencia, bg='gray', fg='black', font=("Helvetica", 14))
button_calcular.pack(pady=20)

# Centralizando os elementos
for widget in root.winfo_children():
    widget.pack_configure(anchor='center')

root.mainloop()
