# Matomäki, Radziwiłł, Tao (2019): Correlations of the von Mangoldt and higher divisor functions I. Long shift ranges

## Citation/link

K. Matomäki, M. Radziwiłł, T. Tao, "Correlations of the von Mangoldt and higher divisor functions I. Long shift ranges", Proc. London Math. Soc. 118 (2019). arXiv:1707.01315 (v3, 18 Feb 2019): https://arxiv.org/abs/1707.01315

## What it says

- **Theorem 1.3 (i)** (read on p. 8): let A > 0, 0 < ε < 1/2, σ = 8/33, X^{σ+ε} <= H <= X^{1-ε}, 0 <= h0 <= X^{1-ε}. Then Σ_{X<n<=2X} Λ(n)Λ(n+h) = S(h)X + O_{A,ε}(X log^{-A} X) "for all but O_{A,ε}(H log^{-A} X) values of h with |h - h0| <= H".
- **Theorem 1.3 (iv)** (averaged Goldbach): Σ_n Λ(n)Λ(N-n) = S(N)N + O(X log^{-A} X) for all but O(H log^{-A} X) integers N in [X, X+H].
- **Prior work, as summarised on p. 5:** the best earlier range is due to Mikawa and Perelli-Pintz: the same conclusion for X^{1/3+ε} <= H <= X^{1-ε}. Footnote 6: "One can also handle the range X^{1-ε} <= H <= X by the same methods" (citing Mikawa and Perelli-Pintz). The older "most h with |h| <= H" results are cited as [10], [44], [4], [78], [57], [70], [41]. I did not resolve the numbers to names, except [57] = Mikawa and [70] = Perelli-Pintz, which the text names.
- **p. 7-8:** for Goldbach, [38, Proposition 19.5] (Iwaniec-Kowalski) gives the asymptotic with error O(X_0 log^{-A} X_0) for all but O(X_0 log^{-A} X_0) even X <= X_0. Perelli-Pintz did short intervals [X_0, X_0 + X_0^{1/3+ε}]. **Halupczok [26]** has variants "with the additional requirement that one of the prime in n = p1 + p2 is constrained to a short interval or an arithmetic progression with large moduli". I have not read Halupczok's paper.

## Relevance (C013, hypothesis (G))

- Every result here has the **p-range (length X) at least as long as the shift range**: h <= X, or |h - h0| <= H with h0 <= X^{1-ε}. Hypothesis (G) needs shifts h ≍ Z with a p-range Y = Z/(log Z)^2, so the shift is **longer** than the p-range by a factor (log Z)^2. Theorem 1.3 does **not** cover (G) directly.
- (G) is a much easier regime than this paper's: it needs only a log-power saving and an interval ratio of (log Z)^2, not a power. See `search-C013-G-and-cascade.md` for the reduction to Lavrik-type results.

## Verified by

Literature agent, 2026-11-25: **read the arXiv PDF, pp. 1-9** (abstract, introduction, prior results, Theorem 1.3). The theorem statement above is transcribed from p. 8. Proofs not read.
