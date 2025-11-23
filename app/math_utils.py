"""Toy math utilities that our sample tests target."""

from __future__ import annotations

from functools import lru_cache


def safe_divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b


def running_total(values):
    total = 0
    out = []
    for value in values:
        total += value
        out.append(total)
    return out


@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n in (0, 1):
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def compute_primes(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for idx in range(2, int(limit ** 0.5) + 1):
        if sieve[idx]:
            step = idx
            start = idx * idx
            sieve[start: limit + 1: step] = [False] * len(range(start, limit + 1, step))
    return [i for i, is_prime in enumerate(sieve) if is_prime]
