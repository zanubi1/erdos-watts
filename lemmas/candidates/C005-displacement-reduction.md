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
