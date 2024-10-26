import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import find_peaks
import sounddevice as sd
import time

# Lista de frequências DTMF, onde o índice representa a tecla correspondente
# Teclas correspondentes aos índices: 0='0', 1='1', 2='2', 3='3', 4='4', 5='5', 6='6', 7='7', 8='8', 9='9'
lista_frequencias = [[941, 1336], [679, 1209], [679, 1336], [679, 1477], 
                     [770, 1209], [770, 1336], [770, 1477], 
                     [825, 1209], [825, 1336], [825, 1477],[679,1633],[770,1633],[825,1633],[941,1209],[941,1209],[941,1477]]

# Função para identificar a tecla DTMF com base nas duas frequências
def identify_dtmf(frequencies):
    # Encontrar o índice na lista de frequências que tem a menor diferença total para o par de frequências fornecido
    closest_freq_index = np.argmin([abs(f[0] - frequencies[0]) + abs(f[1] - frequencies[1]) for f in lista_frequencias])
    return closest_freq_index

# Função para detectar picos das frequências
def detect_dtmf(signal, sample_rate):
    # Calcular a transformada de Fourier
    n = len(signal)
    yf = fft(signal)
    xf = np.fft.fftfreq(n, 1 / sample_rate)

    # Manter apenas a metade positiva do espectro
    positive_xf = xf[:n // 2]
    positive_yf = np.abs(yf[:n // 2])

    # Identificar os picos no espectro de frequência
    peaks, _ = find_peaks(positive_yf, height=0.5 * np.max(positive_yf))
    peak_freqs = positive_xf[peaks]

    # Filtrar apenas as frequências DTMF
    valid_freqs = [f for f in peak_freqs if 600 < f < 1700]

    if len(valid_freqs) >= 2:
        # Ordenar as frequências e pegar as duas mais fortes
        valid_freqs = sorted(valid_freqs)[:2]
        return identify_dtmf(valid_freqs), positive_xf, positive_yf
    else:
        return None, positive_xf, positive_yf

# Função para gravar o som e detectar as frequências DTMF
def detectar_dtmf_gravacao(duracao, fs=8000):
    time.sleep(1)  # Aguardar 1 segundo antes de começar a gravar
    print(f"Gravando por {duracao} segundos...")

    # Grava o áudio
    gravacao = sd.rec(int(duracao * fs), samplerate=fs, channels=1, dtype='float64')
    sd.wait()  # Esperar até que a gravação termine

    # Converter a gravação para uma array unidimensional
    sinal = gravacao[:, 0]

    # Detectar a tecla DTMF a partir do áudio gravado e obter o espectro de frequência
    detected_key_index, freqs, spectrum = detect_dtmf(sinal, fs)

    if detected_key_index is not None:
        if detected_key_index == 10:
            print("A tecla detectada é: A")
        elif detected_key_index == 11:
            print("A tecla detectada é: B")
        elif detected_key_index == 12:
            print("A tecla detectada é: C")
        elif detected_key_index == 13:
            print("A tecla detectada é: D")
        elif detected_key_index == 14:
            print("A tecla detectada é: *")
        elif detected_key_index == 15:
            print("A tecla detectada é: #")
        elif detected_key_index < 10:
            print(f"A tecla detectada é: {detected_key_index}")
    else:
        print("Nenhuma tecla foi detectada.")

    # Criar o primeiro gráfico: Sinal no domínio do tempo
    plt.figure()
    t = np.linspace(0, duracao, len(sinal))
    plt.plot(t[:1000], sinal[:1000])  # Tempo
    plt.plot(t, sinal)
    plt.title('Sinal no Domínio do Tempo')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Amplitude')
    plt.grid()

    # Criar o segundo gráfico: Espectro de frequência
    plt.figure()
    plt.plot(freqs, spectrum)
    plt.title('Espectro de Frequência')
    plt.xlabel('Frequência [Hz]')
    plt.ylabel('Magnitude')
    plt.grid()
    plt.show()

# Exemplo de uso: gravação de áudio e detecção da tecla DTMF
if __name__ == '__main__':
    # Definir parâmetros de gravação
    duracao = 4  # Duração da gravação em segundos

    # Gravar e detectar tecla DTMF
    detectar_dtmf_gravacao(duracao)
