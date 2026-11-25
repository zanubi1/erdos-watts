# Lavrik (1961), Wolke (1989), Mikawa (1991), Perelli-Pintz (1992): prime pairs p, p + h for almost all h

## Citation/link

- A. F. Lavrik, papers in Doklady Akad. Nauk SSSR (1960, vol. 132, pp. 1013-1015; 1961, vol. 136, pp. 281-283), listed on mathnet.ru (https://mathnet.ru/eng/dan24497). Secondary sources also cite Lavrik 1961 as Trudy Mat. Inst. Steklov 64. **I did not see either paper; this citation comes from search snippets.**
- D. Wolke, on the prime twin problem; cited in Mikawa's introduction. Exact reference not seen.
- H. Mikawa, "On prime twins", Tsukuba J. Math. 15 (1991), no. 1, 19-29. Also "On prime twins in arithmetic progressions", Tsukuba J. Math. 16 (1992). Both are on projecteuclid.org and tsukuba.repo.nii.ac.jp; **both hosts fail DNS in this session.**
- A. Perelli, J. Pintz, the 2k-twin primes exceptional set (Compositio Math., early 1990s, from memory; not verified). Cited in MRT 2019 as [70].

## What it says (only from secondary sources)

- **Lavrik.** Search snippets (a UEA abstract; a Mikawa Tsukuba paper) say that Lavrik used the circle method to prove that the Hardy-Littlewood prime-pair formula holds for almost all differences, with an averaged error ≪ x^2 (log x)^{-A} over 2k <= x (in a version uniform for moduli q <= (log x)^B). **I have not seen the exact statement.** In particular I could not confirm whether the counted pairs are {n <= x} or {n, n + 2k <= x} (main term S(2k) x or S(2k)(x - 2k)), or whether the average is L^1 or L^2.
- **Wolke and Mikawa** (search snippet of Mikawa's introduction): Wolke showed that the formula holds for almost all k <= x when 2x <= y <= x^{8/5-ε}, and noted that the density hypothesis would give exponent 2 in place of 8/5. Mikawa pushes the exponent beyond 2. In MRT's notation this is: p-range X, shifts |h| <= H, with X^{1/3+ε} <= H <= X^{1-ε}, and all but O(H log^{-A} X) exceptions (MRT 2019, p. 5, read). Footnote 6 of MRT adds the range X^{1-ε} <= H <= X.

## Relevance (C013, hypothesis (G))

- Wolke, Mikawa, Perelli-Pintz and MRT all have **shift range <= p-range**. (G) has shifts ≍ Z with p <= Z/(log Z)^2, so these do not apply directly.
- **Lavrik is the relevant one.** It covers all shifts h <= x. If its counting function is the natural circle-method one, Σ_{n <= x-h} Λ(n)Λ(n+h) = ∫|F(α)|^2 e(-hα) dα with F = Σ_{n<=x} Λ(n)e(nα), then for h close to x the p-range x - h is short. Applying it at O((log Z)^2) values of x then gives (G). See `search-C013-G-and-cascade.md`. Whether Lavrik's paper states exactly this form is **not verified**.

## Update 2026-11-25 (fourth pass, see `search-C014-G-star.md`)

- N. H. Zhou (arXiv:1704.01908, introduction, read via WebFetch) paraphrases Lavrik as follows: for any A > 0, Σ_{m<=X} Λ(m)Λ(m+u) ~ S(u) X for all even u <= X with O(X (log X)^{-A}) exceptions.
  - This is the **{m <= X}** form, not {m <= X - u}. If it is accurate, Route A in `search-C013-G-and-cascade.md` does not follow directly. C014 uses Route B instead.
  - Zhou dates the result "1970" in the text, but cites Dokl. Akad. Nauk SSSR 132 (1960), 1258-1260. That page range differs from the one above.
- This is still secondary. The original was not read (mathnet.ru fails DNS).

## Verified by

Literature agent, 2026-11-25. **Only search-engine snippets and secondary citations** (MRT 2019 pp. 5-8, which I did read). Lavrik's, Wolke's, Mikawa's and Perelli-Pintz's papers were **not read**: projecteuclid.org and tsukuba.repo.nii.ac.jp fail DNS, and mathnet.ru was not tried for the full text. Before citing anything specific to Lavrik, a human should read Lavrik 1961, or a textbook statement of it.
