# 2026-11-25 - Conditional theorem (direction 1) (prover)

## Goal

Find a hypothesis on the primes, as weak and as standard as possible, under which the permutation property can be proved. The task suggested short-interval hypotheses (H1) Cramér gaps, (H2) Selberg/Cramér uniformity for y >= (log x)^{2+δ}, and (H3) two-sided counts for y ~ log² x. It also asked:
- to explain whether such a hypothesis breaks the loop K <= H(v) + H(n) -> lifetimes -> H;
- if not, to say why, with a construction;
- to identify the minimal extra input.

## Idea

1. Test whether (H1)-(H3) can close the hole-counting loop. They cannot, and there is a clean obstruction: a pseudo-prime set satisfying all of them (and every lemma in the repo) for which the greedy sequence is not a permutation.
2. So the missing input is not about single primes in intervals. Find what *does* distinguish the primes from that model.
3. Answer: a second-generation cascade from a missing value, controlled by a blocking bound that is uniform in the size of the blocking set. It reduces the problem to a binary (Goldbach-for-differences) almost-all statement (G). (G) is implied by Hardy-Littlewood and is probably a theorem.

## Work

### 1. Does (H2) break the L009'/lifetime loop? No.

Assume (H2): π(x+y) - π(x) = (1 + o(1)) y/log x uniformly for y >= (log x)^{2+δ}. Let h = max_{m <= n} H(m).
- By L009' and its Corollary, every hole v at time n has K_n(v) <= 2h. So, by (H2), n - v <= max((log n)^{2+δ}, (2 + o(1)) h log n).
- All holes at time n lie in (n - L, n] with L = max lifetime, so H(n) <= L. This gives h_new <= max((log n)^{2+δ}, (2 + o(1)) h log n), and the multiplier 2 log n > 1 never contracts.
- (H2) is the *truth on average* for interval counts. So no improvement of the interval count can remove the factor log n: it is the honest cost of one prime.
- The loss comes from H <= L. Holes can fill their window with density up to about 1 (50 holes in 87 slots at the H = 50 event), while primes have density 1/log n.

The other inequalities of the repo have the same shape (L012: X^ε <= H(v) - 1; partner counts). More decisively, every inequality in the repo is of the form "K <= (counts of holes)". They are all satisfied by the missing-value profile H(n) ~ n/log n (that is exactly L011). **So no argument that combines them only with interval counts can ever exclude a missing value.**

### 2. The obstruction, made rigorous: the mod-6 model

Let Q be the set consisting of the first integer ≡ 1 (mod 6) after each point of t_{j+1} = t_j + log t_j. Then:
- Q has gaps <= log x + 6, which is better than Cramér;
- Q has (1 + o(1)) y/log x elements in every (x, x+y] with y/log x -> ∞ and y = o(x), so (H1), (H2) and two-sided (H3) all hold;
- its counting function is ~ li(x).

Run the greedy rule with "a(n) + x ∈ Q" in place of "prime". Every sum is ≡ 1 (mod 6), so the terms alternate between the classes 1 and 0 mod 6 (a(1) = 1), and 2, 3, 4, 5, 8, ... never occur.
- Script: `experiments/src/c013_mod6_model.py`.
- Output: sequence 1, 6, 7, 12, 13, 18, ...; used residues {0, 1}; all values < 60 outside these classes missing after 2·10^4 terms; random interval counts within 2.8% of y/log x; max gap 1.84 log x.

The proofs of L001-L012 use only "Q consists of odd numbers" (plus the PNT for Q in L004/L011, which holds). So all of them are true for this model, which still has H(n) ~ (2/3) n.

**Conclusion: (H1)/(H2)/(H3), together with everything proved so far, cannot imply the permutation property.** The missing input must see the *arithmetic* of the primes, at least their local distribution mod small primes. In fact it must see their *pair* correlations; see section 5.

### 3. The cascade (new, elementary)

**Blocking lemma (C013 (a)).** If S is a finite set of values that never occur, then

    #{ k : a(k) + m prime for some m ∈ S } <= max S - 1.

*Proof.* For such k, m is available at step k, so a(k+1) <= m, and a(k+1) ≠ m. So a(k+1) < max S, and k ↦ a(k+1) is injective. ∎

The bound does not depend on |S|. This is what the hole bookkeeping never had: a hole is available only until it is filled, but a *permanently* missing value is available forever. So a large set of small missing values can block only boundedly many steps.

**The cascade.** Let m0 be missing.
- *First generation.* By the lemma with S = {m0}, all but m0 - 1 of the values p - m0 (p prime) never occur. This is L003/L004.
- *Second generation.* Take S = { p - m0 : m0 < p <= Y, p - m0 missing }. Then, apart from <= Y exceptional times, every term a(k) of parity ≡ m0 satisfies: a(k) - m0 + p is composite for all primes p <= Y, except at most 2m0 of them.
- So h = a(k) - m0 lies in Bad_{2m0}(Z, Y) = { even h <= Z : fewer than 2m0 + 1 primes p <= Y have h + p prime }. Since a is injective, |Bad| >= N/2 - Y - m0 (C013 (c)).

**Growth.** Unconditionally, a(n) <= C0 n log n: this is the skeptic's L006 + PNT argument, written out as C013 (b). So the terms a(k), k <= N, lie in [1, Z] with Z ≍ N log N. Choosing Y = o(N) = o(Z/log Z) gives

    missing value  ⇒  |Bad_c(Z, Y)| >= (1/(2C0) - o(1)) Z/log Z   for every large Z and every Y = o(Z/log Z).

### 4. The conditional theorem (C013 (d))

**(G)** For every fixed c, along some Z -> ∞ with Y = o(Z/log Z): all but o(Z/log Z) even h <= Z have more than c representations h = q - p with p <= Y.

**(G) ⇒ the Watts sequence is a permutation.** The full proof is in `lemmas/candidates/C013-blocking-cascade-binary-hypothesis.md`. It uses only L001, L002, L006 and the PNT, and has no GAP? apart from the status of (G) itself.

Numerical sanity check for the primes (`experiments/src/c013_badset.c`):
- Z = 10^8, Y = Z/(ln Z)^2: every even h has r_Y(h) >= 30.
- Even with Y = (ln Z)^3 = 6,250, min r_Y(h) = 29.
- With Y = (ln Z)^2 at Z = 10^7, about 5.5·10^3 h have r = 0.

### 5. How weak is (G)? Is it a theorem?

- (G) follows from uniform Hardy-Littlewood for prime pairs (C013 R2). It needs only "almost all h", only r > c, and only along a subsequence.
- (G) does **not** need short-interval information: Y may be as large as Z/(log Z)^{1+η}.
- In the mod-6 model, (G) fails as the theorem predicts: Bad contains every h ≢ 0 (mod 6).
- *Expected status.* Provable by the classical circle method, in the Estermann (1938) almost-all-Goldbach scheme:
  - minor arcs: Vinogradov's bound for Σ_{p <= Y} e(pα), with sup over the minor arcs << Y (log)^{-A}, times Parseval for the long sum;
  - major arcs: Siegel-Walfisz. The arcs have width about (log)^B/Y, so one only needs the PNT in progressions mod q <= (log)^B on intervals of length Z/(log Z)^C, which Siegel-Walfisz gives pointwise;
  - main term: the standard mean-square evaluation of the singular series, giving exceptional set << Z (log Z)^{-A}.
- **GAP?** This is a sketch from memory. It is not written out, and I found no source stating the unbalanced-range difference version. A quick web search found only the balanced results (Estermann; Montgomery-Vaughan; "almost all even numbers are differences of primes") and Chen-type results with a small prime, none of which is exactly this. If (G) is a theorem, C013 (d) becomes **unconditional**. That claim must go through the literature agent, a skeptic and an analytic number theorist before anyone states it.
- Why a "unary" hypothesis does not suffice in this method: covering almost all of the parity class by the shifts { p - m0 : p <= Y } is precisely the statement that almost every even h is q - p with p small. That is a two-prime event. Upper-bound sieves plus Cauchy-Schwarz give only a positive proportion of good h, far from the 1 - o(1/log Z) needed. A purely unary hypothesis, such as AP-equidistribution in short intervals, is not obviously enough. Whether some cleverer argument works with one is open.

### 6. A structural (dynamics) hypothesis is not needed

The task suggested pairing (H2) with a dynamics hypothesis such as "down-crossings are O(log v)". Two reasons that is the wrong pairing:
- the crossings data (`crossings_1e8`) already refutes that hypothesis, since X tracks H;
- the mod-6 model does not formally rule out "(H2) + a dynamics hypothesis D", because D can fail for the model (H is linear there). But then D carries all the arithmetic content. The natural candidates are either refuted by the data (crossings O(log v)) or already imply the permutation property without (H2) (C010 in C log v form).

The cascade needs **no** dynamics input beyond the greedy rule and the growth bound.

## Outcome

- **Proved (elementary, candidate C013, awaiting skeptic):**
  - (a) the blocking lemma, uniform in |S|;
  - (b) a(n) = O(n log n), from L006 and the PNT;
  - (c) a missing value forces |Bad_{2m0}(Z, Y)| >= N/2 - Y - m0;
  - (d) **(G) ⇒ permutation.**
- **Shown:** interval-count hypotheses (H1)-(H3), even together with L001-L012, cannot suffice (mod-6 model). The L009'/lifetime loop loses exactly the factor log n that is the true cost of one prime, so no improvement in interval counts fixes it.
- **Hypothesis (G):** almost-all binary Goldbach-for-differences with one prime <= Z/(log Z)^2. It is implied by uniform Hardy-Littlewood and is probably a known or routine theorem (GAP?).

## Why it died / what survives

Direction 1 as posed (short-interval hypothesis + hole counting) is dead, for the structural reason in sections 1-2: every bound in the repo also holds for a Cramér-perfect pseudo-prime set whose greedy sequence misses 2/3 of N.

What survives, and supersedes it: C013. The bottleneck has moved entirely to analytic number theory. Is (G), with Y = Z/(log Z)^2 (or any Y = o(Z/log Z)), a theorem? Suggested next steps:
1. A skeptic pass on C013 (a)-(d). It is about one page and elementary.
2. The literature agent: search for "exceptional set" results for p' - p = h with p <= h^θ or p <= h/(log h)^B (Lavrik 1961; Mikawa; Perelli-Pintz; Montgomery-Vaughan 1975; Vaughan's *The Hardy-Littlewood Method*, ch. 3; Matomäki-Radziwiłł-Tao 2019). Also check whether the cascade argument itself appears for the EKG or Yellowstone sequences, or in the A253074 notes.
3. If nothing is citable, write the circle-method proof of (G) as its own candidate (C014), in the Estermann form with Siegel-Walfisz.
