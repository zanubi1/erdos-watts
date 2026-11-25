# 2026-11-25 - C010: bounded prime survival (prover)

## Goal

- **Task A.** Write the full rigorous proof of C009 and its Corollary, with the per-parity count as an explicit sub-lemma and the edge cases checked. Done in `lemmas/candidates/C009-hole-prime-count.md`.
- **Task B.** Attack C010, its weak version (π(n+v) - π(2v) <= F(v) for every hole v at time n), or any nontrivial conditional version.

Notation is as in C009. In addition, for a hole v at time n (2 <= v <= n, v ∉ U_n, ε = v mod 2):
- K_n(v) := π(n+v) - π(2v);
- Ahead(v) := W1, Steal(v,n) := W2, Late(v,n) := W4, as in the C009 proof.

So:
- Ahead(v) is the set of partners w = q - v already used at time v - 1;
- Steal(v,n) is the set of partners first used at a time in [v, n-1];
- Late(v,n) is the set of partners that are still holes at time n.

## Idea

C009 charges each prime that v survives to one of four payers. C010 needs the number of payers that are actually prime partners of v to be O(1), whereas C009 only bounds the number of possible payers, by about 3H.

Four routes were tried, followed by a data check of whether C010 is even the right conjecture:
1. find an exact sharpening of C009;
2. iterate C009, applying it to the partners themselves or to the steal victims;
3. use window localisation (holes are dense in [n-86, n]) together with Brun-Titchmarsh, and conditional prime-count hypotheses;
4. a bootstrap or potential argument closing H <-> K.

## Work

### 1. Sharpening of C009 (proved; written in the C009 file)

**Proposal P1 (C009').** For every hole v at time n,

    K_n(v) <= H(v) + H_{1-ε}(n).

- The identity 1 + B(v) + H_{1-ε}(v-1) = H(v) is exact. It holds because:
  - H_ε(v) = B(v) + 1, since v is itself a hole at time v;
  - H_{1-ε}(v-1) = H_{1-ε}(v), since a(v) ≡ ε.
- The Corollary improves to n - v < ℓ_{2h+1}(2v).
- **Tightness (data, `experiments/src/c009_sharp_check.py`).** Checked on all 4,712,615 holes at n = fi(v) - 1, with 0 violations.
  - Equality K = H(v) + H_{1-ε}(n) holds 1,887 times, with K up to 5 and v up to 9.9·10^6. So C009' cannot be improved by a constant factor in general.
  - Equality, however, only occurs when the right side is <= 9:

    | right side | max K / rhs | max K |
    |---|---|---|
    | 10-19 | 0.60 | 8 |
    | 20-39 | 0.38 | 8 |
    | 40-99 | 0.20 | 8 |

  - Mean K is about 0.9 in every bin.

### 2. Shifted-start version (proved here; proposal, no candidate file)

**Proposal P2 (C009-t).** Let v ∉ U_n, 2 <= v <= t <= n, and ε = v mod 2. Put B_t(v) = #{ x < v : x ≡ ε, x ∉ U_t }. Then

    π(n+v) - π(t+v)  <=  H_{1-ε}(t-1) + B_t(v) + 1 + H_{1-ε}(n).

**Proof.**
- **Primes and partners.** Let q be a prime in (t+v, n+v]. Then q > 2v >= 4, so q is odd, and w = q - v ∈ (t, n] has parity 1 - ε.
- **Case fi(w) <= t - 1.**
  - Then w ∈ U_{t-1} and w > t - 1.
  - By Sub-lemma S of C009 with m = t - 1 >= 1, there are at most H_{1-ε}(t-1) such w.
- **Case t <= k := fi(w) <= n - 1.**
  - This is C009 Step 3 verbatim. a(k) + v = q is prime and v ∉ U_k, so a(k+1) <= v. Also a(k+1) ≠ v, since k + 1 <= n. Hence x = a(k+1) < v.
  - x ≡ ε, and x ∉ U_k ⊇ U_t.
  - The map w ↦ x is injective, so there are at most B_t(v) such w.
- **Case fi(w) = n.** Then w = a(n), so there is at most one such w.
- **Case fi(w) > n (or ∞).** Then w is a parity-(1-ε) hole at time n, so there are at most H_{1-ε}(n) such w. ∎

**Frontier corollary.** If v is the smallest parity-ε hole at time t, then B_t(v) = 0 and

    π(n+v) - π(t+v) <= 1 + H_{1-ε}(t-1) + H_{1-ε}(n).

In this form only **opposite-parity** holes pay.
- Data, with t = T0(v) = max(v, s(v)) and n = fi(v) - 1: 1,692,894 frontier holes, 0 violations.
- The left side is at most 7, and the right side reaches 55.

### 3. A permanent hole forces many opposite-parity holes at every time (proved; proposal)

**Proposal P3.** Let v >= 2 never occur. Then for every n >= v,

    H_{1-ε}(n)  >=  π(n+v) - π(2v) - H(v).

Consequently liminf_{n→∞} H(n) log n / n >= 1. Contrapositive:

    if liminf_{n→∞} H(n) log n / n < 1, then every positive integer occurs.

**Proof.**
- The displayed inequality is C009' rearranged. Its hypotheses hold for every n >= v, since v ∉ U_n.
- H(v) is a constant independent of n.
- π(n+v) - π(2v) = π(n) + O_v(1) = (1+o(1)) n / log n, by the PNT. Only the asymptotic π(x) ~ x/log x is used.
- So H(n) >= H_{1-ε}(n) >= (1 - o(1)) n/log n.
- Finally, v = 1 occurs (a(1) = 1), so a missing value is >= 2. ∎

**Relevance.**
- P3 strengthens the hypothesis side of C008 (i), which needs liminf = 0, to liminf < 1.
- P3 does **not** use C003/C004: it works for *any* missing v, not only the smallest one, and at every time n, not only eventually.
- The partners forced by P3 are time-n holes, not necessarily permanent ones. C004 gives permanent ones, but only for the smallest missing value.
- Literature: this is the same "missing m forces p - m missing" mechanism as C003/C004 (Devlin-Artamonov outline in A253074; EKG smallest-missing argument). It should be cited as such, not claimed as new.

### 4. What the weak version of C010 really asks (observation)

- **Any finite F works.** "K_n(v) <= F(v) for every hole v at every time n" already implies that v occurs, for *any* finite function F, with no BHP needed.
  - If v never occurs, K_n(v) → ∞ as n → ∞ (infinitely many primes), contradicting K_n(v) <= F(v).
  - C010's "F(v) = o(v^{0.525}/log v)" condition, and the GAP? about quantitative BHP, are only needed for the *quantitative* bound on fi(v), not for the permutation property.
- **An n-dependent bound also works.** A bound F(n) = o(n/log n), possibly depending on n, suffices as well, by the PNT as in P3.
- **Warning: the per-v version is the conjecture itself.**
  - "sup_n K_n(v) < ∞ for each v" is *equivalent* to "v occurs". Indeed, if v occurs, K_n(v) is only defined for n < fi(v).
  - So the per-v weak version is just the conjecture restated. The real content of C010 is **uniformity**: a bound by something we can control, such as a constant, C log v, or a small multiple of H.
- **Suggested edit to C010 (not made; orchestrator's call).** Replace the weak version by "K_n(v) <= F(v) for some function F", remark that it is equivalent to the conjecture, and keep K0 / C log v as the uniform targets.

### 5. Is an absolute K0 plausible? (data)

Distribution of K(v) = K_{fi(v)-1}(v) over 4.71M holes:

| K | count | ratio to previous |
|---|---|---|
| 0 | 1,839,794 | |
| 1 | 1,795,207 | 0.98 |
| 2 | 823,757 | 0.46 |
| 3 | 207,534 | 0.25 |
| 4 | 38,782 | 0.19 |
| 5 | 6,443 | 0.17 |
| 6 | 934 | 0.145 |
| 7 | 149 | 0.16 |
| 8 | 15 | 0.10 |

- **The tail looks geometric**, with ratio about 0.15. With roughly independent holes, the maximum of K over the holes v <= X would then grow like log X / log(1/0.15), about +1.2 per decade of hole count.
- **But the tail is creeping.** By decade of v:
  - P(K >= 3) rises 4.0e-2 → 4.2e-2 → 4.9e-2 → 5.45e-2;
  - P(K >= 7) is 0 → 0 → 2.4e-6 → 3.3e-6.
- **Prediction.** max K = 9 or 10 somewhere below v = 10^8 to 10^9.
- **Verdict (heuristic only).** An absolute K0 is **not** supported over K_n(v) = O(log v). The latter would suffice equally well (section 4).
- **Recommended uniform target:** K_n(v) <= C log v. Test: compute max K on [10^7, 10^8].

### 6. Iterating C009 (dead)

- **(a) Apply C009 to a late partner w of v.** The window of w is (2w, n+w], while v + w < 2w. So the prime v + w is outside w's window, and C009 for w says nothing about v. Similarly, v is not a payer of any prime of w: payers of w are partners > w, plus same-parity holes < w, and v has the opposite parity to w. **There is no coupling, so the iteration produces only an independent inequality of the same shape.**
- **(b) Apply C009 to the steal victims x(w) < v.** These are older same-parity holes. Bounding their number again needs H; it gives B(v) <= H_ε(v) - 1 and nothing better.
- **(c) Dynamics of Late (proved; proposal P5).** Let w ∈ Late(v,n), and suppose w is used before v, at time j+1 = fi(w) <= fi(v) - 2. Then a(j+2) <= v and a(j+2) ≠ v, so a(j+2) is a parity-ε hole < v.
  - Proof: the step after w; v + w is prime and v is unused.
  - So Late(v,·) can lose elements only by steals. Over the whole life of v, at most B_t(v) late partners leave Late without v being filled next.
  - This is the "time-n" form of the C003 mechanism. After all smaller same-parity holes are gone, Late(v,·) is monotone non-decreasing.
  - It explains *why* a permanent hole needs ~n/log n partners, but not why a finite-life hole has O(1) of them.
- **(d) Self-improving bound (dead).** The only quantities C009 produces are hole counts, and C009' is attained with equality. No iteration of the same counting can lower the constant 1 in front of H. Any improvement must use *which* values are holes, not *how many* there are.

### 7. Window localisation + prime counts (dead, even conditionally)

**Proposal P6 (middle window; proved).** Let M(v-1) = max U_{v-1}, and let u' be the smallest parity-(1-ε) hole at time n (u' = n+1 if there is none). Then

    #{ q prime : max(2v, v + M(v-1)) < q < v + u', q <= n+v }  <=  B(v) + 1  =  H_ε(v).

**Proof.**
- A partner w = q - v in this range satisfies w > M(v-1), so w ∉ U_{v-1}, and therefore w ∉ W1.
- It also satisfies w < u', w ≡ 1-ε and w <= n, so w is not a hole at time n, and therefore w ∉ W4.
- Hence w ∈ W2 ∪ W3, and C009 Steps 3-4 apply. ∎

**Why it does not help.**
- P6 only says that primes in the "middle" are paid for by steals. The outer windows have lengths M(v-1) - v (upper displacement) and n - u' (lower displacement or lifetime). These are exactly the quantities to be bounded, so the argument is circular.
- **Quantitatively, window counting loses to H.**
  - Unconditional (Brun-Titchmarsh in the Montgomery-Vaughan form π(x+y) - π(x) <= 2y/log y, for y >= 2): with the H = 50 event, whose window has length 86, the two windows give <= 2·2·86/log 86 ≈ 77 > 50 = H.
  - The reason: holes fill 50/87 of their window, a density far above 1/log n. So bounding Late by "primes in the hole window" is worse than bounding it by H.
- **Conditional, under a Cramér / uniform Hardy-Littlewood-type upper bound** π(x+y) - π(x) <= (1+o(1)) y/log x for y >= (log x)^2. This is an unproved hypothesis, stated here only as a hypothesis.
  - Let W >= max lifetime so far. Each window then contributes <= (1+o(1)) W/log n primes, giving K <= 2W/log n + H_ε(v).
  - A lifetime of K primes in a typical region is about K log n. This leads to L <~ 2W + H log n, with W >= L.
  - The coefficient 2 > 1, so the bound does not contract. **Dead even under Cramér-quality prime counts.**
  - The factor 2 comes from having two windows (ahead and late). Even a single window would give coefficient 1, which is borderline and still not contracting.

### 8. Bootstrap H <-> K (dead as stated; threshold recorded)

Let Φ_K(n) := #{ v <= n : π(n+v) - π(2v) <= K }.

- By C009', every hole v < n at time n has K_n(v) <= Hmax(n-1) + H(n), where Hmax(m) = max_{j <= m} H(j). So H(n) <= Φ_{Hmax(n-1)+H(n)}(n).
- **Estimate for Φ (sketch).** For any fixed θ0 > 7/12 and n large, Φ_K(n) <= n^{θ0} + (2+o(1)) K log(2n) + O(1).
  - Put d = n - v. The interval (2n-2d, 2n-d] has length d.
  - For d >= n^{θ0}, use Huxley's short-interval PNT, π(x+y) - π(x) ~ y/log x uniformly for x^{7/12+δ} <= y <= x. When x = 2n-2d < d, use the PNT on the right half of the interval instead.
  - **GAP?**: the uniform-in-x form of Huxley, and the bookkeeping for the right half, are not written out.
- **The loop does not close.** It reads H <= (2+o(1)) (2 Hmax) log n + n^{θ0}, which is vacuous because 4 log n > 1. Each surviving prime is charged to up to ~H payers, while it "costs" only log n of window.
- **Proposal P4 (threshold, conditional).** Suppose there are c >= 0 and θ(n) with θ(n) · 2 log(2n) <= 1/2 for n >= n0, such that every hole v at time n satisfies K_n(v) <= c + θ(n) Hmax(n). Then Hmax(n) = O(n^{θ0}) = o(n/log n), and M = ∅ by P3 or C008.
  - The proof is the two lines above plus the Φ estimate, so it inherits that GAP?.
  - (If θ(n) = o(1/log n), no bootstrap is needed at all: Hmax <= n gives K_n(v) = o(n/log n), and section 4 applies.)
  - Data: at H >= 40, K <= 8 = 0.2 H. So the data is consistent with c = 8, θ = 0, but not with "θ < 1/(4 log n)" being the mechanism.

### 9. Potential function (dead)

- Try Ψ(n) = Σ_{v hole at n} K_n(v).
- Step n → n+1:
  - Ψ gains #{ v hole at n+1 : v + n + 1 prime };
  - it loses K of the value filled, if that value was a hole.
- The gain is again "how many holes are prime partners of a moving point". That is the same correlation as Late, so there is no sign control.
- The drift data (E[ΔH] saturating at -0.07) already showed that rate arguments are too weak.

## Outcome

**Task A: done.** The full proof of C009, Sub-lemma S (both parities), the Corollary, the sharpening C009' (n - v < ℓ_{2h+1}(2v)) and the edge cases are written in `lemmas/candidates/C009-hole-prime-count.md`. There is no GAP? in it.

**Task B: C010 not proved, nor its weak or uniform version.** Proved by-products (proposals here, no candidate files):

| proposal | statement |
|---|---|
| P1 = C009' | K_n(v) <= H(v) + H_{1-ε}(n); tight |
| P2 | shifted-start / frontier version; only opposite-parity holes pay for a frontier hole |
| P3 | a missing v forces H_{1-ε}(n) >= π(n+v) - π(2v) - H(v) at every n; hence liminf H log n / n < 1 ⇒ permutation, without C003/C004 |
| P5 | late partners can only leave by steals |
| P6 | middle-window primes are paid only by steals |
| P4 | conditional bootstrap threshold; has a GAP? in the Huxley-uniform Φ estimate |

**Observation.** The weak form of C010 with F(v) is equivalent to the conjecture. Any finite F suffices, with no BHP needed. The content of C010 is uniformity.

**Data.** The tail of K looks geometric (ratio ≈ 0.15) and slowly creeping. An absolute K0 is not better supported than K = O(log v).

## Why it died / what survives

**Exactly where it dies.** Every argument available bounds the number of possible payers (ahead values, steal victims, late holes), and C009' shows this count is attained. The missing input is arithmetic: the hole set at time n, and the ahead set at time v - 1, meet the shifted prime set {q - v} in O(1) elements (or in o(H/log n)).
- Iterating C009 does not supply this: partners' windows do not contain v + w.
- Window localisation does not supply it either: holes are denser than primes in their window. Even under Cramér-quality prime counts, the coefficient is 2 > 1.
- Bootstrapping H <-> K loses a factor log n.

**What survives.**
- P1 (C009'), P2, P3 and P5/P6 are rigorous; P4 has a GAP?.
- P3 is the cleanest new reduction: liminf H(n) log n / n < 1 suffices.

**Most promising next statement.** A uniform late-and-ahead partner bound, motivated by the reflection lock:

    for every hole v at time n:  #Late(v,n) + #Ahead(v) <= C log v.

- Steals are already bounded by B(v). For P4, steals also need to be bounded by c + θH, which the data suggests: max 5.
- Test it first on [10^7, 10^8], together with max K.
- Structural route (speculative, unchecked): find the right extension of E3 beyond frontiers.
  - By P5, when one hole of a coexisting prime-sum pair (v, w) is filled, the next step fills either the other one or a smaller same-parity hole.
  - The data says the pair is filled at consecutive steps 81.5% of the time.
  - The aim is to charge each late partner of v to a distinct "lock prime" visited by the sums a(k) + a(k+1) during v's life, and to bound the number of such lock primes by O(log v).
