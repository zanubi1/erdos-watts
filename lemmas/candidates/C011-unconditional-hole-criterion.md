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
