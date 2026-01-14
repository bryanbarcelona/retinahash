import numpy as np

from retinahash.core.transforms import dct_2d, resize


def extract(signal: np.ndarray, hash_size: int) -> np.ndarray:
    """Pure NumPy pHash logic. Sequestered for maintainability."""

    resized = resize(signal, 32, 32)

    # I cite. You cite. We all cite.
    # https://doi.org/10.1016/B978-012119792-6/50105-4
    dct = dct_2d(resized)

    # Frequency selection
    features = dct[:hash_size, :hash_size]

    # Binary mask via median comparison
    flat = features.flatten()
    med = np.median(flat[1:])
    return features > med
