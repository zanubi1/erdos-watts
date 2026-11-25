# Search log: L006 (step formula, frontier + overshoot bound)

## Citation/link

No source found that states L006. Sources checked (2026-11-24):

- OEIS A055265, A282695, A282696, A086527, A128280: raw files read via https://raw.githubusercontent.com/oeis/oeisdata/main/seq/ .
- Web searches (several phrasings) for greedy "least unused x with a(n)+x prime" sequences with displacement bounds via primes in short intervals; for the EKG paper's Section 2; for MathOverflow / Math StackExchange threads on A055265.
- Lagarias-Rains-Sloane, "The EKG sequence" (Exp. Math. 11 (2002) 437-446, arXiv:math/0204011) and Applegate et al., "The Yellowstone permutation" (JIS 18 (2015), arXiv:1501.01669): **could not be read**. arxiv.org, emis.univie.ac.at and cs.uwaterloo.ca all fail DNS in this session.

## What it says

- A055265 / A282695 / A282696 / A086527 / A128280: no comment or formula about which prime is chosen at each step, about the smallest missing value (frontier), or about a bound on a(n) - n. A282695 only says the deviations are "remarkably small" and that there is no proof the sequence is a permutation. A086527 gives only a(n)+a(n+1) as a formula and lists primes that never occur (197, 199, 317, ...).
- The search results gave the EKG paper's headline results (permutation, and c1 n <= a(n) <= c2 n), but not the proof text. I cannot say whether the EKG linear-bound proof uses a "smallest missing value + count of blocked candidates" argument.
- Hasler's OEIS wiki page and the A329xxx family (snippets only) talk about existence and greedy failures. No displacement bound was seen.
- An arXiv paper on a related sequence (arXiv:2509.00236, seen only as a search snippet) says proving that every number appears "may be difficult because it involves the gaps between the primes". That is a heuristic remark, not a bound.

## Relevance

For L006 the result is **not found**, which is not the same as new. Part (a) follows directly from the greedy rule: the candidates of the right parity below a(n+1) are exactly the values q_i - a(n) for primes q_i < a(n)+a(n+1), and each of them must be used. Parts (b) and (c) are elementary consequences. Anyone who has worked on this sequence probably knows this, so treat it as folklore or elementary. Do not claim novelty. If the EKG/Yellowstone proofs become readable, check whether their upper bounds use the same "frontier + blocked candidates" counting. In EKG the analogue is "a(n+1) <= the k-th admissible candidate after the frontier".

## Verified by

Literature agent, 2026-11-24. I read the raw OEIS files listed above through the GitHub mirror. Everything else comes from search-engine snippets only. The EKG and Yellowstone papers were NOT read because their hosts were unreachable. To read them, allow arxiv.org or emis.univie.ac.at or cs.uwaterloo.ca.
