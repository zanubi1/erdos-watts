# C011 - Unconditional hole-density criterion

## Statement

Let H(n) be the number of holes at time n, i.e. H(n) = #{ x ∈ [1, n] : x ∉ U_n } with U_n = {a(1), ..., a(n)}, and let H_p(n) be the number of parity p.

**(i)** Suppose v >= 2 never occurs, and put ε = v mod 2. Then for every n >= v,

    H_{1-ε}(n)  >=  π(n + v) - π(2v) - H(v).

**(ii)** Consequently, if some value never occurs, then

    liminf_{n -> ∞}  H(n) · log n / n  >=  1.

Contrapositive: if liminf H(n) log n / n < 1, then the sequence is a permutation of N.

Compared with C008 (ii), this needs liminf < 1 instead of liminf = 0, and it does **not** depend on C003/C004.

## Depends on

- C009, in its sharp form C009' (candidate, awaiting skeptic).
- The prime number theorem, only in the form π(x) ~ x / log x.

## Proof

_From the prover's Proposal P3, attempts/2026-11-25-c010-bounded-prime-survival.md._

**(i)**
- Fix n >= v. Since v never occurs, v ∉ U_n, so C009' applies to the pair (n, v). It gives π(n + v) - π(2v) <= H(v) + H_{1-ε}(n).
- For n = v itself, C009 requires n >= 2, which holds because v >= 2. C009 also allows v = n.
- Rearranging gives (i).

**(ii)**
- Let v be a missing value. Then v >= 2, since a(1) = 1.
- In (i), H(v) and π(2v) are constants independent of n. By the PNT, π(n + v) = (1 + o(1)) n / log n as n -> ∞.
- So H(n) >= H_{1-ε}(n) >= (1 - o(1)) n / log n.
- Hence liminf H(n) log n / n >= 1. ∎

## Remarks

- **Prior art.** The mechanism is the classical one: a missing value forces its shifted primes p - v to be missing or late. See the Devlin-Artamonov outline in A253074 and the EKG smallest-missing argument, and cite them. What is new relative to C004 is only the bookkeeping: it works for *any* missing v and at *every* time n, with the payers counted exactly by C009'.
- **Data.** H(n) <= 50 for n <= 10^7, so H(n) log n / n <= 2·10^-3 there. The hypothesis of (ii) holds by a huge margin wherever we can compute.

## Numerical check

(i) concerns a hypothetical missing value, so it has no direct check. It is C009' rearranged, and C009' is checked to 10^7.

## Review log

- 2026-11-25: candidate created from the prover's Proposal P3. **Awaiting skeptic.**
- 2026-11-25 (skeptic): **PASS, conditional on C009'** (C009 is a candidate under separate review; C011 is no stronger than C009'). Checked:
  - *Restatement.* (i): for all v >= 2 with v ∉ U_m for every m, and for all n >= v: H_{1-ε}(n) >= π(n+v) - π(2v) - H(v). (ii): if there exists a v that never occurs, then liminf_n H(n) log n / n >= 1. Quantifiers are unambiguous. H here equals H_0 + H_1 as in C009.
  - *(i).* The hypotheses of C009' are met for each n >= v: n >= v >= 2 and v <= n, and "v never occurs" implies v ∉ U_n. The rearrangement is exact, with no off-by-one: the right-hand side of C009' uses H(v), not H(v-1). The bound needs only v ∉ U_n, so v does not have to be missing forever. (i) therefore holds for every hole at time n, not only for permanently missing values.
  - *(ii).* v >= 2 because a(1) = 1. π(2v) and H(v) depend only on v, and 0 <= π(n+v) - π(n) <= v, so by the PNT π(n+v) - π(2v) - H(v) = (1+o(1)) n/log n. The constant 1 is correct and does not need weakening. The argument actually proves the stronger statement liminf H_{1-ε}(n) log n / n >= 1 (one parity class only). Chebyshev bounds alone would give only a positive constant, so the PNT is genuinely needed to get constant 1. The contrapositive is valid: the sequence is injective by construction and well defined by L002, so it is a permutation exactly when no value is missing.
  - *Independence from C003/C004.* C011's own proof uses only C009' and the PNT. Whether C009's proof avoids C003/C004 was **not verified here**: this reviewer was shown only C009's Statement. The C009 reviewer must confirm it before the "does not depend on C003/C004" sentence can stand.
  - *False variants (script: greedy prime-sum sequence with arbitrary a(1) and an optional forbidden set; checks C009' for all n <= N and every hole v in [2, n]):*
    - a(1) = 1, N = 2·10^4: 0 violations of C009', max H = 17.
    - Forbidden-value variant (v = 2, 3, 4, 7, 10 never allowed): v is truly missing, yet H(n) stays <= 18, so the conclusion of (ii) is false there. C009' fails massively in that variant (about N violations, excess up to ~2250), which is expected because the mechanism needs v to be *available*. So the C011 step does not "prove" this false variant. All of the weight is on C009', which must use availability, and it apparently does.
    - Other starts, N = 2·10^4: a(1) = 3, 5, 7, 15 give 0 violations. a(1) = 2, 4, 6, 8, 10, 20 each **violate C009' by exactly 1** at a transient hole (e.g. a(1)=6: n=9, v=5, π(14)-π(10) = 2 > H(5) + H_0(9) = 1 + 0; a(1)=2: n=519, v=509). So the identity "1 + B(v) + H_{1-ε}(v-1) = H(v)" or the count in C009' is specific to a(1) = 1 (presumably the start term is an extra uncounted payer). This does not affect C011: an O(1) slack does not change (ii). It is passed on to the C009 reviewer.
  - *Not checked:* the remark "H(n) <= 50 for n <= 10^7" (only seen H <= 17 to 2·10^4). The Prior-art remark asks for citations (A253074, EKG) that are not yet given. Literature agent needed per rule 3.
