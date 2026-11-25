# Search log for C009 (hole prime count / payers) and C010 (bounded prime survival)

## Citation/link

This is a search log, not a single source. Sources are linked in the notes listed below.

## What it says (search on 2026-11-25)

**Question 1.** Is the C009 argument known? The argument: a value v that is still unused at time n has at most "payers" many prime partners q = v + w in (2v, n+v]. The payers are opposite-parity values that were used early, steals forced onto smaller holes, a(n) itself, and opposite-parity holes.

- **Partly known.** The "steal" case (case 2) is the charging argument of **EKG Lemma 7** (Lagarias-Rains-Sloane 2002). There, each admissible partner of the missing value forces the next term to be <= that value. Distinct times then give distinct small values. The special case B(v) = 0 (v is the smallest hole) is the classical "smallest missing value is forced" step: EKG Lemmas 3-4, Yellowstone Theorem 1(vi), and A253074 (Devlin-Artamonov).
- **Not found:** the four-way partition of prime partners (ahead / steal / a(n) / late), its use of the C007 parity count for "ahead" values, and the resulting inequality π(n+v) - π(2v) <= 1 + B(v) + H(v-1) + H(n). I did not find these in any source read.

**Question 2.** Is the C010 conjecture (a hole survives only boundedly many primes), or any lifetime bound on A117922(n) - n, known?

- **Not found.** No proved bound on A117922(n) - n, or on |A055265(n) - n|, appears in A055265, A117922, A117925, A086527, A282695-A282697, A282700, A128280 or A051237. The same holds for Sloane 2018 (which calls the problem possibly "beyond reach" because of prime gaps) and for the EKG and Yellowstone papers, whose bounds are linear sieve bounds for gcd sequences.
- The only quantitative information is empirical: the A282696/7 records (maximum displacement 394 near n ~ 10^8).

**Other hits checked and judged irrelevant:**
- arXiv:2610.15860 (Floros, Slater-Vélez permutation, 2026): abstract only, about absolute differences.
- arXiv:2609.18476 (barrycades, 2026): abstract only.
- A084834 and the "Sisyphus" sequence: snippet only, open-question variants.

## Relevance

- C009: cite LRS 2002 Lemma 7 for the charging step. The full bound appears to be ours, as far as this search reached.
- C010: no prior result found, either for or against.

"I found no prior work" here does **not** mean "there is no prior work". The following were not searched or read this pass:
- the Hasler wiki page (oeis.org);
- the erdosproblems forum thread;
- MathOverflow 241569;
- Guy's UPINT;
- Erdős-Graham 1980;
- the A329333 ff. family;
- the remaining sections of the EKG paper (Section 8).

## Verified by

Literature agent, 2026-11-25. Each linked note records what was actually read:
- [lagarias-rains-sloane-2002.md](lagarias-rains-sloane-2002.md), [applegate-et-al-2015-yellowstone.md](applegate-et-al-2015-yellowstone.md) and [sloane-2018-oeis-notices.md](sloane-2018-oeis-notices.md): PDFs read.
- [oeis-A117922-A086527.md](oeis-A117922-A086527.md): raw OEIS files read.

The web searches (three queries) returned snippets only.
