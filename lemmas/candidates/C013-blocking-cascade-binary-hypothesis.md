# C013 - Permanent holes block their whole parity class; a binary Goldbach-type hypothesis implies the permutation property

## Statement

Notation.
- P is the set of primes. "m occurs" means m = a(k) for some k >= 1; M is the set of values that never occur.
- For real Y >= 1 and integer h >= 1: r_Y(h) := #{ p ∈ P : p <= Y, h + p ∈ P }.
- For real Z, Y >= 1 and integer c >= 0: Bad_c(Z, Y) := { h ∈ [1, Z] : h even, r_Y(h) <= c }.

**(a) Blocking lemma (unconditional).** Let S be a nonempty finite set of positive integers, none of which occurs. Then

    #{ k >= 1 : a(k) + m ∈ P for some m ∈ S }  <=  max S - 1.

In particular (S = {m0}): if m0 never occurs, then at most m0 - 1 primes p > m0 have p - m0 occurring.

**(b) Growth (unconditional; PNT).** There is an absolute constant C0 such that a(n) <= C0 n log n for every n >= 2.

**(c) A missing value forces a large exceptional set (unconditional).** Suppose m0 never occurs. Then for every integer N >= 1, every real Y >= 1 and every real Z >= max_{k <= N} a(k):

    |Bad_{2m0}(Z, Y)|  >=  (N - 1)/2 - Y - m0 + 1.

**(d) Conditional theorem.** Assume

> **(G)** For every integer c >= 0 there are sequences Z_j -> ∞ and Y_j >= 1 such that
>
>     Y_j log Z_j / Z_j -> 0   and   |Bad_c(Z_j, Y_j)| log Z_j / Z_j -> 0.

Then every positive integer occurs, i.e. the Watts sequence is a permutation of N.

The canonical instance of (G) is Y = Z/(log Z)^2 for all large Z: "all but o(Z/log Z) even h <= Z have more than c representations h = q - p with q, p prime and p <= Z/(log Z)^2".

**(d') Sharper form (same proof).** With C0 from (b), it suffices that for some δ > 0 and every c >= 0 there are Z_j -> ∞ and Y_j with Y_j <= δ Z_j/log Z_j and |Bad_c(Z_j, Y_j)| <= (1/(2C0) - 2δ) Z_j/log Z_j.

**Scope.** (a) uses only the greedy rule and injectivity; it holds for every start a(1) and for "prime" replaced by any set Q. (c) uses a(1) = 1 (through L001's a(k) ≡ k) and the fact that all primes involved are odd.

## Depends on

- L001 (a(k) ≡ k mod 2), L002 (well defined, injective).
- L006 (c) and (b), (b') (step formula; u*(n) <= n+1; O*(n) = (n+1-u*(n))/2), for (b).
- The prime number theorem, only as: π(x) - π(3x/4) >= x/(5 log x) for all x >= x_2 (some absolute x_2), for (b).
- For (d): hypothesis (G). **(G) is not proved here.** See Remarks for what implies it and its status.

## Proof

### (a)

Let k >= 1 and m ∈ S with a(k) + m ∈ P.
- m never occurs, so m ∉ U_k = {a(1), ..., a(k)}. With a(k) + m prime, m belongs to A_k = { x >= 1 : x ∉ U_k, a(k) + x ∈ P }.
- a(k+1) = min A_k, so a(k+1) <= m. And a(k+1) ≠ m, because a(k+1) occurs and m does not. Hence 1 <= a(k+1) <= m - 1 <= max S - 1.

So the map k ↦ a(k+1) sends the set in question into [1, max S - 1]. It is injective because the sequence is injective (L002) and k ↦ k + 1 is injective. Hence the set has at most max S - 1 elements.

For S = {m0}: if p > m0 is prime and p - m0 = a(k), then a(k) + m0 = p ∈ P, so k is in the set above, which has <= m0 - 1 elements. The map p ↦ k is injective (p = a(k) + m0). ∎

### (b)

_This is the skeptic's suggested proof in `attempts/2026-11-24-c006-remarks.md` (review of R1), written out._

Fix n >= 1 and use the notation of L006: u*(n), t_n = a(n) + u*(n), the primes q_1 < q_2 < ... that are >= t_n, and O*(n).
- By L006 (c): a(n+1) - (n+1) <= q_K - t_n with K = O*(n) + 1.
- By L006 (b'): O*(n) = (n + 1 - u*(n))/2 <= n/2, since u*(n) >= 1. So K <= n/2 + 1.
- By L006 (b): u*(n) <= n + 1, so t_n <= a(n) + n + 1.

If an interval [t_n, t_n + d] contains at least K primes, then q_K <= t_n + d. Choose

    D = 12 n log n,   d = ceil(t_n / 3) + D,   x = t_n + d.

- Since 3d >= t_n, we have 3x/4 = (3 t_n + 3d)/4 >= t_n, so (3x/4, x] ⊆ [t_n, t_n + d].
- Let n_1 >= 10 be such that 12 n log n >= max(x_2, e) for n >= n_1. For n >= n_1, x >= D >= x_2, so the PNT form gives π(x) - π(3x/4) >= x/(5 log x) >= D/(5 log D), using that x/log x is increasing for x >= e.
- For n >= 10, D = 12 n log n <= n^4, so log D <= 4 log n and D/(5 log D) >= 12 n log n/(20 log n) = 0.6 n >= n/2 + 1 >= K.

So for n >= n_1: a(n+1) <= n + 1 + d <= n + 1 + (a(n) + n + 1)/3 + 1 + 12 n log n, i.e.

    a(n+1) <= a(n)/3 + (4/3)(n + 1) + 1 + 12 n log n <= a(n)/3 + 13 n log n,

where the last step uses (4/3)(n+1) + 1 <= n log n for n >= 10.

Induction. Put C0 = max(20, max_{2 <= n <= n_1} a(n)/(n log n)). Then a(n) <= C0 n log n for 2 <= n <= n_1. If it holds for some n >= n_1, then a(n+1) <= (C0/3 + 13) n log n <= C0 n log n <= C0 (n+1) log(n+1), because C0/3 + 13 <= C0 for C0 >= 19.5. ∎

(Only a lower bound for primes in (3x/4, x] is used; Chebyshev's bounds would also do with a different ratio in place of 3/4. Not optimized.)

### (c)

Fix N, Y, Z as in the statement, and put ε = m0 mod 2. Note m0 >= 2, since a(1) = 1 occurs.

**Step 1: the blocking set.** Let

    S = { p - m0 : p ∈ P, m0 < p <= Y, p - m0 never occurs }.

Every element of S is a positive integer that never occurs, and every element is <= Y - m0 < Y. Let K_S = { k >= 1 : a(k) + m ∈ P for some m ∈ S }. By (a), |K_S| <= max S - 1 < Y if S ≠ ∅, and K_S = ∅ if S = ∅. In both cases |K_S| <= Y - 1 (if Y < 1 + m0 then S = ∅).

**Step 2: the times of parity ε.** Let T = { k ∈ [1, N] : k ≡ ε (mod 2) }. Then |T| >= (N - 1)/2. By L001 (a(k) ≡ k mod 2, using a(1) = 1), a(k) ≡ ε for every k ∈ T. Let

    T' = { k ∈ T : k ∉ K_S, a(k) > m0 }.

At most m0 - 1 indices k have a(k) <= m0 - 1, and none has a(k) = m0. So |T'| >= (N - 1)/2 - (Y - 1) - (m0 - 1).

**Step 3: each k ∈ T' gives an element of Bad_{2m0}(Z, Y).** Fix k ∈ T' and put h = a(k) - m0.
- h >= 1 because a(k) > m0; h <= a(k) <= Z because k <= N; h is even because a(k) ≡ m0 (mod 2).
- Let p <= Y be a prime with h + p ∈ P. Note p is odd (p = 2 would make h + p even and >= 4).
  - Case p <= m0: there are at most π(m0) <= m0 - 1 such primes.
  - Case m0 < p <= Y: h + p = a(k) + (p - m0) ∈ P. If p - m0 never occurred, then p - m0 ∈ S and k ∈ K_S, contradicting k ∈ T'. So p - m0 occurs, and by (a) with S = {m0} there are at most m0 - 1 such primes p.
- Hence r_Y(h) <= 2m0 - 2 <= 2m0, i.e. h ∈ Bad_{2m0}(Z, Y).

**Step 4: count.** The map k ↦ h = a(k) - m0 is injective on T' (the sequence is injective). So

    |Bad_{2m0}(Z, Y)|  >=  |T'|  >=  (N - 1)/2 - Y - m0 + 2  >=  (N - 1)/2 - Y - m0 + 1.   ∎

### (d)

Suppose some value never occurs, and let m0 be one; m0 >= 2. Put c = 2m0 and take the sequences Z_j, Y_j given by (G) for this c. For j large, put

    N_j = floor( Z_j / (C0 log Z_j) ),

with C0 from (b). Then N_j >= 2 for j large, and for 2 <= k <= N_j, a(k) <= C0 k log k <= C0 N_j log N_j <= C0 N_j log Z_j <= Z_j. Also a(1) = 1 <= Z_j. So Z_j >= max_{k <= N_j} a(k), and (c) applies:

    |Bad_c(Z_j, Y_j)|  >=  (N_j - 1)/2 - Y_j - m0 + 1  >=  Z_j/(2 C0 log Z_j) - Y_j - m0 - 1.

Multiply by log Z_j / Z_j. The right side becomes 1/(2C0) - Y_j log Z_j/Z_j - (m0 + 1) log Z_j / Z_j, which tends to 1/(2C0) > 0 by the first condition of (G). The left side tends to 0 by the second condition of (G). Contradiction. Hence no value is missing. ∎

(d') is the same computation with explicit constants: the right side is >= (1/(2C0) - δ - o(1)) Z_j/log Z_j.

## Remarks

**R1. What (G) is.** (G) is an "almost all" statement about the *binary* problem h = q - p with one prime restricted to p <= Y, where Y is only a power of log shorter than Z. It concerns pairs of primes, not the distribution of single primes in intervals.

**R2. Hypotheses that imply (G).**
- *Uniform Hardy-Littlewood for prime pairs* (conjecture): #{ p <= Y : p + h ∈ P } = (1 + o(1)) S(h) ∫_2^Y dt/(log t log(t + h)), uniformly for even 1 <= h <= Y (log Y)^3, as Y -> ∞, where S(h) = 2 C2 Π_{ℓ | h, ℓ > 2} (ℓ-1)/(ℓ-2) >= 2 C2 > 1. With Y = Z/(log Z)^2 this gives r_Y(h) -> ∞ uniformly in even h <= Z, so Bad_c(Z, Y) = ∅ for Z large. Much less is needed: only "almost all h", and only r_Y(h) > c.
- **GAP? (status of (G)).** (G) with Y = Z/(log Z)^2 is very probably provable unconditionally by the classical circle method: Vinogradov's minor-arc bound for Σ_{p <= Y} e(pα), Siegel-Walfisz on the major arcs (the major arcs have width about (log Z)^B / Y, and Siegel-Walfisz gives the PNT in progressions to small moduli on intervals of length Z/(log Z)^C), and the standard singular-series mean values. This is the same scheme as the Chudakov-van der Corput-Estermann theorem (1937-38) that almost all even numbers are sums of two primes, with exceptional set << Z (log Z)^{-A}. The difference here is the unbalanced range p <= Z/(log Z)^2 and the difference q - p in place of a sum. **I have not written this out and have not found a source that states exactly this.** Lavrik (1961, prime pairs for almost all h) and Mikawa (1991) / Matomäki-Radziwiłł-Tao (2019, long shift ranges) treat related averages over shifts, but in different ranges (shift <= length of the prime range). This needs the literature agent and, ideally, an analytic number theorist. If (G) is a theorem, then (d) is an unconditional proof of the conjecture, so this point must be checked with particular care.

**R3. (G) is not implied by any hypothesis on counts of primes in intervals (H1, H2, two-sided H3).** Let Q be a set of integers ≡ 1 (mod 6), with one element just after each point of the sequence t_{j+1} = t_j + log t_j. It has gaps <= log x + 6 and (1 + o(1)) y/log x elements in every interval (x, x+y] with y/log x -> ∞ and y = o(x), which is stronger than Cramér, and its counting function is ~ li(x). Run the greedy rule with "prime" replaced by "in Q". Then every sum is ≡ 1 (mod 6), so a(k) ≡ 1 or 0 (mod 6) for every k, and 2, 3, 4, 5, ... never occur. (`experiments/src/c013_mod6_model.py`: for 2·10^4 terms, the sequence is 1, 6, 7, 12, 13, 18, ...; the used residues mod 6 are {0, 1}; interval counts are within 3% of y/log x; the max gap is 1.84 log x.) All proofs of L001-L012 go through for this Q, since they use only "Q is a set of odd numbers", plus the PNT for Q for L004/L011, which also holds. So **no argument that uses the primes only through interval counts (plus the repo's lemmas) can prove the permutation property.** For this Q, Bad_c(Z, Y) contains all even h ≢ 0 (mod 6): this is exactly the failure of (G) that (c) predicts.

**R4. Why this escapes the H-barrier.** L009'/L011 use only the first generation of partners of a missing value, p - m0, and count them against hole counts. (c) uses the second generation: the partners p - m0 are themselves missing forever, so each of them is *available at every later step*. By (a), all of them together can block at most max S - 1 steps. This bound is uniform in |S|, and that is the whole point. So almost every later term of parity ε has to dodge all the shifted primes p - m0 + (prime), which is a binary additive condition on a(k) - m0. No hole count H appears anywhere.

**R5. Prior art.** (a) with S = {m0} is the classical smallest-missing step (EKG, Lagarias-Rains-Sloane 2002, Lemmas 3-4; Devlin-Artamonov in A253074; L003/L004 here). The union bound "max S - 1, independent of |S|" and the second-generation cascade were not found in the repo's literature notes. **Literature check needed (rule 3).**

## Numerical check

- (a), finite-time form (m unused at time n, k <= n - 1, a(k) + m prime ⇒ a(k+1) < m): `experiments/src/c013_blocking_check.py`, on the first 2·10^6 terms, at 21 times n, with S = all holes at time n. It tested 13,273,867 pairs (k, m), with 0 violations.
- (G) for the actual primes (`experiments/src/c013_badset.c`): for every even h <= 10^8, r_Y(h) >= 30 with Y = Z/(ln Z)^2 = 294,705. Even with Y = (ln Z)^3 = 6,250, min r_Y(h) = 29 (at h = 75,997,078). So Bad_c(10^8, Y) = ∅ for c <= 28 in both cases. With Y = (ln Z)^2 = 259 and Z = 10^7, 5,507 even h have r = 0. So Y must grow faster than log^2, as expected.
- (b): the data has a(n) <= n + 292 for n <= 10^8, far below C0 n log n.

## Review log

- 2026-11-25 (prover): created. (a), (c) and (d) are complete, elementary and short. (b) is the skeptic's sketch from the R1 review, written out. (G) is the open input (R2, GAP?). **Awaiting skeptic, literature agent (on (G) and on R5), and Matteo.**
