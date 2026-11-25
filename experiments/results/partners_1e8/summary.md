# Prime partners of holes to N = 10^8 (2026-11-25)

Command (about 70 s in C, then about 2.5 min in numpy; peak RAM about 9.6 GB):

    python experiments/src/partners.py --terms 100000000 --workdir <scratch>

Raw output: `stdout.txt` (10^8) and `stdout_1e7.txt`. Code: `experiments/src/partners.py` and `partners_gen.c`.

**Code checks.**
- The first 20 terms match A055265.
- The class totals at 10^7 match `holes_dynamics_1e7` exactly.
- A pure-Python brute force for N = 2·10^4 reproduces every count, with 0 mismatches.
- L009' and Sub-lemma S hold for all 47.5M holes.

## Notation

For a hole v, take n = fi(v) - 1. The partners w = q - v (q prime in (2v, n+v]) split into four classes, as in L009:

- **W1 (Ahead):** w was used before time v.
- **W2 (steal):** w was used in [v, n-1], forcing a smaller fill.
- **W3:** w = a(n).
- **W4 (Late):** w is still a hole at time n.

K = |W1| + |W2| + |W3| + |W4|.

## 1. Decomposition

| v range | max K | max W1 | max W2 | max W4 | max W1+W4 | mean W1/W2/W3/W4 |
|---|---|---|---|---|---|---|
| [1e3,1e4) | 6 | 3 | 3 | 3 | 4 | .112/.044/.331/.383 |
| [1e4,1e5) | 7 | 5 | 5 | 5 | 6 | .114/.049/.318/.396 |
| [1e5,1e6) | 8 | 4 | 6 | 7 | 8 | .115/.056/.312/.410 |
| [1e6,1e7) | 8 | 6 | 5 | 7 | 8 | .120/.060/.310/.416 |
| [1e7,1e8) | 11 | 8 | 7 | 8 | **8** | .123/.063/.308/.421 |

- **W1+W4 is flat:** its max is 8 in every 10^7 block, while K reached 11. But its tail is creeping: P(W1+W4 >= 7) is 1.47× higher above 10^7 than below. So the flat 8 is probably luck.
- **The excess K = 9-11 comes from steals plus large H(v).** At K >= 9 the past payers W1 + W2 carry 60-66% of K, and mean H(v) is 28-43. The share of K paid by steals rises from .03 at K = 1 to .32 at K = 10.
- **W1 and W4 are never large together.** For j = 0..8, the max of W4 given W1 = j is 8, 7, 6, 5, 3, 3, 1, 1, 0.

## 2. Null models (v >= 10^3)

Observed partner counts are compared with two placements:
- **g:** the window's actual K primes placed uniformly on its parity-correct slots;
- **p:** independent random primes with density 2/ln.

| class | O/g overall | O/p overall | dispersion vs g |
|---|---|---|---|
| W1 (Ahead) | 0.44 | 0.37 | 0.76 (under) |
| W4 (Late) | 1.70 | 1.28 | 1.55 (over) |
| W1+W4 | - | - | 1.07 (about hypergeometric) |

- **Ahead is genuinely suppressed.** The whole Ahead set's partner rate is 0.36× random, flat over five decades.
- **Late is enhanced relative to its slot share,** with tails about 20× hypergeometric at j = 6. In absolute terms it is suppressed when H(n) is large (O/p 0.18-0.5), because those windows are prime-poor.

## 3. Geometry

| class | n - w: p50 / p99 / max | w - v: p50 / p99 / max |
|---|---|---|
| Late W4 | 8 / 58 / 250 | 15 / 77 / 247 |
| Ahead W1 | 10 / 68 / 232 | 7 / 45 / 203 |
| steal W2 | 12 / 68 / 216 | 13 / 69 / 215 |

- **Where the partners sit:** Late partners are at the top of the window and Ahead partners at the bottom, a median of 17 below the running max.
- **No cut leaves an O(1) side.** Splitting at the running max, or at the smallest Late slot, each side can reach 10.
  - Example: v = 55,252,993 has all 10 of its primes on one side.

## 4. Recursion / contraction

- **No contraction against earlier holes:** K(v) = 10 occurs when the max K of the earlier alive holes is 1.
- **Best affine fits** K <= α·X + β:
  - X = H(v) + H_{1-ε}(n): α = 1/2 gives β = 2.5, at both 10^7 and 10^8.
  - X = H(v): α = 1 gives β = 6.
- **Window test:** "Late partners lie in (n - c ln² n, n]" is vacuous; every Late slot is in that window.
- **Pre-steal (verified, elementary).** If an Ahead partner is w = a(k) with k <= v - 1, then a(k+1) < v. This holds in 100% of 5.83M cases. In 36% of them a(k+1) is not a hole fill.
- **Ahead values are not partners of earlier frontier values:** that rate is 0.104, against a base rate of 0.099.

## 5. Candidate statements (verified for every hole with fi(v) <= 10^8)

- **(A)** For v >= 10^3: |W1| + |W4| <= 0.61 ln v. The observed max ratio is 0.607, at v = 526,514; it is 0.480 on [1e7, 1e8).
- **(B)** K(v) <= ½(H(v) + H_{1-ε}(n)) + 5/2. This halves L009' asymptotically.

## Conclusions

1. **Measured:** W1 + W4 is about hypergeometric relative to the primes actually in the window. "Few payers land on shifted primes" is mostly "few primes times the slot fraction". There is no special arithmetic avoidance, so a bound on W1 + W4 pushes the burden back onto K itself (circular).
2. **Measured:** the one genuine suppression is on Ahead partners, explained by the pre-steal injection. With the steal injection of L009, this gives the crossing bound of L012.
3. **Interpretation:** the hardest class is W4 (Late): it is over-dispersed and favoured. Bounding it needs the spread n - (smallest Late hole), which is overshoot-type data.
4. **Interpretation:** no partner-counting statement found here contracts. Proving C010 needs input on how K itself grows, i.e. on primes in short windows near 2v weighted by the dynamics. It does not reduce to a count of holes.
