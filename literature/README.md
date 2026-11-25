# Literature index

Last pass: 2026-11-25, third pass: C013 search on hypothesis (G) and the cascade. projecteuclid.org, tsukuba.repo.nii.ac.jp, mathnet.ru and export.arxiv.org fail DNS; the erdosproblems forum returns 403; arxiv.org abs/pdf/search work. Previous pass: 2026-11-25 (L009/C010 search; arxiv.org PDFs were reachable via WebFetch this time). Earlier: 2026-11-24 (two passes). **Network note:** even after the allowlist change, www.erdosproblems.com, erdosproblems.com, oeis.org and arxiv.org fail DNS in the agent session. raw.githubusercontent.com works, so OEIS entries were read through the GitHub mirror `oeis/oeisdata` and the erdosproblems status through `teorth/erdosproblems`.

| Source | Relevance | Verified by |
|---|---|---|
| [erdosproblems.com #473 + forum thread](erdosproblems-473.md) | the problem; greedy question open as far as seen; 197 never a sum | mirror + snippets + site database (problems.yaml) read; original page and forum (3 posts) NOT read |
| [OEIS A055265 + cross-refs](oeis-A055265.md) | the sequence; A282695 says no proof; A282696/7 displacement records (394 by n ~ 10^8), which match our runs | raw OEIS files read via GitHub mirror |
| [OEIS A253074 / A253073](oeis-A253074.md) | Devlin-Artamonov "missing x forces late terms" argument: prior art for the L003/L004 technique | raw OEIS file read via GitHub mirror |
| [Google DeepMind formal-conjectures](formal-conjectures.md) | 473.lean formalizes only the main question (solved) and the finite variant (open); **greedy variant not formalized** | raw file read |
| [Hasler OEIS wiki, Prime sums from neighboring terms](oeis-wiki-hasler-prime-sums.md) | context; conjectures only | snippets only (oeis.org unreachable) |
| [Lagarias-Rains-Sloane, EKG (2002)](lagarias-rains-sloane-2002.md) | "smallest missing" proof (Lemmas 3-4); **Lemma 7 = charging argument of L009 case 2**; linear sieve bounds | arXiv PDF read (pp. 1-6, 9-13), 2026-11-25 |
| [Yellowstone permutation (2015)](applegate-et-al-2015-yellowstone.md) | Theorem 1(vi): smallest-missing forcing; no lifetime bound | arXiv PDF pp. 2-5 read |
| [Sloane, OEIS article (2018)](sloane-2018-oeis-notices.md) | calls A055265's permutation property possibly "beyond reach" (prime gaps) | arXiv PDF pp. 1-12 read |
| [OEIS A117922, A117925, A086527, A282700, A128280, A051237](oeis-A117922-A086527.md) | no delay/lifetime bound anywhere; no payer argument | raw OEIS files read via mirror |
| [Search log for L009/C010](search-C009-C010-hole-payers.md) | L009 case 2 is known (EKG Lemma 7); full L009 bound and C010 **not found** | see linked notes |
| [Search log for L006 step formula](search-C006-step-formula.md) | L006: **not found** in the OEIS entries or by web search; elementary/folklore; EKG and Yellowstone proofs still unread | OEIS raw files read; rest snippets; EKG/Yellowstone hosts (arxiv, emis, cs.uwaterloo.ca) unreachable |
| MathOverflow 241569 | Segal's finite version | not yet read |
| [Search log for C013: (G) and the cascade](search-C013-G-and-cascade.md) | (G) **not found stated**; assessed as a routine consequence of Lavrik-type mean values (two sketched reductions, about 80% confidence); blocking lemma/cascade and any permutation proof **not found** | see linked notes; reductions are the agent's own sketches |
| [Matomäki-Radziwiłł-Tao (2019)](matomaki-radziwill-tao-2019.md) | Thm 1.3: prime pairs for almost all h, \|h-h0\| <= H, h0 <= X^{1-ε}; shift <= p-range, so it does not cover (G) | arXiv PDF pp. 1-9 read |
| [Lavrik / Wolke / Mikawa / Perelli-Pintz](lavrik-wolke-mikawa-prime-pairs.md) | almost-all-h prime pairs; Lavrik (all h <= x) is the key input for (G) Route A; exact form **unverified** | snippets + secondary citations only |
| [Bhowmik-Grimmelt (2026) survey](bhowmik-grimmelt-2026-goldbach-exceptional-set.md) | standard Parseval + Chebyshev scheme for Goldbach's exceptional set | arXiv PDF pp. 1-6, 10-13 read |
