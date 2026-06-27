"""FFT and DCT — frequency-domain signal processing with NumPy/SciPy.

Real-world relevance:
    Audio/image compression, sensor analysis, and signal filtering all
    depend on extracting frequency content from time-domain signals.

Core ideas:
    1. FFT converts a time-domain signal into its frequency components.
    2. DCT is similar but uses only real numbers — basis of JPEG & MP3.
    3. Filtering = zeroing unwanted FFT coefficients, then inverting.
    4. Nyquist theorem: maximum detectable frequency = sample_rate / 2.

References:
    https://numpy.org/doc/stable/reference/routines.fft.html
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.dct.html
    https://www.youtube.com/watch?v=spUNpyF58BY  (3Blue1Brown Fourier)
"""

from typing import TYPE_CHECKING

import numpy as np
from scipy.fft import dct, idct

if TYPE_CHECKING:
    from numpy.typing import NDArray


# ---------------------------------------------------------------------------
# Signal generation
# ---------------------------------------------------------------------------
def generate_test_signal(
    frequencies: list[float],
    amplitudes: list[float],
    sample_rate: float,
    duration: float,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Create a synthetic signal that is the sum of sinusoids.

    Each sinusoid has a frequency from *frequencies* and a corresponding
    amplitude from *amplitudes*.  The returned arrays are the time axis
    and the composite signal.

    >>> t, sig = generate_test_signal([440.0], [1.0], 8000.0, 0.01)
    >>> len(t) == len(sig) == int(8000.0 * 0.01)
    True
    """
    if len(frequencies) != len(amplitudes):
        msg = "frequencies and amplitudes must have the same length"
        raise ValueError(msg)

    # np.arange gives us one sample per 1/sample_rate seconds.
    n_samples = int(sample_rate * duration)
    t: NDArray[np.float64] = np.arange(n_samples, dtype=np.float64) / sample_rate

    # Build signal as the sum of sine waves:  A * sin(2*pi*f*t)
    signal: NDArray[np.float64] = np.zeros_like(t)
    for freq, amp in zip(frequencies, amplitudes, strict=True):
        signal = signal + amp * np.sin(2.0 * np.pi * freq * t)

    return t, signal


# ---------------------------------------------------------------------------
# Fast Fourier Transform
# ---------------------------------------------------------------------------
# The FFT decomposes a signal into complex exponentials (sines + cosines).
# The magnitude at each frequency bin tells us "how much" of that frequency
# is present.  The result is symmetric for real inputs, so we keep only
# the positive half.
# ---------------------------------------------------------------------------
def compute_fft(
    signal: NDArray[np.float64],
    sample_rate: float,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute FFT and return positive-frequency bins with magnitudes.

    Returns (frequency_bins, magnitudes) where both arrays cover only
    the range [0, sample_rate/2).  Magnitudes are normalized by N.

    >>> _, sig = generate_test_signal([100.0], [1.0], 1000.0, 1.0)
    >>> freqs, mags = compute_fft(sig, 1000.0)
    >>> float(freqs[np.argmax(mags)])
    100.0
    """
    n = len(signal)

    # np.fft.fft returns N complex coefficients.
    fft_result: NDArray[np.complex128] = np.fft.fft(signal)

    # np.fft.fftfreq maps each bin index to its frequency in Hz.
    freqs = np.asarray(np.fft.fftfreq(n, d=1.0 / sample_rate), dtype=np.float64)

    # Keep only positive frequencies (the negative half is the mirror).
    positive_mask: NDArray[np.bool_] = freqs >= 0
    freqs_pos: NDArray[np.float64] = freqs[positive_mask]

    # Magnitude = |complex coefficient| / N  (normalized)
    magnitudes: NDArray[np.float64] = np.abs(fft_result[positive_mask]) / n

    return freqs_pos, magnitudes


# ---------------------------------------------------------------------------
# Frequency-domain filtering
# ---------------------------------------------------------------------------
# Instead of convolution in time, we can simply zero-out the FFT
# coefficients we don't want, then inverse-FFT back to time domain.
# This is conceptually simple but produces sharp cutoffs (Gibbs ringing).
# ---------------------------------------------------------------------------
def filter_signal(
    signal: NDArray[np.float64],
    sample_rate: float,
    cutoff_freq: float,
    filter_type: str = "lowpass",
) -> NDArray[np.float64]:
    """Low-pass or high-pass filter by zeroing FFT coefficients.

    *filter_type* must be ``"lowpass"`` (keep below cutoff) or
    ``"highpass"`` (keep above cutoff).

    >>> _, sig = generate_test_signal([50.0, 500.0], [1.0, 1.0], 2000.0, 1.0)
    >>> filtered = filter_signal(sig, 2000.0, 200.0, "lowpass")
    >>> len(filtered) == len(sig)
    True
    """
    if filter_type not in ("lowpass", "highpass"):
        msg = f"filter_type must be 'lowpass' or 'highpass', got '{filter_type}'"
        raise ValueError(msg)

    n = len(signal)
    fft_result: NDArray[np.complex128] = np.fft.fft(signal)
    freqs = np.asarray(np.fft.fftfreq(n, d=1.0 / sample_rate), dtype=np.float64)

    # Build a mask: True where we KEEP the coefficient.
    if filter_type == "lowpass":
        mask: NDArray[np.bool_] = np.abs(freqs) <= cutoff_freq
    else:
        mask = np.abs(freqs) >= cutoff_freq

    # Zero out unwanted frequencies, then invert back to time domain.
    filtered_fft: NDArray[np.complex128] = fft_result * mask
    result: NDArray[np.float64] = np.real(np.fft.ifft(filtered_fft)).astype(np.float64)
    return result


# ---------------------------------------------------------------------------
# Discrete Cosine Transform
# ---------------------------------------------------------------------------
# DCT is closely related to the FFT but uses only real-valued cosine basis
# functions.  DCT-II ("the DCT") is the workhorse behind JPEG compression
# and MP3 audio coding — it concentrates energy into a few low-frequency
# coefficients, making it easy to discard the rest.
# ---------------------------------------------------------------------------
def compute_dct(signal: NDArray[np.float64]) -> NDArray[np.float64]:
    """Compute the type-II DCT of *signal*.

    >>> x = np.array([1.0, 2.0, 3.0, 4.0])
    >>> c = compute_dct(x)
    >>> len(c) == len(x)
    True
    """
    result: NDArray[np.float64] = np.asarray(dct(signal, type=2), dtype=np.float64)
    return result


def compute_idct(coefficients: NDArray[np.float64]) -> NDArray[np.float64]:
    """Inverse DCT (type-II) — reconstruct signal from DCT coefficients.

    >>> x = np.array([1.0, 2.0, 3.0, 4.0])
    >>> np.allclose(compute_idct(compute_dct(x)), x)
    True
    """
    result: NDArray[np.float64] = np.asarray(
        idct(coefficients, type=2), dtype=np.float64
    )
    return result


# ---------------------------------------------------------------------------
# Spectral analysis
# ---------------------------------------------------------------------------
def spectral_analysis(
    signal: NDArray[np.float64],
    sample_rate: float,
) -> dict[str, float]:
    """Summarise the spectral content of *signal*.

    Returns a dict with:
        - ``dominant_frequency``: frequency (Hz) with highest magnitude
        - ``total_power``: sum of squared magnitudes (Parseval's theorem)
        - ``bandwidth``: range (Hz) that contains 90 % of total power

    >>> _, sig = generate_test_signal([440.0], [1.0], 8000.0, 1.0)
    >>> info = spectral_analysis(sig, 8000.0)
    >>> abs(info["dominant_frequency"] - 440.0) < 1.0
    True
    """
    freqs, mags = compute_fft(signal, sample_rate)

    # Dominant frequency = frequency bin with the largest magnitude.
    dominant_idx = int(np.argmax(mags))
    dominant_frequency = float(freqs[dominant_idx])

    # Total power via Parseval's theorem (sum of |X_k|^2).
    power: NDArray[np.float64] = mags**2
    total_power = float(np.sum(power))

    # Bandwidth: smallest contiguous frequency range holding >= 90 % power.
    threshold = 0.9 * total_power
    sorted_indices: NDArray[np.intp] = np.argsort(power)[::-1]
    cumulative = float(0)
    freq_set: list[float] = []
    for idx_val in sorted_indices:
        idx = int(idx_val)
        cumulative += float(power[idx])
        freq_set.append(float(freqs[idx]))
        if cumulative >= threshold:
            break

    bandwidth = max(freq_set) - min(freq_set) if freq_set else 0.0

    return {
        "dominant_frequency": dominant_frequency,
        "total_power": total_power,
        "bandwidth": bandwidth,
    }
