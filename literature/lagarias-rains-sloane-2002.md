# Lagarias, Rains, Sloane, "The EKG sequence" (2002)

## Citation/link

J. C. Lagarias, E. M. Rains, N. J. A. Sloane, "The EKG sequence", Experimental Mathematics 11(3) (2002), 437-446. arXiv:math/0204011. Related: Applegate, Havermann, Selcoe, Shevelev, Sloane, Zumkeller, "The Yellowstone permutation", arXiv:1501.01669 (J. Integer Seq. 18 (2015)), same style of proof (not read).

## What it says (from search summaries only)

- EKG: a(1)=1, a(2)=2, a(n) = least unused number sharing a factor with a(n-1). Section 2 proves it is a permutation.
- Proof outline (as summarized): (i) if infinitely many multiples of a prime p appear then all multiples of p appear (take the smallest missing multiple kp; it would be a smaller admissible candidate at some later step); (ii) infinitely many distinct primes divide terms, or else some prime recurs infinitely often; (iii) the smallest missing number k leads to a contradiction via a later term that is a multiple of a suitable prime.
- Separate linear bounds on a(n) use sieve ideas.

## Relevance

Model for C003/C004: the "smallest missing value is an admissible candidate at every late step, so late terms must avoid a structured set" step (EKG Lemma 2.3 style). The key difference: in EKG the admissibility relation (sharing a factor with a fixed prime p) is periodic and has positive density, so the forced avoidance gives a contradiction; for prime sums the admissible set {p - m} has density 1/log, which is why we only get C004's X/log X lower bound for |M ∩ [1,X]| and need a displacement bound (C005) to close. I did not see a C005-type counting reduction in the summaries.

## Verified by

Literature agent, 2026-11-24: **not read**. In the second pass, arxiv.org (abs and pdf) still failed DNS, including on retry. Only search-engine summaries seen. TODO: read Section 2 of arXiv:math/0204011.
