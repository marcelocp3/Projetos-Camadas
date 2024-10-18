import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift
from scipy import signal as window



class signalMeu:
    def __init__(self):
        self.init = 0

    def __init__(self):
        self.init = 0

 
    def calcFFT(self,signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        #y  = np.append(signal, np.zeros(len(signal)*fs))
        N  = len(signal)
        T  = 1/fs
        xf = np.linspace(-1.0/(2.0*T), 1.0/(2.0*T), N)
        yf = fft(signal)
        return(xf, fftshift(yf))

    def plotFFT(self, signal, fs):
        x,y = self.calcFFT(signal, fs)
        plt.figure()
        plt.plot(x, np.abs(y))
        plt.title('Fourier')
