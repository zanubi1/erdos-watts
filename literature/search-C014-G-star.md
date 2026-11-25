# Search log for C014 (G*): an unbalanced almost-all-shifts prime-pair theorem (shifts h <= Z, p <= Y = Z/(log Z)^C)

Date: 2026-11-25. Literature agent, fourth pass. Network: arxiv.org (abs, html, pdf) works. mathnet.ru, projecteuclid.org, link.springer.com, en.wikipedia.org, encyclopediaofmath.org and terrytao.wordpress.com fail DNS.

## Citation/link

- [Zhou] N. H. Zhou, "Primes in higher-order progressions on average", arXiv:1704.01908v4 (2019). HTML introduction and Theorem 1.1 read via WebFetch.
- [Akeno] M. Akeno, "Small gaps between Goldbach primes", arXiv:2508.02769v3 (2025). HTML Section 1 read via WebFetch.
- [Hal] K. Halupczok, arXiv:1212.4406 (JTNB). Abstract only.
- Lavrik: see `lavrik-wolke-mikawa-prime-pairs.md`. No new primary access.
- Pan Chengdong school, "An elementary approach to the twin primes problem", Monatsh. Math. (Springer, doi 10.1007/s00605-004-0270-3). Search snippet only.

## What it says

1. **Lavrik's statement, secondary form ([Zhou], introduction).** Zhou paraphrases Lavrik as follows: for ℓ = 1, given any A > 0, the asymptotic Σ_{m<=X} Λ(m)Λ(m+u) ~ S(u) X holds for all even u <= X with at most O(X (log X)^{-A}) exceptions.
   - Here the m-range is **m <= X** (not m <= X - u), and the shifts satisfy u <= X. So shift range = p-range: balanced.
   - Zhou's text says "In 1970", but his bibliography entry is "A. F. Lavrik, On the distribution of k-twin primes, Dokl. Akad. Nauk SSSR 132 (1960), 1258-1260". This is internally inconsistent. Our earlier note has Dokl. 132, pp. 1013-1015 (from a mathnet snippet).
   - **Consequence for Route A of C013 (search-C013 note):** if Zhou's paraphrase is accurate, Lavrik's count is over {m <= X}, and Route A (which needed {n <= x - h}) does not follow directly from the statement. C014 uses Route B instead, so this matters only for the "prior art" sentence.
2. **Unbalanced analogue for polynomial shifts ([Zhou], Theorem 1.1).** For integer ℓ >= 2 and A > 0 there is B = B_ℓ(A) such that, for X^{1-1/(2ℓ)} (log X)^B < y <= X,
   Σ_{1<=u<=y} | Σ_{m <= X^{1/ℓ}} Λ(m^ℓ + u)Λ(m) - S_ℓ(u) X^{1/ℓ} |^2 ≪ y X^{2/ℓ} (log X)^{-A}.
   - This is structurally the unbalanced situation of (G*): m-range X^{1/ℓ}, shifts up to X, and a mean-square L^2 estimate over shifts. It is proved by the circle method (Zhou: circle method plus a Weyl-inequality variant).
   - It **does not cover ℓ = 1**, which is (G*).
3. **Sum analogue with one small prime ([Akeno], Proposition 1.4).** Let c ∈ (1/6, 1]. For almost all even N ∈ (X/2, X], #{p + p' = N : p <= X^c} = S(N) X^c / ((ln X^c)(ln N)) (1 + o(1)).
   - It is introduced by "A Siegel-Walfisz type theorem for almost all short intervals yields the following result", and followed by "We omit the proof."
   - A remark (after Theorem 1.3) says the exceptional sets in "all the above results" are O(X (ln X)^{-A}). Whether it covers Prop. 1.4 is unclear to me.
   - This is the **Goldbach (sum) version** with one prime much smaller than the target, a far more unbalanced situation (power ratio) than (G*). It is not a difference statement, it is not stated for p <= X/(log X)^C, and **no proof is given**.
4. **[Hal]:** binary/ternary Goldbach with primes in short intervals near X_i of length X_i^θ (θ >= 0.933). The primes are large ones in short intervals, not small ones. Not (G*).
5. **Searches for "Goldbach with one small prime", "p_1 <= N^θ almost all", or "differences of primes, almost all h, small prime"** (web, extended mode) found nothing else. Richstein's numerics (smallest Goldbach prime <= 5569 up to 10^14) appeared but are irrelevant. Brüdern, Kawada, Perelli-Pintz and Mikawa appeared only with balanced or short-interval results (Goldbach numbers in short intervals, sparse sequences). I did not read those papers.

## Relevance (C014 (G*))

- **(G*) itself was not found stated.** No published statement in the difference form with shifts up to Z and p <= Z/(log Z)^C turned up, in Lavrik's form as paraphrased by Zhou or elsewhere. This is "I found none", not "none exists". Lavrik's original, Mikawa, Kawada and Brüdern-Perelli remain unread.
- **"Folklore by the same proof" is well supported.**
  - [Zhou] Thm 1.1 proves the exact unbalanced L^2-over-shifts structure (short sum over m, shifts up to X) by the circle method, for ℓ >= 2.
  - [Akeno] Prop. 1.4 asserts a much more unbalanced sum version (p <= X^c, c > 1/6) as a routine consequence, with the proof omitted.
  - The ℓ = 1, log-power-ratio case is easier than either. That matches C014's own assessment ("No step is new").
- **Suggested citation wording for C014:** "We found no statement of (G*) in the literature. Lavrik (as quoted in Zhou, arXiv:1704.01908) treats shifts u <= X with m <= X. The unbalanced structure appears for polynomial shifts in Zhou, Thm 1.1, and for sums with one small prime in Akeno, arXiv:2508.02769, Prop. 1.4 (proof omitted). Our proof is the standard circle-method argument."

## Update 2026-11-25 (fifth pass)

- **Mikawa 1991**, as quoted in Suzuki arXiv:1610.09084, Theorem A (read): n <= X, shifts h <= H <= X. It does not contain (G\*).
- **Lavrik**: three secondary paraphrases (Zhou; arXiv:2605.21529, Thm 6.16; Baier 2004 abstract snippet) disagree on the counting range. None has shifts longer than the prime range. The original is still unread.
- **New candidate prior art:** Perelli-Pintz, JLMS (2) 47 (1993) 41-49, Theorem 3. According to Suzuki, Remark 4, it gives the result for the count with n-range Y and shifts h ∈ [X, X+H]. That is the unbalanced direction of (G\*).
  - **Unread.** Until it is read, the claim "(G\*) not found stated" must carry this caveat.
  - See `suzuki-2016-prime-vs-prime-power.md`.

## Verified by

Literature agent, 2026-11-25.
- **Read via WebFetch extraction** (the tool paraphrases; quotes are short): [Zhou] introduction and Theorem 1.1; [Akeno] Section 1.
- **Abstract only:** [Hal].
- **Snippets only:** the Pan-school Monatshefte paper, and everything about Lavrik.
- **Not read:** Lavrik (1960/61), Mikawa (1991/92), Perelli-Pintz, Kawada, Brüdern-Perelli, Wolke, Vaughan's book.
