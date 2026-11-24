# C006 - Step formula: the next term is governed by primes after the frontier and the overshoot

## Statement

Notation, for n >= 1:

- U_n = {a(1), ..., a(n)} is the set of used values.
- π_n is the parity of a(n+1). By L001 it is the opposite of the parity of a(n).
- u*(n) = min { x >= 1 : x ≡ π_n (mod 2), x ∉ U_n } is the parity frontier.
- t_n = a(n) + u*(n).
- q_1 < q_2 < ... are the primes >= t_n.
- O*(n) = #{ x ∈ U_n : x ≡ π_n (mod 2), x > u*(n) } is the overshoot in the parity of the next term.

Then:

**(a) Exact formula.** a(n+1) = q_{b+1} - a(n), where b = b(n) = #{ i : q_i < a(n) + a(n+1) }. Moreover, for every i <= b, the value q_i - a(n) lies in U_n. Hence b(n) <= O*(n).

**(b) Frontier bound.** u*(n) <= n + 1.

**(c) Consequence.** a(n+1) - (n+1) <= q_{O*(n)+1} - t_n. That is, the upper displacement at step n+1 is at most the length of the shortest interval [t_n, t_n + d] containing O*(n) + 1 primes.

## Depends on

L001, L002.

## Proof

To be written by the prover.

## Numerical check

- (a) holds with equality for every n < 10^7: `experiments/src/overshoot_extra.py`, line "exact formula check: True" in `experiments/results/overshoot_1e7/extra.txt`.
- (b) holds for every n < 10^7: max u*(n) - n = 1.
- (c) holds for every n < 10^7: the bound is at most 1542, against an actual max upper displacement of 188.

## Review log

- 2026-11-24: stated from the overshoot experiment (session 2). **Awaiting prover, then skeptic.**
