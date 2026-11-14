# File Hash Checker

A Python command-line tool that computes cryptographic hashes of files and verifies file integrity. A file that has been altered will no longer match its expected hash, which is a core idea in digital forensics and chain of custody.

## Features

- Computes MD5, SHA-1, SHA-256 and SHA-512 hashes
- Verifies a file against an expected hash
- Reads files in 1 MiB chunks, so large files don't fill memory
- Clear exit codes for use in scripts

## Usage

```

python hash_checker.py FILE                     # SHA-256 (default)

python hash_checker.py FILE -a md5              # choose an algorithm

python hash_checker.py FILE -e <expected_hash>  # verify against a hash

python hash_checker.py FILE --all               # show several algorithms

```

## Exit codes

- `0` success (and hash matches, if `--expected` was given)
- `1` hash mismatch
- `2` error (file not found, bad algorithm, etc.)

## Demo

1. Hash a file and note the SHA-256.
   <img width="600" height="60" alt="Screenshot 2026-11-13 234347" src="https://github.com/user-attachments/assets/b92ee060-5372-469e-b8c5-296670d4393d" />

2. Change one letter in the file and run again: every hash changes completely.
<img width="600" height="60" alt="Screenshot 2026-11-13 235837" src="https://github.com/user-attachments/assets/847a7388-5570-4f86-a023-39091e2f5095" />



3. Verify with the original hash: `FAIL Hash does NOT match!`
   <img width="600" height="60" alt="Screenshot 2026-11-13 235231" src="https://github.com/user-attachments/assets/5513ac6c-fd08-4e7f-9e5e-a26c8f92aa66" />

   

4. Restore the file and verify again: `OK Hash matches. File is intact.`
<img width="600" height="60" alt="Screenshot 2026-11-13 235201" src="https://github.com/user-attachments/assets/ef870b5d-1543-4c6e-9791-a9c5d50ff97b" />

## Built with

Python 3 (`hashlib`, `hmac`, `argparse`, `pathlib`)
