"""ai-excited-01 entry: "The Wave That Roars".

This program writes the entry image (art.jpg, stored next to this file)
to the output entry file: $MAKEFUN_OUTPUT_DIR/entry.png when that
environment variable is set, otherwise /output/entry.png. The image
bytes are copied unchanged, after a magic-byte check that they are a
real JPEG or PNG.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "art.jpg")

JPEG_MAGIC = b"\xff\xd8"
PNG_MAGIC = b"\x89\x50"


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.png")


def check_image_magic(data):
    """Accept JPEG or PNG content; refuse anything else with a clear error."""
    if data[:3] == b"\xff\xd8\xff":
        return "JPEG"
    if data[:2] == PNG_MAGIC:
        return "PNG"
    raise ValueError(
        "source image is neither JPEG nor PNG (first bytes: %s)"
        % (data[:4].hex(" ") or "<empty file>")
    )


def main():
    with open(SOURCE, "rb") as f:
        data = f.read()
    kind = check_image_magic(data)

    dest = output_path()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        written = f.write(data)

    if written != len(data):
        raise IOError(
            "short write to %s: %d of %d bytes" % (dest, written, len(data))
        )
    print("wrote %s (%s, %d bytes, source %d bytes)" % (dest, kind, written, len(data)))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
