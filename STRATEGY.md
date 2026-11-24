# Strategy

_Last updated: 2026-11-25 (setup)._

## Goal

Prove that the Watts greedy sequence a(n) (OEIS A055265) is a permutation of N. Failing that: a substantial conditional or partial result.

## What we know so far

- **L001** consecutive terms alternate in parity (trivial, proven).
- **L002** the sequence is well defined (trivial, proven).
- **C003** (draft proof) if m is the smallest value that never appears, then from some point on, a(n) + m is composite for every term a(n) of parity opposite to m.
- **C004** (draft proof) the set M of missing values is either empty or contains all but finitely many numbers of the form p - m (p prime, m = min M). In particular, |M ∩ [1, X]| >= (1 - o(1)) X / log X if M is nonempty.
- **C005** (draft proof) **reduction:** if a(n) <= n + f(n) with f nondecreasing and f(x) = o(x / log x), then M is empty, i.e. the sequence is a permutation.

C003-C005 need a skeptic pass and a literature check. They may well be folklore.

## Data (experiments/results)

| N | max a(n) | max abs(a(n) - n) | smallest value not yet seen |
|---|---|---|---|
| 10^6 | 1,000,018 | 156 | 999,949 |
| 10^7 | 10,000,013 | 200 | 9,999,963 |

The displacement grows very slowly (consistent with ~ (log n)^2, i.e. prime-gap scale). Every m below the frontier appears within ~200 steps of index m.

## Main line of attack

By C005, it is enough to prove the **upper displacement bound**

    a(n) <= n + o(n / log n).

The data suggests the truth is far stronger (about (log n)^2), so there is a lot of room. Ideas to explore:

1. **Frontier dynamics.** Let u_e(n), u_o(n) be the smallest unused even/odd numbers after n steps. Show a(n+1) cannot jump far above the frontier: after a(n), among the unused numbers of the right parity just above the frontier, some x makes a(n) + x prime. The issue is that "used" numbers above the frontier block candidates. Bound the number of used values above the frontier (call it the overshoot) and show it can't build up.
2. **Potential function.** Find a quantity (e.g. overshoot, or max(a(1..n)) - n) that grows by at most O(prime gap) per "excursion" and is forced back down.
3. **Compare with EKG.** Lagarias-Rains-Sloane's proof that the EKG sequence is a permutation uses "if p appears then multiples follow" control. Look for an analogue: once the frontier is passed, terms are pulled back.

## Secondary lines

- Weaker unconditional statements: every even number appears? Infinitely many fixed points? Every m <= 10^7 appears (computational, done).
- Conditional results: under Cramér-type prime gap bounds, or Hardy-Littlewood, does the displacement bound follow?

## Open questions for the next session

- [ ] Skeptic pass on C003, C004, C005.
- [ ] Literature agent: is C005 (or the "missing set is empty or large" trick) known? Check OEIS wiki (Hasler, "Prime sums from neighboring terms"), MathOverflow, the erdosproblems.com forum thread for #473, Google DeepMind formal-conjectures (is #473 formalized?).
- [x] Literature pass 2026-11-24 (partial, network-limited): nothing found showing the greedy question resolved; no proved displacement bound seen. The C003/C004 trick looks like a known technique (cf. Devlin-Artamonov outline in OEIS A253074, EKG Lemma 2.3) - cite it, do not claim novelty. C005 not seen, but it is a routine counting step. **Still TODO:** allow www.erdosproblems.com, oeis.org, github.com, arxiv.org and re-read the originals (see literature/README.md).
- [ ] Experimenter: track the overshoot (number of used values above the smallest unused value) over time; correlate the worst displacement spots (e.g. n ≈ 8,526,046) with large prime gaps.
