import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def onda_sonora_corda(densidade, tensao, comprimento, tempo, amplitude_max=1):
    # Função para calcular a frequência a partir de outros parâmetros
    def calcular_frequencia(densidade, tensao, comprimento):
        frequencia = (1 / (2 * comprimento)) * np.sqrt(tensao / densidade)
        return frequencia

    # Frequência da onda
    frequencia = calcular_frequencia(densidade, tensao, comprimento)

    # Velocidade de propagação da onda
    velocidade = np.sqrt(tensao / densidade)

    # Constante de onda
    k = 2 * np.pi / (comprimento)

    # Amplitude da onda
    amplitude = amplitude_max * (comprimento / np.pi)

    # Posição da corda
    posicao = np.linspace(0, comprimento, 1000)

    # Tempo
    t = np.linspace(0, tempo, 1000)

    # Onda sonora
    onda = np.zeros((len(posicao), len(t)))

    for i in range(len(posicao)):
        for j in range(len(t)):
            onda[i, j] = amplitude * np.sin(k * posicao[i] - 2 * np.pi * frequencia * t[j])

    return posicao, t, onda

# Parâmetros
densidade = 1.2  # densidade linear em g/cm^3
comprimento = 1  # comprimento em metros
tensao = 929280  # tensão em N (calculada anteriormente)
tempo = 1.0  # tempo em segundos
amplitude_max = 1  # amplitude máxima da onda

# Gerar a onda sonora da corda
posicao, t, onda = onda_sonora_corda(densidade, tensao, comprimento, tempo, amplitude_max)

# Configuração da animação
fig, ax = plt.subplots()
line, = ax.plot(posicao, onda[:, 0], lw=2)
ax.set_ylim(-1.2 * amplitude_max, 1.2 * amplitude_max)
ax.set_xlim(0, comprimento)
ax.set_xlabel('Posição na Corda (m)')
ax.set_ylabel('Amplitude')
ax.set_title('Onda Sonora da Corda')

# Função de animação
def animate(i):
    line.set_ydata(onda[:, i])
    return line,

# Criar animação
ani = FuncAnimation(fig, animate, frames=len(t), interval=50)

plt.show()
