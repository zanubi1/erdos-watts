# C008 - Hole-density criterion for the permutation property

## Statement

For X >= 1, let H(X) = #{ v ∈ [1, X] : v ∉ U_X } be the number of holes below X at time X, where U_X = {a(1), ..., a(X)}.

**(i) Identity.** H(X) = #{ k ∈ [1, X] : a(k) > X }.

**(ii) Criterion (conditional on C004).** If

    liminf_{X -> ∞}  H(X) · log X / X  =  0,

then every positive integer occurs in the sequence.

**(iii) Averaged form.** Let S(X) = Σ_{k <= X} max(a(k) - k, 0). For every X >= 1 and every integer D >= 1,

    H(X) <= D + S(X) / D.

Consequently, if S(X) = o(X^2 / (log X)^2) along some sequence X -> ∞, then every positive integer occurs.

## Depends on

- L002, for (i) and (iii).
- C004 (candidate, skeptic PASS conditional on C003), for (ii) and the "consequently" in (iii). So (ii) is conditional on C003 and C004.

## Proof

_Transcribed 2026-11-25 from the prover's Remark R3b in C006, with the steps written out._

**(i)** The values a(1), ..., a(X) are distinct, so |U_X| = X. Split U_X into the values <= X and the values > X:

    |U_X ∩ [1, X]| + #{ k <= X : a(k) > X } = X.

The holes are [1, X] \ U_X, so H(X) = X - |U_X ∩ [1, X]| = #{ k <= X : a(k) > X }. ∎

**(ii)**
- Let M be the set of values that never occur, and suppose M ≠ ∅. Let m = min M.
- Any v ∈ M ∩ [1, X] never occurs, so in particular v ∉ U_X, and v is a hole. Hence |M ∩ [1, X]| <= H(X) for every X.
- By C004, |M ∩ [1, X]| >= π(X + m) - π(m + 1) - (N0 - 1), for constants m and N0 that do not depend on X.
- By Chebyshev's bound π(Y) >= c Y / log Y (for Y >= 2, with an absolute c > 0), the right side is >= (c/2) X / log X for all X >= X_1, for some X_1.
- So H(X) log X / X >= c/2 for all X >= X_1, contradicting the liminf being 0. Hence M = ∅. ∎

**(iii)**
- By (i), H(X) counts the k <= X with a(k) > X. Split these k into two groups.
- k > X - D: there are at most D such k in [1, X].
- k <= X - D: then a(k) - k > X - k >= D. So each such k contributes more than D to S(X). Since every term of S(X) is >= 0, there are fewer than S(X)/D such k.
- Hence H(X) <= D + S(X)/D.

For the consequence:
- Take D = ceil( sqrt(S(X)) ) + 1 >= 1. This gives H(X) <= 2 sqrt(S(X)) + 3, using S/D <= sqrt(S).
- If S(X) = o(X^2 / (log X)^2) along a sequence X_j -> ∞, then H(X_j) = o(X_j / log X_j). Apply (ii). ∎

## Remarks

- **Why (ii) is a real weakening** (prover's R2/R3): a permanent hole contributes 1 to H(X), whereas any frontier-based quantity (such as O*) becomes linear in X as soon as one value is missing. So the hypothesis of (ii) is not trivially equivalent to the conclusion; all of its strength comes from C004.
- The data are far inside the criterion: H(X) <= 50 for X <= 10^7, against X / log X ≈ 6 · 10^5.
- Open: no proof of H(X) = o(X / log X), even along a subsequence, is in sight. It needs "holes get filled" structure (STRATEGY route 1).

## Numerical check

To be done by the experimenter: (i), and (iii) for several D, at every X <= 10^7.

## Review log

- 2026-11-25: candidate created from C006 Remark R3b. **Awaiting experimenter and skeptic.**
