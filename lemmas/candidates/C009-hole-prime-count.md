# C009 - A hole can survive only as many primes as it has "payers"

## Statement

Notation:
- U_n = {a(1), ..., a(n)}.
- H_p(m) = #{ x ∈ [1, m] : x ≡ p (mod 2), x ∉ U_m } is the number of holes of parity p at time m.
- B(v) = #{ x < v : x ≡ v (mod 2), x ∉ U_v } is the number of smaller same-parity holes at time v.

Let n >= 2 and 2 <= v <= n with v ∉ U_n, and put ε = v mod 2. Then

    π(n + v) - π(2v)  <=  1 + B(v) + H_{1-ε}(v - 1) + H_{1-ε}(n).

**Sharp form (C009').** Since 1 + B(v) + H_{1-ε}(v - 1) = H(v) exactly (see "Sharpening" in the proof), equivalently

    π(n + v) - π(2v)  <=  H(v) + H_{1-ε}(n).

This bound is attained: equality occurs 1,887 times up to 10^7.

**Corollary.** Suppose H(m) <= h for all m <= n, where H = H_0 + H_1. Then every hole v at time n (2 <= v <= n, v ∉ U_n) satisfies

    n - v  <  ℓ_{2h+1}(2v),   where ℓ_K(x) = (the K-th prime > x) - x.

(The first draft had the weaker ℓ_{3h+2}.)

## Depends on

L001, L002. Uses the per-parity count from C007 Step 2, generalized to both parities: at time m, the number of used values of parity p that are > m equals H_p(m).

## Proof

_Full write-up by the prover (2026-11-25), replacing the experimenter's draft. The argument is the draft's four-case split; every step is now written out, and the edge cases are checked at the end._

### Conventions

- a(1), a(2), ... is the Watts sequence; U_m = {a(1), ..., a(m)} for m >= 1, and U_0 = ∅.
- For x >= 1, fi(x) = the unique k with a(k) = x if x occurs, and fi(x) = ∞ otherwise. It is well defined because the terms are pairwise distinct (Fact F2).
- "Parity p" means ≡ p (mod 2), with p ∈ {0, 1}.
- A_m = { x >= 1 : x ∉ U_m, a(m) + x prime }. By L002, A_m ≠ ∅, and by definition a(m+1) = min A_m.

### Basic facts

- **F1 (parity).** For every k >= 1, a(k) ≡ k (mod 2).
  - *Proof.* L001 gives a(k+1) ≢ a(k) (mod 2) for all k >= 1, and a(1) = 1 ≡ 1. Induct on k.
- **F2 (injectivity).** a(j) ≠ a(k) for all j < k.
  - *Proof.* a(k) = min A_{k-1}, and A_{k-1} ∩ U_{k-1} = ∅. Since a(j) ∈ U_{k-1}, a(k) ≠ a(j).
- **F3 (monotonicity).** U_j ⊆ U_k for j <= k. Also x ∈ U_k if and only if fi(x) <= k.
  - *Proof.* Immediate from the definitions and F2.

### Sub-lemma S (per-parity count)

**Statement.** For every m >= 1 and every p ∈ {0, 1}:

    #{ x ∈ U_m : x ≡ p (mod 2), x > m }  =  H_p(m).

Equivalently, H_p(m) = #{ k ∈ [1, m] : k ≡ p, a(k) > m }.

**Proof.**
- Fix m >= 1 and p ∈ {0, 1}. Let N_p(m) = #{ k ∈ [1, m] : k ≡ p (mod 2) }. (So N_1(m) = ceil(m/2) and N_0(m) = floor(m/2); the values are not needed.)
- **Step S1: exactly N_p(m) used values have parity p.**
  - The map k ↦ a(k) is a bijection from [1, m] onto U_m, by F2.
  - By F1, a(k) ≡ p if and only if k ≡ p.
  - So it restricts to a bijection from { k ∈ [1, m] : k ≡ p } onto { x ∈ U_m : x ≡ p }. Hence #{ x ∈ U_m : x ≡ p } = N_p(m).
- **Step S2: exactly N_p(m) - H_p(m) of them are <= m.**
  - The set I_p = { x ∈ [1, m] : x ≡ p } has exactly N_p(m) elements. These are the same integers as in the definition of N_p(m).
  - By definition of H_p(m), exactly H_p(m) elements of I_p are not in U_m. So #(I_p ∩ U_m) = N_p(m) - H_p(m).
  - I_p ∩ U_m is exactly { x ∈ U_m : x ≡ p, x <= m }, because every element of U_m is >= 1.
- **Step S3: subtract.** { x ∈ U_m : x ≡ p } is the disjoint union of the part with x <= m and the part with x > m. So

      #{ x ∈ U_m : x ≡ p, x > m } = N_p(m) - (N_p(m) - H_p(m)) = H_p(m).

- **The equivalent form.** Apply the bijection of S1 once more: x = a(k) with k <= m, and x ≡ p if and only if k ≡ p.
- Nothing in S1-S3 depended on p, so the argument covers both parities. In particular, it covers both parities of m. (C007 Step 2 is the special case p ≡ m + 1.) ∎

**Remark.** S uses a(1) = 1 through F1. For a different start a(1) = c with c even, F1 becomes a(k) ≡ k + 1, and S fails by ±1. The skeptic's variant test in C007 shows exactly this.

### Proof of C009

Fix n >= 2 and v with 2 <= v <= n and v ∉ U_n. Put ε = v mod 2.

Let Q = { q prime : 2v < q <= n + v }, so that #Q = π(n + v) - π(2v). If v = n, then Q = ∅ and the claim holds, since its right side is >= 1. The argument below does not need this case split, though.

**Step 0: the partner map.**
- Let q ∈ Q. Then q > 2v >= 4, so q is an odd prime.
- Define w(q) := q - v. Then:
  - v < w(q) <= n, since 2v < q <= n + v;
  - w(q) ≡ 1 - ε (mod 2), since q is odd: w(q) = q - v ≡ 1 - ε;
  - w(q) + v = q is prime.
- The map q ↦ w(q) is injective, being a translation.
- So #Q = #W, where W := { w(q) : q ∈ Q } ⊆ (v, n].
- Every w ∈ W satisfies w >= v + 1 >= 3. In particular w ∈ [1, n].

**Step 1: the partition.** For w ∈ W, fi(w) ∈ {1, 2, ...} ∪ {∞}. Split W into four disjoint sets:
- W1 = { w ∈ W : fi(w) <= v - 1 };
- W2 = { w ∈ W : v <= fi(w) <= n - 1 };
- W3 = { w ∈ W : fi(w) = n };
- W4 = { w ∈ W : fi(w) >= n + 1, or fi(w) = ∞ }.

The ranges [1, v-1], [v, n-1], {n} and [n+1, ∞] ∪ {∞} partition {1, 2, ...} ∪ {∞}; some of them may be empty (for example [v, n-1] when v = n). So #W = #W1 + #W2 + #W3 + #W4.

**Step 2: #W1 <= H_{1-ε}(v - 1) (ahead values).**
- Put m = v - 1. Then m >= 1, since v >= 2, so S applies.
- Let w ∈ W1. Then:
  - w ∈ U_m, by F3, since fi(w) <= m;
  - w ≡ 1 - ε;
  - w > v > m.
- So W1 ⊆ { x ∈ U_m : x ≡ 1 - ε, x > m }. By S with p = 1 - ε, this set has exactly H_{1-ε}(v - 1) elements.

**Step 3: #W2 <= B(v) (steals).** Let w ∈ W2 and k = fi(w), so that v <= k <= n - 1 and a(k) = w.
- **(a) v is available at step k.**
  - v ∉ U_n and U_k ⊆ U_n (F3, k <= n). So v ∉ U_k.
  - a(k) + v = w + v = q is prime.
  - v >= 1. Hence v ∈ A_k.
- **(b) the greedy rule.** a(k+1) = min A_k <= v.
- **(c) a(k+1) ≠ v.**
  - Since k + 1 <= n, a(k+1) ∈ U_n, and v ∉ U_n. So a(k+1) ≠ v.
  - **This is exactly where k <= n - 1 is needed.** For k = n, a(n+1) ∉ U_n, and a(n+1) = v is possible. That situation is case W3.
  - So x(w) := a(k+1) satisfies 1 <= x(w) < v.
- **(d) parity.**
  - By F1, k ≡ a(k) = w ≡ 1 - ε. So k + 1 ≡ ε.
  - By F1 again, x(w) = a(k+1) ≡ ε.
- **(e) x(w) was a hole at time v.**
  - x(w) = a(k+1) ∈ A_k, so x(w) ∉ U_k.
  - Since k >= v, U_v ⊆ U_k (F3). Hence x(w) ∉ U_v.
- **(f) conclusion.** By (c), (d) and (e), x(w) ∈ { x < v : x ≡ ε, x ∉ U_v }. This set has B(v) elements.
- **(g) injectivity.**
  - If w ≠ w' are in W2, then fi(w) ≠ fi(w'), since fi(w) determines w = a(fi(w)).
  - So fi(w) + 1 ≠ fi(w') + 1, and x(w) = a(fi(w)+1) ≠ a(fi(w')+1) = x(w'), by F2.
  - Hence #W2 <= B(v).

**Step 4: #W3 <= 1.** If w ∈ W3, then a(n) = w. So W3 ⊆ {a(n)}.

**Step 5: #W4 <= H_{1-ε}(n) (late values).**
- Let w ∈ W4. Then fi(w) > n (possibly ∞), so w ∉ U_n by F3.
- Also 1 <= w <= n and w ≡ 1 - ε.
- So W4 ⊆ { x ∈ [1, n] : x ≡ 1 - ε, x ∉ U_n }, a set of H_{1-ε}(n) elements.
- The case fi(w) = ∞ needs no separate treatment: it is included here.

**Step 6: sum.** By Steps 0-5,

    π(n+v) - π(2v) = #W = #W1 + #W2 + #W3 + #W4 <= H_{1-ε}(v-1) + B(v) + 1 + H_{1-ε}(n).   ∎

### Sharpening (exact rewriting of the right side)

_Added by the prover. It changes nothing in the argument above, but it gives a cleaner statement and a better Corollary constant. Proposed as an addendum to the Statement; the decision is the orchestrator's and Matteo's._

**Claim.** Under the hypotheses of C009, 1 + B(v) + H_{1-ε}(v-1) = H(v), where H = H_0 + H_1. Hence

    π(n + v) - π(2v)  <=  H(v) + H_{1-ε}(n).        (C009')

**Proof.**
- **(i) H_ε(v) = B(v) + 1.**
  - The parity-ε integers in [1, v] are the parity-ε integers in [1, v-1], together with v itself.
  - v ∉ U_v, since U_v ⊆ U_n (F3) and v ∉ U_n.
  - So H_ε(v) = #{ x < v : x ≡ ε, x ∉ U_v } + 1 = B(v) + 1.
- **(ii) H_{1-ε}(v) = H_{1-ε}(v-1).**
  - The parity-(1-ε) integers in [1, v] are the same as those in [1, v-1], since v ≡ ε.
  - For such x: U_v = U_{v-1} ∪ {a(v)}, and a(v) ≡ v ≡ ε by F1. So a(v) ≠ x, and x ∉ U_v if and only if x ∉ U_{v-1}.
  - Here v - 1 >= 1, so H_{1-ε}(v-1) is defined.
- Adding (i) and (ii) gives 1 + B(v) + H_{1-ε}(v-1) = H_ε(v) + H_{1-ε}(v) = H(v). ∎

**Numerical note.** (C009') is checked at n = fi(v) - 1 for all 4,712,615 holes with fi(v) <= 10^7, with 0 violations. Its right side equals the original right side in every case, as it must. Equality K = H(v) + H_{1-ε}(n) occurs 1,887 times, including K = 5 at large v (equality cases with K >= 2 occur up to v ≈ 9.9·10^6). So **C009' is tight; no improvement of the constant is possible without new input**. Equality occurs only when the right side is <= 9: when the right side is >= 10, max K/rhs = 0.6, and when it is >= 40, max K/rhs = 0.2. (Script `experiments/src/c009_sharp_check.py`, 2026-11-25; see also the attempt file `attempts/2026-11-25-c010-bounded-prime-survival.md`.)

### Proof of the Corollary

Hypothesis: n >= 2, and H(m) <= h for every m with 1 <= m <= n. Let v be a hole at time n, with 2 <= v <= n and v ∉ U_n.

- **Each term on the right side is <= h.**
  - B(v) <= H_ε(v) - 1 <= H(v) - 1 <= h - 1, by (i) above. Here 1 <= v <= n.
  - H_{1-ε}(v-1) <= H(v-1) <= h, since 1 <= v-1 <= n-1.
  - H_{1-ε}(n) <= H(n) <= h.
- **The interval (2v, n+v] contains few primes.**
  - From C009: π(n+v) - π(2v) <= 1 + (h-1) + h + h = 3h. The draft's 3h + 1 is also true, but weaker.
  - From (C009'), even better: π(n+v) - π(2v) <= H(v) + H_{1-ε}(n) <= 2h.
- **Turning a prime count into a length.** Let K >= 1 be an integer with π(n+v) - π(2v) <= K - 1. Let P_K(2v) be the K-th prime > 2v, which exists because there are infinitely many primes.
  - If n + v >= P_K(2v), then (2v, n+v] would contain the K primes > 2v up to P_K(2v), so π(n+v) - π(2v) >= K, a contradiction.
  - Hence n + v < P_K(2v), that is, n - v < P_K(2v) - 2v = ℓ_K(2v).
- **Conclusions.**
  - With K = 3h + 2, the inequality 3h + 1 <= K - 1 holds, so we get the stated Corollary: n - v < ℓ_{3h+2}(2v).
  - With K = 2h + 1 and (C009'), we get the sharper n - v < ℓ_{2h+1}(2v).
- **About h.** h >= 1 automatically, since v itself is a hole at time v, so H(v) >= 1. ∎

In particular, applied at n = fi(v) - 1 for a value v that occurs with fi(v) > v: if H(m) <= h for all m < fi(v), then the lifetime satisfies L(v) = fi(v) - v <= ℓ_{2h+1}(2v). This needs fi(v) - 1 >= 2, which holds because fi(v) > v >= 2.

### Edge cases (checked)

- **v = 2.**
  - Then m = v - 1 = 1, and S holds for m = 1: U_1 = {1}, and H_0(1) = 0 = #{x ∈ U_1 even, x > 1}; H_1(1) = 0 = #{x ∈ U_1 odd, x > 1}.
  - B(2) counts x < 2 with x even, so B(2) = 0.
  - Q ⊆ (4, n+2], and all its elements are odd. Fine.
- **v - 1 = 1.** This is the same case as v = 2; S is stated for m >= 1, so Step 2 is valid.
- **v = n.**
  - Q = (2n, 2n] ∩ primes = ∅, so the claim is trivial.
  - The proof also goes through formally: W2's range [n, n-1] is empty.
- **n = 2.** Then v = 2 = n, which is the previous case. (Note that 2 ∈ U_2 for the actual sequence, since a(2) = 2, so the hypothesis is vacuous.)
- **fi(w) = ∞.** This falls in W4. Step 5 uses only w ∉ U_n, which holds.
- **Case 2 needs k <= n - 1.** This is used in Step 3(c), to put a(k+1) in U_n and so exclude a(k+1) = v. At k = n, the greedy rule may choose v itself, and then no smaller hole is consumed. That w is a(n), and it is counted in W3 instead. Without the bound k <= n - 1, the injection into B(v) would fail.
- **Case 2 needs k >= v.** This is used in Step 3(e), to get U_v ⊆ U_k, so that x(w) is a hole at time v. By parity, k ≠ v (k ≡ 1-ε, v ≡ ε). So in fact k >= v + 1, but this is not needed.
- **q = 2 cannot occur.** q > 2v >= 4.
- **The prime 2 in A_k (Step 3).** The only property used is that v ∈ A_k. That q = a(k) + v is prime is given; whether it is odd is irrelevant there.

No step is marked GAP?. The proof uses only L001, L002, a(1) = 1, and the definition of the sequence. It uses no prime-number theorem: "infinitely many primes" is used only in the Corollary, to define P_K.

## Numerical check

`experiments/src/holes_dynamics.py`, section `bounds`. Checked for all 4.71M holes v at n = fi(v) - 1, and for the smallest hole at every n <= 10^7: 0 violations.
- The left side is at most 8; the right side reaches 52.
- See `experiments/results/holes_dynamics_1e7/summary.md`.
- 2026-11-25 (experimenter, N = 10^8): (C009') checked at n = fi(v) - 1 for all 47,519,524 completed holes v <= 10^8 (42,806,899 with v in [10^7, 10^8)), and at n = N for the 14 holes still open: **0 violations**. Equalities: 6,483 in total (4,596 in [10^7, 10^8)), max K at equality 5, equality with K >= 2 up to v = 99,990,736. Left side max 11, right side max 112; max K/rhs is 0.70 for rhs in [10, 20), 0.50 for [20, 40), 0.24 for >= 40. Script `experiments/src/k_survival_1e8.py`.

## Review log

- 2026-11-25: candidate created from the hole-dynamics experiment (E5). The main session checked the four-case split. **Awaiting prover (write-up), literature and skeptic.**
- 2026-11-25 (prover): full proof written. Added Sub-lemma S (per-parity count, both parities), the edge-case check, and the sharpening (C009') π(n+v) - π(2v) <= H(v) + H_{1-ε}(n), which is an exact rewriting of the right side; the Corollary improves to n - v < ℓ_{2h+1}(2v). No GAP?. **Awaiting skeptic.**
- 2026-11-25 (literature): Case 2 ("steals") is the charging argument of Lagarias-Rains-Sloane 2002, EKG Lemma 7 (each admissible partner of a missing value forces a smaller next term, and distinct times give distinct values). Cite it. The special case B(v) = 0 is the classical smallest-missing step (EKG Lemmas 3-4, Yellowstone Theorem 1(vi), A253074). I did **not find** the four-case partition or the inequality itself in the sources read. No delay bound for A055265 was found anywhere. See literature/search-C009-C010-hole-payers.md.
- 2026-11-25 (editor): added the sharp form (C009') and the improved corollary ℓ_{2h+1} to the Statement, both proved in the prover's write-up. **Awaiting skeptic.**
