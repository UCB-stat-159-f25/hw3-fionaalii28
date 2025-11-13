import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# whiten the data
def whiten(strain, interp_psd, dt):
    Nt = len(strain)
    freqs = np.fft.rfftfreq(Nt, dt)
    hf = np.fft.rfft(strain)
    norm = 1.0 / np.sqrt(1.0 / (dt * 2))
    white_hf = hf / np.sqrt(interp_psd(freqs)) * norm
    white_ht = np.fft.irfft(white_hf, n=Nt)
    return white_ht


# write strain data to a wav file
def write_wavfile(filename, fs, data):
    d = np.int16(data / np.max(np.abs(data)) * 32767 * 0.9)
    wavfile.write(filename, int(fs), d)


# shift the frequency of a signal
def reqshift(data, fshift=100, sample_rate=4096):
    """Frequency shift the signal by a constant value."""
    x = np.fft.rfft(data)
    T = len(data) / float(sample_rate)
    df = 1.0 / T
    nbins = int(fshift / df)
    y = np.roll(x.real, nbins) + 1j * np.roll(x.imag, nbins)
    y[0:nbins] = 0.0
    z = np.fft.irfft(y)
    return z


# plotting function for PSD/SNR/template visualization
def plot_func(time, timemax, SNR, pcolor, det, eventname, plottype,
              tevent, strain_whitenbp, template_match,
              data_psd, datafreq, template_fft, d_eff, freqs, fs):
    """Generate plots for matched filter SNR, whitened strain, and PSD comparisons."""

    # Plot SNR vs time
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(time - timemax, SNR, pcolor, label=det + ' SNR(t)')
    plt.grid(True)
    plt.ylabel('SNR')
    plt.xlabel(f'Time since {timemax:.4f}')
    plt.legend(loc='upper left')
    plt.title(det + ' matched filter SNR around event')

    plt.subplot(2, 1, 2)
    plt.plot(time - timemax, SNR, pcolor, label=det + ' SNR(t)')
    plt.grid(True)
    plt.ylabel('SNR')
    plt.xlim([-0.15, 0.05])
    plt.xlabel(f'Time since {timemax:.4f}')
    plt.legend(loc='upper left')
    plt.savefig(f'figures/{eventname}_{det}_SNR.{plottype}')

    # Plot whitened strain and template
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(time - tevent, strain_whitenbp, pcolor, label=det + ' whitened h(t)')
    plt.plot(time - tevent, template_match, 'k', label='Template(t)')
    plt.ylim([-10, 10])
    plt.xlim([-0.15, 0.05])
    plt.grid(True)
    plt.xlabel(f'Time since {timemax:.4f}')
    plt.ylabel('whitened strain (units of noise stdev)')
    plt.legend(loc='upper left')
    plt.title(det + ' whitened data around event')

    plt.subplot(2, 1, 2)
    plt.plot(time - tevent, strain_whitenbp - template_match, pcolor, label=det + ' resid')
    plt.ylim([-10, 10])
    plt.xlim([-0.15, 0.05])
    plt.grid(True)
    plt.xlabel(f'Time since {timemax:.4f}')
    plt.ylabel('whitened strain (units of noise stdev)')
    plt.legend(loc='upper left')
    plt.title(det + ' residual whitened data after subtracting template')
    plt.savefig(f'figures/{eventname}_{det}_matchtime.{plottype}')

    # Plot PSD and template comparison
    plt.figure(figsize=(10, 6))
    template_f = np.abs(template_fft) * np.sqrt(np.abs(datafreq)) / d_eff
    plt.loglog(datafreq, template_f, 'k', label='template(f)*sqrt(f)')
    plt.loglog(freqs, np.sqrt(data_psd), pcolor, label=det + ' ASD')
    plt.xlim(20, fs / 2)
    plt.ylim(1e-24, 1e-20)
    plt.grid(True)
    plt.xlabel('frequency (Hz)')
    plt.ylabel('strain noise ASD (strain/√Hz)')
    plt.legend(loc='upper left')
    plt.title(det + ' ASD and template around event')
    plt.savefig(f'figures/{eventname}_{det}_matchfreq.{plottype}')
