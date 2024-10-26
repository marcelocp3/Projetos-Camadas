
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import windows

class signalMeu:
    def __init__(self):
        self.init = 0

    def __init__(self):
        self.init = 0

 
    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        # W = windows.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        # yf = fft(signal*W)
        yf = fft(signal)
        
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs):
        x,y = self.calcFFT(signal, fs)
        plt.figure()
        plt.plot(x, np.abs(y))
        plt.xlim(500, 2000)
        plt.title('Fourier')
        plt.show()
        
        return x, y
