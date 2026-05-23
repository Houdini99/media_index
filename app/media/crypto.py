"""AES-256-CTR encryption for private media files.

CTR mode is chosen so encrypted videos can still be streamed with HTTP
byte-range requests: each plaintext byte offset maps to a deterministic
counter block, so the server can decrypt arbitrary ranges without first
reading the whole file.

On-disk layout: `nonce(16 bytes) || ciphertext`. No auth tag — integrity
of media bytes is not the goal here (we already trust our own disk); the
goal is confidentiality of file contents at rest.
"""
import os
from typing import Iterator, Optional

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY_BYTES = 32          # AES-256
NONCE_BYTES = 16        # AES block size; serves as initial counter block
BLOCK_SIZE = 16
CHUNK_SIZE = 64 * 1024  # streaming chunk for encrypt/decrypt I/O


def new_key() -> bytes:
    return os.urandom(KEY_BYTES)


def _counter_at(nonce: bytes, byte_offset: int) -> bytes:
    """Counter block for the CTR position covering `byte_offset` (rounded
    down to a 16-byte boundary)."""
    n = int.from_bytes(nonce, 'big')
    advance = byte_offset // BLOCK_SIZE
    return ((n + advance) % (1 << 128)).to_bytes(NONCE_BYTES, 'big')


def encrypt_file(src_path: str, dst_path: str, key: bytes) -> None:
    nonce = os.urandom(NONCE_BYTES)
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce)).encryptor()
    with open(src_path, 'rb') as src, open(dst_path, 'wb') as dst:
        dst.write(nonce)
        while True:
            chunk = src.read(CHUNK_SIZE)
            if not chunk:
                break
            dst.write(cipher.update(chunk))
        dst.write(cipher.finalize())


def plaintext_size(enc_path: str) -> int:
    """Plaintext size = file size minus the 16-byte nonce prefix."""
    return max(0, os.path.getsize(enc_path) - NONCE_BYTES)


def iter_decrypted(
    enc_path: str,
    key: bytes,
    start: int = 0,
    end: Optional[int] = None,
) -> Iterator[bytes]:
    """Yield decrypted bytes for the half-open plaintext range [start, end)."""
    psize = plaintext_size(enc_path)
    if end is None or end > psize:
        end = psize
    if start < 0 or start >= end:
        return

    block_start = (start // BLOCK_SIZE) * BLOCK_SIZE
    skip = start - block_start
    to_read = end - block_start

    with open(enc_path, 'rb') as f:
        nonce = f.read(NONCE_BYTES)
        if len(nonce) != NONCE_BYTES:
            return
        f.seek(NONCE_BYTES + block_start)
        cipher = Cipher(algorithms.AES(key), modes.CTR(_counter_at(nonce, block_start))).decryptor()

        first = True
        while to_read > 0:
            chunk = f.read(min(CHUNK_SIZE, to_read))
            if not chunk:
                break
            to_read -= len(chunk)
            plain = cipher.update(chunk)
            if first:
                plain = plain[skip:]
                first = False
            if plain:
                yield plain
        tail = cipher.finalize()
        if tail:
            yield tail
