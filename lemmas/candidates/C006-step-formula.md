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

### literature

- 2026-11-24 (literature agent): **Not found.** Checked the raw OEIS files for A055265, A282695, A282696, A086527 and A128280, plus web searches. No source states the step formula or the frontier/overshoot displacement bound. Part (a) is immediate from the greedy rule, so treat it as elementary or folklore, not new. The EKG and Yellowstone proofs could not be read because their hosts are unreachable, so a "frontier + blocked candidates" analogue there is unchecked. See `literature/search-C006-step-formula.md`.

---

## Remarks (NOT part of the lemma; prover, 2026-11-24)

Everything below is separate from C006. Each item is labelled **[proved]** (elementary, from C006 and the definitions), **[proved modulo cited theorem]**, or **[speculative]**. Notation:
- Dup(k) = a(k) - k and Dlo(k) = k - a(k).
- H(n) = #{ v <= n : v ∉ U_n } is the number of holes below n at time n.
- H_π(n) = the same count restricted to v ≡ π_n (mod 2).

### R0. Prime-counting inputs, with exact forms

- **Huxley (1972)**, "On the difference between consecutive primes", Invent. Math. 15, 164-170 (see also Iwaniec-Kowalski, *Analytic Number Theory*, ch. 10). For every ε > 0,

      π(x) - π(x - y) = (1 + o(1)) y / log x   as x -> ∞, uniformly for x^{7/12+ε} <= y <= x.

  Recalled from memory, not re-read in this session; it is the standard form.

  We use it with ε = 1/60 (7/12 + 1/60 = 0.6). This gives x_1 such that for all t >= 1 and d >= 1 with t + d >= x_1 and d >= (t + d)^{0.6}:

      #{ primes in (t, t + d] } >= d / (2 log(t + d)).   (H)

  To get (H), take x = t + d and y = d. Then y <= x automatically, so no condition "d <= t" is needed.

- **Baker-Harman-Pintz (2001)**, "The difference between consecutive primes, II", Proc. London Math. Soc. (3) 83, 532-562.
  - Theorem 1: for all x > x_0, [x - x^{0.525}, x] contains a prime. Confirmed via a search snippet of the paper; the full text was not reachable.
  - The quantitative form "≥ (9/100) x^{0.525} / log x primes" is recalled from memory. **GAP? (citation detail, unverified).** It only affects the exponent of the harmless n^{0.6} term below, not any conclusion.

- **Brun-Titchmarsh, in the Montgomery-Vaughan form** (The large sieve, Mathematika 20 (1973) 119-134): for all x >= 1 and y > 1, π(x + y) - π(x) < 2y / log y.

### R1. Best clean bound from (c) [proved modulo Huxley; constants not optimized]

There are absolute constants n_0 and C such that for all n >= n_0:

    a(n+1) - (n+1)  <=  q_{O*(n)+1} - t_n - 2O*(n)  <=  n^{0.61} + 3 (O*(n) + 1) log n.

With the quantitative BHP bound (GAP? above), 0.61 can be replaced by 0.53. Under RH, by any exponent > 1/2.

**Proof sketch.** Write K = O*(n) + 1 <= n/2 + 1.

1. *Reduction to (H).* By (H), q_K - t_n <= d for any d with:
   - t_n + d >= x_1;
   - d >= (t_n + d)^{0.6};
   - d >= 2K log(t_n + d).

2. *Choice of d.* Take Z := 3 max(t_n, 2n log(t_n + n), x_1^2, 10^6) and d := Z^{0.6} + 2K log Z.
   - For n large, t_n + d <= Z/3 + Z^{0.6} + (n + 2) log Z <= Z. The last term is <= Z/3 because log Z <= 1.5 log(t_n + n) for large n.
   - So all three conditions hold, and Dup(n+1) <= d.

3. *Polynomial bootstrap.* Since t_n <= a(n) + n + 1, step 2 gives a(n+1) <= n + 1 + d.
   - Assume a(n) <= B n^2. Then a(n+1) <= n + 1 + O_B((n^2)^{0.6}) + O(n log n) <= B(n+1)^2. Here B is chosen large enough to absorb both the initial segment n <= n_1 and the constants.
   - Feeding the bound back twice by the same induction (a(n) <= B' n^{1.21}, then a(n) <= B'' n log n) gives a(n) = O(n log n).
   - Then log Z <= log n + log log n + O(1), and Z^{0.6} <= n^{0.61} for large n.

**Unconditional by-product (same proof, O* <= n/2):** a(n) = O(n log n). This is weak, but I could not find any proved growth bound in the literature notes. Before citing it, it should go through skeptic review as its own candidate.

**Optimality of the method (Brun-Titchmarsh).**
- [t_n, q_K] contains K primes, so with y = q_K - t_n + 1 we get K < 2y / log y. Hence q_K - t_n >= (1/2 - o(1)) K log K.
- So route (c) can never give better than about (1/2) O*(n) log O*(n).
- To get Dup(n) = o(n / log n), as C005 needs, route (c) therefore needs **O*(n) = o(n / (log n)^2)**. This is sufficient by R1, and necessary up to the log K vs log n distinction.
- The data agree that (c) is very lossy: for n <= 10^7, the (c) bound has max 1740, (c') has max 1542, and the true Dup has max 188.

### R2. Why the (c) route is circular with respect to C005 [proved]

(i) **O* controls the lower displacement:** Dlo(n+1) <= 2O*(n).
By Step a.1 and (b'): n + 1 - a(n+1) <= n + 1 - u*(n) = 2O*(n).

(ii) **The lower displacement controls O*:** if u*(n) = a(k), then k > n (since u*(n) ∉ U_n) and

    Dlo(k) = k - u*(n) >= n + 1 - u*(n) = 2O*(n).

So sup O* and sup Dlo are the same quantity up to a factor 2: the overshoot is the lower displacement seen from the frontier. This matches the experiment's O = n + 1 - u(n), which is >= 2O*.

(iii) **The input is stronger than the output.** Assume O*(n) = o(n), even without the (log n)^2. Then M = ∅ directly, with no need for C005:
- Given v >= 1, pick n large with n + 1 ≡ v (mod 2) and 2O*(n) < n + 1 - v.
- Then u*(n) = n + 1 - 2O*(n) > v and v ≡ π_n, so v ∈ U_n by minimality of u*.

So the chain "(c) + Huxley + C005" needs a hypothesis (O* = o(n / (log n)^2)) that is strictly stronger than its conclusion.

(iv) **Averaging O* does not help.** Suppose M ≠ ∅, with m = min M. For every n >= m with n + 1 ≡ m (mod 2), u*(n) <= m, so O*(n) >= (n + 1 - m)/2. Hence Σ_{n<=X} O*(n) >= X^2/8 - O(mX).
- So any averaged hypothesis Σ_{n<=X} O*(n) = o(X^2), even along a subsequence, already implies M = ∅ by itself.
- **Every input phrased through the frontier u*, pointwise or averaged, is as strong as the conclusion.** A single permanent hole makes O* linear.

### R3. A non-circular replacement: holes instead of frontier [proved, elementary]

**R3a (hole-count step bound).** Let q'_1 < q'_2 < ... be the primes >= a(n) + n + 1. Then for all n >= 1:

    a(n+1) - (n+1)  <=  q'_{H_π(n)+1} - (a(n) + n + 1).

*Proof.*
- **The y_i are valid candidates.** a(n) + n + 1 >= 1 + 2 = 3 and a(n) + n + 1 is odd by (P), so every q'_i is odd. Then y_i := q'_i - a(n) ≡ π_n, y_i >= n + 1, a(n) + y_i is prime, and the y_i are distinct.
- **Exactly H_π(n) used values of parity π_n exceed n.**
  - By (Cnt), exactly floor(n/2) used values have parity π_n.
  - [1, n] contains floor(n/2) integers ≡ n + 1 (mod 2). Of these, exactly floor(n/2) - H_π(n) are used.
  - Subtracting, exactly H_π(n) used values of parity π_n exceed n.
- **One y_i is unused.** Among y_1, ..., y_{H_π+1}, at least one is not used. It lies in A_n, so a(n+1) <= y_{H_π+1}. ∎

H_π(n) <= O*(n), since the holes of parity π_n that are <= n lie in [u*, n]. So R3a counts fewer primes than (c), from a base point a(n) + n + 1 >= t_n. With Huxley exactly as in R1:

    Dup(n+1) <= n^{0.61} + 3 (H_π(n) + 1) log n   for n >= n_0.

Data, n <= 10^7: R3a bound max 554 (vs 1542 for (c')); H_π <= 30; H <= 50; mean H = 8.8.

**R3b (density reduction, conditional on C004).**
- **Identity:** H(X) = #{ k <= X : a(k) > X }. Proof: |U_X| = X.
- **Claim:** if liminf_{X->∞} H(X) log X / X = 0, then M = ∅.
- **Proof:** M ∩ [1, X] ⊆ [1, X] \ U_X, so |M ∩ [1, X]| <= H(X). C004 with Chebyshev gives |M ∩ [1, X]| >> X / log X for all large X whenever M ≠ ∅.
- **Averaged corollary.** Let S(X) = Σ_{k<=X} max(a(k) - k, 0). For every integer D >= 1, H(X) <= D + S(X)/D. (The k > X - D contribute at most D; any other k with a(k) > X has a(k) - k > D.) So S(X) = o(X^2 / (log X)^2) along a subsequence already gives M = ∅.
- **Why this is a genuine weakening.** A permanent hole contributes 1 to H, not ~X as it does to O*. So, unlike (iii)-(iv), this hypothesis is not trivially equivalent to the conclusion. Its strength comes only from C004.

### R4. What is still missing [speculative]

- **R3a closes a recursion in the upper displacement alone, but the recursion does not contract.**
  - Since H_π(n) <= H(n) <= #{ k <= n : Dup(k) > n - k } <= max_{k<=n} Dup(k), we get

        D(n+1) <= n^{0.61} + 3 (D(n) + 1) log n,   where D(n) := max_{k<=n} Dup(k).

  - This breaks the link to the lower displacement, but it has a multiplier of 3 log n > 1, so iterating it gives nothing.
  - Averaging does not help either. There is an exact identity Σ_{n<=X} H(n) = Σ_{k<=X} (min(a(k), X+1) - k)^+ (numerically, sum H = 88,212,972 vs sum Dup^+ = 88,213,040 at 10^7). Averaging R3a therefore gives S <= 3 log X · S + ..., again with no contraction.
- **The loss is structural.** Each hole can cost up to a whole run of blocked primes (about log n per prime) of displacement, and Brun-Titchmarsh shows that no prime-counting input can lower the per-hole cost below about (1/2) log.
- **What would suffice** (any one of these, together with C004 via R3b):
  1. H(X) = o(X / log X) for infinitely many X; or equivalently-in-strength S(X) = o(X^2 / (log X)^2) along a subsequence.
  2. A statement that the partners y_i = q'_i - a(n) are *not* systematically used. For example, on average over n the number of i <= H_π(n) + 1 with y_i used is at most (1 - δ) times the trivial count, with the deficit converted into a bound H(n+1) <= H(n) - (filling events) + (creation events) that has net negative drift when H(n) is large.

  This is the "holes get filled" (wait-time / reflection-lock) content of STRATEGY route 1. No prime-counting estimate supplies it; it needs structure of the sequence itself.
- **Bottom line.**
  - (c) and its hole version R3a convert the problem into bounding holes.
  - R3b shows that a density bound on holes (o(X / log X) infinitely often) is enough with C004, and that is the weakest target found here.
  - No proof of it is in sight.
