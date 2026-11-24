# C005 - Reduction: an upper displacement bound implies the permutation property

## Statement

Suppose there is a nondecreasing function f: N -> N with f(x) = o(x / log x) such that

    a(n) <= n + f(n)   for all n.

Then every positive integer occurs in the sequence.

## Depends on

C004.

## Draft proof

Fix X and put X' = X - f(X) (assume X' >= 1, true for large X). For n <= X', using f nondecreasing,

    a(n) <= n + f(n) <= X' + f(X') <= X' + f(X) = X.

So a(1), ..., a(X') are X' distinct integers in [1, X]. Every value in [1, X] not among them is either in M or occurs later; in any case

    |M ∩ [1, X]| <= X - X' = f(X) = o(X / log X).

If M were nonempty, C004 would give |M ∩ [1, X]| >= (1 - o(1)) X / log X, a contradiction for large X. Hence M = ∅. ∎

## Remarks

- Only an **upper** bound on a(n) is needed. No lower bound.
- Data: max |a(n) - n| is 156 for n <= 10^6 and 200 for n <= 10^7, so numerically f(x) ~ C (log x)^2 looks plausible - far stronger than needed.
- This turns the problem into: **show the sequence cannot run ahead of the identity by more than o(n / log n)**.

## Numerical check

Upper displacement max(a(n) - n) for n <= 10^7: see `experiments/results/run_1e7/summary.md` (max |a(n) - n| = 200).

## Review log

- 2026-11-25: drafted at setup. **Awaiting skeptic + literature check.**
- 2026-11-24 (skeptic): **PASS, conditional on C004** (C004 is still a candidate, so C005 is only as good as C004; it must not move to `proven/` before C004 does).
  - Restated: if there is a nondecreasing f: N -> N with f(x)/(x/log x) -> 0 and a(n) <= n + f(n) for every n >= 1, then M := {m >= 1 : m != a(n) for all n} is empty.
  - Step checks. (i) X' = X - f(X) >= 1 for large X: since f(X) = o(X/log X) = o(X), X - f(X) -> infinity. OK. (ii) For 1 <= n <= X': n + f(n) <= X' + f(X') by monotonicity of n and f; f(X') <= f(X) because X' <= X and f is nondecreasing. So a(n) <= X. OK. (iii) a(1..X') are distinct (the greedy rule excludes used values; well-definedness is L002), so they fill X' slots of [1, X]; M ∩ [1, X] is disjoint from them by definition of M, giving |M ∩ [1, X]| <= f(X). OK, no off-by-one. (iv) For fixed m, pi(X+m) - pi(m) - N0 ~ X/log X by PNT (Chebyshev-type bounds would suffice), so C004 gives a lower bound of order X/log X, contradicting f(X) = o(X/log X). OK.
  - The proof is a pure counting reduction and uses nothing specific to the prime rule beyond C004, so it cannot "prove" a false variant on its own; any variant (other a(1), composite sums) would need its own analogue of C004.
  - Numerical sanity (n <= 10^6, greedy.py): max(a(n) - n) = 156; with F(X) = max_{n<=X} max(a(n)-n, 0), I checked that a(n) <= X for all n <= X - F(X) at X = 10^3, 10^4, 10^5, 9*10^5. Consistent.
  - Minor, non-blocking: the "nondecreasing" assumption can be dropped (replace f by its running max, which is still o(x/log x) since x/log x is eventually increasing); "for all n" can be relaxed to "for all n >= n0". The lemma only reduces the problem: the hypothesis a(n) <= n + o(n/log n) is itself unproven. The earlier log entry is dated 2026-11-25, which is after this review date; please fix the date.
