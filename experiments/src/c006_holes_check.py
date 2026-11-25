"""C006 Remark R3a check: Dup(n+1) <= q'_{H_par(n)+1} - (a(n)+n+1), hole counts H(n), sum identity.
Usage: python experiments/src/c006_holes_check.py N"""
import sys, numpy as np
sys.path.insert(0,'/home/user/erdos-watts/experiments/src')
from greedy import generate, sieve
N=int(sys.argv[1])
seq=generate(N+1)
L=8*N+1000; isp=sieve(L); primes=np.flatnonzero(isp)
used=np.zeros(L+2,bool); used[1]=True
# holes of each parity <= n at time n ; maintain counts
Hp=[0,0]  # unused values <= n by parity
# after n=1: values<=1: 1 used -> no holes
maxH=0; maxR3=0; sumC=0; sumDup=0; maxC=0
for n in range(1,N+1):
    a=int(seq[n-1]); nxt=int(seq[n]); par=(n+1)&1
    H=Hp[par]
    tp=a+n+1
    k=np.searchsorted(primes,tp)
    r3=int(primes[k+H])-tp
    dup=nxt-(n+1)
    assert dup<=r3,(n,dup,r3)
    maxR3=max(maxR3,r3); maxH=max(maxH,H)
    C=Hp[0]+Hp[1]; sumC+=C; maxC=max(maxC,C)
    # step to n+1: add value n+1 to range, use nxt
    used[nxt]=True
    if nxt<=n: Hp[nxt&1]-=1
    if not used[n+1]: Hp[(n+1)&1]+=1
    sumDup+=max(nxt-(n+1),0)
print('N',N,'max H_par',maxH,'max C(n)',maxC,'mean C(n)',sumC/N,'sum Dup+',sumDup,'sum C',sumC,'max R3 bound',maxR3)
