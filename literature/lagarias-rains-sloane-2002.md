# Lagarias, Rains, Sloane, "The EKG sequence" (2002)

## Citation/link

J. C. Lagarias, E. M. Rains, N. J. A. Sloane, "The EKG sequence", Experimental Mathematics 11(3) (2002), 437-446. arXiv:math/0204011 (v1, 31 Mar 2002). The Yellowstone paper now has its own note: [applegate-et-al-2015-yellowstone.md](applegate-et-al-2015-yellowstone.md).

## What it says (read 2026-11-25, arXiv PDF pp. 1-13)

- Definition: a(1)=1, a(2)=2, and a(n) is the least unused number with gcd(a(n-1), a(n)) > 1.
- **Section 2: "controlling primes".** If p | a(n-1) and a(n) is the smallest unused multiple of p, then p is a *controlling prime* for a(n). B_p(n) is the smallest multiple of p not in {a(1..n-1)}, so a(n) = min{B_p(n) : p | a(n-1)}.
  - Lemma 1: when a prime p > 2 first divides a term, a(n) = qp, then a(n+1) = p. New primes appear in increasing order.
  - Lemma 3: if infinitely many multiples of p appear, all do. Proof: take the first missed multiple kp, and a late a(n) = lp. Then a(n+1) = kp, "because ... all smaller possible values which are ever going to appear in the sequence have already appeared."
  - Lemma 4: the same with the smallest missed integer k in place of kp.
  - Theorem 1: EKG is a permutation.
- **Section 5, Theorem 2: a(n) <= 14n.** Proof by a "window" W of multiples of the controlling prime, plus counting of entry and exit points (P1-P4) and an inclusion-exclusion sieve over the controlling primes. The remark compares it to Hooley 1976.
- **Section 6, Theorem 3: a(n) >= n/260.**
  - Lemma 6: if a(n) = kp, then k has appeared by time n+1.
  - **Lemma 7:** if at least 4k even numbers occur in {a(1..n)}, then {1..k} ⊆ {a(1..n+1)}. Proof (paraphrase): let 2m be the largest missing even number <= 2k. Then every even a(i) > 2m with i <= n is followed by a(i+1) <= 2k, "since 2m is always available". There are at least 2k even terms > 2k, each followed by a distinct value <= 2k. That is more values than exist, a contradiction.
- Conjectures (asymptotics, a(n) ~ n(1 + 1/(3 log n)), and so on) remain open.

## Relevance

- **L003/L004**: Lemmas 3-4 are the "smallest missing value is always an admissible candidate" mechanism. Cite them, together with A253074.
- **L009 case 2 ("steals")**: EKG Lemma 7 is the same **charging argument**. Each time a term is an admissible partner of a missing value, the next term is forced to be no larger than that value. Distinct times give distinct small values, so the number of partner occurrences is bounded by the number of available smaller values.
  - L009 refines this in two ways. It charges to the *smaller holes* B(v) rather than to all values <= v. It also adds cases 1, 3 and 4, which count partners never used while v is missing.
  - The charging step itself is prior art (LRS 2002, Lemma 7) and should be cited. I did not see the full four-way partition, or any bound of the form "number of admissible partners while missing <= number of payers", stated as such.
- **Lifetime bounds**: Theorems 2-3 are linear bounds proved by sieving. They are not bounds on (first occurrence of n) - n. The density of the admissible relation is positive in EKG and 1/log in our case, so the sieve does not transfer directly.

## Verified by

Literature agent, 2026-11-25: **read** the arXiv PDF of math/0204011v1, pages 1-6 and 9-13 (Sections 1-3, 5, 6 and the start of 7). Pages 7-8 (heuristics) and 14+ (generalizations, Section 8) were not read. On 2026-11-25 arxiv.org was reachable through the WebFetch tool, although earlier passes failed DNS. The 2026-11-24 "summaries only" version of this note is superseded.
