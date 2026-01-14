# RetinaHash  
**Lightweight, pure-NumPy perceptual hashing for images**

RetinaHash computes compact, rotation-invariant fingerprints of images using only NumPy...no OpenCV, no PIL, no Scipy.  
Perfect for duplicate detection, near-duplicate search, and lightweight image clustering.

## Features
- **Pure NumPy** – runs anywhere Python runs  
- **Rotation invariant** – same hash for 0°, 90°, 180°, 270° rotations  
- **Auto-crop** – strips solid scanner borders automatically  
- **Extensible** – plug-in architecture for new hash algorithms  
- **Fast** – ~1 ms per 512×512 image on a laptop CPU (**TRUST ME BRO** Benchmark, lol.)

## Install
```bash
pip install retinahash
```
Or better, because you are sane and use uv to manage your projects:
```bash
uv add retinahash
```
(or drop the `retinahash/` folder into your project—zero dependencies beyond NumPy).

## Quick Start
```python
import imageio.v3 as iio          # any loader will do but numpy array is expected
from retinahash import RetinaHash

img = iio.imread("photo.jpg")
h   = RetinaHash.phash(img, rotation_invariant=True)
print(h)        # 16-char hex string, e.g. 'a5f3c1e8d2b4906e'
```

Compare two images (via Hamming distance):
```python
h1 = RetinaHash.phash(img1)
h2 = RetinaHash.phash(img2)
distance = RetinaHash.distance(h1, h2)
```

## API
`RetinaHash.hash(image, method='phash', hash_size=8, rotation_invariant=False, auto_crop=False)`  
`RetinaHash.phash(image, **kwargs)` – convenience wrapper  
`RetinaHash.distance(hex1, hex2)` – Hamming distance between two hex hashes  

## Algorithms
| Key  | Description |
|------|-------------|
| `phash` | DCT-based perceptual hash (default) |

More algorithms (`ahash`, `dhash`, `whash`, …) can be added by dropping a new module into `retinahash/strategies/` and registering it in `STRATEGIES`.

## Customisation
```python
# 16-bit hash, auto-crop on, rotation invariant
h = RetinaHash.hash(img, method='phash', hash_size=16,
                    auto_crop=True, rotation_invariant=True)
```

## License
MIT – do what you want, just keep the copyright notice.

---

That’s it—clone, hash, dedupe.