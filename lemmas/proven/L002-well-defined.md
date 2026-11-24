# L002 - The sequence is well defined

_Trivial setup lemma (no skeptic pass required)._

## Statement

For every n, the set { x >= 1 : x not in {a(1..n)} and a(n) + x prime } is nonempty, so a(n+1) exists.

## Proof

Let U = {a(1), ..., a(n)} and K = max U. There are infinitely many primes, so pick a prime p > a(n) + K. Then x = p - a(n) > K, so x is unused, x >= 1, and a(n) + x = p is prime.

(OEIS cites Dirichlet; plain infinitude of primes suffices.)

## Review log

- 2026-11-25: written at setup.
