# L012 - Primes survived by a hole are paid by down-crossings of its level

## Statement

For v >= 2 and n >= 2, define the number of down-crossings of level v up to time n:

    X_v(n) = #{ j ∈ [2, n] : a(j-1) > v > a(j) }.

Let n >= 2 and 2 <= v <= n with v ∉ U_n, and put ε = v mod 2. Then

    π(n + v) - π(2v)  <=  X_v(n) + 1 + H_{1-ε}(n).

More precisely, with W1..W4 as in L009: |W1| + |W2| <= X_v(n), |W3| <= 1 and |W4| <= H_{1-ε}(n).

**(b) Parity-refined form and its ceiling** (added 2026-11-25; skeptic PASS). Same hypotheses as (a). Let X^ε_v(n) count only the down-crossings j with a(j) ≡ ε (mod 2). Then

    |W1| + |W2|  <=  X^ε_v(n)  <=  H(v) - 1,     and     X_v(n)  <=  H(v - 1) + H(v) - 1.

**Scope.** Part (a) and the bound X <= H(v-1) + H(v) - 1 hold for every starting value a(1). The middle bound X^ε <= H(v) - 1 needs a(1) odd; it fails for even starts, as the skeptic checked. The proof uses no parity facts (neither F1 nor Sub-lemma S of L009); w ≡ 1 - ε comes from q being odd.

## Depends on

The partition W1-W4 from the proof of L009 (Steps 0-1 and 4-5; facts F2 and F3). L001 is not used. L002 is not needed either, since v ∈ A_k already shows that A_k is nonempty.

## Proof

Use the partner set W = { q - v : q prime, 2v < q <= n + v } ⊆ (v, n] and its partition W1-W4 by fi(w), from L009 Steps 0-1. Steps 4-5 of L009 give |W3| <= 1 and |W4| <= H_{1-ε}(n). It remains to inject W1 ∪ W2 into the set of down-crossings.

Let w ∈ W1 ∪ W2 and k = fi(w), so that k <= n - 1 and a(k) = w > v.

- **v is available at step k.** v ∉ U_k, since k <= n and v ∉ U_n. Also a(k) + v = q is prime. So v ∈ A_k, and a(k+1) <= v.
- **a(k+1) ≠ v.** k + 1 <= n and v ∉ U_n, so a(k+1) ≠ v. (For W1 this also follows from k + 1 <= v < fi(v).)
- **So j := k + 1 is a down-crossing.** j ∈ [2, n], a(j-1) = w > v and a(j) < v.
- **Injectivity.** w ↦ fi(w) is injective (L009 F2), and so is k ↦ k + 1.

Hence |W1| + |W2| <= X_v(n). Summing the four classes gives the claim. ∎

**Proof of (b)** (from the crossings experiment's proposal P1, written out by the main session).
- **|W1| + |W2| <= X^ε.** For the crossings j = k + 1 built above, a(k) = w has parity 1 - ε, so by L001 a(j) has parity ε.
- **Crossings with j <= v.** Map j to k = j - 1 <= v - 1. Then a(k) > v > v - 1, so a(k) is a used value > v - 1 at time v - 1.
  - If a(j) ≡ ε, then a(k) ≡ 1 - ε (L001). By Sub-lemma S of L009 at m = v - 1, there are exactly H_{1-ε}(v-1) such used values.
  - Without the parity restriction: #{x ∈ U_m : x > m} = H(m), because |U_m| = m. This needs no parity argument, so the bound X <= H(v-1) + H(v) - 1 holds for every a(1).
  - j ↦ a(j-1) is injective (F2).
- **Crossings with v < j <= n.** Map j to a(j) < v. Since j - 1 >= v, a(j) ∉ U_{j-1} ⊇ U_v, so a(j) is a hole < v at time v.
  - With parity ε it is counted by B(v). Without the restriction, it is one of the H(v) - 1 holes < v at time v (v itself is a hole at time v).
  - Injective by F2.
- **Sum.** X^ε <= H_{1-ε}(v-1) + B(v) = H(v) - 1, by the identity in L009's Sharpening. Also X <= H(v-1) + H(v) - 1. ∎

## Remarks

- **Relation to L009.** L009 bounds |W1| by H_{1-ε}(v-1) (Sub-lemma S) and |W2| by B(v), whose sum is H(v) - 1. L012 replaces that sum by a single dynamical quantity, the number of times the sequence jumps from above v to below v.
  - Neither bound dominates the other in general.
  - X_v(n) counts *all* down-crossings, including those not caused by a prime partner of v.
- **Prior art.** The W2 half is the steal injection, i.e. EKG Lemma 7's charging argument. The W1 half ("pre-steal") was found in the partners experiment: it held in 100% of 5.83M cases.
- **Why it might help (heuristic, not a claim).** If down-crossings of a level are O(log v) while that level is pending, C010 (C log v form) reduces to a bound on W4 alone. W4 is the class the experiment found hardest.

## Numerical check

- Skeptic, 2026-11-25: all (n, v) pairs with n <= 3·10^6 (24.1M pairs), 0 violations. Starts a(1) ∈ {2, 3, 4, 5, 6, 7, 10, 13, 20, 101} to 2·10^5, 0 violations.
- X_v(n) > H(v) - 1 at 4.49M pairs and < H(v) - 1 at 16.5M pairs, so neither bound dominates.
- Experimenter, 2026-11-25, to 10^8. Code: `experiments/src/crossings.py` + `crossings_gen.c`.
  - Checks on the code: the brute-force selftest at N = 4000 found 0 mismatches. K and W1..W4 match `partners_gen.c` on all 47,519,538 holes (fi(v) <= 10^8, or still open at 10^8), with n = fi(v) - 1.
  - K <= X_v(n) + 1 + H_{1-ε}(n): 0 violations, with equality in 2,966 holes (0.006%).
  - |W1| + |W2| <= X_v(n): 0 violations, with equality in 0.47% of holes.
  - **Parity-refined form.** Let X^ε count only the crossings with a(j) ≡ v (mod 2).
    - |W1| + |W2| <= X^ε_v(n): 0 violations, equality 4.7%.
    - K <= X^ε + 1 + H_{1-ε}(n): 0 violations, equality 0.08%.
    - Per class: W1 <= E^ε (crossings with j <= v) and W2 <= L^ε (crossings with v < j <= n), both with 0 violations.
  - **X against H(v) - 1** on [1e7, 1e8]: X is smaller in 57.0% of holes, equal in 12.9% and larger in 30.1%. The largest excess X - (H(v) - 1) is 47. The max of X is 113, at v = 95,956,519.
  - **X^ε against H(v) - 1.** X^ε_v(n) <= H(v) - 1 held in every case, and an elementary injection proves it (experimenter's reply, 2026-11-25). So the parity-refined L012 is never weaker than L009' for W1 + W2. Above 10^7 it is strictly sharper in 97.5% of holes.
  - **Growth.** X_v(n) does not look O(log v). By decade, max X / ln v is 0.95, 1.53, 2.28, 2.79, 4.33, 4.54, 6.25, which tracks the growth of H(v).

## Review log

- 2026-11-25: candidate created by the main session from the partners experiment's pre-steal observation. **Awaiting experimenter and skeptic.**
- 2026-11-25 (skeptic): **PASS** (statement and proof as written). Checked:
  - *Restatement.* For all n >= 2 and all v in [2, n] with v ∉ U_n: |W1| + |W2| <= X_v(n), |W3| <= 1, |W4| <= H_{1-ε}(n), hence π(n+v) - π(2v) <= X_v(n) + 1 + H_{1-ε}(n). Constants are absolute; no "large n"; no hidden quantifier swap.
  - *Availability.* For w ∈ W1 ∪ W2, k = fi(w) <= n - 1 <= n, so U_k ⊆ U_n (L009 F3) and v ∉ U_k; a(k) + v = q is prime. So v ∈ A_k and a(k+1) = min A_k <= v. Correct.
  - *a(k+1) ≠ v.* k + 1 <= n puts a(k+1) in U_n, and v ∉ U_n. Correct for both W1 and W2. The W1 parenthetical is also right: k <= v - 1 gives k + 1 <= v, and fi(v) > n >= v.
  - *Range and strictness.* k >= 1 gives j = k + 1 >= 2; k <= n - 1 gives j <= n. a(j-1) = w > v holds because W ⊆ (v, n] (L009 Step 0, which needs q > 2v), and a(j) < v follows from <= v and ≠ v. Both inequalities are strict, as X_v requires.
  - *Injectivity.* w = a(fi(w)), so w ↦ fi(w) is injective and so is k ↦ k + 1. Correct. The partition W1-W4 and the bounds for W3 and W4 are reused from L009 Steps 0-1, 4-5, which are in proven/.
  - *Scope (stronger than stated).* No step uses F1 (parity of a(k)) or Sub-lemma S. Step 0 gets w ≡ 1 - ε from q being odd, not from F1. So L012 holds for **every** start a(1), unlike L009'. The proof is in fact generic: it works for any rule of the form a(k+1) = min of an admissible set that contains v whenever a(k) + v is prime and v is unused. So it does not "prove" any false variant that I could find.
  - *Numerics (own C script, scratchpad c012_check.c; Fenwick range-add for X_v, exact W1-W4 classification by fi).* a(1) = 1, N = 3·10^6, **every** n <= N and every hole v in [2, n]: 24,089,445 (n, v) pairs. Violations: 0 for |W1|+|W2| <= X_v(n), 0 for |W3| <= 1, 0 for |W4| <= H_{1-ε}(n), 0 for the total. Equality |W1|+|W2| = X_v(n) at 528,316 pairs. The generated sequence matches overshoot_1e7/sequence.npy (a(3·10^5) = 299990, same partial sum), and its first 20 terms match OEIS. Variants a(1) ∈ {2,3,4,5,6,7,10,13,20,101}, N = 2·10^5, all pairs (about 1.25M each): 0 violations in every class.
  - *Remark "neither bound dominates".* Confirmed numerically: over all pairs, X_v(n) > H(v) - 1 in 4.49M cases and X_v(n) < H(v) - 1 in 16.5M cases (a(1) = 1, N = 3·10^6).
  - *Dependencies.* L009 is in proven/, and so is L002. L001 is listed but not used: only F2, F3 and the definition of A_k are needed. Note also that L002 is not really needed here, because v ∈ A_k already shows A_k ≠ ∅.
  - *Editorial (non-blocking).* (1) Add a Scope line saying the lemma holds for every a(1). (2) Remove L001 from "Depends on", or say that it is not used. (3) Fill in the Numerical check section. The "to do" there asks for 10^8, and I ran 3·10^6 with all pairs. (4) The "Why it might help" remark is a heuristic, not a claim. Note that X_v(n) counts every down-crossing, so the bound can be much weaker than L009' at a level the sequence oscillates across; it is useful only if such levels are rare.
- 2026-11-25 (editor): applied the skeptic's editorial points (1)-(4).
- 2026-11-25 (main session): added part (b), the crossings experiment's P1, with a written proof. The 10^8 run found 0 violations of (b). **(b) awaits a skeptic.** (a) has a skeptic PASS.
- 2026-11-25 (skeptic, part (b)): **PASS** for (b) as written, with scope a(1) = 1 (more generally a(1) odd). Checked:
  - *Restatement.* Same hypotheses as (a): n >= 2, 2 <= v <= n, v ∉ U_n, ε = v mod 2. X^ε_v(n) = #{ j ∈ [2, n] : a(j-1) > v > a(j), a(j) ≡ ε }. Claims: (i) |W1| + |W2| <= X^ε_v(n); (ii) X^ε_v(n) <= H(v) - 1; (iii) X_v(n) <= H(v-1) + H(v) - 1. Editorial: (b) does not restate these hypotheses. It inherits them from (a); say so explicitly.
  - *(i).* The crossings j = fi(w) + 1 from (a) have a(j-1) = w ≡ 1 - ε (Step 0, q odd), so a(j) ≡ ε by L001. L001's alternation holds for every a(1), so (i) holds for every start.
  - *Split j <= v / j > v, boundary j = v.* The classes [2, v] ∩ [2, n] and [v+1, n] partition [2, n]. j = v goes to the first class: k = v - 1 >= 1, and a(v-1) ∈ U_{v-1}. The second class needs j - 1 >= v, which fails at j = v, so putting j = v in the first class is forced and correct. No off-by-one.
  - *First injection (j <= v, j ↦ a(j-1)).* k = j - 1 ∈ [1, v-1], so a(k) ∈ U_{v-1} (F3). a(k) > v > v - 1. For a(j) ≡ ε, L001 gives a(k) ≡ 1 - ε. So a(k) lies in { x ∈ U_{v-1} : x ≡ 1 - ε, x > v - 1 }, which by Sub-lemma S at m = v - 1 >= 1 has H_{1-ε}(v-1) elements. S needs F1, hence a(1) odd. Injective because j ↦ j - 1 ↦ a(j-1) (F2).
  - *Second injection (v < j <= n, j ↦ a(j)).* a(j) ∉ U_{j-1} (F2), and U_v ⊆ U_{j-1} since j - 1 >= v (F3), so a(j) is a hole at time v. a(j) < v (strict, by definition of a crossing). With a(j) ≡ ε it lies in the set counted by B(v). Injective by F2.
  - *Sum.* H_{1-ε}(v-1) + B(v) = H(v) - 1 is the L009 Sharpening identity. It needs v ∉ U_v (true since v <= n) and F1 (a(1) odd).
  - *"Holes < v at time v" = H(v) - 1.* H(v) counts the holes in [1, v] at time v. v is one of them, since v ∉ U_v. So exactly H(v) - 1 holes are < v. Correct.
  - *(iii) holds for every a(1).* The proof cites "S summed over both parities". The summed statement #{ x ∈ U_m : x > m } = H(m) needs no parity: |U_m| = m, so this count is m - |U_m ∩ [1, m]| = H(m). The second class needs no parity either. So (iii) holds for every a(1), but S itself, as proved in L009, needs a(1) odd. Editorial: replace "S summed over both parities" by this one-line count, and narrow the a(1) = 1 scope note to (ii) only.
  - *Dependencies.* L001, L009 (F2, F3, Sub-lemma S, Sharpening) are in proven/. Not conditional.
  - *Numerics (own C script, scratchpad c012b.c).* Fenwick range-add per parity for X^ε and X. |W1| + |W2| is maintained incrementally as #{ w ∈ (v, n] : w + v prime, fi(w) <= n - 1 }. A Python brute force (brute.py) agrees exactly at N = 600 for a(1) ∈ {1, 2, 6}. With a(1) = 1, **every** n <= 10^7 and every hole v in [2, n]: 88,212,972 pairs (this matches L009's skeptic count). Violations: 0 for (i), 0 for (ii), 0 for (iii), 0 for the per-class bounds E^ε <= H_{1-ε}(v-1) and L^ε <= B(v) and their unrestricted analogues, 0 for the identity. Equality: (i) at 8,422,904 pairs, (ii) at 2,383,444 pairs, (iii) at 594,114 pairs. So all three bounds are attained.
  - *Variants.* For odd a(1) ∈ {3, 5, 7, 13, 101} (N = 2·10^5, all pairs): 0 violations of anything. For even a(1) ∈ {2, 4, 6, 10, 20}: (i) and (iii) hold (0 violations), but (ii) **fails** at about 13.1k pairs each, together with the identity. Smallest case: a(1) = 6, so a = 6, 1, 2, ... At n = v = 3, X^1 = 1 (j = 2) but H(3) - 1 = 0. This matches the proof, which uses F1 only in S and in the identity. So the proof does not "prove" a false variant, and the a(1) = 1 scope is necessary for (ii).
- 2026-11-25 (editor): applied the skeptic's edits to (b): restated the hypotheses, gave a parity-free count for the X bound, and narrowed the scope note to the middle bound. (a) and (b) now both have a skeptic PASS. **Ready for promotion to L012 on Matteo's OK.**
- 2026-11-25: Matteo's OK. **Moved to lemmas/proven/ as L012 (formerly L012).**
