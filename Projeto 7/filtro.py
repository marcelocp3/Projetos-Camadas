import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.signal import butter, lfilter
import soundfile as sf

# Configuração do filtro passa-baixa
def butter_lowpass(cutoff, fs, order=2):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=2):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Parâmetros do filtro
fs = 44100  # Taxa de amostragem
cutoff = 1000  # Frequência de corte em Hz

# Gravação de áudio (como no seu código)
duration = 5  # Duração da gravação em segundos
# print("Gravando áudio...")
# audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
audio, samplerate = sf.read("__Hai Yorokonde - Kocchi no Kento__.mp3")
sd.wait()
audio = audio.flatten()

# Aplicação do filtro passa-baixa
filtered_audio = lowpass_filter(audio, cutoff, fs)

# Exibir o áudio original e o filtrado no domínio do tempo
t = np.linspace(0, duration, len(audio), endpoint=False)
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t, audio)
plt.title("Sinal Original")
plt.xlabel("Tempo [s]")
plt.ylabel("Amplitude")

plt.subplot(2, 1, 2)
plt.plot(t, filtered_audio)
plt.title("Sinal Filtrado (Passa-Baixa)")
plt.xlabel("Tempo [s]")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()

# Reproduzir o áudio filtrado (opcional)
sd.play(filtered_audio, fs)
sd.wait()
