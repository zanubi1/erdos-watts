# C003 - The smallest missing value blocks a translate of the primes

## Statement

Suppose some positive integer never occurs in the sequence, and let m be the smallest such. Then there is N0 such that for every n >= N0 with a(n) of parity opposite to m, the number a(n) + m is composite.

## Depends on

L001, L002.

## Draft proof

Every x < m occurs, so there are finitely many indices at which the values 1, ..., m-1 occur; let N0 exceed all of them. Fix n >= N0 with a(n) of parity opposite to m. Suppose for contradiction a(n) + m is prime.

Consider the set S = { x >= 1 : x not in {a(1..n)}, a(n) + x prime }. Every x < m is in {a(1..n)} because n >= N0, so S contains no x < m. And m is not in {a(1..n)} (m never occurs), and a(n) + m is prime, so m ∈ S. Hence min S = m, so a(n+1) = m, contradicting that m never occurs. ∎

(Parity of a(n) opposite to m is not used in the argument; it only matters because if a(n) and m have the same parity, a(n) + m is even and > 2, so composite anyway.)

## Numerical check

Not applicable directly (concerns a hypothetical missing value).

## Review log

- 2026-11-25: drafted at setup. **Awaiting skeptic.**
