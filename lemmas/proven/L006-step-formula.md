# L006 - Step formula: the next term is governed by primes after the frontier and the overshoot

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

_Written 2026-11-24 by the prover. Uses only the definition of the sequence, L001 and L002. No input from prime number theory: the only fact about primes used is that 2 is the only even prime._

### 0. Setup and conventions

Throughout, n >= 1 is fixed but arbitrary. By L002, a(1), ..., a(n+1) exist. They are pairwise distinct: for each k >= 1, a(k+1) is chosen outside U_k by definition. Hence |U_n| = n.

The definition of a(n+1) reads:

    a(n+1) = min A_n,   where A_n := { x >= 1 : x ∉ U_n, a(n) + x is prime }.   (D)

A_n is nonempty by L002, so the minimum exists.

By L001, a(k) ≡ k (mod 2) for every k >= 1 (a(1) = 1 and the parity alternates). In particular

    π_n ≡ n + 1 (mod 2)   and   a(n) ≢ π_n (mod 2).   (P)

**Step 0.1: every element of A_n has parity π_n.** Let x ∈ A_n and p = a(n) + x.
- If p = 2, then a(n) = x = 1. But then x = a(n) ∈ U_n, contradicting x ∉ U_n.
- So p is an odd prime, and x = p - a(n) ≢ a(n) (mod 2). By (P), x ≡ π_n.

(This is the L001 argument restated for an arbitrary candidate rather than only for a(n+1).)

**Step 0.2: u*(n) is well defined, and t_n is odd with t_n >= 3.**
- The set { x >= 1 : x ≡ π_n, x ∉ U_n } is nonempty, since U_n is finite. So u*(n) exists.
- By (P), a(n) and u*(n) have opposite parity, so t_n = a(n) + u*(n) is odd.
- Both are >= 1 and they are distinct (opposite parity), so t_n >= 1 + 2 = 3.

Consequently every prime q_i >= t_n satisfies q_i >= 3, so q_i is odd. Then, by (P), q_i - a(n) ≡ 1 - a(n) ≡ π_n (mod 2) for every i. (There are infinitely many q_i, by Euclid.)

### (a)

**Step a.1: a(n+1) >= u*(n).**
- a(n+1) ∈ A_n, so a(n+1) has parity π_n (Step 0.1), and a(n+1) ∉ U_n.
- So a(n+1) belongs to the set whose minimum is u*(n). Hence a(n+1) >= u*(n).

**Step a.2: s_n is one of the q_i.** Put s_n := a(n) + a(n+1).
- s_n is prime by (D).
- s_n >= a(n) + u*(n) = t_n by Step a.1.
- So s_n = q_j for a unique j >= 1.

Since q_1 < q_2 < ..., we have { i : q_i < s_n } = {1, ..., j-1}. So b(n) = j - 1, i.e. s_n = q_{b+1}, i.e.

    a(n+1) = q_{b+1} - a(n).

**Step a.3: blocked partners are used.** Fix i with 1 <= i <= b, and put x_i := q_i - a(n).
- x_i >= t_n - a(n) = u*(n) >= 1, so x_i is a positive integer.
- a(n) + x_i = q_i is prime.
- x_i < s_n - a(n) = a(n+1), since q_i < q_{b+1} = s_n.

If x_i ∉ U_n, then x_i ∈ A_n and x_i < a(n+1) = min A_n, a contradiction. Hence x_i ∈ U_n. This proves the "moreover" clause.

**Step a.4: b(n) <= O*(n).** For 1 <= i <= b:
- x_i ≡ π_n (mod 2) (Step 0.2);
- x_i ∈ U_n (Step a.3);
- x_i >= u*(n) (Step a.3), and x_i ≠ u*(n) because u*(n) ∉ U_n. So x_i > u*(n).

Hence x_i ∈ S := { x ∈ U_n : x ≡ π_n, x > u*(n) }, the set counted by O*(n). The map i ↦ x_i is injective, since the q_i are distinct. So b = |{x_1, ..., x_b}| <= |S| = O*(n).

**Edge case, b = 0.** This happens iff s_n = q_1. In particular, if q_1 = t_n (i.e. t_n is prime), then u*(n) ∈ A_n. By Step a.1 this forces a(n+1) = u*(n) and b = 0. This is consistent with the above and is not an extra case.

### (b) Exact count per parity

Since a(k) ≡ k (mod 2) (from (P)), the values of parity π_n ≡ n+1 used by time n are exactly a(k) for k <= n with k ≡ n+1 (mod 2). The number of such k in {1, ..., n} is:
- if n is even (π_n odd): #{odd k <= n} = n/2;
- if n is odd (π_n even): #{even k <= n} = (n-1)/2.

In both cases it is floor(n/2). Since the a(k) are distinct,

    #{ x ∈ U_n : x ≡ π_n } = floor(n/2).   (Cnt)

The number of integers in [1, n+1] of parity π_n ≡ n+1 is:
- if n is even: #{odd numbers in [1, n+1]} = n/2 + 1;
- if n is odd: #{even numbers in [1, n+1]} = (n+1)/2.

In both cases it is floor(n/2) + 1.

So [1, n+1] contains floor(n/2) + 1 values of parity π_n, and at most floor(n/2) of them are used. By pigeonhole, at least one value x in [1, n+1] with x ≡ π_n is not in U_n. Hence u*(n) <= x <= n + 1. ∎(b)

**Supplement (b'), exact overshoot identity (not in the original statement; proved here because it sharpens (c)).**

    O*(n) = (n + 1 - u*(n)) / 2.   In particular u*(n) ≡ n + 1 (mod 2).

Proof:
- By minimality of u*(n), every x in [1, u*(n) - 1] with x ≡ π_n is in U_n. Also u*(n) ∉ U_n.
- So the used values of parity π_n split into those < u*(n) and those > u*(n), and O*(n) = (Cnt) - #{ 1 <= x < u*(n) : x ≡ π_n }.
- u*(n) ≡ π_n ≡ n+1. Then:
  - If n is even, u* is odd and #{odd x < u*} = (u* - 1)/2, so O* = n/2 - (u* - 1)/2 = (n + 1 - u*)/2.
  - If n is odd, u* is even and #{even x < u*} = (u* - 2)/2, so O* = (n-1)/2 - (u* - 2)/2 = (n + 1 - u*)/2. ∎

(b') implies (b), since O*(n) >= 0. It also gives the exact identity

    a(n+1) - (n+1) = (q_{b(n)+1} - t_n) - 2 O*(n),   (E)

because a(n+1) - (n+1) = (a(n+1) - u*(n)) - (n + 1 - u*(n)) and a(n+1) - u*(n) = s_n - t_n = q_{b+1} - t_n.

### (c)

By (a), b(n) <= O*(n), and q_i is increasing in i. So q_{b+1} <= q_{O*(n)+1}. From (E) and O*(n) >= 0:

    a(n+1) - (n+1) = (q_{b+1} - t_n) - 2 O*(n)
                   <= (q_{O*(n)+1} - t_n) - 2 O*(n)        (c')
                   <=  q_{O*(n)+1} - t_n.                  (c)

The same follows without (b'): a(n+1) - (n+1) = q_{b+1} - a(n) - (n+1) = (q_{b+1} - t_n) + (u*(n) - (n+1)), and the last bracket is <= 0 by (b).

**Interpretation.** For K >= 1, put d_K := q_K - t_n. The interval [t_n, t_n + d] contains at least K primes iff q_K <= t_n + d. So d_K is the smallest d >= 0 such that [t_n, t_n + d] contains K primes. With K = O*(n) + 1 this is the interval statement in (c). ∎(c)

**Remark on (c').** It is never worse than (c). Since consecutive odd primes differ by at least 2,

    q_{O*+1} - t_n - 2O* = (q_1 - t_n) + Σ_{i=1}^{O*} (q_{i+1} - q_i - 2) >= 0.

(c') is attained exactly when b(n) = O*(n).

### GAP? marks

None. Every step uses only (D), L001, L002, and the fact that 2 is the only even prime. Points a skeptic should check:
1. Step 0.1 excludes the prime 2 for *all* candidates x, not only for a(n+1). This is what makes all q_i odd and puts the x_i in the right parity class.
2. Step a.4: "x_i > u*(n)" uses u*(n) ∉ U_n, not just x_i >= u*(n).
3. The count (Cnt) uses a(k) ≡ k (mod 2) for all k, which needs a(1) = 1.

## Numerical check

- (a) holds with equality for every n < 10^7: `experiments/src/overshoot_extra.py`, line "exact formula check: True" in `experiments/results/overshoot_1e7/extra.txt`.
- (b) holds for every n < 10^7: max u*(n) - n = 1.
- (c) holds for every n < 10^7. Correction (prover, 2026-11-24): the literal bound q_{O*+1} - t_n of (c) reaches **1740** for n <= 10^7 (1178 for n <= 10^6). The figure **1542** quoted earlier is the sharper bound (c') = q_{O*+1} - t_n - 2O*(n). Actual max upper displacement: 188.
- Re-checked for every n <= 10^7 with a prover's independent script, which asserts on every step: Step 0.2 (t_n odd, >= 3); (a), including that every blocked partner is used and > u*(n); b <= O*; (b); (b') O* = (n+1-u*)/2; the identity (E); (c'); (c); and Dlo(n+1) <= 2O*(n) (see Remarks). All passed.

## Review log

- 2026-11-24: stated from the overshoot experiment (session 2). **Awaiting prover, then skeptic.**
- 2026-11-24 (prover): full proof of (a), (b), (c) written, with no GAP? in the lemma itself. Added (b') O*(n) = (n+1-u*(n))/2, the exact identity (E) and the sharper bound (c'). Corrected the numerical note (1542 is the bound (c'); (c) itself reaches 1740). Checks are in `experiments/src/c006_check.py` and `c006_holes_check.py`. The Remarks section is **not** part of the lemma. Attempt file: `attempts/2026-11-24-c006-step-formula.md`. **Awaiting skeptic.**
- 2026-11-25 (skeptic): **PASS** for (a), (b), (b'), (E), (c), and the (c') remark. I read only the Statement, Depends on, Proof and GAP? sections (lines 1-147), not the Remarks, the attempt file or the prover's scripts.
  - Checked step by step: Step 0.1 excludes p = 2 for every candidate x, since a(n) = x = 1 would make x ∈ U_n. Step 0.2 shows t_n is odd and >= 3, so every q_i is odd and q_i - a(n) ≡ π_n. Step a.1 is minimality. Step a.2 uses s_n >= t_n, and b = j - 1 is right. Step a.3 shows x_i >= u* >= 1 and x_i < a(n+1), so x_i ∈ U_n by minimality of (D). Step a.4: x_i ≠ u* because u* ∉ U_n, and i ↦ x_i is injective. (Cnt) = floor(n/2) needs a(k) ≡ k (mod 2), which L001 gives (proven, trivial setup lemma) together with a(1) = 1. The integer count in [1, n+1] and the pigeonhole step are right in both parities. (b') is right in both parity cases; I recomputed (u*-2)/2 for even u*. (E) is an exact rearrangement. (c) follows from b <= O*, monotonicity of q_i and O* >= 0. The interval reading d_K = q_K - t_n is right, with "length" meaning d for [t, t+d]. The (c') remark holds because q_1 >= t_n and odd primes differ by >= 2, and equality holds iff b = O*. n = 1 also works: u* = 2, t = 3, O* = 0.
  - Dependencies: only L001 and L002, both in `lemmas/proven/`. No other input.
  - Numerical check (my own scripts, not the prover's). On `experiments/results/overshoot_1e7/sequence.npy` (10^7 terms) I recomputed u*(n) from the sequence. All of these hold for every n < 10^7: u* <= n+1; n+1-u* is even; b <= O* = (n+1-u*)/2 (max b = 15, max O* = 100); (E) holds exactly; every blocked partner q_i - a(n) with i <= b has first index <= n (4,894,240 steps with b > 0, 0 failures); and (c) holds. Checking blocked partners also confirms the stored sequence follows the greedy rule. A separate brute-force check (all parities searched, own generator) up to n = 2*10^4 also passes.
  - Variant test. With a(1) = 2 or 4, (a) still holds, but (b'), (E) and (c) fail from n = 1 or 2 on; for example, a(1) = 2 gives u*(2) = 4 > 3. The proof uses a(1) = 1 exactly at (Cnt), as its GAP? note 3 says, so it does not "prove" the false variant. The composite-sum variant is not covered, because Step 0.1 fails there.
  - Cosmetic, not a gap: q_i, b and O* depend on n, but the notation hides this. It is clear from context.

### literature

- 2026-11-24 (literature agent): **Not found.** Checked the raw OEIS files for A055265, A282695, A282696, A086527 and A128280, plus web searches. No source states the step formula or the frontier/overshoot displacement bound. Part (a) is immediate from the greedy rule, so treat it as elementary or folklore, not new. The EKG and Yellowstone proofs could not be read because their hosts are unreachable, so a "frontier + blocked candidates" analogue there is unchecked. See `literature/search-C006-step-formula.md`.

---

## Remarks

The prover's Remarks (R0-R4: prime-counting consequences, circularity, the holes version, and what is missing) are not part of this lemma. They were moved on 2026-11-25 to `attempts/2026-11-24-c006-remarks.md`. R3a/R3b became L007/L008. R1 (the Huxley-based bound and a(n) = O(n log n)) is unreviewed.
- 2026-11-25 (main-session review, with Matteo's delegated OK): PASS. Re-derived (a), (b), (b') in both parities ((n+1-u*)/2 via (u*-1)/2 or (u*-2)/2), (E) and (c). The prover's Remarks were moved to attempts/2026-11-24-c006-remarks.md, because they contain unreviewed material (R1). **Moved to lemmas/proven/ as L006 (formerly C006).**
