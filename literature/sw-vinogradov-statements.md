# Siegel-Walfisz (SW) and Vinogradov-Vaughan (V): exact statements, as quoted by readable sources

Purpose: check the forms of (SW) and (V) cited from memory in `lemmas/candidates/C014-almost-all-differences.md` ("Depends on"). The primary books (Vaughan, *The Hardy-Littlewood Method*; Iwaniec-Kowalski, *Analytic Number Theory*; Davenport, *Multiplicative Number Theory*) were **not** accessible. Everything below comes from papers that quote them.

## Citation/link

Sources actually read (full text or relevant pages):
- [LZ] A. Languasco, A. Zaccagnini, "A Diophantine problem with prime variables", arXiv:1206.0252v1 (2012). PDF pp. 1-10 read (page images).
- [BG] G. Bhowmik, L. Grimmelt, "The exceptional set of the Goldbach problem", arXiv:2607.27282v2 (2026), to appear in Analysis Mathematica. HTML read via WebFetch (Sections 4.1-4.3 and the bibliography).
- [Tao5] T. Tao, "Every odd number greater than 1 is the sum of at most five primes", arXiv:1201.6656. PDF pp. 2-3 read (page images).
- [Ah] arXiv:2103.15648 ("Triquadratic p-rational fields"), HTML Section 4.2 read via WebFetch (paraphrase plus short quotes from the tool).
- [Ex] arXiv:2606.04677 ("An explicit surjectivity threshold for digit sums of primes"), HTML read via WebFetch (Lemma 6 only).
- [Ext] arXiv:2011.06627 ("An extension of the Siegel-Walfisz theorem"), introduction read via WebFetch.

Not accessible in this session (DNS failure): en.wikipedia.org, encyclopediaofmath.org, terrytao.wordpress.com, link.springer.com, mathnet.ru, pub.math.leidenuniv.nl, personal.science.psu.edu (Vaughan's own notes). The Encyclopedia of Mathematics "Vaughan identity" entry and the Wikipedia Siegel-Walfisz page were seen **only as search snippets**.

## What it says

### (V) Vinogradov's estimate in Vaughan's form

- **[BG], Proposition 4.1 ("Vinogradov-Vaughan").** S(α) := Σ_{n<=N} Λ(n) e(αn). If (a, q) = 1 and |α - a/q| < q^{-2}, then
  S(α) ≪ (N q^{-1/2} + N^{4/5} + (Nq)^{1/2}) (log N)^4.
  Not proved there; no theorem number is given in the text. Vaughan's book (2nd ed., 1997) is in the bibliography as [23].
- **[LZ], Lemma 3, labelled "(Vaughan [17], Theorem 3.1)".** [17] = R. C. Vaughan, *The Hardy-Littlewood method*, 2nd ed., Cambridge U. P., 1997. Statement: α real, a, q positive integers, (a, q) = 1 and |α - a/q| < q^{-2}. Then S_1(α) ≪ (X/√q + √(Xq) + X^{4/5}) log^4 X. **Caveat:** in [LZ], S_1(α) = Σ_{δX <= p <= X} log p · e(pα) (primes in [δX, X], not Λ over [1, X]). That sum differs from Σ_{n<=X} Λ(n)e(nα) by a sum over n <= δX (the same bound at δX) and by prime powers (O(X^{1/2} log X)). So the shape is the same.
- **[Tao5], display (1.3).** "A typical estimate in the minor arc case": |S(x, α)| ≪ (x/√q + x/√(x/q) + x^{4/5}) log^3 x, with S(x, α) = Σ_{n<=x} Λ(n)e(nα), and "see e.g. [19, Theorem 13.6]" (= Iwaniec-Kowalski). The surrounding text places α = a/q + β with (a, q) = 1 and |β| <= 1/(qQ). Tao does not spell out the exact hypotheses of IK 13.6 there. Note x/√(x/q) = √(xq).
- **[Ex], Lemma 6.** An explicit version "following the proof of IK Theorem 13.6", for α = A/Q exactly, with (A, Q) = 1 and 100 <= x, Q <= x: |Σ_{n<=x} Λ(n)e(αn)| <= 23 (Q^{1/2} x^{1/2} + Q^{-1/2} x + x^{4/5}) (log x)^3. This is that paper's own restatement, not IK's wording.
- Encyclopedia of Mathematics, "Vaughan identity" (**search snippet only**): the same bound with log^4 N, attributed to Vaughan's original article.

### (SW) Siegel-Walfisz

- **[Ah], Theorem 4.3, cited as "[13, Corollary 5.29]",** with [13] = Iwaniec-Kowalski, *Analytic Number Theory*, AMS Colloq. Publ. 53, 2004. Hypotheses: a, q ∈ N, q >= 1, (a, q) = 1, C > 0, q ≪ (log x)^C. Conclusion: ψ(x; q, a) = x/φ(q) + O(x/(log x)^C) for every x >= 2. The implied constant depends only on C. (This is the log-power form, the same C for range and saving. Reported by WebFetch as a paraphrase with short quotes.)
- **[BG], Section 4.1 (character form, no citation).** There is c > 0 such that for every A > 0, uniformly for non-principal χ mod q with q <= (log X)^A, ψ(X, χ) ≪ X e^{-c√(log X)}. The implied constant depends on A and is ineffective.
- **[Ext], introduction, equation (1) (no citation).** π(x; q, a) = π(x)/φ(q) + O_A(x/(log x)^A), uniformly for 2 <= q <= (log x)^A and (a, q) = 1.
- **Davenport, Ch. 22:** **not verified.** A search snippet (Springer TOC of GTM 74) lists the chapter "Siegel's Theorem" (Springer chapter DOI suffix _21) between "The Prime Number Theorem for Arithmetic Progressions (I)" and "(II)". So "(II)" is plausibly Chapter 22, the chapter where the Siegel-Walfisz form is usually quoted from. I did not see the chapter text.

## Relevance (C014, "Depends on")

- **(V): the cited form is confirmed** as to shape (N q^{-1/2} + N^{4/5} + N^{1/2} q^{1/2}) and the (log N)^4 power, by [BG] (for the Λ-sum) and [LZ] (for the prime sum, with the label "Vaughan, The Hardy-Littlewood method, 2nd ed., Theorem 3.1").
  - The theorem number "3.1" rests on one secondary citation, [LZ].
  - IK Thm 13.6 is quoted by [Tao5] with (log x)^3, as C014 recalled.
  - **Hypothesis difference:** both [BG] and [LZ] state a **strict** inequality |α - a/q| < q^{-2}, while C014 writes <=. This is harmless for C014: Step 2 actually produces |α - a/q| < 1/(qQ') <= 1/q^2, which is strict.
- **(SW): the cited form is confirmed in the log-power version** (IK Cor. 5.29 as quoted by [Ah]: q ≪ (log x)^C gives error x (log x)^{-C}). That is exactly the consequence C014 uses ("we use only ... C_{M,K} x (log x)^{-K}"; take C = max(M, K)).
  - The exp(-c√(log x)) form is attested only in character form ([BG], with c absolute, which is stronger than C014's c_M).
  - Davenport Ch. 22 is not verified.
- Since C014 needs only the qualitative forms (Remark R2), **none of the discrepancies found affect C014.**

## Update 2026-11-25 (sixth pass): the books are still unread

**Access.** The allowlist now includes link.springer.com, en.wikipedia.org, terrytao.wordpress.com, mathnet.ru, projecteuclid.org, tsukuba.repo.nii.ac.jp and export.arxiv.org. **All of them still fail DNS** (getaddrinfo ENOTFOUND), also on a retry after a delay. Only arxiv.org resolves. Google Books is not on the list. So **IK, Davenport and Vaughan were NOT read in this pass either.** No exact book statement can be quoted.

**New secondary evidence**
- arXiv:2505.07803v2 ("Log-free bounds on exponential sums over primes"), eq. (1.1), read via WebFetch extraction:
  - S(α; x) ≪ (x/√q + x^{4/5} + √(qx)) (log x)^3 "when α = a/q + O*(1/q^2)". That is the **non-strict** |α - a/q| <= 1/q^2, with O* meaning implied constant 1.
  - A footnote says "Vaughan proves this with a (log x)^4".
  - So the log^3 form is in the literature under a non-strict hypothesis, and the log^4 form is attributed to Vaughan. This is consistent with C014.
- Davenport: the search tool reports a Springer listing in which the chapter with DOI suffix _21 is "Siegel's Theorem". If the suffix equals the chapter number, Ch. 21 = Siegel's theorem, and Ch. 22 = "The Prime Number Theorem for Arithmetic Progressions (II)" is where SW should be. **Snippet only; unverified.**

**Item-by-item comparison with C014 "Depends on"** (against the best available secondary quotes)

| Item | C014's form | Best available quote | Verdict |
|---|---|---|---|
| (SW), the form used | for every M, K: \|ψ(x;q,r) - x/φ(q)\| <= C_{M,K} x (log x)^{-K} for q <= (log x)^M | IK Cor. 5.29 via [Ah]: q ≪ (log x)^C gives O_C(x (log x)^{-C}), x >= 2 | **Matches.** Take C = max(M, K). C014 uses M = B+1 < K = 3B+12, so C = K covers it. |
| (SW), the form stated | O(x exp(-c_M √log x)) | only [BG]'s character form (c absolute) | Stated form unverified against a book. **Not used** by the proof, so no gap. |
| (V) Vaughan | strict \|α - a/q\| < q^{-2}, (log X)^4, C_V absolute | [LZ] Lemma 3 = "Vaughan Thm 3.1"; [BG] Prop 4.1: strict, log^4 | **Matches** (secondary). |
| (V) IK 13.6 | "(log X)^3 there, which is stronger" | Tao (1.3): log^3, hypothesis via \|β\| <= 1/(qQ); 2505.07803: log^3 under non-strict \|α-a/q\| <= q^{-2} (not attributed to IK) | Consistent. IK's exact hypothesis is unverified. **Not used.** |

**No GAP found.** Nothing in C014 is stronger than any form quoted in the secondary literature.

**Pages Matteo would need to upload (literature/private/)**
1. Iwaniec-Kowalski, *Analytic Number Theory* (AMS Colloq. Publ. 53, 2004):
   - §5.9: the pages from Siegel's theorem (Thm 5.28) through Cor. 5.29;
   - §13.5: the page with Theorem 13.6 and its hypotheses.
2. Davenport, *Multiplicative Number Theory*, 3rd ed. (GTM 74): the end of Ch. 22, where the SW statement for ψ(x; q, a) appears, and the chapter titles of Ch. 20-22.
3. Vaughan, *The Hardy-Littlewood Method*, 2nd ed.: Ch. 3, Theorem 3.1 (the statement), and §3.2 (Goldbach exceptional set; the model for C014).

Page numbers are not given because I could not see the books' tables of contents.

## Verified by

Sixth pass (2026-11-25): arXiv:2505.07803 read only via WebFetch extraction. The Davenport chapter numbering comes from a search-result summary. **No book was read.**

Literature agent, 2026-11-25.
- **Read** (page images or HTML text): [LZ] pp. 1-10; [Tao5] pp. 2-3.
- **Read via WebFetch extraction** (the tool paraphrases; the quotes are short): [BG] Sections 4.1-4.3 and the bibliography; [Ah] Section 4.2; [Ex] Lemma 6; [Ext] introduction.
- **NOT read:** Vaughan's book, Iwaniec-Kowalski, Davenport. The theorem numbers (Vaughan Thm 3.1, IK Thm 13.6, IK Cor. 5.29) are confirmed only through those secondary citations; Davenport Ch. 22 is not confirmed at all. A human with the books should do a final check.

## Update 2026-11-25 (main session): Siegel-Walfisz read from Wikipedia

**Verified by:** the main session read the Statement section of https://en.wikipedia.org/wiki/Siegel%E2%80%93Walfisz_theorem (revision oldid=1321322946, via curl and action=raw). Quoted:

> given any real number N there exists a positive constant C_N depending only on N such that ψ(x;q,a) = x/φ(q) + O(x exp(-C_N (log x)^{1/2})), whenever (a, q) = 1 and q ≤ (log x)^N. The constant C_N is not effectively computable because Siegel's theorem is ineffective.

- **Comparison.** This matches C014's (SW) **word for word**: the same uniformity range q ≤ (log x)^M, the same error, and the same ineffectivity. The log-power consequence that C014 uses follows at once. No gap.
- **Still not read:** the textbook sources (IK Cor. 5.29, Davenport Ch. 22) and Vinogradov (Vaughan Thm 3.1).
- **Mikawa 1991 (projecteuclid):** curl gets an anti-bot page instead of the PDF.
