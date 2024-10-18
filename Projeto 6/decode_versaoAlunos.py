#Importe todas as bibliotecas
from suaBibSignal import signalMeu
import peakutils
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time

# Frequências DTMF
dtmf_freq = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3',
    (770, 1209): '4', (770, 1336): '5', (770, 1477): '6',
    (852, 1209): '7', (852, 1336): '8', (852, 1477): '9',
    (941, 1336): '0'
}

#função para converter intensidade acústica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return sdB

def identificar_tecla(freqs):
    for (f1, f2), tecla in dtmf_freq.items():
        if min(abs(f1 - freqs[0]), abs(f1 - freqs[1])) < 5 and min(abs(f2 - freqs[0]), abs(f2 - freqs[1])) < 5:
            return tecla
    return None

def main():
    print("Inicializando decoder")
    
    # Parâmetros de gravação
    fs = 44100  # Taxa de amostragem
    duration = 5  # Duração em segundos
    sd.default.samplerate = fs
    sd.default.channels = 1
    
    print(f"Iniciando gravação em {duration} segundos...")
    for i in range(5):
        print(f"Gravando em {5-i}...")
        time.sleep(1)
    print("Gravando...")
    
    # Gravação
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Gravação finalizada.")
    
    # Processando o sinal
    audio = audio.flatten()  # Se necessário, converte para 1D
    t = np.linspace(0, duration, len(audio), endpoint=False)
    
    # Plota o áudio captado no domínio do tempo
    plt.figure()
    plt.plot(t[:1000], audio[:1000])
    plt.title("Sinal Gravado no Tempo")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Amplitude")
    plt.grid()

    # Utiliza a classe signalMeu para calcular a FFT
    signal_meu = signalMeu()
    xf, yf = signal_meu.calcFFT(audio, fs)
    
    # Plota a Transformada de Fourier
    plt.figure()
    plt.plot(xf, np.abs(yf))
    plt.title("Transformada de Fourier do Sinal Gravado")
    plt.xlabel("Frequência [Hz]")
    plt.ylabel("Amplitude")
    plt.grid()
    
    # Identifica os picos
    indices = peakutils.indexes(np.abs(yf), thres=0.3, min_dist=50)
    freqs_picos = xf[indices]
    print(indices)

    
    print(f"Frequências detectadas: {freqs_picos}")
    
    # Identifica a tecla pressionada
    tecla = identificar_tecla(freqs_picos)
    
    if tecla:
        print(f"A tecla pressionada foi: {tecla}")
    else:
        print("Tecla não reconhecida.")
    
    plt.show()

if __name__ == "__main__":
    main()
