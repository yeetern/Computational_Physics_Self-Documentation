#!/usr/bin/env python3
"""
Stream-search a digit pattern (<=6 digits) inside a saved pi digits file.

Indexing convention (default):
- If the file contains ONLY fractional digits:
    position=1 means the first digit after the decimal point.
- If the file contains "3."+fraction:
    use --file_has_3dot to adjust so position still refers to fractional digits.

Usage:
  python pi_search.py --file pi_1e6.txt --pattern 040106
  python pi_search.py --file pi_1e6_with3.txt --pattern 040106 --file_has_3dot
"""

import argparse


def stream_find_first(path: str, pattern: str, chunk_size: int = 1024 * 1024):
    """
    Return 0-indexed position from file start for first occurrence, else None.
    Streaming with overlap to catch cross-chunk matches.
    """
    overlap = len(pattern) - 1
    buf = ""
    consumed = 0  # count of chars read from file excluding buf

    with open(path, "r", encoding="utf-8") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            data = buf + chunk
            idx = data.find(pattern)
            if idx != -1:
                # global 0-indexed from file start:
                return (consumed - len(buf)) + idx

            buf = data[-overlap:] if overlap > 0 else ""
            consumed += len(chunk)

    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="pi digits file")
    ap.add_argument("--pattern", required=True, help="digit pattern (<=6 digits)")
    ap.add_argument("--chunk", type=int, default=1024 * 1024, help="chunk size (default 1MB)")
    ap.add_argument("--file_has_3dot", action="store_true",
                    help='Set if file begins with "3." so output position refers to fractional digits')
    args = ap.parse_args()

    pattern = args.pattern.strip()
    if not pattern.isdigit():
        raise SystemExit("pattern must be digits only.")
    if len(pattern) == 0 or len(pattern) > 6:
        raise SystemExit("pattern length must be 1..6")

    found0 = stream_find_first(args.file, pattern, args.chunk)
    if found0 is None:
        print("[NOT FOUND] within file range.")
        return

    # Convert to 1-indexed position in fractional digits
    # If file starts with "3.", fractional digits start at file index 2.
    fractional_start = 2 if args.file_has_3dot else 0
    fractional_pos_1 = (found0 - fractional_start) + 1

    if fractional_pos_1 <= 0:
        print("[FOUND] pattern occurs before fractional digits (check file_has_3dot flag).")
        print(f"raw_index_0 = {found0}")
        return

    print(f"[FOUND] fractional_position = {fractional_pos_1:,} (1-indexed after decimal point)")
    print(f"        raw_file_index_0    = {found0:,}")


if __name__ == "__main__":
    main()
