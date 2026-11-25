# C012 - Primes survived by a hole are paid by down-crossings of its level

## Statement

For v >= 2 and n >= 2, define the number of down-crossings of level v up to time n:

    X_v(n) = #{ j ∈ [2, n] : a(j-1) > v > a(j) }.

Let n >= 2 and 2 <= v <= n with v ∉ U_n, and put ε = v mod 2. Then

    π(n + v) - π(2v)  <=  X_v(n) + 1 + H_{1-ε}(n).

More precisely, with W1..W4 as in L009: |W1| + |W2| <= X_v(n), |W3| <= 1 and |W4| <= H_{1-ε}(n).

**Scope.** The statement holds for every starting value a(1). The proof uses no parity facts (neither F1 nor Sub-lemma S of L009); w ≡ 1 - ε comes from q being odd.

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

## Remarks

- **Relation to L009.** L009 bounds |W1| by H_{1-ε}(v-1) (Sub-lemma S) and |W2| by B(v), whose sum is H(v) - 1. C012 replaces that sum by a single dynamical quantity, the number of times the sequence jumps from above v to below v.
  - Neither bound dominates the other in general.
  - X_v(n) counts *all* down-crossings, including those not caused by a prime partner of v.
- **Prior art.** The W2 half is the steal injection, i.e. EKG Lemma 7's charging argument. The W1 half ("pre-steal") was found in the partners experiment: it held in 100% of 5.83M cases.
- **Why it might help (heuristic, not a claim).** If down-crossings of a level are O(log v) while that level is pending, C010 (C log v form) reduces to a bound on W4 alone. W4 is the class the experiment found hardest.

## Numerical check

- Skeptic, 2026-11-25: all (n, v) pairs with n <= 3·10^6 (24.1M pairs), 0 violations. Starts a(1) ∈ {2, 3, 4, 5, 6, 7, 10, 13, 20, 101} to 2·10^5, 0 violations.
- X_v(n) > H(v) - 1 at 4.49M pairs and < H(v) - 1 at 16.5M pairs, so neither bound dominates.
- Pending: the 10^8 check by the experimenter.

## Review log

- 2026-11-25: candidate created by the main session from the partners experiment's pre-steal observation. **Awaiting experimenter and skeptic.**
- 2026-11-25 (skeptic): **PASS** (statement and proof as written). Checked:
  - *Restatement.* For all n >= 2 and all v in [2, n] with v ∉ U_n: |W1| + |W2| <= X_v(n), |W3| <= 1, |W4| <= H_{1-ε}(n), hence π(n+v) - π(2v) <= X_v(n) + 1 + H_{1-ε}(n). Constants are absolute; no "large n"; no hidden quantifier swap.
  - *Availability.* For w ∈ W1 ∪ W2, k = fi(w) <= n - 1 <= n, so U_k ⊆ U_n (L009 F3) and v ∉ U_k; a(k) + v = q is prime. So v ∈ A_k and a(k+1) = min A_k <= v. Correct.
  - *a(k+1) ≠ v.* k + 1 <= n puts a(k+1) in U_n, and v ∉ U_n. Correct for both W1 and W2. The W1 parenthetical is also right: k <= v - 1 gives k + 1 <= v, and fi(v) > n >= v.
  - *Range and strictness.* k >= 1 gives j = k + 1 >= 2; k <= n - 1 gives j <= n. a(j-1) = w > v holds because W ⊆ (v, n] (L009 Step 0, which needs q > 2v), and a(j) < v follows from <= v and ≠ v. Both inequalities are strict, as X_v requires.
  - *Injectivity.* w = a(fi(w)), so w ↦ fi(w) is injective and so is k ↦ k + 1. Correct. The partition W1-W4 and the bounds for W3 and W4 are reused from L009 Steps 0-1, 4-5, which are in proven/.
  - *Scope (stronger than stated).* No step uses F1 (parity of a(k)) or Sub-lemma S. Step 0 gets w ≡ 1 - ε from q being odd, not from F1. So C012 holds for **every** start a(1), unlike L009'. The proof is in fact generic: it works for any rule of the form a(k+1) = min of an admissible set that contains v whenever a(k) + v is prime and v is unused. So it does not "prove" any false variant that I could find.
  - *Numerics (own C script, scratchpad c012_check.c; Fenwick range-add for X_v, exact W1-W4 classification by fi).* a(1) = 1, N = 3·10^6, **every** n <= N and every hole v in [2, n]: 24,089,445 (n, v) pairs. Violations: 0 for |W1|+|W2| <= X_v(n), 0 for |W3| <= 1, 0 for |W4| <= H_{1-ε}(n), 0 for the total. Equality |W1|+|W2| = X_v(n) at 528,316 pairs. The generated sequence matches overshoot_1e7/sequence.npy (a(3·10^5) = 299990, same partial sum), and its first 20 terms match OEIS. Variants a(1) ∈ {2,3,4,5,6,7,10,13,20,101}, N = 2·10^5, all pairs (about 1.25M each): 0 violations in every class.
  - *Remark "neither bound dominates".* Confirmed numerically: over all pairs, X_v(n) > H(v) - 1 in 4.49M cases and X_v(n) < H(v) - 1 in 16.5M cases (a(1) = 1, N = 3·10^6).
  - *Dependencies.* L009 is in proven/, and so is L002. L001 is listed but not used: only F2, F3 and the definition of A_k are needed. Note also that L002 is not really needed here, because v ∈ A_k already shows A_k ≠ ∅.
  - *Editorial (non-blocking).* (1) Add a Scope line saying the lemma holds for every a(1). (2) Remove L001 from "Depends on", or say that it is not used. (3) Fill in the Numerical check section. The "to do" there asks for 10^8, and I ran 3·10^6 with all pairs. (4) The "Why it might help" remark is a heuristic, not a claim. Note that X_v(n) counts every down-crossing, so the bound can be much weaker than L009' at a level the sequence oscillates across; it is useful only if such levels are rare.
- 2026-11-25 (editor): applied the skeptic's editorial points (1)-(4).
