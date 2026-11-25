# C012 - Primes survived by a hole are paid by down-crossings of its level

## Statement

For v >= 2 and n >= 2, define the number of down-crossings of level v up to time n:

    X_v(n) = #{ j ∈ [2, n] : a(j-1) > v > a(j) }.

Let n >= 2 and 2 <= v <= n with v ∉ U_n, and put ε = v mod 2. Then

    π(n + v) - π(2v)  <=  X_v(n) + 1 + H_{1-ε}(n).

More precisely, with W1..W4 as in L009: |W1| + |W2| <= X_v(n), |W3| <= 1 and |W4| <= H_{1-ε}(n).

## Depends on

L001, L002, and the partition from the proof of L009 (Steps 0-1, 4-5).

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
- **Why it might help.** If down-crossings of a level are O(log v) while that level is pending, C010 (C log v form) reduces to a bound on W4 alone. W4 is the class the experiment found hardest.

## Numerical check

To do: compare X_v(fi(v)-1) with H(v) - 1, and test the inequality for all holes up to 10^8.

## Review log

- 2026-11-25: candidate created by the main session from the partners experiment's pre-steal observation. **Awaiting experimenter and skeptic.**
