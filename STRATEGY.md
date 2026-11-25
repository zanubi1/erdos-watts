# Strategy

_Last updated: 2026-11-25 (session 2: skeptic pass on L003-L005, literature pass, overshoot experiment, L006 proved and reviewed). The dates "2026-11-25" in the setup entries are a typo for the setup day; they come before this session._

## Goal

Prove that the Watts greedy sequence a(n) (OEIS A055265) is a permutation of N. Failing that, get a substantial conditional or partial result.

## What we know so far

**Proven** (`lemmas/proven/`). L003-L009 and L011 were promoted on 2026-11-25, after skeptic passes plus a main-session review with Matteo's delegated OK. They were formerly C003-C009 and C011.

- **L001**: consecutive terms alternate in parity, so a(k) ≡ k (mod 2). Trivial.
- **L002**: the sequence is well defined. Trivial.
- **L003**: if m is the smallest missing value, then a(n) + m is composite for all n >= N0.
- **L004**: if the missing set M is nonempty, then |M ∩ [1, X]| >> X / log X. In particular, M finite implies M empty.
- **L005**: if a(n) <= n + o(n / log n), then M = ∅.
- **L006** (step formula): a(n+1) = q_{b+1} - a(n), with q_i the primes >= a(n) + u*(n) and b <= O*(n). Also O*(n) = (n+1-u*(n))/2. Its prover Remarks are unreviewed and live in `attempts/2026-11-24-c006-remarks.md`.
- **L007** (hole step bound): a(n+1) - (n+1) <= (the length from a(n)+n+1 needed to see H_π(n)+1 primes).
- **L008**: H(X) = #{ k <= X : a(k) > X }, and H(X) <= D + S(X)/D. Criterion (ii) is superseded by L011.
- **L009** (payers): for a hole v at time n, π(n+v) - π(2v) <= H(v) + H_{1-ε}(n). This is the sharp form L009', and it is attained. Needs a(1) odd.
  - Corollary: if H <= h up to time n, then every hole v at time n has n - v < ℓ_{2h+1}(2v).
- **L011** (unconditional criterion): if some v is missing, then H(n) >= (1 - o(1)) n / log n. So **liminf H(n) log n / n < 1 implies the permutation property**. Needs only L009 and the PNT.

**Open** (`lemmas/candidates/`):
- **C010** (conjecture): a uniform bound on the number of primes a hole survives, K(v) := π(fi(v)-1+v) - π(2v) <= K0, or <= C log v. Either implies the permutation property.
  - Data: max K is 8 up to 10^7 and **11 up to 10^8**. The per-decade maxima 6, 7, 8, 8, 11 fit about 2 + 1.1 log10 v, so **C log v is the realistic target**.

**Reductions now available** (all proven). Any one of these proves the conjecture:
1. a(n) <= n + o(n / log n) (L005);
2. H(n) <= (1 - δ) n / log n for infinitely many n (L011);
3. C010 in any uniform form.

Literature status:
- **L003/L004 are a known technique.** The same "smallest missing value forces p - m to be missing" mechanism is in the Devlin-Artamonov proof outline in OEIS A253074 (the variant where adjacent sums must be non-prime). Cite it, together with the EKG "smallest missing" argument, and do not claim novelty.
- **L005 was not found in any source.** It is a routine counting step: call it "not found", not "new".

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

| N | max a(n) - n (upper, what L005 needs) | max n - a(n) (lower) = max overshoot | smallest value not yet seen |
|---|---|---|---|
| 10^6 | 156 | 150 | 999,949 |
| 10^7 | **188** (n = 8,525,842) | 200 (n = 8,526,046) | 9,999,963 |

The earlier "max |a(n)-n| = 200" was the *lower* displacement. Both quantities are about 0.7-0.8 (ln n)^2. See `experiments/results/overshoot_1e7/summary.md`.

### Findings of the overshoot experiment

1. **Overshoot is lower displacement.**
   - Exact identity: O(n) = n + 1 - u(n), where u(n) is the smallest unused value.
   - Exact relation: max O = max (n - a(n)).
   - **Warning:** O(n) = o(n) already *is* the permutation property. "Bound the overshoot" is not a weaker subgoal. The upper bound in L005 is the genuinely weaker target.
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

By L005, it is enough to prove a(n) <= n + o(n / log n). The data says the truth is about (log n)^2.

The bottleneck is the circularity between the two displacements:
- upper displacement <= (prime-counting length) + overshoot, by the step formula;
- overshoot = lower displacement.

To break it:

_Update 2026-11-25: route 1 is now made precise by L009-L011. A uniform bound on the number of primes a hole survives (C010) suffices, and so does H(n) < (1-δ) n/log n infinitely often (L011). See "Open questions" for the current target. Routes 1-3 below are kept for history; item 3 is done (L006)._

1. **Wait-time lemma.** If m is overtaken at step n (the running max passes m), then m is used within W(n) steps, for some W(n) = o(n / log n).
   - **Plausible route:** the reflection lock. While the sums sit on a prime q, the partner q - m of each left-behind m is reached in order.
   - **Data:** the maximum wait is 309 for m < 10^7.
   - **Consequence:** a wait bound gives O(n) = o(n / log n), which directly gives M = ∅ and bypasses L005. It is therefore the whole problem; look for a version that needs only an *averaged* or *density* bound, and combine it with L004.
2. **Density route (combine L004 with averages).**
   - L004 needs |M ∩ [1, X]| >> X / log X if M is nonempty.
   - So it suffices to show that, for infinitely many X, all but o(X / log X) values <= X appear before step X + o(X).
   - This needs averaged control only, not a pointwise bound. It may be reachable with Brun-Titchmarsh or Selberg sieve upper bounds on primes in short intervals, plus a counting argument on blocked primes (mean 0.79 per step in the data).
3. **Step-formula lemma.** Write up item 4 above as candidate L006 and send it through the experimenter -> skeptic loop. It is elementary and is needed by both routes.

## Secondary lines

- **Weaker unconditional statements:**
  - Does every even number appear?
  - Are there infinitely many fixed points?
  - Are there infinitely many n in A070942 (the first n terms are exactly 1..n)? That would imply the permutation property.
- **Conditional results:** under Cramér-type gap bounds, or Hardy-Littlewood, does the displacement bound follow?
- **Formalization:** a Lean statement of the greedy variant, plus L001/L002/L003-L005, as a contribution to formal-conjectures.

## Open questions for the next session

- [x] Skeptic pass on L003, L004, L005 (2026-11-24): all PASS, with L004 and L005 conditional on their predecessors.
- [x] L003-L009 and L011 promoted to proven (2026-11-25).
- [x] Literature pass (2026-11-24): see "Literature" above.
- [ ] Still unread: erdosproblems.com/473 page and forum, Hasler's wiki page, the EKG paper (arXiv:math/0204011). The hosts are blocked by DNS; read them manually or from a different environment.
- [x] Overshoot experiment (2026-11-24): `experiments/results/overshoot_1e7/`.
- [ ] Fix `experiments/results/run_1e7/summary.md` (and `run_1e6`): relabel "max |a(n)-n|" as the lower displacement and add the upper one.
- [x] L006 (step formula): proved, skeptic PASS (2026-11-25). Awaiting Matteo.
- [x] L007/L008 created from L006 Remarks R3a/R3b; skeptic PASS (2026-11-25), L008 (ii) conditional on L003/L004. Awaiting Matteo.
- [x] Hole-dynamics experiment (2026-11-25): `experiments/results/holes_dynamics_1e7/`. There is no restoring drift. Lifetimes are governed by a prime count (L009). Pair and prime-sum-free ideas are dead.
- [x] L009 (with L009') and L011: proved, skeptic PASS (2026-11-25). Awaiting Matteo.
- [x] 10^8 run (2026-11-25): `experiments/results/k_survival_1e8/`. Max K = 11, so K0 = 8 fails. Max H = 75. All eight OEIS displacement records match.
- [ ] **Next target:** a uniform bound on the prime partners of a hole. For every hole v at time n, show #Late(v,n) + #Ahead(v) <= C log v, where:
  - Late(v,n) is the partners w = q - v still unused at time n;
  - Ahead(v) is the partners used before time v.

  With L009 this gives C010 in its C log v form, and hence the permutation property. It needs arithmetic input: the hole set (a dense set of about 50 values in [n-86, n], reflection-locked around a prime) must meet the shifted primes {q - v} in O(log v) elements. Counting payers alone is tight (L009' equality) and cannot do it. The data shows that worst cases are prime-dense windows, not large gaps. See `attempts/2026-11-25-c010-bounded-prime-survival.md` for what died: iterating L009 on partners, window counting (coefficient 2 > 1), and bootstrapping H against K.
- [ ] Secondary: since L011 needs only H(n) < (1-δ) n/log n infinitely often, look for *any* sublinear bound on H. Even H(n) = O(n / log n) with a small constant would be enough.
- [ ] The R1 citation (quantitative Baker-Harman-Pintz) is marked GAP?: its source PDF was unreachable from this session.
- [ ] By-product claim a(n) = O(n log n) unconditionally: sketch only, needs its own candidate file and review.
