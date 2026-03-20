"""Tests for FFT / DCT signal-processing utilities."""

import pytest

np = pytest.importorskip("numpy")
scipy = pytest.importorskip("scipy")

from concepts.fft_dct import (  # noqa: E402
    compute_dct,
    compute_fft,
    compute_idct,
    filter_signal,
    generate_test_signal,
    spectral_analysis,
)


class TestGenerateTestSignal:
    def test_single_frequency_length(self) -> None:
        t, sig = generate_test_signal([440.0], [1.0], 8000.0, 1.0)
        assert len(t) == 8000
        assert len(sig) == 8000

    def test_multiple_frequencies(self) -> None:
        """Sum of two sinusoids has expected sample count."""
        t, sig = generate_test_signal([100.0, 300.0], [1.0, 0.5], 4000.0, 0.5)
        assert len(t) == 2000
        assert len(sig) == 2000

    def test_mismatched_lengths_raises(self) -> None:
        with pytest.raises(ValueError):
            generate_test_signal([100.0], [1.0, 2.0], 1000.0, 1.0)


class TestComputeFFT:
    def test_440hz_peak(self) -> None:
        """A pure 440 Hz sine wave should peak at 440 Hz in the FFT."""
        _, sig = generate_test_signal([440.0], [1.0], 8000.0, 1.0)
        freqs, mags = compute_fft(sig, 8000.0)
        peak_freq = float(freqs[np.argmax(mags)])
        assert abs(peak_freq - 440.0) < 1.0

    def test_positive_frequencies_only(self) -> None:
        _, sig = generate_test_signal([100.0], [1.0], 1000.0, 1.0)
        freqs, _mags = compute_fft(sig, 1000.0)
        assert float(np.min(freqs)) >= 0.0


class TestFilterSignal:
    def test_lowpass_removes_high_frequency(self) -> None:
        """Low-pass at 200 Hz should eliminate a 440 Hz component."""
        _, sig = generate_test_signal([50.0, 440.0], [1.0, 1.0], 8000.0, 1.0)
        filtered = filter_signal(sig, 8000.0, 200.0, "lowpass")

        # FFT of filtered signal should have negligible energy at 440 Hz.
        freqs, mags = compute_fft(filtered, 8000.0)
        idx_440 = int(np.argmin(np.abs(freqs - 440.0)))
        assert float(mags[idx_440]) < 0.01

    def test_highpass_removes_low_frequency(self) -> None:
        _, sig = generate_test_signal([50.0, 440.0], [1.0, 1.0], 8000.0, 1.0)
        filtered = filter_signal(sig, 8000.0, 200.0, "highpass")

        freqs, mags = compute_fft(filtered, 8000.0)
        idx_50 = int(np.argmin(np.abs(freqs - 50.0)))
        assert float(mags[idx_50]) < 0.01

    def test_invalid_filter_type_raises(self) -> None:
        _, sig = generate_test_signal([100.0], [1.0], 1000.0, 1.0)
        with pytest.raises(ValueError):
            filter_signal(sig, 1000.0, 200.0, "bandpass")


class TestDCT:
    def test_roundtrip(self) -> None:
        """DCT -> IDCT should recover the original signal."""
        original = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        recovered = compute_idct(compute_dct(original))
        assert np.allclose(recovered, original)

    def test_roundtrip_random(self) -> None:
        rng = np.random.default_rng(42)
        original = rng.standard_normal(128)
        recovered = compute_idct(compute_dct(original))
        assert np.allclose(recovered, original)


class TestSpectralAnalysis:
    def test_dominant_frequency(self) -> None:
        _, sig = generate_test_signal([440.0], [1.0], 8000.0, 1.0)
        info = spectral_analysis(sig, 8000.0)
        assert abs(info["dominant_frequency"] - 440.0) < 1.0

    def test_total_power_positive(self) -> None:
        _, sig = generate_test_signal([100.0], [2.0], 4000.0, 1.0)
        info = spectral_analysis(sig, 4000.0)
        assert info["total_power"] > 0.0

    def test_bandwidth_key_present(self) -> None:
        _, sig = generate_test_signal([100.0, 500.0], [1.0, 1.0], 4000.0, 1.0)
        info = spectral_analysis(sig, 4000.0)
        assert "bandwidth" in info
