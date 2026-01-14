import numpy as np


def to_gray(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image
    # Luma conversion
    return np.dot(image[..., :3], [0.299, 0.587, 0.114])


def resize(image: np.ndarray, width: int, height: int) -> np.ndarray:
    """NumPy Bilinear Interpolation for dependency-free scaling."""
    old_h, old_w = image.shape
    x = np.linspace(0, old_w - 1, width)
    y = np.linspace(0, old_h - 1, height)
    xi, yi = x.astype(int), y.astype(int)
    xf, yf = (x - xi).reshape(1, width), (y - yi).reshape(height, 1)

    # Clamping for edge safety
    xi_next = np.minimum(xi + 1, old_w - 1)
    yi_next = np.minimum(yi + 1, old_h - 1)

    a, b = image[yi][:, xi], image[yi][:, xi_next]
    c, d = image[yi_next][:, xi], image[yi_next][:, xi_next]
    return a * (1 - xf) * (1 - yf) + b * xf * (1 - yf) + c * (1 - xf) * yf + d * xf * yf


def dct_2d(block: np.ndarray) -> np.ndarray:
    """Matrix-based Discrete Cosine Transform (Type II)."""
    n = block.shape[0]
    i, j = np.indices((n, n))
    basis = np.cos(np.pi * i * (2 * j + 1) / (2 * n))
    return np.dot(basis, np.dot(block, basis.T))


def autocrop(image: np.ndarray, threshold: int = 250) -> np.ndarray:
    """Removes solid borders (like white scanner edges) using pure NumPy."""
    # Create mask of 'content' (pixels darker than threshold)
    # I assume white borders typical for flatbed scans at least mine have a white bg.
    # For black borders it would be the inverse image > threshold <- maybe in the future?
    mask = image < threshold
    if not np.any(mask):
        return image

    # Find the bounding box of the mask
    coords = np.argwhere(mask)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1

    return image[y0:y1, x0:x1]
