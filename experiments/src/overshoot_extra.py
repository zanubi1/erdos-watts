"""Follow-up checks on an overshoot.py run (needs sequence.npy and blocked.npy in --dir).

1. Exact step formula a(n+1) = u_par(n) + (P_{k+b} - t_n), t_n = a(n) + u_par(n), P_k = first prime >= t_n,
   b = blocked(n); and the bound obtained by replacing b with O_par(n).
2. Multiplicity of each prime q as a sum a(n) + a(n+1), vs the prime gap just below q.
3. Upper-displacement records vs maximal prime gaps near 2n.

Usage: python experiments/src/overshoot_extra.py --dir experiments/results/overshoot_1e7
"""
import argparse, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from overshoot import derived, Gaps, records  # noqa: E402
ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--dir", default="experiments/results/overshoot_1e7")
d = ap.parse_args().dir + "/"
seq=np.load(d+'sequence.npy'); bl=np.load(d+'blocked.npy')
D=derived(seq); N=len(seq); n=D['n']
G=Gaps(2*int(seq.max())+10000)
nxt=seq[1:]
up=np.where(nxt%2==0, D['u_e'][:-1], D['u_o'][:-1])
Op=np.where(nxt%2==0, D['O_e'][:-1], D['O_o'][:-1])
print('max u_par(n)-n', int((up-n[:-1]).max()), 'max u(n)-n', int((D['u']-n).max()))
t=seq[:-1]+up
idx=np.searchsorted(G.p,t)
B=G.p[idx+Op]-t + up - (n[:-1]+1)   # bound on Dup(n+1)
dup=nxt-(n[:-1]+1)
print('bound holds:', bool(np.all(dup<=B)), 'max bound', int(B[10:].max()), 'at n+1=', int(np.argmax(B[10:]))+12, 'actual max Dup', int(dup.max()))
print('mean slack', float((B-dup)[N//10:].mean()))
# also bound with blocked instead of O_par (exact)
E=G.p[idx+bl[1:]]-t+up-(n[:-1]+1)
print('exact formula check:', bool(np.all(E==dup)))
# bound with K = O(n) (total overshoot) instead of O_par
B2=G.p[idx+D['O'][:-1]]-t+up-(n[:-1]+1)
print('bound with total O: max', int(B2[10:].max()))
# prime multiplicity as sums
s=seq[:-1]+seq[1:]
vals,cnt=np.unique(s,return_counts=True)
o=np.argsort(cnt)[::-1][:12]
print('most reused sum-primes (q, multiplicity, gap below q, first n, last n):')
for j in o:
    q=int(vals[j]); w=np.flatnonzero(s==q)
    pi=np.searchsorted(G.p,q)
    print(q, int(cnt[j]), int(G.p[pi]-G.p[pi-1]), int(w[0])+1, int(w[-1])+1)
# correlation multiplicity vs gap below
pi=np.searchsorted(G.p,vals); gb=G.p[pi]-G.p[np.maximum(pi-1,0)]
sel=vals>2*10**6
print('corr(mult, gap below) for q>2e6:', np.corrcoef(cnt[sel],gb[sel])[0,1])
for g in [50,100,150]:
    m=sel&(gb>=g); print(f'gap below >= {g}: mean mult {cnt[m].mean():.1f}, max {cnt[m].max()}, count {m.sum()}')
print('overall mean mult (q>2e6):', cnt[sel].mean(), 'max', cnt[sel].max())
# Dup records vs record gaps
r=records(D['Dup'])
for i in r[r>100000]:
    nn=i+1; g,p=G.max_gap_in(2*nn-400,2*nn+400)
    rec=[(pp,gg) for pp,gg in G.record_gaps if abs(pp-2*nn)<600]
    print('Dup record',int(D['Dup'][i]),'@',nn,'maxgap near 2n',g,'@',p,'record gap nearby:',rec)
