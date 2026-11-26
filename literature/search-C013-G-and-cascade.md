# Search log for C013: is hypothesis (G) known? Is the blocking/cascade argument known?

Date: 2026-11-25. Literature agent. Network: arxiv.org (abs, pdf, search) and raw.githubusercontent.com worked. projecteuclid.org, tsukuba.repo.nii.ac.jp, mathnet.ru and export.arxiv.org fail DNS. www.erdosproblems.com/forum returned HTTP 403. oeis.org was not retried; the GitHub mirror was used instead.

## Citation/link

This is a search log. The sources are listed below; per-source notes:
- `matomaki-radziwill-tao-2019.md` (read, pp. 1-9);
- `lavrik-wolke-mikawa-prime-pairs.md` (snippets only);
- `bhowmik-grimmelt-2026-goldbach-exceptional-set.md` (read, partly).

Also used:
- N. Evans, "Correlations of almost primes", arXiv:2102.12297 (read p. 1-2);
- H. Li, Z. Liu, "Fourth moments of prime exponential sums and exceptional sets for sums and differences of primes", arXiv:2610.26756 (abstract page only);
- K. Halupczok, "Goldbach's problem with primes in arithmetic progressions and in short intervals", JTNB 2013, arXiv:1212.4406 (abstract only).

## What it says / findings

### Q1. Hypothesis (G)

(G): for each c, all but o(Z/log Z) even h <= Z have r_Y(h) = #{p <= Y : p + h prime} > c, with Y log Z/Z -> 0 (canonical Y = Z/(log Z)^2).

**(i) Explicitly stated somewhere? Not found.** Ranges of the results I could check:

| Result | p-range (length) | shift range | covers (G)? |
|---|---|---|---|
| Lavrik 1961 (snippets only) | x (see caveat) | all 2k <= x | possibly, via the reduction below, **if** the pairs counted are n, n + h <= x |
| Wolke (snippet) | y | k <= x, 2x <= y <= x^{8/5-ε} | no (shift < p-range) |
| Mikawa 1991; Perelli-Pintz (via MRT p. 5 and Evans fn. 1) | X | \|h\| <= H, X^{1/3+ε} <= H <= X (all but O(H log^{-A} X)) | no |
| MRT 2019, Thm 1.3(i) (read) | (X, 2X] | \|h - h0\| <= H, X^{8/33+ε} <= H <= X^{1-ε}, h0 <= X^{1-ε} | no |
| Chudakov / van der Corput / Estermann; Montgomery-Vaughan; Pintz (sums) | unrestricted (n1 + n2 = N) | - | no (sum, no small-prime restriction) |
| Halupczok 2013 (abstract only) | one prime in a short interval [X, X + X^θ] | - | not checked; it is a sum problem; might contain the sum analogue |
| Li-Liu 2026 (abstract) | unrestricted differences, under quasi-GRH | - | no |

Not found in my searches: any statement of the shape "almost all even h <= Z are q - p with p <= Z/(log Z)^B", or "almost all even n are p1 + p2 with p1 <= n/(log n)^B". Several targeted web searches ("one small prime", "Goldbach with one prime small", "difference of primes ... small prime") found nothing. **This means I found nothing; it does not show that nothing exists.** Halupczok, Kawada, Brüdern-Perelli and Vaughan's book were **not read**.

**(ii) Routine consequence? My assessment: yes, very probably (confidence about 80%).** There are two routes.

*Route A: reduction to Lavrik's theorem.* This route requires Lavrik's statement to be in the "both primes <= x" form. Suppose, for every fixed A,

    Σ_{h <= x} | Σ_{n <= x-h} Λ(n)Λ(n+h) - S(h)(x-h) |  ≪_A  x^2 (log x)^{-A}.        (Lav)

(Or the L^2 version with x^3 (log x)^{-A}. This is exactly what Parseval gives from F(α) = Σ_{n<=x} Λ(n)e(nα), since ∫|F|^2 e(-hα) dα = Σ_{n<=x-h} Λ(n)Λ(n+h).) Then (G) follows:
- Let L = log Z. Take x_j = Y + jY/2 for 0 <= j <= 2Z/Y = 2L^2. The blocks I_j = (x_j - Y, x_j - Y/2] cover (Y/2, Z].
- For h ∈ I_j, the p-range is x_j - h ∈ [Y/2, Y), so Σ_{n <= x_j - h} Λ(n)Λ(n+h) counts only n <= Y. Its main term is S(h)(x_j - h) >= Y/2, using S(h) >= 2C2 > 1 for even h.
- By (Lav) at x = x_j <= 2Z, the number of h ∈ I_j with error > Y/4 is ≪ Z^2 L^{-A}/Y = Z L^{2-A}. Summing over the 2L^2 + 1 values of j gives ≪ Z L^{4-A}.
- Every other even h ∈ (Y/2, Z] has Σ_{n<=Y} Λ(n)Λ(n+h) >= Y/4. After removing the prime powers (≪ √Y L^2 + L^3), this gives r_Y(h) ≫ Y/L^2 -> ∞.
- The h <= Y/2 number at most Y = o(Z/L).

So |Bad_c(Z, Y)| ≪ Z L^{4-A} + Y = o(Z/log Z). This is (G), even for Y = Z/(log Z)^B with any fixed B.

**Caveat:** I could not read Lavrik's paper. The snippet says "averaged error over 2k <= x ≪ x^2 (log x)^{-A}", but I could not confirm whether the pair count is {n <= x - 2k} (as in (Lav)) or {n <= x}. If it is {n <= x}, the p-range is always x and Route A fails.

*Route B: direct circle method* (the standard Lavrik / Chudakov scheme with unbalanced lengths). I sketched this in detail and found no obstacle:
- Let f(α) = Σ_{n<=Y} Λ(n)e(nα) and g(α) = Σ_{m<=2Z} Λ(m)e(mα). Then R(h) = ∫ g \bar f e(-hα) dα for h <= 2Z - Y.
- Let P = L^B and Q = Y/P.
- **Minor arcs** (P < q <= Q): Vinogradov gives sup|f| ≪ Y L^{4-B/2}, and ∫|g|^2 ≪ Z L. So the contribution to Σ_h |R - R*|^2 is ≪ Y^2 Z L^{9-B}.
- **Major arcs** (q <= P, |β| <= P/(qY)): Siegel-Walfisz handles f directly. It also handles g *pointwise*, because the partial-summation loss (1 + |β| Z) <= P L^2 is only a log power when Z/Y = L^2. So no Gallagher-type lemma is needed.
- **Main term:** the main term is S_P(h)·Y. The truncated singular series is controlled in mean square by the standard bound Σ_{h<=Z} |S(h) - S_P(h)|^2 ≪ Z P^{-1+ε}, as in the Goldbach exceptional set proof (Iwaniec-Kowalski Prop. 19.5, Vaughan's book Ch. 3; not re-read).
- **Result:** Σ_{h ∈ (Z/2, Z]} |R(h) - S(h)Y|^2 ≪ Y^2 Z L^{-A}. Chebyshev's inequality then gives an exceptional set ≪ Z L^{-A}.
- **What it uses:** only Vinogradov, Siegel-Walfisz (ineffective constants) and the singular-series mean value, the same inputs as Chudakov-van der Corput-Estermann.
- **Not written out in full.** An analytic number theorist should confirm it.

**(iii) Open?** Very unlikely. The regime (shift/length ratio (log Z)^2, log-power savings only) is far easier than anything in the MRT/Mikawa line, which fights for power ratios.

### Q2. Blocking lemma (a), cascade (c), and the permutation property

- **A055265** (raw OEIS file via oeisdata mirror, revision #119, Nov 03 2026). Comments unchanged: "Does every positive integer eventually occur?" (Kamenetsky 2009); Wilson v: "almost certainly yes, on probabilistic grounds"; "no proof is known" (for the A051237 limit). There is no proof and no Goldbach-based argument.
- **erdosproblems #473** (teorth/erdosproblems problems.yaml, re-read). Still `status: proved`, last update 2025-08-31; this refers to the main question. `forum: 3 posts`. The forum page returned 403; **not read.**
- **formal-conjectures 473.lean** (re-read): only `erdos_473` (solved) and `erdos_473.variants.finite` (open). No greedy statement.
- **arXiv metadata searches** (arxiv.org/search; this searches titles, abstracts and comments, not full text): "prime sum permutation greedy" gave 0 results. "lexicographically earliest permutation prime" gave only Sloane's OEIS survey (1805.10343, already noted: calls A055265 possibly beyond reach). "adjacent sums prime permutation" gave only Z.-W. Sun 1309.1679 (unrelated). "Watts sequence prime" and "Erdős problem 473" gave nothing relevant.
- **Web searches** (MathOverflow/MSE, "greedy ... prime sums ... Goldbach") found nothing relevant.
- **A051237, A086527, A117922, A128280**: re-checked earlier (see `oeis-A117922-A086527.md`): no proof, no conditional result.
- **EKG / Yellowstone** (earlier notes):
  - (a) with |S| = 1 is the classical smallest-missing step (Lagarias-Rains-Sloane Lemmas 3-4; Devlin-Artamonov in A253074).
  - The EKG proofs use prime/sieve inputs, not binary Goldbach-type inputs. I found no EKG-style proof that uses a binary additive (Goldbach/Lavrik) hypothesis.
- **Not found:** the union form "S never-occurring ⇒ at most max S - 1 blocked steps, uniformly in |S|"; the second-generation cascade (c); and any proof, conditional or not, that A055265 or a greedy prime-sum sequence is a permutation. (a) is a two-line pigeonhole and could well be folklore. Treat it as "not found", not "new".

## Relevance

- C013 (d) is conditional only on (G). If Route A or Route B is confirmed, C013 becomes an **unconditional proof** of the permutation property. That would answer Watts' question in Erdős #473, which is open according to every source checked.
- Before any claim:
  1. read Lavrik's exact statement (or a textbook version) to settle Route A, or write out Route B in full;
  2. run a skeptic pass on C013 (a)-(d), in particular (b) and the parity bookkeeping in (c). A skeptic PASS on the implication was recorded in C013 on the same day;
  3. get an analytic number theorist to check.

## Verified by

Literature agent, 2026-11-25.
- **Read:** MRT 2019 pp. 1-9 (arXiv PDF); Evans 2102.12297 pp. 1-2; Bhowmik-Grimmelt pp. 1-6 and 10-13; raw A055265 (oeisdata mirror); problems.yaml entry #473; 473.lean.
- **Abstracts only:** Li-Liu 2610.26756; Halupczok 1212.4406.
- **Snippets only:** Lavrik, Wolke, Mikawa, Perelli-Pintz.
- **Not accessible:** projecteuclid, tsukuba repository, mathnet.ru, erdosproblems forum (403).
- **Not attempted (no access or no time):** Vaughan's "The Hardy-Littlewood method", Iwaniec-Kowalski Ch. 19, Montgomery-Vaughan 1975, Kawada, Brüdern-Perelli, Wolke's paper, Guy's UPINT, Erdős-Graham 1980.
- The Route A/B reductions are **my own sketches**, not taken from a source.
