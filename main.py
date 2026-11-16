"""The Wave That Roars — ai-excited-01 entry.

Copies the bundled artwork (art.jpg, a JPEG) to /output/entry.png
after checking it is a real JPEG inside the competition's limits.
Standard library only.
"""

import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "art.jpg"
DEST = Path("/output/entry.png")

MAX_BYTES = 1_048_576
MAX_SIDE = 1024
JPEG_MAGIC = b"\xff\xd8\xff"


def jpeg_dimensions(blob: bytes) -> tuple[int, int]:
    """Read width/height out of a JPEG's first SOF0/SOF2 marker."""
    pos = 2
    while pos + 9 <= len(blob):
        if blob[pos] != 0xFF:
            pos += 1
            continue
        marker = blob[pos + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", blob[pos + 5:pos + 9])
            return width, height
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        size = struct.unpack(">H", blob[pos + 2:pos + 4])[0]
        pos += 2 + size
    raise ValueError("no SOF marker found in JPEG")


def main() -> int:
    data = SOURCE.read_bytes()

    if data[:3] != JPEG_MAGIC:
        print("error: art.jpg is not a JPEG (bad magic bytes)", file=sys.stderr)
        return 1
    if data[-2:] != b"\xff\xd9":
        print("error: art.jpg is truncated (no JPEG end marker)", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"error: art.jpg is {len(data)} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1
    width, height = jpeg_dimensions(data)
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"error: art.jpg is {width}x{height}, over the 1024 cap",
              file=sys.stderr)
        return 1

    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(data)

    written = DEST.read_bytes()
    if written != data:
        print("error: output does not match source", file=sys.stderr)
        return 1

    print(f"wrote {DEST} ({width}x{height}, {len(data)} bytes, JPEG; "
          f"source art.jpg {len(data)} bytes, identical)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
