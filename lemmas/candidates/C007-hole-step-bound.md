# C007 - Hole-count step bound

## Statement

Notation, for n >= 1:
- U_n = {a(1), ..., a(n)} and π_n = parity of a(n+1), as in C006.
- H_π(n) = #{ v ∈ [1, n] : v ≡ π_n (mod 2), v ∉ U_n } is the number of holes below n in the parity of the next term.
- q'_1 < q'_2 < ... are the primes >= a(n) + n + 1.

Then for every n >= 1:

    a(n+1) - (n+1)  <=  q'_{H_π(n)+1} - (a(n) + n + 1).

That is, the upper displacement at step n+1 is at most the length of the shortest interval starting at a(n) + n + 1 that contains H_π(n) + 1 primes.

Also H_π(n) <= O*(n), where O*(n) is as in C006. So this bound counts no more primes than C006 (c), and it starts from a base point a(n) + n + 1 >= t_n.

## Depends on

L001, L002. The count (Cnt) from the proof of C006 (b) is reproved below, so C006 is not needed except for the comparison remark H_π(n) <= O*(n).

## Proof

_Transcribed 2026-11-25 from the prover's Remark R3a in C006, with the steps written out._

Fix n >= 1.

**Facts used.**
- By L001 and a(1) = 1, a(k) ≡ k (mod 2) for all k. So π_n ≡ n + 1 and a(n) ≢ π_n (mod 2).
- The values a(1), ..., a(n) are distinct (each a(k+1) ∉ U_k).
- By definition, a(n+1) = min A_n, where A_n = { x >= 1 : x ∉ U_n, a(n) + x prime }.

**Step 1: the candidates y_i.**
- a(n) + n + 1 is odd: a(n) ≡ n, so a(n) + n + 1 ≡ 2n + 1 ≡ 1 (mod 2). Also a(n) + n + 1 >= 1 + 1 + 1 = 3.
- So every q'_i is an odd prime >= 3.
- Put y_i := q'_i - a(n). Then y_i >= n + 1 >= 1, a(n) + y_i = q'_i is prime, and the y_i are pairwise distinct and increasing in i.
- Parity: y_i ≡ 1 - a(n) ≡ 1 - n ≡ n + 1 ≡ π_n (mod 2).

**Step 2: exactly H_π(n) used values of parity π_n exceed n.**
- The values of parity π_n in U_n are exactly a(k) for k <= n with k ≡ n + 1 (mod 2). There are floor(n/2) such k. Since the a(k) are distinct, #{ x ∈ U_n : x ≡ π_n } = floor(n/2).
- The integers in [1, n] that are ≡ n + 1 (mod 2) number floor(n/2):
  - if n is even, these are the odd numbers <= n, of which there are n/2;
  - if n is odd, these are the even numbers <= n, of which there are (n-1)/2.
- Of these, exactly floor(n/2) - H_π(n) are in U_n, by the definition of H_π.
- So the number of x ∈ U_n with x ≡ π_n and x > n is floor(n/2) - (floor(n/2) - H_π(n)) = H_π(n).

**Step 3: some y_i with i <= H_π(n) + 1 is unused.**
- y_1, ..., y_{H_π(n)+1} are H_π(n) + 1 distinct values, all of parity π_n and all > n (Step 1).
- By Step 2, at most H_π(n) of them lie in U_n. So some y_j with j <= H_π(n) + 1 is not in U_n.
- Then y_j ∈ A_n, so a(n+1) <= y_j <= y_{H_π(n)+1} = q'_{H_π(n)+1} - a(n).
- Subtracting n + 1 from both sides gives the claim. ∎

**Comparison with C006: H_π(n) <= O*(n).**
- Every hole v counted by H_π(n) satisfies v ≥ u*(n), by the minimality of u*(n).
- So the holes counted by H_π(n) lie in [u*(n), n] and have parity π_n. If u*(n) = n + 1, there are none.
- The number of parity-π_n integers in [u*(n), n] is (n + 1 - u*(n))/2, since u*(n) ≡ π_n ≡ n + 1 and u*(n) <= n + 1 (C006 (b)).
- This equals O*(n). All parity-π_n integers below u*(n) are used: there are (u*(n) - 1)/2 of them if n is even and (u*(n) - 2)/2 if n is odd. Exactly floor(n/2) used values have parity π_n (Step 2), and u*(n) itself is unused. So O*(n) = floor(n/2) minus that count, which is (n + 1 - u*(n))/2 in both cases. Hence H_π(n) <= O*(n).
- The base point satisfies a(n) + n + 1 >= a(n) + u*(n) = t_n, by C006 (b).

## Numerical check

`experiments/src/c006_holes_check.py` asserts the inequality for every n <= 10^7 (prover, 2026-11-24). Measured up to 10^7:
- max of the bound: 554, against 1542 for C006 (c') and an actual max upper displacement of 188;
- max H_π = 30, max H = 50, mean H = 8.8.

## Review log

- 2026-11-25: candidate created from C006 Remark R3a. **Awaiting skeptic.**
- 2026-11-25 (skeptic): **PASS** for the main inequality (depends only on L001, L002 and a(1) = 1). **PASS, conditional on C006 (b)** for the comparison H_π(n) <= O*(n) and the base-point remark a(n)+n+1 >= t_n; C006 is still a candidate, so those two remarks inherit its status. Checked:
  - Step 1: a(n)+n+1 odd and >= 3, so every q'_i is an odd prime, y_i >= n+1, y_i ≡ π_n; distinct and increasing. OK.
  - Step 2: #{k <= n : k ≡ n+1} = floor(n/2) in both parities of n; same count for parity-π_n integers in [1, n]; hence #{x ∈ U_n : x ≡ π_n, x > n} = H_π(n) exactly. OK (uses a(k) ≡ k, i.e. a(1) odd).
  - Step 3: pigeonhole over H_π+1 candidates, a(n+1) = min A_n <= y_j <= y_{H_π+1}. OK, no off-by-one.
  - Comparison: "(b')" is not in C006's Statement section (cited from its proof). Re-derived independently: all parity-π integers < u* are used, u* ≡ n+1, and floor(n/2) used values of parity π give O* = (n+1-u*)/2; parity-π integers in [u*, n] also number (n+1-u*)/2 when u* <= n+1. This needs C006 (b) (u* <= n+1). Suggest inlining this 3-line derivation instead of citing (b').
  - Numerics (own script, independent incremental hole count, cross-checked by brute recount for n < 3000 and sampled n < 2·10^5): 0 violations of the main inequality and 0 of H_π <= O* for n < 10^7 on sequence.npy; max bound 554, max H_π 30 (matches the file). Equality (disp = bound) is attained, so the bound is tight at some steps.
  - Variants a(1) = c ∈ {2,3,4,5,6,9,10}, 2·10^4 terms: main inequality holds for all c (the proof adapts: for even c the used-above-n count is H_π - (n mod 2) <= H_π). The comparison H_π <= O* FAILS for even c (~1565 steps each, e.g. u* = n, H_π = 1, O* = 0). The written comparison proof uses the a(1) = 1 parity via (b'), so it does not "prove" the false variant; but this shows the comparison is genuinely parity-dependent, not a general fact.
- 2026-11-25 (editor): inlined the derivation of O*(n) = (n+1-u*(n))/2 in the comparison, as the skeptic suggested, instead of citing C006 (b'). The argument is unchanged.
