# Erdős Problem #473

**Link:** https://www.erdosproblems.com/473 (source: Erdős-Graham 1980 [ErGr80], problem attributed to Segal). Forum thread: https://www.erdosproblems.com/forum/thread/473

## What it says (paraphrase)

- Main question: is there a permutation a(1), a(2), ... of the positive integers with a(k) + a(k+1) always prime? Status: **solved, yes** (Odlyzko; no reference given on the page).
- Watts suggested the greedy construction a(1) = 1, a(n+1) = least unused x with a(n) + x prime, and asked whether every positive integer occurs, and whether every prime occurs as a sum.
- van Doorn (comments): not every prime occurs as a sum - 197 never does. A search snippet of the forum thread additionally says a commenter noted that 199 does not occur as a sum either (snippet only, author not identified, not verified).
- Segal's finite version: for every n >= 2, is there a permutation of {1..n} with adjacent sums prime? Likely yes on probabilistic grounds; known for infinitely many n (MathOverflow 241569).
- As far as we could see (mirror + search snippets), **the greedy question "does every positive integer occur?" is still open**; no proof, disproof or partial result is reported.

## Warning about one search snippet

On 2026-11-24 a web-search summary of the forum thread claimed "no integer ≡ 1 (mod 3) is ever in the sequence ... resolved up to a finite check". This is **false for A055265** (1, 4, 7 are among the first terms: 1, 2, 3, 4, 7, ...) and is almost certainly the search summarizer mixing in another problem. Do not cite it.

## Relevance

Defines our target (Watts' greedy question). The page status "solved" refers to the main question, not to the greedy sub-question. Nothing found here bears on C003-C005.

## Verified by

- Setup session (dated 2026-11-25 in the log) read only a **mirror** (primereboot.pages.dev, "last verified January 15, 2026").
- Literature agent, 2026-11-24: tried to fetch the **original page and the forum thread; both failed** (host www.erdosproblems.com is not in this session's allowed network domains, DNS lookup fails). Saw only web-search snippets/summaries of the forum thread (title "473 Discussion Thread"), which agree with the mirror on 197 and add the 199 remark. **The original page and the forum thread have still not been read.** TODO: allow www.erdosproblems.com and re-read, in particular to check for comments newer than January 2026.
