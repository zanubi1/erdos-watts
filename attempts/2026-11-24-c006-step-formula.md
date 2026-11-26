# 2026-11-24 - C006 step formula (prover)

## Goal

1. Prove C006 (a), (b), (c) rigorously.
2. In a separate Remarks section, say what (c) gives when combined with short-interval prime theorems, why that is circular with respect to C005, and what weaker averaged or density input would suffice.

## Idea

- (a) is immediate from the minimality in the greedy rule.
  - The only care needed: exclude the prime 2 for every candidate x, not just for a(n+1).
  - This gives t_n >= 3 odd, so all q_i are odd and every partner q_i - a(n) has parity π_n.
  - Use u*(n) ∉ U_n to get strict inequality x_i > u*(n).
- (b) is pigeonhole on the parity class π_n ≡ n+1, with the exact count floor(n/2) of used values per parity coming from a(k) ≡ k (mod 2).
- (c) follows from (a) and (b).

## Work

- **Proof.** Written in full in `lemmas/candidates/C006-step-formula.md`.
- **By-product (b'): the exact identity O*(n) = (n + 1 - u*(n))/2.** It gives:
  - the exact relation Dup(n+1) = (q_{b+1} - t_n) - 2O*(n);
  - the sharper bound (c'), whose right side is (c) minus 2O*.
  - This also explains the old figure 1542 in the C006 numerical note: it was the (c') bound. The literal (c) bound reaches 1740.
- **Numerical checks to 10^7, all pass** (`experiments/src/c006_check.py`, about 50 s). Every step asserts:
  - t_n odd and >= 3;
  - the exact formula, with blocked partners used and > u*;
  - b <= O*;
  - (b) and (b');
  - (E), (c'), (c);
  - Dlo(n+1) <= 2O*(n).
- **Remarks, with prime-number inputs.**
  - Huxley (7/12) gives, unconditionally for large n: Dup(n+1) <= n^{0.61} + 3(O*(n)+1) log n. Quantitative BHP would only improve the exponent 0.61 to about 0.53; that quantitative form is recalled from memory and marked GAP?.
  - Brun-Titchmarsh (Montgomery-Vaughan) shows the method cannot do better than about (1/2) O* log O*.
  - By-product: a(n) = O(n log n) unconditionally (sketch; needs its own review).
- **Circularity, proved.**
  - Dlo(n+1) <= 2O*(n) <= Dlo(time at which u*(n) is used).
  - O* = o(n) alone already implies M = ∅.
  - If M ≠ ∅, then Σ_{n<=X} O* >= X^2/8 - O(X). So no pointwise or averaged hypothesis on O* is weaker than the conclusion.
- **Replacement: count holes instead of measuring from the frontier.**
  - R3a: Dup(n+1) <= q'_{H_π(n)+1} - (a(n)+n+1), where H_π(n) is the number of unused values <= n of parity π_n. Data to 10^7: bound max 554, H_π <= 30, H <= 50, mean H 8.8 (`experiments/src/c006_holes_check.py`).
  - R3b: with C004, H(X) = o(X/log X) infinitely often implies M = ∅. So does S(X) = Σ_{k<=X} Dup^+(k) = o(X^2/(log X)^2) along a subsequence.

## Outcome

- C006 (a), (b), (c) are proved, with no GAP? in the lemma. Awaiting skeptic.
- Remarks R1-R4 are recorded in the lemma file, clearly separated from it.

## Why it died / what survives

**What survives:**
- C006 and (b'), (E), (c').
- The hole-count step bound R3a, and the density reduction R3b. Both are candidates for their own C### files after review.

**What dies:**
- Using (c) with any prime-in-short-interval theorem to feed C005. It needs O* = o(n/(log n)^2), and that hypothesis alone (even O* = o(n)) already implies the permutation property.
- Averaged versions of the O* hypothesis die the same way, because a single permanent hole makes O* linear.

**What is still open:**
- R3a gives a recursion in the upper displacement alone, D(n+1) <= n^{0.61} + 3(D(n)+1) log n. It does not contract: each hole costs about log n.
- The identity Σ H(n) = Σ Dup^+ shows that averaging cannot fix this.
- A proof needs structural input that holes get filled (net negative drift of H when H is large). That is the wait-time / reflection-lock route, not a prime-counting estimate.
