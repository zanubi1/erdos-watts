# Erdős Problem #473

**Link:** https://www.erdosproblems.com/473 (source: Erdős-Graham 1980 [ErGr80], problem attributed to Segal).

## What it says (paraphrase)

- Main question: is there a permutation a(1), a(2), ... of the positive integers with a(k) + a(k+1) always prime? Status: **solved, yes** (Odlyzko; no reference given on the page).
- Watts suggested the greedy construction a(1) = 1, a(n+1) = least unused x with a(n) + x prime, and asked whether every positive integer occurs, and whether every prime occurs as a sum.
- van Doorn (comments): not every prime occurs as a sum - 197 never does.
- Segal's finite version: for every n >= 2, is there a permutation of {1..n} with adjacent sums prime? Likely yes on probabilistic grounds; known for infinitely many n (MathOverflow 241569).

## Relevance

Defines our target (Watts' greedy question). Note the page status "solved" refers to the main question, not to the greedy sub-question.

## Verified by

Setup session 2026-11-25 read only a **mirror** (primereboot.pages.dev, "last verified January 15, 2026") because the original page could not be fetched. **TODO:** read the original page and its forum thread; check whether the greedy question has since been resolved.
