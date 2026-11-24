# C004 - The missing set is empty or has size at least ~ X / log X

## Statement

Let M be the set of positive integers that never occur in the sequence. If M is nonempty, then

    |M ∩ [1, X]| >= π(X + m) - π(m) - N0 = (1 - o(1)) X / log X,

where m = min M and N0 is as in C003. In particular, **M finite implies M empty**.

## Depends on

C003.

## Draft proof

Let m = min M and N0 as in C003. Let p be a prime with p > m + 1, and set v = p - m >= 2. Then v + m = p is prime.

Claim: v ∈ M ∪ {a(1), ..., a(N0 - 1)}.
Suppose v occurs at some index n >= N0, i.e. a(n) = v. Then a(n) + m = p is prime, contradicting C003. So either v never occurs (v ∈ M) or it only occurs before index N0.

The map p -> p - m is injective, so the number of v <= X obtained this way is π(X + m) - π(m + 1). At most N0 - 1 of them lie in {a(1..N0-1)}. Hence |M ∩ [1, X]| >= π(X + m) - π(m + 1) - (N0 - 1), which is ~ X / log X by the prime number theorem (Chebyshev's lower bound is enough for >> X / log X).

If M is finite, the left side is bounded while the right side tends to infinity: contradiction. So M finite implies M empty. ∎

## Numerical check

Up to 10^7 terms, the only values not yet seen are 13 values just below the current max (the "frontier"), consistent with M = ∅.

## Review log

- 2026-11-25: drafted at setup. **Awaiting skeptic.** Literature check needed: this "a missing value forces many missing values" trick is probably folklore for greedy prime-sum sequences.
