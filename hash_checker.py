#!/usr/bin/env python3
"""
File Hash Checker
-----------------
Compute a file's hash and optionally verify it against an expected value.

Usage:
    python hash_checker.py FILE                      # prints SHA-256
    python hash_checker.py FILE -a md5               # choose an algorithm
    python hash_checker.py FILE -e <expected_hash>   # verify against a hash
    python hash_checker.py FILE --all                # show several algorithms

Exit codes:
    0  success (and hash matches, if --expected was given)
    1  hash mismatch
    2  error (file not found, bad algorithm, etc.)
"""

import argparse
import hashlib
import hmac
import sys
from pathlib import Path

CHUNK_SIZE = 1024 * 1024  # read 1 MiB at a time so large files don't fill memory
DEFAULT_ALGORITHM = "sha256"
COMMON_ALGORITHMS = ["md5", "sha1", "sha256", "sha512"]


def compute_hash(path: Path, algorithm: str = DEFAULT_ALGORITHM) -> str:
    """Return the hex digest of the file at `path` using `algorithm`."""
    hasher = hashlib.new(algorithm)
    with path.open("rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()


def hashes_match(actual: str, expected: str) -> bool:
    """Compare two hex digests, ignoring case and surrounding whitespace."""
    actual = actual.strip().lower()
    expected = expected.strip().lower()
    return hmac.compare_digest(actual, expected)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute and verify file hashes."
    )
    parser.add_argument("file", type=Path, help="path to the file to hash")
    parser.add_argument(
        "-a", "--algorithm",
        default=DEFAULT_ALGORITHM,
        help=f"hash algorithm (default: {DEFAULT_ALGORITHM}). "
             f"Available: {', '.join(sorted(hashlib.algorithms_guaranteed))}",
    )
    parser.add_argument(
        "-e", "--expected",
        help="expected hash to verify against",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="print md5, sha1, sha256 and sha512 for the file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    algorithm = args.algorithm.lower()

    if not args.file.exists():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        return 2
    if not args.file.is_file():
        print(f"Error: not a regular file: {args.file}", file=sys.stderr)
        return 2
    if algorithm not in hashlib.algorithms_available:
        print(f"Error: unsupported algorithm: {algorithm}", file=sys.stderr)
        return 2

    try:
        if args.all:
            for algo in COMMON_ALGORITHMS:
                print(f"{algo.upper():<7} {compute_hash(args.file, algo)}")
            if not args.expected:
                return 0

        actual = compute_hash(args.file, algorithm)
    except PermissionError:
        print(f"Error: permission denied: {args.file}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return 2

    if not args.all:
        print(f"{algorithm.upper()}: {actual}")

    if args.expected:
        if hashes_match(actual, args.expected):
            print("OK Hash matches. File is intact.")
            return 0
        print("FAIL Hash does NOT match!")
        print(f"  Expected: {args.expected.strip().lower()}")
        print(f"  Actual:   {actual}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
