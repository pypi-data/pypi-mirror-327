import numpy as np
import scipy.fft as fft
import scipy.signal.windows as window
import scipy.signal as scisig
from scipy.sparse.linalg import spsolve
import scipy.stats as scistats
import statistics
from typing import Optional, Tuple, List, Union


import numpy as np
from scipy import fft, signal
from typing import Optional, Tuple

def get_FFT(
    time_signal: np.ndarray,
    sampling_freq: float,
    scaling_factor: float,
    shift_bool: Optional[bool] = True,
    window_func: Optional[str] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Get FFT Function: find the Fast Fourier Transform (FFT) for a specific time signal

    Inputs:
        time_signal: (numpy array)
            time signal of interest.
        sampling_freq: (float)
            sampling frequency corresponding to the time signal of interest.
        scaling_factor: (float)
            scaling factor for the FFT
        shift_bool: (boolean, optional, default = True)
            boolean if the FFT should be shifted with fftshift or not.
        window_func: (str, optional, default = 'hann')
            string specifying the window function corresponding to scipy.signal.windows to apply. Options include 'hann', 'hamming', 'blackman', etc.

    Returns:
        FFT_Freq: (array like)
            FFT frequency array.
        FFT_signal: (array like)
            Absolute Value of the FFT of the time signal of interest.
    Notes:
        This function returns the absolute value of the FFT signal.
    """

    # Function:
    N = len(time_signal)
    T = 1 / sampling_freq

    # Dictionary to map window function names to scipy.signal window functions
    window_functions = {
        'hann': signal.windows.hann,
        'hamming': signal.windows.hamming,
        'blackman': signal.windows.blackman,
        'bartlett': signal.windows.bartlett,
        'flattop': signal.windows.flattop,
        'parzen': signal.windows.parzen,
        'bohman': signal.windows.bohman,
        'blackmanharris': signal.windows.blackmanharris,
        'nuttall': signal.windows.nuttall,
        'barthann': signal.windows.barthann,
        'cosine': signal.windows.cosine,
        'exponential': signal.windows.exponential,
        'tukey': signal.windows.tukey,
        'taylor': signal.windows.taylor,
    }

    if window_func in window_functions:
        hw = window_functions[window_func](N)
        A = len(hw) / sum(hw)
    else:
        hw = 1
        A = 1

    FFT_signal = fft.fft(time_signal * hw) * A * scaling_factor / N
    FFT_freq = fft.fftfreq(len(time_signal), T)

    # Initializing Output Variables
    output1 = None
    output2 = None

    if shift_bool:
        output1 = fft.fftshift(FFT_freq)
        output2 = abs(fft.fftshift(FFT_signal))
    else:
        output1 = FFT_freq
        output2 = abs(FFT_signal)

    return output1, output2


def spectral_kurtosis(
    time_signal: np.ndarray,
    sampling_freq: float,
    Nw: int,
    No: int,
    window_stft: Optional[str] = "hann",
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Spectral kurtosis function: Find the spectural kurtosis for a specific time signal and sampling frequency for a given window and overlap length.

    Inputs:
        time_signal: (numpy array)
            time signal of interest.
        sampling_freq: (float)
            sampling frequency corresponding to the time signal of interest.
        Nw: (int)
            Window Length.
        No: (int)
            Window Overlap Length.
        window_stft: (string, optional, default = 'hann')
            window type to be applied. This variable should not be set to "None"

    Returns:
        freq: (array like)
            STFT frequency array
        t_stft: (array like)
            STFT time points (from scipy.signal.stft function) corresponding to the time signal of interest
        signal_stft: (array like)
            STFT (from scipy.signal.stft function) corresponding to the time signal of interest
    Notes:
        Signal windowing is always applied
    """

    # Function:
    freq, t_stft, signal_stft = scisig.stft(
        x=time_signal, fs=sampling_freq, window=window_stft, nperseg=Nw, noverlap=No
    )
    SK_list = []
    for i in range(len(freq)):
        # SK = (1/len(t) * np.sum(np.abs(signal_stft[i,:])**4)) / ((  1/len(t) * np.sum(np.abs(signal_stft[i,:]))**2  )**2) - 2
        SK = (
            np.mean(np.abs(signal_stft[i, :]) ** 4)
            / (np.mean(((np.abs(signal_stft[i, :]) ** 2))) ** 2)
            - 2
        )  # Formula from MEV781 course
        SK_list.append(SK)
    return freq, t_stft, signal_stft, SK_list


def spectral_kurtosis_plot(  # this function is incomplete
    signal_array: np.ndarray,
    time_array: np.ndarray,
    sampling_freq: float,
    Nw: int,
    No: int,
    window_stft: Optional[str] = "hann",
) -> None:
    """
    this function is incomplete

    Get FFT Function

    Inputs:


    Returns:
        freq: (array like)
            STFT frequency array
        t_stft: (array like)
            STFT time points (from scipy.signal.stft function) corresponding to the time signal of interest
        signal_stft: (array like)
            STFT (from scipy.signal.stft function) corresponding to the time signal of interest
    Notes:
        Signal windowing is always applied
    """

    # Imports:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import cm

    Nw_list = 2 ** np.arange(2, Nw)
    No_list = Nw_list[1] / 2
    fig = plt.figure(figsize=(10, 10))
    fig.tight_layout()
    ax = plt.axes(projection="3d")
    ax.set_title(
        "Spectral Kurtosis Contour For Varying Window Lengths and Overlap Lengths"
    )
    ax.set_box_aspect(aspect=None, zoom=0.95)
    res = int(5e3)
    x_mat = np.zeros(shape=(len(Nw_list), res))
    y_mat = np.zeros(shape=(len(Nw_list), res))
    z_mat = np.zeros(shape=(len(Nw_list), res))

    for i in range(len(Nw_list)):
        # for i in range(len(No_list)):
        freq, t_stft, signal_stft, SK_i = spectral_kurtosis(
            signal=signal_array,
            sample_freq=len(signal_array) / time_array[-1],
            Nw=Nw_list[i],
            No=No_list,
        )

        ax[i, 0].set_title(
            "Window Length of {}, With Overlap Length {}".format(Nw_list[i], No_list[i])
        )
        # plt.plot(*abs(x_stft_damaged), color = 'green', label = 'Hanning Windowed Healthy FFT')#, alpha = 0.5)
        # plt.show()
        vmin_stft = 0
        vmax_stft = (np.max(signal_array) - np.min(signal_array)) / ((i * 7) + 20)
        # print(vmax_stft)
        ax[i, 0].pcolormesh(
            t_stft,
            freq,
            abs(signal_stft),
            shading="gouraud",
            vmin=vmin_stft,
            vmax=vmax_stft,
        )
        ax[i, 0].set_xlabel("Time [seconds]")
        ax[i, 0].set_ylabel("Frequency [Hz]")

        ax[i, 1].set_title(
            "Window Length of {}, With Overlap Length {}".format(Nw_list[i], No_list[i])
        )
        ax[i, 1].plot(SK_i, freq)
        ax[i, 1].set_xlabel("Spectural Kurtosis Magnitude")
        ax[i, 1].set_ylabel("Frequency [Hz]")
        # ax[j, i].plot(freq, SK_i, color = 'red')
        # ax[j, i].pcolormesh(t_stft_i, freqs_stft_i, abs(x_stft_damaged_i), shading='gouraud')

        # ax[j, i].set_ylim(None, 15000)
        # ax[j, i].set_xlim(None, 0.5)
    X = x_mat
    Y = y_mat
    Z = z_mat
    # Normalize to [0,1]
    norm = plt.Normalize(Z.min(), Z.max())
    colors_contour = cm.viridis_r(norm(Z))
    ax.plot_surface(X, Y, Z, cmap="viridis_r", lw=3, rstride=1, cstride=1, alpha=0.5)
    # ax.plot_wireframe(X, Y, Z, rstride = 3, cstride = 100)#, alpha=0.5)
    ax.contour(
        X, Y, Z, zdir="z", stride=5, cmap="viridis_r", linestyles="solid", offset=0
    )
    ax.contour(X, Y, Z, zdir="z", stride=5, colors="k", linestyles="solid")

    ax.set_xlabel("Frequency [Hz]", labelpad=20)
    ax.set_ylabel("Window Length", labelpad=20)
    ax.set_zlabel("SK Magnitude", labelpad=5)

def filter(order: int, F_cutoff: np.ndarray, Fs: float, x: np.ndarray) -> np.ndarray:
    """
    Input:
    filter order: (integer), cutoff limits, Sampling frequency, signal
    """
    F_cutoff = np.array(F_cutoff)
    nyq = 0.5 * Fs
    F_c = F_cutoff / nyq
    sos = scisig.butter(N=order, Wn=F_c, btype="bandpass", analog=False, output="sos")
    filtered = scisig.sosfilt(sos, x)
    return filtered


# filter_low, filter_high = [5500, 9000] #From SK contour
# # filter_low, filter_high = [6000, 9500] #From SK contour

def get_statistics(
    data: np.ndarray, round_to: Optional[int] = 4
) -> Tuple[float, float, float, float, float, float, float, float]:
    """
    Input:
    data (array)
    round_to (int, optional)

    Returns:
    minimum, maximum, mean, variance, skewness, kurtosis, Root Mean Square (RMS), Crest Factor (CF)
    """
    minn = np.round(np.min(data), round_to)
    maxx = np.round(np.max(data), round_to)

    mean = np.round(np.mean(data), round_to)
    var = np.round(statistics.variance(data), round_to)
    skew = np.round(scistats.skew(data), round_to)
    kurtosis = np.round(scistats.kurtosis(data), round_to)
    RMS = np.round(np.sqrt(np.sum(data**2)), round_to)
    CF = np.round(np.max(data) / np.sqrt(np.sum(data**2)), round_to)

    return minn, maxx, mean, var, skew, kurtosis, RMS, CF

def TSA(
    raw_signal: np.ndarray,
    Nr: int,
    speed: float,
    sampling_frequency: float,
    Ns: Optional[int] = None,
) -> np.ndarray:
    """
    Time Synchronous Averaging (TSA) is a signal processing method used to reduce noise and extract periodic components from a signal.

    THIS FUNCTION ASSUMES CONSTANT SPEED!!!

    Parameters
    ----------
    raw_signal : np.ndarray
        The raw input signal to be processed. This signal should contain more revolutions than the specified Nr value.
    Nr : int
        The number of rotations to be be considered from the time signal. The length of the signal should be perfectly divisible by Nr
    speed: float
        The rotational speed of the shaft in RPM corresponding to the input signal.
    sampling_frequency: float
        The sampling frequency of the signal.

    Optional Parameters
    -------------------
    Ns : int, optional
        The number of points per shaft rotation. This is usually set to the number of points per shaft rotation. If not provided, Ns is calculated from the speed and sampling frequency.
        One might want to provide this variable if an interpolated signal is provided where the number of points per shaft rotation does not correspond to the calculated value from the speed and sampling frequency.

    Returns
    -------
    np.ndarray
        The processed signal after applying TSA.
    """
    if Ns is None:
        Ns = int(
            1 / (speed / 60) * sampling_frequency
        )  # Number of points per shaft rotation

    # Ns = len(signal) // Nr # number of points for averaging. This is usually set to the number of points per shaft rotation - THIS ISNT A CLEVER WAY TO DO IT

    signal = raw_signal[
        : Nr * Ns
    ]  # contracting the signal to the correct length for the number of rotations considered

    sig_list = np.zeros(shape=(Nr, Ns))
    for i in range(0, Nr):
        sig_list[i, :] = signal[i * Ns : Ns + i * Ns]

    return np.resize((1 / Nr) * np.sum(sig_list, axis=0), len(signal))
