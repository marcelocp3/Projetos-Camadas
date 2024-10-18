#importe as bibliotecas
from suaBibSignal import signalMeu
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys

# Frequências DTMF
dtmf_freq = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '0': (941, 1336)
}

#funções caso queriam usar para sair...
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db
def todB(s):
    sdB = 10*np.log10(s)
    return sdB

def main():
    print("Inicializando encoder")
    tecla = input("Digite uma tecla de 0 a 9: ")
    
    if tecla not in dtmf_freq:
        print("Tecla inválida")
        return

    freq1, freq2 = dtmf_freq[tecla]
    print(f"Gerando Tom referente ao símbolo : {tecla}")
    
    # Parâmetros
    fs = 44100  # Taxa de amostragem
    duration = 2  # Duração do sinal em segundos
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    # Gera as senoides
    senoide1 = np.sin(2 * np.pi * freq1 * t)
    senoide2 = np.sin(2 * np.pi * freq2 * t)
    signal = senoide1 + senoide2
    
    # Reproduz o som
    sd.play(signal, fs)
    sd.wait()  # Aguarda o fim da reprodução
    
    # Plota o gráfico no domínio do tempo
    plt.figure()
    plt.plot(t[:1000], signal[:1000])
    plt.title(f"Sinal no Tempo - Tecla {tecla}")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Amplitude")
    plt.grid()

    # Utiliza a classe signalMeu para calcular e plotar a FFT
    signal_meu = signalMeu()
    signal_meu.plotFFT(signal, fs)

    plt.show()

if __name__ == "__main__":
    main()
