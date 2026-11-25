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
- The number of parity-π_n integers in [u*(n), n] is (n + 1 - u*(n))/2 = O*(n), using C006 (b'). Hence H_π(n) <= O*(n).
- The base point satisfies a(n) + n + 1 >= a(n) + u*(n) = t_n, by C006 (b).

## Numerical check

`experiments/src/c006_holes_check.py` asserts the inequality for every n <= 10^7 (prover, 2026-11-24). Measured up to 10^7:
- max of the bound: 554, against 1542 for C006 (c') and an actual max upper displacement of 188;
- max H_π = 30, max H = 50, mean H = 8.8.

## Review log

- 2026-11-25: candidate created from C006 Remark R3a. **Awaiting skeptic.**
