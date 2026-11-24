# Strategy

_Last updated: 2026-11-24 (session 2: skeptic pass on C003-C005, literature pass, overshoot experiment). The dates "2026-11-25" in the setup entries are a typo for the setup day; they come before this session._

## Goal

Prove that the Watts greedy sequence a(n) (OEIS A055265) is a permutation of N. Failing that, get a substantial conditional or partial result.

## What we know so far

- **L001**: consecutive terms alternate in parity. Trivial, proven.
- **L002**: the sequence is well defined. Trivial, proven.
- **C003**: if m is the smallest value that never appears, then a(n) + m is composite for all n >= N0.
  - Skeptic: **PASS** (2026-11-24). It depends only on L002.
  - Awaiting Matteo.
- **C004**: if the missing set M is nonempty, then |M ∩ [1, X]| >= π(X+m) - π(m+1) - (N0-1) >> X / log X. In particular, M finite implies M empty.
  - Skeptic: **PASS, conditional on C003**.
  - Editorial fix needed: add the line showing the parity hypothesis holds (m >= 2, so p is odd and v = p - m has the opposite parity to m). Also state the "(1 - o(1)) X/log X" as a lower bound.
  - Awaiting Matteo.
- **C005** (reduction): if a(n) <= n + f(n) with f(x) = o(x / log x), then M is empty.
  - Skeptic: **PASS, conditional on C004**.
  - Optional simplifications: "f nondecreasing" can be dropped (replace f by its running max), and "for all n" can be relaxed to "for n >= n0".
  - Awaiting Matteo.

Proof status of the chain: if Matteo accepts C003 -> C004 -> C005, then **an upper displacement bound a(n) <= n + o(n/log n) proves the conjecture.**

Literature status:
- **C003/C004 are a known technique.** The same "smallest missing value forces p - m to be missing" mechanism is in the Devlin-Artamonov proof outline in OEIS A253074 (the variant where adjacent sums must be non-prime). Cite it, together with the EKG "smallest missing" argument, and do not claim novelty.
- **C005 was not found in any source.** It is a routine counting step: call it "not found", not "new".

## Literature (2026-11-24, see `literature/`)

- **Status:** the greedy question is still **open** as far as we can see.
  - OEIS A282695: "There is no proof at present for the conjecture that A055265 is a permutation".
  - The erdosproblems database (teorth/erdosproblems, problems.yaml) marks #473 as "proved", but that refers to the main (non-greedy) question.
- **Formal-conjectures:** `FormalConjectures/ErdosProblems/473.lean` formalizes only the main question (solved, with a linked formal proof using a non-greedy construction) and Segal's finite variant (open). **The greedy variant is not formalized.** A Lean statement of it would be a small, concrete contribution.
- **Displacement data:** no proved bound on displacement exists anywhere.
  - OEIS records A282696/A282697 give the records of |a(n) - n|. They match our runs exactly (156 at n = 678,572; 200 at n = 8,526,046), an independent check of our code.
  - Beyond our data the records reach 316 at n ≈ 1.08e8 and later 394.
- **Correction:** A076990 and A243625 are *not* displacement sequences; they are related greedy sequences.
- **Still unread:** the original erdosproblems.com/473 page and its forum thread (3 posts), Hasler's OEIS wiki page, and the EKG paper. The erdosproblems.com, oeis.org and arxiv.org hosts still fail DNS lookup from the session even after the allowlist change, so a human may need to read these.

## Data (experiments/results)

| N | max a(n) - n (upper, what C005 needs) | max n - a(n) (lower) = max overshoot | smallest value not yet seen |
|---|---|---|---|
| 10^6 | 156 | 150 | 999,949 |
| 10^7 | **188** (n = 8,525,842) | 200 (n = 8,526,046) | 9,999,963 |

The earlier "max |a(n)-n| = 200" was the *lower* displacement. Both quantities are about 0.7-0.8 (ln n)^2. See `experiments/results/overshoot_1e7/summary.md`.

### Findings of the overshoot experiment

1. **Overshoot is lower displacement.**
   - Exact identity: O(n) = n + 1 - u(n), where u(n) is the smallest unused value.
   - Exact relation: max O = max (n - a(n)).
   - **Warning:** O(n) = o(n) already *is* the permutation property. "Bound the overshoot" is not a weaker subgoal. The upper bound in C005 is the genuinely weaker target.
2. **Worst spots sit at large prime gaps near 2n, not near n.**
   - Six of the nine upper-displacement records after 10^5 sit exactly on a maximal prime gap at 2n. Example: the 188 sits at the record gap 180 after 17,051,707.
   - Top events are at the 99th percentile of local gap size against a random control.
3. **Mechanism (observed, not proven): the reflection lock.**
   - Inside a gap (p, q) near 2n, the sums lock onto q (and q + 12), and the sequence follows x ↦ q - x for about the length of the gap.
   - The upper excursion is about q - 2n.
   - A left-behind value m is picked up when its partner q - m comes up, a delay of about q - 2m.
4. **Step formula (exact, elementary).** a(n+1) = u_par(n) + (P_{k+b} - t_n), where:
   - t_n = a(n) + u_par(n);
   - P_k is the first prime >= t_n;
   - b is the number of blocked primes, and b <= O_par(n).

   Hence a(n+1) - (n+1) <= 1 + (length needed, starting at t_n, to see O_par(n)+1 primes). On its own this is circular: it bounds the upper displacement in terms of the overshoot.
5. **Exact link between the two displacements:** Dup(n+1) = (s_n - 2n - 1) + Dlo(n), where s_n = a(n) + a(n+1).

## Main line of attack

By C005, it is enough to prove a(n) <= n + o(n / log n). The data says the truth is about (log n)^2.

The bottleneck is the circularity between the two displacements:
- upper displacement <= (prime-counting length) + overshoot, by the step formula;
- overshoot = lower displacement.

To break it:

1. **Wait-time lemma (next target).** If m is overtaken at step n (the running max passes m), then m is used within W(n) steps, for some W(n) = o(n / log n).
   - **Plausible route:** the reflection lock. While the sums sit on a prime q, the partner q - m of each left-behind m is reached in order.
   - **Data:** the maximum wait is 309 for m < 10^7.
   - **Consequence:** a wait bound gives O(n) = o(n / log n), which directly gives M = ∅ and bypasses C005. It is therefore the whole problem; look for a version that needs only an *averaged* or *density* bound, and combine it with C004.
2. **Density route (combine C004 with averages).**
   - C004 needs |M ∩ [1, X]| >> X / log X if M is nonempty.
   - So it suffices to show that, for infinitely many X, all but o(X / log X) values <= X appear before step X + o(X).
   - This needs averaged control only, not a pointwise bound. It may be reachable with Brun-Titchmarsh or Selberg sieve upper bounds on primes in short intervals, plus a counting argument on blocked primes (mean 0.79 per step in the data).
3. **Step-formula lemma.** Write up item 4 above as candidate C006 and send it through the experimenter -> skeptic loop. It is elementary and is needed by both routes.

## Secondary lines

- **Weaker unconditional statements:**
  - Does every even number appear?
  - Are there infinitely many fixed points?
  - Are there infinitely many n in A070942 (the first n terms are exactly 1..n)? That would imply the permutation property.
- **Conditional results:** under Cramér-type gap bounds, or Hardy-Littlewood, does the displacement bound follow?
- **Formalization:** a Lean statement of the greedy variant, plus L001/L002/C003-C005, as a contribution to formal-conjectures.

## Open questions for the next session

- [x] Skeptic pass on C003, C004, C005 (2026-11-24): all PASS, with C004 and C005 conditional on their predecessors.
- [ ] Matteo: review C003-C005; on OK, apply the editorial fixes from the review logs and move them to `lemmas/proven/`.
- [x] Literature pass (2026-11-24): see "Literature" above.
- [ ] Still unread: erdosproblems.com/473 page and forum, Hasler's wiki page, the EKG paper (arXiv:math/0204011). The hosts are blocked by DNS; read them manually or from a different environment.
- [x] Overshoot experiment (2026-11-24): `experiments/results/overshoot_1e7/`.
- [ ] Fix `experiments/results/run_1e7/summary.md` (and `run_1e6`): relabel "max |a(n)-n|" as the lower displacement and add the upper one.
- [ ] Write candidate C006 (step formula) and state a precise density-version target for route 2.
