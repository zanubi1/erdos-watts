# C014 - Almost all even h <= Z are q - p with p <= Z/(log Z)^2 (hypothesis (G) of C013)

## Statement

Notation.
- Λ is the von Mangoldt function, and e(x) = exp(2πix). T = R/Z.
- Z is a real parameter, L = log Z, Y = Z/L^2 (real), N = Z + Y.
- For integers h >= 1: R(h) = R_Y(h) := Σ_{1 <= n <= Y} Λ(n) Λ(n+h).
- The twin singular series: for integers h, S(h) := Σ_{q >= 1} μ(q)^2 c_q(h)/φ(q)^2. Here c_q(h) = Σ_{a mod q, (a,q)=1} e(ah/q) is Ramanujan's sum.
  - The series converges absolutely (Step 0).
  - For even h, S(h) = 2 C2 Π_{p | h, p > 2} (p-1)/(p-2), with C2 = Π_{p>2} (1 - 1/(p-1)^2) = 0.6601...
  - For odd h, S(h) = 0.

**(G\*) Theorem.** For every A > 0 there are constants Z_0(A) and C(A) such that for all real Z >= Z_0(A):

    (i)   Σ_{1 <= h <= Z} | R_Y(h) - S(h) Y |^2  <=  C(A) · Z Y^2 L^{-3A},
    (ii)  #{ h ∈ [1, Z] : h even, |R_Y(h) - S(h) Y| > Y L^{-A} }  <=  C(A) · Z L^{-A}.

(C(A) is ineffective, through Siegel-Walfisz.)

**Corollary (G).** For every integer c >= 0 there is Z_1(c) such that for every real Z >= Z_1(c), with Y = Z/(log Z)^2:

    |Bad_c(Z, Y)|  <=  C(2) Z (log Z)^{-2},

where Bad_c(Z, Y) = { h ∈ [1, Z] : h even, r_Y(h) <= c } and r_Y(h) = #{ p prime : p <= Y, p + h prime } (the notation of C013).

In particular, Z_j = j and Y_j = Z_j/(log Z_j)^2 satisfy hypothesis (G) of C013 (d): Y_j log Z_j / Z_j = 1/log Z_j -> 0, and |Bad_c(Z_j, Y_j)| log Z_j / Z_j <= C(2)/log Z_j -> 0.

Moreover, for Z large, every even h ∈ [1, Z] outside the exceptional set in (ii) with A = 2 has r_Y(h) >= Z/(4 (log Z)^4).

## Depends on

External theorems. All statements below are **recalled from memory**. The proof only needs them up to the value of a fixed power of log, so a misremembered exponent of log does not matter (see Remark 2).

- **(SW) Siegel-Walfisz.** For every M > 0 there is c_M > 0 such that, uniformly for x >= 2, 1 <= q <= (log x)^M and (r, q) = 1,
  ψ(x; q, r) := Σ_{n <= x, n ≡ r (q)} Λ(n) = x/φ(q) + O_M( x exp(-c_M (log x)^{1/2}) ).
  References: Davenport, *Multiplicative Number Theory*, 3rd ed., Ch. 22; Iwaniec-Kowalski, *Analytic Number Theory*, Cor. 5.29. The constants are ineffective.
  - We use only the consequence: for every M, K > 0, |ψ(x;q,r) - x/φ(q)| <= C_{M,K} x (log x)^{-K} in the same range.
- **(V) Vinogradov's estimate, in Vaughan's form.** If (a, q) = 1, q >= 1 and |α - a/q| < q^{-2} (strict, as in the sources; Step 2 produces a strict inequality), then for X >= 2
  |Σ_{n <= X} Λ(n) e(nα)| <= C_V ( X q^{-1/2} + X^{4/5} + X^{1/2} q^{1/2} ) (log X)^4,
  with C_V absolute.
  References: R. C. Vaughan, *The Hardy-Littlewood Method*, 2nd ed., Thm 3.1; Iwaniec-Kowalski Thm 13.6 (I recall (log X)^3 there, which is stronger).
- **(D) Dirichlet's approximation theorem.** For real α and integer Q' >= 1 there are integers a and 1 <= q <= Q' with |qα - a| <= 1/(Q'+1). Hardy-Wright, Thm 185 / §11.3.
- **(C) Chebyshev.** ψ(x) := Σ_{n<=x} Λ(n) <= 2x for x >= 1 (Rosser-Schoenfeld give ψ(x) < 1.04x).
- **(P) Parseval** on T. For Φ ∈ L^2(T), Σ_{h∈Z} |∫_T Φ(α) e(-hα) dα|^2 = ∫_T |Φ|^2.
- **Ramanujan sums** (elementary; Hardy-Wright §16.6, Montgomery-Vaughan §4.1).
  - c_q(h) is real, c_q(-h) = c_q(h), and c_q(h) is multiplicative in q.
  - c_p(h) = p - 1 if p | h, and c_p(h) = -1 if p ∤ h.
  - c_q(a) = μ(q) if (a, q) = 1.
  - Hence, for squarefree q, |c_q(h)| = φ((q, h)).
- Nothing from the repo. C014 is pure analytic number theory. C013 (d) uses it.

**Method / prior art.** This is the textbook circle-method proof of the *Goldbach exceptional set theorem* (Chudakov, van der Corput, Estermann 1937-38; written e.g. in Vaughan's book, Ch. 3), and the same scheme as for prime pairs in Lavrik 1961. Note that Lavrik's theorem, as paraphrased in the literature, uses equal ranges (shifts u <= X for m <= X), so it does not directly give (G\*). It is adapted to unbalanced lengths: one sum of length Y = Z/L^2, the other of length N ≈ Z. **No step is new.** The only point to check is that the unbalanced lengths cost only powers of L. Every such cost is absorbed by the free parameter B below. I have not seen (G\*) stated in this exact unbalanced form; see `literature/search-C013-G-and-cascade.md`.

## Proof

Throughout, A > 0 is fixed and

    B := 3A + 12,   P := L^B,   δ := P/N,   K := 3B + 12.

All constants implied by ≪ depend only on A (through B and K, and through the constants of (SW) with M = B + 1). "Z large" means Z >= Z_0(A). Note that Z <= N <= 2Z, log N <= 2L, and log Y >= L/2 for Z large.

Exponential sums:

    F(α) := Σ_{1 <= n <= Y} Λ(n) e(nα),   G(α) := Σ_{1 <= m <= N} Λ(m) e(mα),   v_X(β) := Σ_{1 <= n <= X} e(nβ).

### Step 0. Arithmetic facts about S and S_P

Put f(r) := μ(r)^2 (r/φ(r))^2. Define k multiplicative, supported on squarefree numbers, with k(p) := (p/(p-1))^2 - 1 = (2p-1)/(p-1)^2.
- For every p, k(p) <= 6/p. (This is equivalent to 4p^2 - 11p + 6 >= 0, which holds for p >= 2.)
- For every n >= 1, (n/φ(n))^2 = Π_{p|n} (1 + k(p)) = Σ_{e | n} k(e). In particular f(r) <= Σ_{e|r} k(e).

**(0a)** For all X >= 1:

    Σ_{r <= X} f(r) <= Σ_{n <= X} (n/φ(n))^2 <= Σ_e k(e) X/e = X Π_p (1 + k(p)/p) <= C_f X,

with C_f := Π_p (1 + 6/p^2) < ∞.

**(0b)** For X >= 1, by partial summation from (0a): Σ_{r <= X} f(r)/r <= C_f (1 + log X). This bounds Σ_{q<=X} μ(q)^2/φ(q) and Σ_{d<=X} μ(d)^2 d/φ(d)^2, since both are <= Σ_{r<=X} f(r)/r.

**(0c)** Put ε(X) := Σ_{r > X} μ(r)^2/φ(r)^2. Then ε(X) <= ε(0) =: C_ε < ∞ for every X, and ε(X) <= 2C_f/X for X >= 1. (Partial summation: Σ_{r>X} f(r)/r^2 <= 2∫_X^∞ C_f t/t^3 dt.)

**(0d) Pointwise bound.** For q squarefree, write q = d r with d = (q, h). Then (d, r) = 1 and φ(q) = φ(d)φ(r), so μ(q)^2 |c_q(h)|/φ(q)^2 = μ(q)^2/(φ(d) φ(r)^2). Summing over q, for every h ≠ 0 and every X >= 0:

    Σ_{q > X} μ(q)^2 |c_q(h)|/φ(q)^2  <=  Σ_{d | h} (μ(d)^2/φ(d)) ε(X/d).       (0.1)

- With X = 0, this shows that S(h) converges absolutely. It also gives |S(h)| <= C_ε Σ_{d|h} μ(d)^2/φ(d) = C_ε h/φ(h).
- The same bound holds for the truncation S_P(h) := Σ_{q <= P} μ(q)^2 c_q(h)/φ(q)^2: |S_P(h)| <= C_ε h/φ(h).
- By (0a), therefore,

    Σ_{1 <= h <= Z} ( S(h)^2 + S_P(h)^2 )  <=  2 C_ε^2 C_f Z.       (0.2)

**(0e) Euler product.** By absolute convergence and multiplicativity in q, S(h) = Π_p (1 + c_p(h)/(p-1)^2). The factor is p/(p-1) if p | h, and 1 - 1/(p-1)^2 if p ∤ h. For p = 2 this is 2 or 0.
- So S(h) = 0 for h odd.
- For h even, S(h) = 2 C2 Π_{p|h, p>2} (p-1)/(p-2), using (p/(p-1)) / (1 - 1/(p-1)^2) = (p-1)/(p-2).
- In particular, **S(h) >= 2C2 = 1.3203... > 1 for every even h.**

**(0f) Mean square of the tail.** Let E_P(h) := Σ_{q > P} μ(q)^2 |c_q(h)|/φ(q)^2, so |S(h) - S_P(h)| <= E_P(h). Then

    Σ_{1 <= h <= Z} E_P(h)^2  <=  C_0 Z (1 + log P)/P,     with C_0 absolute.       (0.3)

*Proof.* By (0.1), E_P(h) <= Σ_{d|h} w_d ε_d with w_d = μ(d)^2/φ(d) and ε_d = ε(P/d). Expand the square and swap sums (all terms are >= 0). Use #{h <= Z : [d1, d2] | h} <= Z/[d1, d2] = Z (d1, d2)/(d1 d2):

    Σ_h E_P(h)^2 <= Z Σ_{d1, d2} w_{d1} w_{d2} ε_{d1} ε_{d2} (d1, d2)/(d1 d2).

- Bound ε_{d2} <= C_ε.
- For fixed d1, sum over d2 by grouping according to e | (d1, d2) (with (d1, d2) <= Σ_{e | (d1,d2)} φ(e)). Write d2 = e s with (e, s) = 1:

      Σ_{d2} μ(d2)^2 (d1,d2)/(d2 φ(d2))  <=  Σ_{e | d1} φ(e) μ(e)^2/(e φ(e)) · Σ_s μ(s)^2/(s φ(s))  <=  C_1 Σ_{e|d1} μ(e)^2/e  <=  C_1 d1/φ(d1).

  Here C_1 = Σ_s μ(s)^2/(sφ(s)) < ∞, and Σ_{e|d} μ(e)^2/e = Π_{p|d}(1 + 1/p) <= d/φ(d).
- So Σ_h E_P^2 <= C_ε C_1 Z Σ_{d1} μ(d1)^2 ε(P/d1)/φ(d1)^2.
- Split at d1 = P:
  - For d1 <= P, use ε(P/d1) <= 2C_f d1/P and (0b). This gives <= (2C_f/P) · C_f(1 + log P).
  - For d1 > P, use ε(P/d1) <= C_ε and (0c). This gives <= C_ε · 2C_f/P.

  This proves (0.3). ∎

_Remark: (0.3) is weaker than the standard Σ_{h<=Z} |S(h) - S_P(h)|^2 ≪ Z P^{-1} log P type bounds (Montgomery-Vaughan 1975, Vaughan's book Ch. 3; recalled from memory, not re-read), and we need nothing stronger. The proof above is self-contained, so no literature form of the singular-series mean value is used._

### Step 1. Fourier expression for R(h)

For every integer h with 1 <= h <= Z:

    R(h) = ∫_T G(α) \overline{F(α)} e(-hα) dα.       (1.1)

Indeed, the integral equals Σ_{m <= N, n <= Y} Λ(m)Λ(n) [m - n = h]. If n <= Y and 1 <= h <= Z, then m = n + h <= Y + Z = N, so the constraint m <= N is automatic and the sum is R(h). (We used only that m is an integer and m <= Y + Z.)

### Step 2. Arcs

For 1 <= q <= P and 1 <= a <= q with (a, q) = 1 (for q = 1 take a = 1, i.e. a/q ≡ 0), put

    M(q, a) := { α ∈ T : ||α - a/q|| <= δ },    M := ∪ M(q, a),    m := T \ M.

**Disjointness.** For distinct fractions a/q ≠ a'/q' with q, q' <= P, ||a/q - a'/q'|| >= 1/(qq') >= P^{-2} > 2δ = 2P/N, as soon as N > 2P^3. This holds for Z large. On M(q, a), write α = a/q + β with β ∈ [-δ, δ] uniquely determined.

**Minor arcs: q is large.** Let α ∈ m. Apply (D) with Q' := ⌊N/P⌋. This gives a, q with 1 <= q <= Q' and |qα - a| <= 1/(Q'+1) < P/N; we may assume (a, q) = 1. Then

    ||α - a/q|| < P/(qN) <= δ.

- If q <= P, then α ∈ M(q, a mod q), a contradiction. So q > P.
- Also |α - a/q| < 1/(qQ') <= 1/q^2, since q <= Q'.

So (V) applies to G (with X = N):

    sup_{α ∈ m} |G(α)|  <=  C_V ( N P^{-1/2} + N^{4/5} + N^{1/2} (N/P)^{1/2} ) (log N)^4  ≪  N P^{-1/2} L^4.       (2.1)

(We used q <= Q' <= N/P in the third term, and N^{4/5} <= N P^{-1/2} for Z large.)

### Step 3. Major arcs: approximation of F and G (Siegel-Walfisz)

**Claim 3.** Let X ∈ {Y, N}. Uniformly for 1 <= q <= P, (a, q) = 1 and |β| <= δ,

    | Σ_{n <= X} Λ(n) e(n(a/q + β)) - (μ(q)/φ(q)) v_X(β) |  ≪  X L^{2B-K}  =  X L^{-B-12}.       (3.1)

*Proof.* Let D(x) := Σ_{n <= x} Λ(n) e(an/q) - (μ(q)/φ(q)) ⌊x⌋ for x >= 1, and D(x) := 0 for x < 1.

(i) **1 <= x <= X^{1/2}.** By (C), |D(x)| <= ψ(x) + x <= 3 X^{1/2}.

(ii) **X^{1/2} < x <= X.** Split n by its residue r mod q:

    Σ_{n<=x} Λ(n) e(an/q) = Σ_{(r,q)=1} e(ar/q) ψ(x; q, r) + Σ_{n <= x, (n,q) > 1} Λ(n) e(an/q).

- The last sum runs over n = p^k with p | q. Its modulus is <= Σ_{p | q} log p · (log x/log p) = ω(q) log x <= log^2 x.
- For Z large, log x >= (log Y)/2 >= L/4. So q <= P = L^B <= (L/4)^{B+1} <= (log x)^{B+1}.
- So (SW) with M = B + 1, in its log-power form with exponent K, gives ψ(x; q, r) = x/φ(q) + O(x (log x)^{-K}) for each (r, q) = 1.
- Since Σ_{(r,q)=1} e(ar/q) = c_q(a) = μ(q), we get Σ_{n<=x} Λ(n)e(an/q) = μ(q)x/φ(q) + O(φ(q) x (log x)^{-K} + log^2 x).
- Replacing x by ⌊x⌋ in the main term costs <= 1.

With φ(q) <= P = L^B and (log x)^{-K} <= 4^K L^{-K}, this gives |D(x)| ≪ X L^{B-K} + L^2 ≪ X L^{B-K}.

So sup_{x<=X} |D(x)| ≪ X L^{B-K} + X^{1/2} ≪ X L^{B-K}.

(iii) **Partial summation** (Riemann-Stieltjes, with D(1^-) = 0). Since Σ_{n<=X} e(n(a/q + β)) e(-an/q) = v_X(β), the left side of (3.1) equals

    | Σ_{n <= X} (Λ(n) e(an/q) - μ(q)/φ(q)) e(nβ) | = | D(X) e(Xβ) - 2πiβ ∫_1^X D(x) e(xβ) dx |  <=  (1 + 2π|β|X) sup_{x<=X} |D(x)|.

Here X <= N, so |β| X <= δN = P. Hence the left side is ≪ (1 + 2πP) X L^{B-K} ≪ X L^{2B-K}. ∎

Define on M, for α = a/q + β ∈ M(q, a):

    F*(α) := (μ(q)/φ(q)) v_Y(β),    G*(α) := (μ(q)/φ(q)) v_N(β).

By (3.1), sup_M |F - F*| ≪ Y L^{-B-12} and sup_M |G - G*| ≪ N L^{-B-12}.

_Why the unbalanced lengths are harmless here._ The arcs have width δ = P/N, which is adapted to the long sum G (|β| N <= P). For the short sum F, |β| Y <= P Y/N <= P/L^2, which is even smaller. Both partial-summation losses are at most 1 + 2πP, a power of L. (SW) is applied only at x >= Y^{1/2}, with q <= L^B <= (log x)^{B+1}.

### Step 4. The singular integral

For integers 1 <= h <= Z define

    I(h) := ∫_{-δ}^{δ} v_N(β) \overline{v_Y(β)} e(-hβ) dβ.

Then I(h) = ⌊Y⌋ - τ(h) with |τ(h)| <= 1/(2δ) = N/(2P). Proof:
- By orthogonality, ∫_{-1/2}^{1/2} v_N \bar v_Y e(-hβ) dβ = #{(m, n) : 1 <= m <= N, 1 <= n <= Y, m - n = h} = ⌊Y⌋, since every n <= Y has n + h <= N (as in Step 1).
- For 0 < |β| <= 1/2 and every X >= 1, |v_X(β)| = |sin(π⌊X⌋β)/sin(πβ)| <= 1/(2|β|), because |sin πβ| >= 2|β|.
- Hence τ(h) := ∫_{δ < |β| <= 1/2} v_N \bar v_Y e(-hβ) dβ satisfies |τ(h)| <= 2∫_δ^∞ dβ/(4β^2) = 1/(2δ).

### Step 5. Main term on the major arcs

Put J(h) := ∫_M G*(α) \overline{F*(α)} e(-hα) dα. On M(q, a), G* \bar F* e(-hα) = (μ(q)^2/φ(q)^2) v_N(β) \bar v_Y(β) e(-ha/q) e(-hβ). Summing over a with (a,q)=1 gives c_q(-h) = c_q(h). So

    J(h) = Σ_{q <= P} (μ(q)^2 c_q(h)/φ(q)^2) · I(h) = S_P(h) (⌊Y⌋ - τ(h)).       (5.1)

(Here the uniform width δ of the arcs is essential: I(h) does not depend on q.)

### Step 6. Decomposition and the five mean squares

For 1 <= h <= Z, by (1.1) and (5.1):

    R(h) - S(h) Y = R_m(h) + E_M(h) + (S_P(h) - S(h)) ⌊Y⌋ + S(h)(⌊Y⌋ - Y) - S_P(h) τ(h),

where
- R_m(h) := ∫_m G \bar F e(-hα) dα, and
- E_M(h) := ∫_M (G \bar F - G* \bar F*) e(-hα) dα.

By (a_1 + ... + a_5)^2 <= 5 Σ a_i^2, Σ_{h<=Z} |R(h) - S(h)Y|^2 <= 5 (Σ_1 + ... + Σ_5), with the five sums below.

**Σ_1 (minor arcs).** By (P) applied to Φ = 1_m G \bar F (summing over all h ∈ Z only increases the left side), then (2.1), (C) and ∫_T |F|^2 = Σ_{n<=Y} Λ(n)^2 <= (log Y) ψ(Y) <= 2 Y L:

    Σ_1 := Σ_{h<=Z} |R_m(h)|^2 <= ∫_m |G|^2 |F|^2 <= (sup_m |G|)^2 ∫_T |F|^2 ≪ N^2 P^{-1} L^8 · Y L ≪ Z^2 Y L^{9-B}.

Since Z = Y L^2, this is **Z Y^2 L^{11-B}**.

_Check of the powers of L (delicate part 1)._ The trivial size of Σ_h R(h)^2 is Z Y^2. The minor-arc term is Z^2 Y L^{9-B} = Z Y^2 · (Z/Y) · L^{9-B} = Z Y^2 L^{11-B}. The factor Z/Y = L^2 comes from taking the sup of the *long* sum G and the L^2 norm of the *short* sum F. It is paid for by the choice B = 3A + 12.

**Σ_2 (major-arc approximation; delicate part 2).** By (P) applied to Φ = 1_M (G \bar F - G* \bar F*):

    Σ_2 := Σ_h |E_M(h)|^2 <= ∫_M |G \bar F - G* \bar F*|^2 <= 2∫_M |G - G*|^2 |F|^2 + 2∫_M |G*|^2 |F - F*|^2.

- First term: <= 2 (sup_M |G - G*|)^2 ∫_T |F|^2 ≪ N^2 L^{-2B-24} Y L ≪ Z Y^2 L^{-2B-21}.
- Second term: <= 2 (sup_M |F - F*|)^2 ∫_M |G*|^2. By disjointness of the arcs,

      ∫_M |G*|^2 = Σ_{q<=P} μ(q)^2 φ(q)/φ(q)^2 ∫_{-δ}^{δ} |v_N|^2 <= ⌊N⌋ Σ_{q<=P} μ(q)^2/φ(q) <= N C_f (1 + log P)

  by (0b). So the second term is ≪ Y^2 L^{-2B-24} · Z L ≪ Z Y^2 L^{-2B-23}.

So **Σ_2 ≪ Z Y^2 L^{-2B-21}**.

**Σ_3 (singular-series tail; delicate part 3).** By (0.3): Σ_3 := ⌊Y⌋^2 Σ_{h<=Z} |S_P(h) - S(h)|^2 <= Y^2 · C_0 Z (1 + B log L) L^{-B}. This is **≪ Z Y^2 L^{1-B}**.

**Σ_4 (rounding of Y).** By (0.2): Σ_4 := Σ_h S(h)^2 (⌊Y⌋ - Y)^2 <= 2C_ε^2 C_f Z. This is **≪ Z**.

**Σ_5 (tail of the singular integral; delicate part 4).** By Step 4 and (0.2): Σ_5 := Σ_h S_P(h)^2 τ(h)^2 <= (N/(2P))^2 · 2C_ε^2 C_f Z ≪ Z^3 L^{-2B}. Since Z^2 = Y^2 L^4, this is **Z Y^2 L^{4-2B}**.

_The main term (delicate part 4)._ Steps 4-5 show that the major arcs reproduce exactly S_P(h)⌊Y⌋. The only loss is the tail τ(h), which is <= N/(2P), smaller than Y by the factor L^{2-B}/2. This works only because the arc width δ = P/N is much larger than 1/Y: δY = P Y/N ≍ L^{B-2}. If the arcs were |β| <= 1/(qQ) with Q = N/P (width P/(qN)), then for q close to P the width would be about 1/N < 1/Y, and the tail would be as large as the main term. This is why Step 2 uses arcs of uniform width P/N.

**Total.** For Z large (B >= 12):

    Σ_{1<=h<=Z} |R(h) - S(h) Y|^2  ≪  Z Y^2 ( L^{11-B} + L^{-2B-21} + L^{1-B} + Y^{-2} + L^{4-2B} )  ≪  Z Y^2 L^{11-B}  =  Z Y^2 L^{-3A-1}.

This proves (i), with room to spare.

**(ii).** By Chebyshev's inequality (counting form),

    #{h <= Z : |R(h) - S(h)Y| > Y L^{-A}} <= (Y L^{-A})^{-2} Σ_h |R - SY|^2 ≪ L^{2A} · Z L^{-3A-1} <= Z L^{-A}. ∎

### Step 7. From Λ-weights to prime counts: Corollary (G)

Fix c >= 0. Apply (ii) with A = 2. Let h ∈ [1, Z] be even, and outside the exceptional set of (ii), whose size is <= C(2) Z L^{-2}.

- **Lower bound for R(h).** By (0e), S(h) >= 2C2 > 1.32. So R(h) >= (2C2 - L^{-2}) Y >= Y for Z large.
- **Prime powers.** Split R(h) according to whether n and n+h are both primes. A term with Λ(n)Λ(n+h) ≠ 0 where n or n + h is a prime power p^k with k >= 2 has:
  - either n ∈ [1, Y] such a power, with at most Σ_{2<=k<=log_2 Y} Y^{1/k} <= 2Y^{1/2} choices for Z large;
  - or n + h ∈ [1, N] such a power, with at most 2N^{1/2} choices, each of which determines n.

  Each term is <= log Y · log N <= (log N)^2. So these terms contribute <= 4 N^{1/2} (log N)^2 <= 4 (2Z)^{1/2} (2L)^2 = o(Y).
- **Counting.** The remaining terms have n = p and n + h = p + h both prime, with p <= Y. Each is <= log Y log N <= (log N)^2 <= 2L^2 for Z large (log N <= L + 1). Hence

      r_Y(h) >= (R(h) - 4 N^{1/2} (log N)^2) / (2L^2) >= (Y/2)/(2L^2) = Z/(4L^4)

  for Z large.

So r_Y(h) > c once Z/(4L^4) > c. Hence for Z >= Z_1(c), Bad_c(Z, Y) is contained in the exceptional set of (ii) with A = 2, and |Bad_c(Z, Y)| <= C(2) Z L^{-2}. The statements about Z_j = j follow. ∎

## Remarks

**R1. Where the unbalanced lengths enter, and why they are harmless.** They enter in three places, each costing a power of L that B = 3A + 12 absorbs:
- Σ_1: the factor Z/Y = L^2.
- Step 3: the partial-summation loss 1 + 2πP, and the condition q <= (log x)^{B+1} for x >= Y^{1/2}.
- Σ_5: the tail N/P versus Y.

Hence the same proof gives (G\*) for Y = Z/L^D with any fixed D, with B = 3A + D + 10 (not written out).

**R2. Robustness to misremembered constants.**
- If (V) holds with (log X)^c in place of (log X)^4, then Σ_1 becomes Z Y^2 L^{2c+3-B}. Take B = 3A + 2c + 4.
- If (SW) is used in the weaker form with an error (log x)^{-K'} for every K', that is all we use.

So the proof does not depend on the exact exponents in the cited theorems, only on their qualitative forms:
- (V): a saving of q^{-1/2} on minor arcs, up to a fixed power of log;
- (SW): an arbitrary log-power saving for q <= (log x)^M.

**R3. Effectivity.** C(A) and Z_0(A) are ineffective, because of (SW). The deduction in C013 (d) needs no effectivity.

**R4. Route A (Lavrik) was not used.** Lavrik's exact statement is still unread. The proof here is direct (Route B) and uses only (SW), (V), (D), (C), (P) and elementary facts about Ramanujan sums.

## Numerical check

Code: `experiments/src/c014_variance.c`. It computes R_Y(h) exactly for **every** even h <= Z, with Y = floor(Z/(ln Z)^2) and prime powers included, and compares it with S(h)Y. Raw output: `experiments/results/c014_variance/stdout.txt`.

| Z | Y | mean_h ((R - SY)/Y)^2 | max_h \|R/(SY) - 1\| | #{h : \|R-SY\| > Y/(ln Z)^{1/2}} | min r_Y(h) |
|---|---|---|---|---|---|
| 10^6 | 5,239 | 1.45e-2 | 0.354 | 14,756 | 43 |
| 3·10^6 | 13,487 | 7.26e-3 | 0.269 | 6,632 | 102 |
| 10^7 | 38,492 | 3.14e-3 | 0.176 | 554 | 276 |
| 3·10^7 | 101,209 | 1.44e-3 | 0.131 | 2 | 651 |
| 10^8 | 294,705 | 6.00e-4 | 0.087 | 0 | 1,692 |

- The mean of S(h) over even h <= Z is 2.0000 at every Z, which checks the S(h) code.
- The normalised variance decreases roughly like (log)^c/Y, i.e. square-root cancellation. That is far stronger than the proved L^{-3A-1}.
- **Caveat.** For A >= 1, the threshold Y L^{-A} is still below the square-root fluctuation size (about √Y · log Z) at these Z. So many h exceed it: 1.5·10^6 of 5·10^7 at A = 1, Z = 10^8. (G\*) is asymptotic for fixed A, and the data can only probe A ≈ 1/2. There the exceptional set drops to 0, as predicted.
- Consistent with C013's check: Bad_c(10^8, Y) = ∅ for all c < 1,692.

## Review log

- 2026-11-25 (prover): created. Route B written out in full. **Self-assessed GAP? items:**
  1. **GAP? (citation exactness).** The exact forms of (SW) and (V), and their theorem numbers in Davenport / Iwaniec-Kowalski / Vaughan, are recalled from memory and were not re-read. R2 explains why only their qualitative shape matters. Still, a human should confirm the theorem numbers.
  2. (Resolved while drafting.) A first draft took K = 2B + 1, which gives only X L^{-1} in (3.1). That is too weak for Σ_2. Now K := 3B + 12. Σ_2 uses (3.1) as X L^{-B-12}.

  No other step is, to my knowledge, uncertain. Awaiting skeptic (give them Statement + Proof only), literature agent (is (G\*) stated somewhere?), and an analytic number theorist.
- 2026-11-25 (literature): citation check; see `literature/sw-vinogradov-statements.md` and `literature/search-C014-G-star.md`. The books themselves were not accessible; everything below comes from secondary quotes.
  - **(V)** confirmed with (log N)^4 by Bhowmik-Grimmelt arXiv:2607.27282, Prop. 4.1, and by Languasco-Zaccagnini arXiv:1206.0252, Lemma 3, which is labelled "Vaughan, The Hardy-Littlewood method, 2nd ed., Theorem 3.1". Both sources state a strict |α - a/q| < q^{-2}. Step 2 produces a strict inequality anyway, so this is harmless. IK Thm 13.6 is quoted with (log x)^3 (Tao, arXiv:1201.6656, (1.3)).
  - **(SW)** confirmed in the log-power form (q ≪ (log x)^C gives error x (log x)^{-C}) as IK Cor. 5.29 (quoted in arXiv:2103.15648, Thm 4.3). That is all the proof uses. Davenport Ch. 22 is not verified.
  - **Conclusion of C014 unaffected.** GAP? item 1 is reduced to "theorem numbers confirmed only secondarily".
  - **(G\*)** not found stated. Unbalanced analogues exist: Zhou arXiv:1704.01908, Thm 1.1 (polynomial shifts, ℓ >= 2), and Akeno arXiv:2508.02769, Prop. 1.4 (sums with p <= X^c, proof omitted). So "standard by the same proof" is well supported.
  - Lavrik, as paraphrased by Zhou, is the balanced {m <= X} form, so the Method paragraph should not suggest that Lavrik covers (G\*).
- 2026-11-25 (skeptic): I read only Statement, Depends on, Proof, Remarks and Numerical check, plus the statement of C013 (to match the definitions of r_Y and Bad_c). I did not read attempts/. I checked every inequality and every exponent of L by hand, and reran the numerics with an independent implementation. **Verdict: PASS on every step.** No mathematical gap found. Two cosmetic points and one procedural caveat are listed at the end.
  - **Step 0: PASS.**
    - k(p) <= 6/p is equivalent to 4p^2-11p+6 >= 0, with roots 3/4 and 2, so it holds with equality at p = 2.
    - (0a): (n/φ(n))^2 = Σ_{e|n} k(e), and f(r) <= (r/φ(r))^2. (0b) and (0c) follow by partial summation. The bounds μ^2/φ(q) <= f(q)/q and μ^2 d/φ(d)^2 = f(d)/d are correct.
    - (0.1): for squarefree q, the map q -> (d, r) = ((q,h), q/(q,h)) is injective. |c_q(h)| = φ(d), so the term equals 1/(φ(d)φ(r)^2) and r > X/d. Dropping the coprimality conditions only enlarges the sum. Σ_{d|h} μ^2(d)/φ(d) = h/φ(h). (0.2) follows from (0a).
    - (0.3): #{h <= Z : [d1,d2] | h} <= Z(d1,d2)/(d1 d2). The identity n = Σ_{e|n} φ(e) gives the regrouping d2 = es with (e,s) = 1, and Π_{p|d}(1+1/p) <= d/φ(d). The split at d1 = P gives 2C_f^2(1+log P)/P + 2C_ε C_f/P. All terms are nonnegative, so the interchanges are legitimate.
    - (0e): the Euler product is valid by absolute convergence and multiplicativity of μ^2 c_q(h)/φ(q)^2 in q. The local factors, the p = 2 factor (2 or 0) and (p/(p-1))/(1-1/(p-1)^2) = (p-1)/(p-2) are all correct. So S(h) >= 2C2 for even h.
    - Independent check: the Euler product agrees with the truncated Ramanujan series (q <= 4000) at h = 2, 6, 30, 210, 999990 and 9999990, to within the truncation error.
  - **Step 1: PASS.** n <= Y and h <= Z give n + h <= N, so the constraint m <= N is automatic. m >= 1 is also automatic. The sums are finite, so the interchange is trivial.
  - **Step 2: PASS.**
    - Disjointness: 1/(qq') >= P^{-2} > 2P/N once N > 2P^3. Also δ < 1/2, so β is unique.
    - Dirichlet in the form ||qα|| <= 1/(Q'+1) is correct (Q'+2 points in Q'+1 boxes). Q'+1 > N/P gives a strict < P/(qN) <= δ. Reducing a/q to lowest terms keeps |q'α - a'| <= |qα - a|, so "we may assume (a,q)=1" is fine.
    - So q > P, and |α - a/q| < 1/(q(Q'+1)) <= q^{-2}.
    - (V) is Vaughan, *HL Method*, Thm 3.1, in the form I also recall. With P < q <= N/P, both Nq^{-1/2} and N^{1/2}q^{1/2} are <= N P^{-1/2}. The q <= N/P bound is used correctly in the third term. N^{4/5} <= N P^{-1/2}. So sup_m |G| ≪ N P^{-1/2} L^4 (log N <= 2L).
  - **Step 3: PASS.**
    - x > X^{1/2} >= Y^{1/2} gives log x >= L/4 for Z large. Then q <= L^B <= (L/4)^{B+1} once L >= 4^{B+1}, so (SW) with M = B+1 applies. Its constant depends only on A.
    - Σ_{(r,q)=1} e(ar/q) = c_q(a) = c_q(1) = μ(q), since (a,q) = 1.
    - The terms with (n,q) > 1 are p^k with p | q. They contribute <= ω(q) log x <= log^2 x.
    - The summed SW error is φ(q) x (log x)^{-K} <= 4^K X L^{B-K}. The ranges x <= X^{1/2} (<= 3X^{1/2}) and the L^2 term are absorbed because X >= Z/L^2.
    - Partial summation: Σ_{n<=X} a_n e(nβ) = D(X)e(Xβ) - 2πiβ ∫_1^X D(x)e(xβ)dx is correct for a_n = Λ(n)e(an/q) - μ(q)/φ(q). The loss is 1 + 2π|β|X <= 1 + 2πP. This gives X L^{2B-K} = X L^{-B-12}. Verified.
  - **Steps 4-5: PASS.**
    - Orthogonality gives ⌊Y⌋ over the full circle. |v_X(β)| <= 1/(2|β|) on 0 < |β| <= 1/2 (Jordan). The tail is <= 2∫_δ^∞ dβ/(4β^2) = 1/(2δ).
    - J(h) = S_P(h)(⌊Y⌋ - τ(h)) is an exact identity. It does use (1) disjointness and δ < 1/2, so that ∫_M = Σ_{q,a} ∫_{-δ}^{δ}, (2) e(-hα) = e(-ha/q)e(-hβ) for integer h, (3) Σ_a e(-ha/q) = c_q(h), real and even, and (4) the q-independent width, so that I(h) factors out. All four hold.
  - **Step 6: PASS.**
    - The decomposition R - SY = R_m + E_M + (S_P - S)⌊Y⌋ + S(⌊Y⌋ - Y) - S_P τ is an exact identity (expanded and checked).
    - Parseval is applied to Φ = 1_m G \bar F and Φ = 1_M(G\bar F - G*\bar F*). Both are bounded, hence in L^2. Restricting to 1 <= h <= Z only drops terms.
    - Σ_1 = N^2 P^{-1} L^8 · 2YL ≪ Z Y^2 L^{11-B}. Σ_2 ≪ Z Y^2 L^{-2B-21}. Here ∫_M |G*|^2 = Σ_q μ^2 φ(q)/φ(q)^2 ∫|v_N|^2 <= ⌊N⌋ Σ_{q<=P} μ^2/φ(q) uses disjointness, and is correct.
    - Σ_3 ≪ Z Y^2 L^{1-B} log L. Σ_4 ≪ Z. Σ_5 ≪ (N/P)^2 Z = Z Y^2 L^{4-2B}.
    - The trivial size of Σ_h R(h)^2 is indeed ≍ Z Y^2.
    - The total is Z Y^2 L^{-3A-1}, and Chebyshev gives (ii) with Z L^{-A-1}.
    - R1 (general D) and R2 (log exponent c) recomputed: correct.
  - **Step 7: PASS.**
    - Prime-power terms: <= (2Y^{1/2} + 2N^{1/2})(log N)^2 = o(Y).
    - Weights on prime pairs: <= log Y log N <= 2L^2. So r_Y(h) >= Z/(4L^4) off the exceptional set, and Bad_c ⊆ exceptional set once Z/(4L^4) > c.
    - Definitions match C013 (r_Y and Bad_c with real Y, h ∈ [1,Z] even). Z_j = j satisfies both limits in (G).
  - **Sanity (item 8): no conflict found.**
    - (G*) is the classical Chudakov-Estermann / Lavrik mean-square argument. The ranges are unbalanced only by a power of L, and the proof shows that this costs only L-powers. This is plausible: Σ_1 has ratio (N/Y) L^{9-B}.
    - The same proof correctly *fails* for Y = Z^θ, θ < 1 (Σ_1 loses Z^{1-θ}). That is where the genuinely hard short-range results (zero-density methods) live.
    - Siegel zeros only make the constants ineffective, because SW is used only for q <= (log x)^{B+1} (R3).
    - The mod-6 model set Q of C013 R3 violates SW, so the proof does not "prove" that false variant.
    - The size of the exceptional set, ≪ Z L^{-A}, matches the classical Goldbach exceptional-set bound.
  - **Numerics (item 9).** I reran `experiments/src/c014_variance.c` at Z = 10^6, 3·10^6, 10^7 and reproduced the table exactly. I also wrote an independent check (numpy FFT correlation, real Y, all h including odd, separate Euler-product code). It gives Σ_{h<=Z} |R-SY|^2/(Z Y^2) = 7.26e-3 at Z = 10^6 and 1.57e-3 at Z = 10^7, about 0.2 L^2/Y, i.e. square-root cancellation. Odd h contribute about 1e-3 of the total. The exceptional counts agree with the C code to within a few units (floor vs real Y). As the prover says, at A >= 1 the threshold Y L^{-A} is still below the √Y·L fluctuation at these Z, so (ii) cannot be tested for A >= 1 numerically. That is expected, not a counterexample.
  - **Cosmetic.**
    - (1) The "Moreover" sentence of the Statement (r_Y(h) >= Z/(4(log Z)^4)) should say "for Z >= Z_2(A=2)". It is proved only for Z large.
    - (2) (ii) is proved for all h, not only even h. Harmless.
  - **Procedural caveat (not a gap).** The forms of (SW) and (V) match my own recollection: Vaughan Thm 3.1 with (log X)^4, IK Cor 5.29, Davenport Ch. 22. But my recollection is not a re-reading of the source, and by R2 only their qualitative shape matters. Given the stakes, this PASS should be followed by an external analytic number theorist and Matteo before C014 moves to proven/. The novelty of the combined result rests on C013, not on C014. C014 is routine.
- 2026-11-25 (editor): Method paragraph corrected (Lavrik uses equal ranges, so it does not cover (G\*) directly); (V) is now stated with strict inequality. No change to the argument.

- 2026-11-25 (analytic-referee): **PASS.** Refereed blind from Statement/Depends on/Proof/Remarks only (no earlier Review log, attempts/ or literature/ read before the verdict). Per step: Step 0 PASS (rechecked k(p) <= 6/p ⇔ 4p^2-11p+6 >= 0, equality at p=2; (0a)-(0c) partial summation incl. boundary-term sign; (0d) via |c_q(h)| = φ((q,h)) and the injective q -> (d,r) map; (0e) Euler product incl. the p=2 factor 2/0 and (p-1)/(p-2); (0f) expansion, (d1,d2) = Σ_{e|(d1,d2)} φ(e), split at d1 = P). Step 1 PASS (m = n+h <= N automatic). Step 2 PASS (disjointness needs N > 2P^3, strict; Dirichlet in the form ||qα|| <= 1/(Q'+1) gives ||α - a/q|| < δ for q <= P and |α-a/q| < 1/(qQ') <= q^{-2}; reduction to lowest terms harmless; third term of (V) uses q <= N/P). Step 3 PASS (SW only at x > X^{1/2} >= Y^{1/2}, log x >= L/4, q <= L^B <= (log x)^{B+1}; (n,q)>1 terms <= ω(q) log x; partial-summation loss 1 + 2π|β|X <= 1+2πP for both X = Y, N; exponent 2B-K = -B-12 rechecked). Step 4 PASS (|v_X| <= 1/(2|β|), |τ| <= 1/(2δ)). Step 5 PASS (uniform width makes I(h) independent of q; Σ_a e(-ha/q) = c_q(h)). Step 6 PASS: the five-term decomposition is an exact identity; all Parseval uses are on Φ = 1_E · (trig. polynomial) ∈ L^2(T); exponents recomputed: Σ_1 ≪ ZY^2 L^{11-B}, Σ_2 ≪ ZY^2 L^{-2B-21}, Σ_3 ≪ ZY^2 L^{1-B}, Σ_4 ≪ Z, Σ_5 ≪ ZY^2 L^{4-2B}; dominant 11-B = -3A-1 with B = 3A+12; (ii) by Chebyshev gives ≪ Z L^{-A-1}. Step 7 PASS (S(h) >= 2C2 > 1.32 for even h; prime powers <= 4N^{1/2}(log N)^2 = o(Y); each prime-pair weight <= (L+1)L <= 2L^2; r_Y(h) >= Z/(4L^4)).
  No GAP or error located. Cosmetic only: the same symbol C(A) is used in (i) and (ii) (take the max); the Iwaniec-Kowalski exponent in (V) and the strict/non-strict form of the hypothesis |α - a/q| < q^{-2} are recalled from memory, but the proof produces the strict form and R2 makes the log exponent irrelevant.
  Divergences from Vaughan Ch. 3 (Goldbach exceptional set; recalled from memory): (a) difference m - n = h with conjugate F̄ instead of a sum: harmless; (b) unbalanced lengths Y = Z/L^2 vs N ≈ Z: minor arcs bounded by sup_m|G|^2 · ||F||_2^2, loses exactly Z/Y = L^2, absorbed by B; (c) singular-series tail proved self-contained via (0.1) and a divisor expansion instead of the Ramanujan-sum mean value: weaker bound Z log P/P but sufficient; (d) singular integral done as the exact lattice count ⌊Y⌋ minus a tail τ <= N/(2P), which requires δY ≍ L^{B-2} -> ∞, satisfied: harmless. Major-arc width P/N uniform in q, as in Vaughan.
  Known obstructions considered: Siegel zeros only make C(A), Z_0(A) ineffective (via SW), no effect on truth; unbalanced range is only a power of L shorter (not Z^θ, θ < 1), and the proof would visibly fail for Y = Z^θ (Σ_1 loss Z^{1-θ}) - consistent with the known difficulty; uniformity in q only needed for q <= L^B, within SW; no parity issue (a variance/almost-all statement with binary Λ·Λ, as in Lavrik/Mikawa/Perelli-Pintz). Strength vs. literature (from memory): the hard direction in the literature (Mikawa 1993, Perelli-Pintz) is the h-range shorter than the n-range; here the h-range is longer, which is the easier direction, so the claim is not suspiciously strong.
  Numerics (scratchpad script c014_check.py, Z = 10^6, Y = Z/L^2): reproduced mean_h even ((R-SY)/Y)^2 = 1.450e-2 and max |R/(SY)-1| = 0.354, matching the manuscript table; mean of S over even h = 2.0000; Σ_{h<=2·10^4} |S - S_P|^2 / (H(1+log P)/P) = 0.044, 0.0064, 0.0014 for P = 10, 50, 200, consistent with (0.3); k(p) <= 6/p verified for the first 1000 primes.
