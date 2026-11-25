# Search log: is the C013 cascade (or any proof that A055265 is a permutation) already known?

Date: 2026-11-25. Literature agent, fifth pass of the day. Targeted novelty check for C013 ((a) blocking lemma in union form, (c) second-generation cascade, (d) reduction to the binary hypothesis (G)) and, by extension, for the combination C013 + C014.

## Citation/link

Sources consulted in this pass (all URLs as fetched):
- arXiv listing search, https://arxiv.org/search/ (titles/abstracts/comments only, not full text). Queries and result counts are listed below.
- export.arxiv.org API: **failed DNS** (not reachable from this session). So there was no API query; the listing search was used instead.
- OEIS raw files via the mirror https://raw.githubusercontent.com/oeis/oeisdata/main/seq/: A055265 (rev. #119, Nov 03 2026), A051237 (rev. #42, Feb 16 2025), A128280 (rev. #27, Jul 19 2021), A055266, A253074, A088643, A076990, A243625, A070942, A073659, A057063.
- M. F. Hasler, "Prime sums from neighboring terms", OEIS wiki, https://oeis.org/wiki/User:M._F._Hasler/Prime_sums_from_neighboring_terms (oeis.org was reachable this time).
- erdosproblems: https://www.erdosproblems.com/forum/thread/473 and https://erdosproblems.com/forum/thread/473 both returned **HTTP 403**. Forum user pages also returned 403. The status was read from teorth/erdosproblems `data/problems.yaml`.
- google-deepmind/formal-conjectures: issue #748 and PR #6099 (merged Sep 18 2026), read on github.com.
- J. C. Lagarias, E. M. Rains, N. J. A. Sloane, "The EKG sequence", Experiment. Math. 11 (2002), arXiv:math/0204011. **PDF pp. 3-6 read** (Section 2, Lemmas 1-4, Theorem 1).
- P. Hofman, M. Pilipczuk, "A few new facts about the EKG sequence", J. Integer Seq. 11 (2008), Article 08.4.2. **Search snippets only**; cs.uwaterloo.ca fails DNS.
- A. Floros, "A note on the Slater-Vélez permutation", arXiv:2610.15860 (abstract only).
- MathOverflow / math.stackexchange: direct fetch **blocked** ("unable to fetch"). Only web-search snippets were used.

## What it says / findings

### 1. arXiv (listing search; titles/abstracts only)

| Query | Results | Relevant |
|---|---|---|
| "lexicographically earliest" permutation | 1 | Sloane 1805.10343 (already noted) |
| greedy permutation prime sum | 1 | none (automata paper) |
| prime sums consecutive terms permutation | 1 | none |
| "permutation of the natural numbers" prime | 1 | EKG paper |
| EKG sequence permutation | 2 | EKG, Sloane |
| Yellowstone permutation | 2 | Yellowstone 1501.01669, Sloane |
| Erdős problem 473 | 0 | - |
| greedy sequence Goldbach | 0 | - |
| Hofman Pilipczuk | 1 | none (EKG paper not on arXiv) |

The arXiv search does not cover full text, so these counts do not exclude a paper that mentions A055265 only in its body.

### 2. OEIS

- **A055265** (rev. #119): no proof, no conditional result. The comments still ask "Does every positive integer eventually occur?" (Kamenetsky 2009), with Wilson's probabilistic "almost certainly yes".
- **A051237** (rev. #42): limit of rows = A055265, stated without proof. Greathouse (2011): assuming Dickson / Hardy-Littlewood B, no backtracking is needed in the pyramid. Conditional, and about the pyramid, not about the permutation property.
- **A128280** (a(0)=0 / a(1)=2 variant; rev. #27): "may be" a rearrangement; for a(0)=0 it is a conjecture. Hasler 2020 formula: a(2n-1) = A055265(2n-1)+1, a(2n) = A055265(2n)-1. So **A128280 is a permutation iff A055265 is**, and C013 covers it automatically. No proof is given.
- **Variants with another a(1):** the web search found no other OEIS entry of the form "smallest unused, sum with previous term prime" with a(1) >= 3. I could not run a full-text grep of the oeisdata mirror (no code-search tool in this session), so **this is "not found", not "does not exist"**.
- **A253074 / A055266** (sum never prime): there is a proof outline (Devlin-Artamonov; simplified by Hasler, Nov 25 2019). A missing x forces the multiples k·x, ..., (k+p)·x to all be of the form prime minus something, and a residue argument mod a prime p gives a contradiction. This is **(a) with |S| = 1 plus a congruence argument**. There is no union over a set of missing values, no second generation, and no additive (binary) input. It works because "composite" is a set closed under a congruence obstruction; for "prime" there is no such obstruction.
- **Related greedy rules** A076990 (three-term sums), A243625 (semiprime sums), A088643 (pyramid rows), A073659: conjectures or nothing; no proofs. A057063 has a MathOverflow proof (mathoverflow.net/q/416089) but is a different, non-greedy construction. It is irrelevant.
- **Hasler wiki** (read via WebFetch extraction): surjectivity: "So far we don't have a formal proof for this", plus a k-tuple heuristic. Existence of the next term is "easy" when at most one more prime is required. **No proof for any (M,N) case with N >= 1.**

### 3. erdosproblems.com #473

- The forum thread was **not read** (HTTP 403 on both host forms, and on user pages).
- From search snippets of the problem page and its mirrors: the main question was answered by Odlyzko (no reference). Watts' greedy question is presented as open. van Doorn notes 197 is never a sum a(k)+a(k+1).
- problems.yaml: #473 still `proved` (main question), last update 2025-08-31, `forum: 3 posts`, formalized (2026-09-18).
- formal-conjectures PR #6099 (merged 2026-09-18) formalizes `erdos_473` (solved, linked to an external Lean proof of the main question) and the finite variant (open). **The greedy question/A055265 is not formalized and is not mentioned** (PR and issue #748 read).
- I cannot exclude that one of the 3 forum posts discusses the greedy sequence.

### 4. "Missing value forces many missing values" + additive inputs

- **EKG** (read, Section 2): Lemma 3 says "if infinitely many multiples of p appear then all multiples of p appear" (first missed multiple kp would be chosen after any later multiple lp). Lemma 4 says "all multiples of p appear ⇒ all integers appear". Both are the single-missing-value forcing step, i.e. (a) with S = {m0}. The input is purely multiplicative (gcd); there is no sum over a set of missing values and no additive input. Section 8 (generalizations) concerns gcd-restricted sequences (not re-read this pass).
- **Yellowstone** (earlier note, pp. 2-5): single smallest-missing forcing; nothing additive.
- **Hofman-Pilipczuk 2008** (snippets only): proves the LRS conjecture that p is preceded by 2p and followed by 3p; nothing additive as far as snippets show. **Not read.**
- **Slater-Vélez / Floros 2026** (abstract only): greedy difference-permutation; no primes in the abstract.
- **Web searches** ("smallest missing/unused" + Goldbach; Chen's theorem + greedy permutation; MO/MSE "sum is prime" + "every integer appears"): nothing that uses a Goldbach/Chen/Lavrik-type binary theorem to prove that a greedy sequence is a permutation.

### Conclusion

**Not found:**
- the union form of the blocking lemma ("a set S of never-occurring values blocks at most max S - 1 steps, independent of |S|");
- the second-generation cascade (c);
- a reduction of Watts' question to an almost-all binary statement like (G);
- any proof (conditional or unconditional) that A055265, A128280 or any prime-sum greedy variant is a permutation.

The closest prior art is the single-value forcing step in EKG Lemmas 3-4, Yellowstone Thm 1, and Devlin-Artamonov/Hasler in A253074. It must be cited for (a) with |S| = 1.

**Caveats:**
- This is "I found no prior work", not "there is no prior work".
- Unread: the erdosproblems forum (3 posts), MO/MSE pages themselves, arXiv full text, Hofman-Pilipczuk, Guy UPINT C1 and Erdős-Graham 1980.
- (a) is a two-line pigeonhole and may well be folklore.

## Relevance

- C013 (a), (c), (d): no prior source found. If C013 + C014 survive expert review, the result would appear to be new. An external check (MathOverflow and/or an analytic number theorist) is the right next step before any claim.
- C013 R5: cite EKG Lemmas 3-4 and A253074 for the |S| = 1 case.
- A128280 is equivalent to A055265 (Hasler's formula), so the same argument settles both.

## Verified by

Literature agent, 2026-11-25.
- **Read (actual source):** EKG arXiv PDF pp. 3-6; raw OEIS files A055265, A051237, A128280, A055266, A253074, A088643, A076990, A243625, A070942, A073659, A057063 (via WebFetch extraction, so paraphrased, not seen byte-for-byte); Hasler OEIS wiki (WebFetch extraction); formal-conjectures issue #748 and PR #6099; problems.yaml entry #473; arXiv listing-search result pages.
- **Abstract only:** Floros 2610.15860.
- **Snippets only:** the erdosproblems #473 page and forum, Hofman-Pilipczuk, MathOverflow/MSE.
- **Not accessible:** export.arxiv.org (DNS); erdosproblems forum (403); mathoverflow.net and math.stackexchange.com (blocked); cs.uwaterloo.ca (DNS).
