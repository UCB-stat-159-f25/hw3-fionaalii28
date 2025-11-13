# ligotools/tests/test_utils.py
import numpy as np
from pathlib import Path
from scipy.io import wavfile
from ligotools.utils import whiten, reqshift, write_wavfile


def test_whiten_preserves_shape_and_behavior():
    """
    Verify whiten() returns an array of the same length and roughly normalized values.
    """
    fs = 4096.0
    dt = 1.0 / fs
    t = np.arange(0, 1.0, dt)
    x = np.sin(2*np.pi*150*t) + 0.5*np.sin(2*np.pi*400*t)

    # Flat PSD means whitening should act like an identity scaling
    interp_psd = lambda freqs: np.ones_like(freqs)
    y = whiten(x, interp_psd, dt)

    assert y.shape == x.shape, "Whitened signal should preserve shape"
    assert np.isfinite(y).all(), "Output must be finite"
    # correlation > 0.95 → shape preserved
    corr = np.corrcoef(x, y)[0, 1]
    assert corr > 0.95


def test_reqshift_and_writewavfile(tmp_path: Path):
    """
    Test that reqshift changes signal frequency and write_wavfile outputs valid file.
    """
    fs = 4096
    t = np.linspace(0, 1, fs)
    f0 = 440.0
    data = np.sin(2*np.pi*f0*t)

    # --- reqshift ---
    shifted = reqshift(data, fshift=100, sample_rate=fs)
    assert shifted.shape == data.shape
    assert not np.allclose(shifted, data), "Shifted signal should differ from input"

    # --- write_wavfile ---
    outfile = tmp_path / "test.wav"
    write_wavfile(outfile, fs, data)
    assert outfile.exists() and outfile.stat().st_size > 0

    rate, arr = wavfile.read(outfile)
    assert rate == fs
    assert arr.dtype == np.int16
    assert len(arr) == len(data)
