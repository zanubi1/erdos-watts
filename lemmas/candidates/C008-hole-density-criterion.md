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
- By C004 (as stated there), |M ∩ [1, X]| >= π(X + m) - π(m) - N0, for constants m and N0 that do not depend on X.
- By Chebyshev's bound π(Y) >= c Y / log Y (for Y >= 2, with an absolute c > 0), the right side is >= (c/2) X / log X for all X >= X_1, for some X_1.
- So H(X) log X / X >= c/2 for all X >= X_1, contradicting the liminf being 0. Hence M = ∅. ∎

**(iii)**
- By (i), H(X) counts the k <= X with a(k) > X. Split these k into two groups.
- k > X - D: there are at most D such k in [1, X].
- k <= X - D: then a(k) - k > X - k >= D. So each such k contributes more than D to S(X). Since every term of S(X) is >= 0, there are at most S(X)/D such k.
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
- 2026-11-25 (skeptic): **PASS (conditional)**. (i) and (iii) are unconditional, given only L002 (distinct values, a(k) defined for all k). (ii) and the "consequently" in (iii) are **conditional on C004, hence on C003**. Neither is in `lemmas/proven/`. Checked:
  - (i): |U_X| = X splits into values <= X and values > X. Correct for every X >= 1.
  - (ii) quantifiers: m and N0 depend only on the (fixed) sequence, not on X. π(X+m) >= π(X) >= cX/log X (Chebyshev lower bound, X >= 2), minus a constant, is >= (c/2)X/log X for all X >= X_1. So the conclusion is H(X) log X / X >= c/2 for *all* large X. That contradicts liminf = 0, so liminf (not lim) is the right, weaker hypothesis, and having it along one subsequence is enough. No quantifier swap. The proof needs C004 for all large X. C004's Statement does not write the quantifier on X explicitly ("for all X" or "for all large X"); either reading is enough here, but C004 should state it.
  - (iii): k in (X-D, X] gives at most D indices. For k <= X-D, a(k) > X gives a(k)-k >= D+1. Choosing D = ceil(sqrt S)+1 gives an integer >= 1, D <= sqrt S + 2 and S/D <= sqrt S (also when S = 0). So H <= 2 sqrt S + 2, and the "+3" in the text is also valid. Then S = o(X^2/log^2 X) along X_j gives H(X_j) = o(X_j/log X_j), so the liminf is 0.
  - Sanity script (greedy.py, first 20000 terms, matches A055265 start 1,2,3,4,7,6,5,8,9,10,13): (i) exact and (iii) for D = 1..59 at every X <= 3000. 0 violations.
  - **Editorial fixes required (do not affect validity):** (a) Step 3 of (ii) misquotes C004. The C004 file gives π(X+m) - π(m) - N0, not π(X+m) - π(m+1) - (N0-1). The quoted form is larger by π(m) - π(m+1) + 1 ∈ {0,1}, so C008 currently cites a slightly *stronger* claim than C004 proves. Replace it with C004's actual bound; the argument is unchanged. (b) In (iii), "fewer than S(X)/D such k" fails when S = 0 and there are no such k (0 < 0). Write "at most S(X)/D".
- 2026-11-25 (editor): applied the skeptic's editorial fixes (a) and (b) to lines 39 and 46. No change to the argument.
