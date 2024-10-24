import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt
import sounddevice as sd

# Solicitar a tecla
tecla = int(input("Digite a tecla (0-9): "))
frequencias = []  # Frequências da tecla
lista_teclas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
lista_frequencias = [[941, 1336], [679, 1209], [679, 1336], [679, 1477], 
                     [770, 1209], [770, 1336], [770, 1477], 
                     [825, 1209], [825, 1336], [825, 1477]]

# Verificar se a tecla é válida
if tecla in lista_teclas:
    print("Tecla válida")
    index = lista_teclas.index(tecla)
    frequencia1 = lista_frequencias[index][0]
    frequencia2 = lista_frequencias[index][1]
    frequencias.append(frequencia1)
    frequencias.append(frequencia2)
else:
    print("Tecla inválida")
    exit()

# Função para gerar a onda senoidal
def gerar_senoide(frequencias, fs, duracao):
    t = np.linspace(0, duracao, int(fs * duracao))  # Vetor de tempo
    sinal = np.zeros_like(t)
    for freq in frequencias:
        sinal += np.sin(2 * np.pi * freq * t)
    return t, sinal

# Função para aplicar a Transformada de Fourier
def aplicar_fourier(signal, fs):
    Y = fft(signal)
    frequencies = np.fft.fftfreq(len(Y), 1/fs)
    magnitude = np.abs(Y)
    return frequencies, magnitude

# Parâmetros da simulação
fs = 44100  # frequência de amostragem, 44.1 kHz (qualidade CD)
duracao = 4  # 2 segundos de duração

# Gerar a onda senoidal
t, sinal = gerar_senoide(frequencias, fs, duracao)

# Emitir o som gerado usando sounddevice
sd.play(sinal, fs)
sd.wait()  # Esperar até o som terminar

# Plotar o sinal no domínio do tempo (antes da Transformada de Fourier)
plt.figure(figsize=(10, 4))
plt.plot(t[:1000], sinal[:1000])  # Mostrar apenas os primeiros 1000 pontos para melhor visualização
plt.title("Sinal no Domínio do Tempo")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

# Aplicar a Transformada de Fourier
frequencies, magnitude = aplicar_fourier(sinal, fs)

# Plotar o espectro de frequências (depois da Transformada de Fourier)
plt.figure(figsize=(10, 4))
plt.plot(frequencies[:len(frequencies)//2], magnitude[:len(magnitude)//2])
plt.title("Espectro de Frequências (Transformada de Fourier)")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.show()
