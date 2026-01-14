import numpy as np

from retinahash.core.transforms import autocrop, to_gray
from retinahash.core.utils import bits_to_hex, hamming_distance
from retinahash.strategies import phash


class RetinaHash:
    """
    The Orchestrator.
    Handles rotation invariance, auto-cropping, and algorithm dispatching.
    """

    STRATEGIES = {"phash": phash.extract}

    @classmethod
    def _prepare(cls, image: np.ndarray, auto_crop: bool) -> np.ndarray:
        """Standardizes the image signal."""
        signal = to_gray(image)
        if auto_crop:
            signal = autocrop(signal)
        return signal

    @classmethod
    def hash(
        cls,
        image: np.ndarray,
        method: str = "phash",
        hash_size: int = 8,
        rotation_invariant: bool = False,
        auto_crop: bool = False,
    ) -> str:
        """Generic entry point with full rotation support."""

        extract_func = cls.STRATEGIES.get(method)
        if not extract_func:
            raise ValueError(f"Algorithm '{method}' not found.")

        signal = cls._prepare(image, auto_crop)

        def get_hex_for_signal(sig):
            bits = extract_func(sig, hash_size)
            return bits_to_hex(bits)

        # Rotate or not, that is the question
        if not rotation_invariant:
            return get_hex_for_signal(signal)

        # Rotate it is my friend
        hashes = []
        for k in [0, 1, 2, 3]:  # 0, 90, 180, 270 degrees
            rotated_sig = np.rot90(signal, k)
            hashes.append(get_hex_for_signal(rotated_sig))

        return min(hashes)

    @classmethod
    def phash(cls, image: np.ndarray, **kwargs) -> str:
        """Convenience method for pHash."""
        return cls.hash(image, method="phash", **kwargs)

    @staticmethod
    def distance(h1: str, h2: str) -> int:
        return hamming_distance(h1, h2)
