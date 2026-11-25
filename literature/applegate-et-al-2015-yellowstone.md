# Applegate, Havermann, Selcoe, Shevelev, Sloane, Zumkeller, "The Yellowstone permutation" (2015)

## Citation/link

D. L. Applegate, H. Havermann, B. Selcoe, V. Shevelev, N. J. A. Sloane, R. Zumkeller, "The Yellowstone permutation", arXiv:1501.01669 [math.NT] (v1 7 Jan 2015, v2 8 Mar 2015). It is commonly cited as J. Integer Sequences 18 (2015), article 15.6.7. That journal reference was not visible on the arXiv abstract page, so it is unverified here. OEIS A098550.

## What it says (read 2026-11-25, arXiv PDF pp. 2-5)

- Definition: a(n) is the least unused number with gcd(a(n), a(n-2)) > 1 and gcd(a(n), a(n-1)) = 1.
- **Theorem 1** (permutation) has six steps.
  - (i) The sequence is infinite.
  - (ii) Infinitely many primes divide its terms.
  - (iii) Every prime divides some term.
  - (iv) Every prime divides infinitely many terms.
  - (v) Every prime occurs as a term.
  - (vi) Let k be the smallest missing number. Once gcd(a(N1), k) > 1 for some late N1, it holds for **all** later n. Otherwise some j has gcd(a(j), k) > 1 and gcd(a(j+1), k) = 1, which would force a(j+2) = k. This contradicts (v).
- The paper notes that the same argument applies to many variants (sets Ω, other starts). It gives no details.
- Section 3: the growth model ("Hypothesis A") is only empirical. No proved lifetime or delay bound.

## Relevance

- Step (vi) is the same "smallest missing value is forced at the first admissible moment" mechanism as EKG Lemmas 3-4 and A253074. It is relevant to L003, and to L009 case 2 only in the special case B(v) = 0.
- It contains no counting of payers and no bound on how long a value can stay missing.

## Verified by

Literature agent, 2026-11-25: **read** pages 2-5 of the arXiv PDF (Sections 1-2 and the start of Section 3) via WebFetch. The rest of the paper was not read.
