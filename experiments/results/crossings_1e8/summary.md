# Down-crossings of levels to N = 10^8 (2026-11-25)

Command (about 70 s in C, then about 40 s in numpy; peak RAM about 12 GB):

    python experiments/src/crossings.py --terms 100000000 --workdir <scratch>

- **Code checks.** `--selftest` brute-forces every field at N = 4000 with 0 mismatches. K and W1..W4 match `partners_gen.c` on all 47,519,538 holes.
- **Raw output** is in `stdout.txt`.

## Notation

Hole v, at time n = fi(v) - 1, with ε = v mod 2.

- X = X_v(n) = #{ j <= n : a(j-1) > v > a(j) } is the number of down-crossings of level v.
- X^ε counts only the crossings that land on a(j) ≡ ε.

## C012 checks (all 47.5M holes): 0 violations

| inequality | equality fraction |
|---|---|
| K <= X + 1 + H_{1-ε}(n) | 0.006% |
| W1+W2 <= X | 0.47% |
| W1+W2 <= X^ε | 4.72% |
| X^ε <= H(v) - 1 (C012 b) | 2.65% |
| X <= H(v-1) + H(v) - 1 (C012 b) | 0.57% |

## Size of X at holes

| v | max X | mean X | max X^ε | max H(v)-1 | P(X > H(v)-1) | max X / ln v |
|---|---|---|---|---|---|---|
| [1e3,1e4) | 21 | 3.31 | 10 | 16 | .296 | 2.28 |
| [1e4,1e5) | 32 | 4.53 | 15 | 28 | .300 | 2.79 |
| [1e5,1e6) | 59 | 5.82 | 30 | 40 | .300 | 4.33 |
| [1e6,1e7) | 72 | 7.09 | 39 | 49 | .302 | 4.54 |
| [1e7,1e8] | 113 | 8.37 | 58 | 74 | .301 | 6.25 |

- **X is not O(log v).** Its max over ln v rises steadily, and its max tracks H(v).
- **Large X does not mean large K:** the largest X is 113 (at v = 95,956,519), where K = 9.

## Crossings of all levels

- **Mean X_v(∞):** about 0.78 ln v, rising by about 1.8 per decade.
- **Max X_v(∞):** 121 above 10^7.
- **Crossings are local.** Every crossing has j - v within the displacement range: [-290, +251] above 10^7, with 99% within ±72.
- **Exact identities (0 failures):**
  - up-crossings minus down-crossings equals a boundary term;
  - X_v(∞) <= H(v-1) + H(v) - [fi(v) ≠ v].

## Residual W4 must carry, if crossings are bounded

| v | max K | max K - X - 1 | max W4 |
|---|---|---|---|
| [1e5,1e6) | 8 | 4 | 7 |
| [1e6,1e7) | 8 | 4 | 7 |
| [1e7,1e8] | 11 | 6 | 8 |

The largest residual, 6, is at v = 73,818,656: K = 7, X = 0, W4 = 6.

## Conclusions

1. **Measured.** C012 (a) and (b) hold on all 47.5M holes.
2. **Measured.** X is not O(log v): its maximum grows with H(v). So the crossing bound does **not** escape the circularity. Its proven ceiling (C012 b) is itself H(v) - 1.
3. **Measured.** The residual for W4 is small (max 6, at most 0.33 ln v) and occurs where X is tiny.
4. **Interpretation.** Every bound found so far (L009', C012, the partner counts) reduces the primes survived by a hole to H. Bounding H through lifetimes loses a factor of log n. No counting identity in the sequence's own data breaks this loop. The missing input is distributional: how the primes in short windows near 2v interact with the dynamics.
