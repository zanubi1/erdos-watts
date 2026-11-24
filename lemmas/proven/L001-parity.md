# L001 - Consecutive terms alternate in parity

_Trivial setup lemma (no skeptic pass required)._

## Statement

For all n >= 1, a(n) and a(n+1) have opposite parity.

## Proof

a(n) and a(n+1) are distinct positive integers, so a(n) + a(n+1) >= 1 + 2 = 3. It is prime by definition, hence an odd prime, so the two terms have opposite parity. Since a(1) = 1, a(n) is odd for n odd and even for n even.

## Numerical check

Holds for the first 10^7 terms (by construction of `greedy.py`, which only searches the opposite parity; first 100,000 terms also match OEIS A055265).

## Review log

- 2026-11-25: written at setup.
