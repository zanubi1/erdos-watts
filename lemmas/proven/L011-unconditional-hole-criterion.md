# L011 - Unconditional hole-density criterion

## Statement

Let H(n) be the number of holes at time n, i.e. H(n) = #{ x ∈ [1, n] : x ∉ U_n } with U_n = {a(1), ..., a(n)}, and let H_p(n) be the number of parity p.

**(i)** Suppose v >= 2 never occurs, and put ε = v mod 2. Then for every n >= v,

    H_{1-ε}(n)  >=  π(n + v) - π(2v) - H(v).

**(ii)** Consequently, if some value never occurs, then

    liminf_{n -> ∞}  H(n) · log n / n  >=  1.

Contrapositive: if liminf H(n) log n / n < 1, then the sequence is a permutation of N.

Compared with L008 (ii), this needs liminf < 1 instead of liminf = 0, and it does **not** depend on L003/L004.

## Depends on

- L009, in its sharp form L009' (proven).
- The prime number theorem, only in the form π(x) ~ x / log x.

## Proof

_From the prover's Proposal P3, attempts/2026-11-25-c010-bounded-prime-survival.md._

**(i)**
- Fix n >= v. Since v never occurs, v ∉ U_n, so L009' applies to the pair (n, v). It gives π(n + v) - π(2v) <= H(v) + H_{1-ε}(n).
- For n = v itself, L009 requires n >= 2, which holds because v >= 2. L009 also allows v = n.
- Rearranging gives (i).

**(ii)**
- Let v be a missing value. Then v >= 2, since a(1) = 1.
- In (i), H(v) and π(2v) are constants independent of n. By the PNT, π(n + v) = (1 + o(1)) n / log n as n -> ∞.
- So H(n) >= H_{1-ε}(n) >= (1 - o(1)) n / log n.
- Hence liminf H(n) log n / n >= 1. ∎

## Remarks

- **Prior art.** The mechanism is the classical one: a missing value forces its shifted primes p - v to be missing or late. See the Devlin-Artamonov outline in A253074 and the EKG smallest-missing argument, and cite them. What is new relative to L004 is only the bookkeeping: it works for *any* missing v and at *every* time n, with the payers counted exactly by L009'.
- **Data.** H(n) <= 50 for n <= 10^7, so H(n) log n / n <= 2·10^-3 there. The hypothesis of (ii) holds by a huge margin wherever we can compute.

## Numerical check

(i) concerns a hypothetical missing value, so it has no direct check. It is L009' rearranged, and L009' is checked to 10^7.

## Review log

- 2026-11-25: candidate created from the prover's Proposal P3. **Awaiting skeptic.**
- 2026-11-25 (skeptic): **PASS, conditional on L009'** (L009 is a candidate under separate review; L011 is no stronger than L009'). Checked:
  - *Restatement.* (i): for all v >= 2 with v ∉ U_m for every m, and for all n >= v: H_{1-ε}(n) >= π(n+v) - π(2v) - H(v). (ii): if there exists a v that never occurs, then liminf_n H(n) log n / n >= 1. Quantifiers are unambiguous. H here equals H_0 + H_1 as in L009.
  - *(i).* The hypotheses of L009' are met for each n >= v: n >= v >= 2 and v <= n, and "v never occurs" implies v ∉ U_n. The rearrangement is exact, with no off-by-one: the right-hand side of L009' uses H(v), not H(v-1). The bound needs only v ∉ U_n, so v does not have to be missing forever. (i) therefore holds for every hole at time n, not only for permanently missing values.
  - *(ii).* v >= 2 because a(1) = 1. π(2v) and H(v) depend only on v, and 0 <= π(n+v) - π(n) <= v, so by the PNT π(n+v) - π(2v) - H(v) = (1+o(1)) n/log n. The constant 1 is correct and does not need weakening. The argument actually proves the stronger statement liminf H_{1-ε}(n) log n / n >= 1 (one parity class only). Chebyshev bounds alone would give only a positive constant, so the PNT is genuinely needed to get constant 1. The contrapositive is valid: the sequence is injective by construction and well defined by L002, so it is a permutation exactly when no value is missing.
  - *Independence from L003/L004.* L011's own proof uses only L009' and the PNT. Whether L009's proof avoids L003/L004 was **not verified here**: this reviewer was shown only L009's Statement. The L009 reviewer must confirm it before the "does not depend on L003/L004" sentence can stand.
  - *False variants (script: greedy prime-sum sequence with arbitrary a(1) and an optional forbidden set; checks L009' for all n <= N and every hole v in [2, n]):*
    - a(1) = 1, N = 2·10^5: 0 violations of L009', max H = 31.
    - Forbidden-value variant (v = 2, 3, 4, 7, 10 never allowed): v is truly missing, yet H(n) stays <= 18, so the conclusion of (ii) is false there. L009' fails massively in that variant (about N violations, excess up to ~2250), which is expected because the mechanism needs v to be *available*. So the L011 step does not "prove" this false variant. All of the weight is on L009', which must use availability, and it apparently does.
    - Other starts, N = 2·10^4: a(1) = 3, 5, 7, 15 give 0 violations. a(1) = 2, 4, 6, 8, 10, 20 each **violate L009' by exactly 1** at a transient hole (e.g. a(1)=6: n=9, v=5, π(14)-π(10) = 2 > H(5) + H_0(9) = 1 + 0; a(1)=2: n=519, v=509). So the identity "1 + B(v) + H_{1-ε}(v-1) = H(v)" or the count in L009' is specific to a(1) = 1 (presumably the start term is an extra uncounted payer). This does not affect L011: an O(1) slack does not change (ii). It is passed on to the L009 reviewer.
  - *Not checked:* the remark "H(n) <= 50 for n <= 10^7" (this reviewer only saw H <= 31 up to 2·10^5). The Prior-art remark asks for citations (A253074, EKG) that are not yet given. Literature agent needed per rule 3.
- 2026-11-25 (editor): the L009 skeptic confirmed that L009 and L009' depend only on L001/L002, so the claim that L011 does not depend on L003/L004 stands, conditional on L009 being accepted. Prior-art citations for the mechanism: A253074 (Devlin-Artamonov) and LRS 2002 (EKG, Lemmas 3-4 and 7).
- 2026-11-25 (main-session review, with Matteo's delegated OK): PASS. (i) is L009' at each n >= v (n >= 2, v ∉ U_n). (ii): π(n+v) - π(2v) - H(v) = (1+o(1)) n/log n by the PNT, since π(n+v) - π(n) <= v. It depends only on L009 (L001/L002) and the PNT, not on L003/L004. **Moved to lemmas/proven/ as L011 (formerly C011).**
- 2026-11-25 (formalizer): **formalized: yes.** File: lean/ErdosWatts/L011.lean. Theorems: (i) `L011_i` (ℕ, truncated subtraction), `L011_i_int` (ℤ), and the stronger `L011_i_hole` (needs only v ∉ U_n). (ii) `L011_ii` (primary form: ∀ ε > 0, eventually H(n) ≥ (1-ε) n/log n), `L011_ii_holes` (the same for the single parity class H_{1-ε}(n)), `L011_ii_ratio` (eventually H(n) log n / n ≥ 1-ε), `L011_ii_liminf_ereal` (1 ≤ liminf, with the liminf in EReal: no side conditions), `L011_ii_liminf` (the liminf in ℝ, with the hypothesis `IsCoboundedUnder (· ≥ ·)`). Contrapositive: `L011_criterion` (if ∃ δ > 0 with H(n) ≤ (1-δ) n/log n for ∃ᶠ n, then every v ≥ 1 occurs), `L011_criterion_liminf_ereal` (EReal liminf < 1 implies every v ≥ 1 occurs), `L011_criterion_liminf` (ℝ liminf < 1 plus coboundedness). Every (ii) form holds for an arbitrary missing v ≥ 1, not only the smallest.
  Axioms (all nine main theorems): `[propext, Classical.choice, Quot.sound]`, e.g. `'ErdosWatts.L011_criterion' depends on axioms: [propext, Classical.choice, Quot.sound]`. Explicit hypotheses: none. The PNT comes from Mathlib's `Nat.isEquivalent_primeCounting`, used through the pure-PNT helpers `L004_rhs_isEquivalent` and `eventually_ge_of_isEquivalent` in L004.lean. The file imports L004.lean for those helpers only and does not use L003 or the L004 bound.
  Discrepancies informal vs formal: (1) In ℝ, `Filter.liminf` is a junk value (0) when the sequence tends to +∞, so the ℝ-liminf forms carry the side condition `IsCoboundedUnder (· ≥ ·) atTop (H(n) log n / n)`. The EReal forms are unconditional and match the informal extended-real liminf. (2) "Permutation of N" is stated as `∀ v ≥ 1, Occurs v`. It is equivalent to `Function.Bijective aPNat` by `aPNat_bijective_iff` (Conjecture.lean), which is not imported here so that the file stays clear of `Conjecture.lean`. (3) (i) uses truncated ℕ subtraction in `L011_i`. `L011_i_int` gives the untruncated ℤ form. GAPs found: none.
