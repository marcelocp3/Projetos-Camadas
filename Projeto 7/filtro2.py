import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
from scipy.signal import freqz

# Parâmetros do filtro
fs = 44100  # Taxa de amostragem
fc = 2500   # Frequência de corte
zeta = 0.707  # Fator de amortecimento

# K = np.tan((np.pi * fc) / fs)
    
# Cálculo dos coeficientes
a = 0.05345
b = 0.04517
d = -1.506
e = 0.6043

# Função para aplicar o filtro passa-baixa de segunda ordem
def filtro(entrada,a,b,d,e):
    y = np.zeros_like(entrada)
    for n in range(2, len(entrada)):
        y[n] = (-d * y[n - 1]) - (e * y[n - 2]) + (a * entrada[n - 1]) + (b * entrada[n - 2])
    return y

# Gravação do áudio
duration = 5  # Duração da gravação em segundos
# print("Gravando...")
# audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
# sd.wait()

# So muda o aquirvo de audio
audio, samplerate = sf.read('__Hai Yorokonde - Kocchi no Kento__.mp3')
audio = audio.flatten()

# Aplicação do filtro
audio_filtrado = filtro(audio,a,b,d,e)

# Cálculo do ganho de saída em relação à entrada
ganho_dB = 20 * np.log10(np.max(np.abs(audio_filtrado)) / np.max(np.abs(audio)))
print(f"Ganho da saída em relação à entrada: {ganho_dB:.2f} dB")

# Exibir o áudio original e o áudio filtrado
t = np.linspace(0, duration, len(audio), endpoint=False)
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t, audio)
plt.title("Sinal Original")
plt.xlabel("Tempo [s]")
plt.ylabel("Amplitude")

plt.subplot(2, 1, 2)
plt.plot(t, audio_filtrado)
plt.title("Sinal Filtrado (Passa-Baixa de Segunda Ordem)")
plt.xlabel("Tempo [s]")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()

# Diagrama de Bode
w, h = freqz([a, b], [1, d, e], fs=fs)
plt.figure(figsize=(10, 6))

# Magnitude em dB
plt.subplot(2, 1, 1)
plt.plot(w, 20 * np.log10(abs(h)))
plt.title("Diagrama de Bode - Magnitude")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Magnitude [dB]")
plt.grid()

# Fase em graus
plt.subplot(2, 1, 2)
angles = np.unwrap(np.angle(h))
plt.plot(w, np.degrees(angles))
plt.title("Diagrama de Bode - Fase")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Fase [graus]")
plt.grid()

plt.tight_layout()
plt.show()

# Reproduzir o áudio filtrado na mesma taxa de amostragem
sd.play(audio_filtrado, samplerate)
sd.wait()
