#!/usr/bin/env python3
"""
string_encryption.py
Quick tester for algorithm_package.algorithm(key, message).

Usage examples:
  python string_encryption.py -k "secret" -m "hello world"
  echo "hello from stdin" | python string_encryption.py -k "secret" --stdin
"""

import argparse
import sys

try:
    # expects you've run: pip install -e .
    from algorithm_package import algorithm
except Exception as e:
    print("Failed to import algorithm_package. Did you run 'pip install -e .' in your venv?")
    raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Test algorithm(key, message) and print tag")
    parser.add_argument("-k", "--key", required=False, default="secret", help="Key string (default: 'secret')")
    parser.add_argument("-m", "--message", required=False, help="Message string (default: 'hello world')")
    parser.add_argument("--stdin", action="store_true", help="Read message from STDIN instead of -m")
    args = parser.parse_args()

    key = args.key
    if args.stdin:
        message = sys.stdin.read()
    else:
        message = args.message or "hello world"

    # Compute tag
    tag = algorithm(key, message)

    print("=== algorithm(key, message) ===")
    print(f"key     : {repr(key)}")
    print(f"message : {repr(message)}")
    print(f"tag     : {tag}")

    # --- quick sanity checks ---
    # 1) Deterministic
    assert tag == algorithm(key, message), "Determinism check failed."

    # 2) Changing message should (likely) change tag
    changed_msg_tag = algorithm(key, message + "!")
    print("message change ->", "OK (tag changed)" if changed_msg_tag != tag else "WARNING (tag did not change)")

    # 3) Changing key should (likely) change tag
    changed_key_tag = algorithm(key + "1", message)
    print("key change     ->", "OK (tag changed)" if changed_key_tag != tag else "WARNING (tag did not change)")


if __name__ == "__main__":
    main()
