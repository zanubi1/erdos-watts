# DRAFT, not posted. Review before posting.

**Title:** Does "almost all even h are q − p with p ≤ h/log²h" imply the greedy prime-sum sequence (A055265) is a permutation?

Let a(1)=1, and let a(n+1) be the least positive integer not yet used such that a(n)+a(n+1) is prime (OEIS A055265; Watts' question in Erdős problem #473). Is every positive integer a term? I believe this is open. I would be grateful for a check of the following argument, which I may have gotten wrong.

Write r_Y(h) = #{p ≤ Y prime : h+p prime}.

**(a)** If S is a finite set of values that never occur, then #{k : a(k)+m is prime for some m ∈ S} ≤ max S − 1. Reason: each such k forces a(k+1) < m, and k ↦ a(k+1) is injective. The bound does not depend on |S|.

**(c)** Suppose m₀ never occurs. Apply (a) both to S = {p − m₀ : p ≤ Y prime, p − m₀ never occurs} and to {m₀}. Using a(k) ≡ k (mod 2), this shows that for all but O(Y + m₀) indices k ≤ N with a(k) ≡ m₀ (mod 2), the even number h = a(k) − m₀ has r_Y(h) ≤ 2m₀. Since a(n) ≪ n log n, about Z/log Z distinct even h ≤ Z are "bad" in this sense.

So it suffices to show **(G)**: for each c, all but o(Z/log Z) even h ≤ Z have r_Y(h) > c, with Y = Z/(log Z)².

I believe (G) follows from a standard circle-method argument. The inputs are Vinogradov's minor-arc bound for Σ_{p≤Y} e(pα), Siegel–Walfisz on the major arcs (fine here because Z/Y = (log Z)²), and the mean square of the singular series. This gives Σ_{h≤Z} |Σ_{n≤Y} Λ(n)Λ(n+h) − 𝔖(h)Y|² ≪ ZY²(log Z)^{−A}.

**Questions:**
1. Is this argument, or the reduction (a)+(c), already known?
2. Is there an error? In particular, is the unbalanced (G) known or standard, e.g. as a variant of Lavrik's theorem?

I do not claim a proof. A 2-page write-up of each part is available. (By a formula of Hasler, the same argument would also settle A128280.)
