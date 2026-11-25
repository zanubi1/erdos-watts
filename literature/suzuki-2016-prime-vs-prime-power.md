# Suzuki (2016), "On prime vs. prime power pairs": secondary statement of Mikawa (1991) and a pointer to Perelli-Pintz (1993), Theorem 3

## Citation/link

Y. Suzuki, "On prime vs. prime power pairs", arXiv:1610.09084v1 (28 Oct 2016), https://arxiv.org/abs/1610.09084. Pages 1-5 and 15-17 (introduction, notation, Theorem 2, Sections 8-9, references) were read as page images.

## What it says

- **Notation (p. 1, eq. (1)):** Ψ(X, h) = Σ_{n <= X} Λ(n) Λ(n + h). The n-range is **n <= X**, not n <= X - h.
- **Theorem A (p. 2), attributed to "Mikawa [13], Perelli and Pintz [17]".** Quoted: "Let X, H, A >= 2, and ε > 0. Assume X^{1/3+ε} <= H <= X. Then we have Ψ(X,h) = S(h)X + O(XL^{-A}) for all but ≪ HL^{-A} even numbers h ∈ [1, H]."
  - Here L = log X (p. 4).
  - [13] = H. Mikawa, *On prime twins*, Tsukuba J. Math. 15 (1991), 19-29.
  - [17] = A. Perelli, J. Pintz, *On the exceptional set for Goldbach's problem in short intervals*, J. London Math. Soc. (2) 47 (1993), 41-49.
- **Remark 4 (p. 16)**, paraphrased.
  - Restricting n^k <= Y in Ψ*_k just replaces X by Y.
  - "as Perelli and Pintz [17, Theorem 3] mentioned, we can obtain the result for the counting function Ψ*_k(Y, h) with h ∈ [X, X+H]."
  - This is motivated by representing N = p' - p^k.
  - So Perelli-Pintz Theorem 3 apparently treats **shifts h much larger than the n-range** (h near X, n <= Y). That is the direction of (G*).
  - Suzuki does not state the ranges of Y and H relative to X.
- **Theorem 2 (p. 5)** is an L^2-over-shifts estimate proved by the same Farey dissection as C014: P = L^B, major arcs of width 1/(qQ) and 1/(qR), with R = X P^{-4}. Its structure is the same as C014's: mean square over shifts, truncated singular series S(h, P), and then Chebyshev.

## Relevance

- **Mikawa (as stated by Suzuki):** shifts h <= H <= X with n <= X, so the shift range is at most the n-range. With X = Y = Z/L^2, this covers only h <= Z/L^2, which is a 1/L^2 fraction of [1, Z]. **It does not contain (G\*), and does not make it immediate.** (G\*) needs shifts up to L^2 times the n-range.
  - The hard part of Mikawa's paper is short shift ranges (H down to X^{1/3+ε}). C014 does not need that.
- **Perelli-Pintz 1993, Theorem 3** (unread, known only through this one sentence) is a **possible prior statement of a (G\*)-type result**: n-range Y, shifts in [X, X+H].
  - If it allows Y ≍ X/(log X)^2 and H ≍ X, then (G\*) would follow by covering [1, Z] with O(1) such intervals (plus the trivial range h <= Y).
  - **Not verified.** The paper must be read before C014 calls itself "not found stated".

## Verified by

Literature agent, 2026-11-25 (sixth pass). **Read** pp. 1-5 and 15-17 of the arXiv PDF as page images. The quotes above are from those pages. Mikawa's and Perelli-Pintz's papers themselves were **NOT read**. projecteuclid.org, tsukuba.repo.nii.ac.jp and dei.unipd.it fail DNS, and the Wiley host was not tried.
