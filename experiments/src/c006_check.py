"""C006 check: asserts (a), b<=O*, (b), (b') O*=(n+1-u*)/2, identity (E), (c'), (c), Dlo(n+1)<=2O*(n) for n<=N.
Usage: python experiments/src/c006_check.py N   (10^7 takes ~50 s)"""
import sys, numpy as np
sys.path.insert(0,'/home/user/erdos-watts/experiments/src')
from greedy import generate, sieve
N=int(sys.argv[1])
seq=generate(N+1)  # a(1..N+1)
L=8*N+1000; isp=sieve(L)
primes=np.flatnonzero(isp)
used=np.zeros(L+2,bool); low=[2,1]
used[1]=True; low[1]=3
cnt=[0,1]  # used counts per parity
maxc=0; maxref=0; maxdup=0; bad=0; tight=0
for n in range(1,N+1):
    a=int(seq[n-1]); nxt=int(seq[n])
    par=1-(a&1)
    assert (n+1)%2==par
    us=low[par]
    assert us<=n+1
    Ostar=cnt[par]-((us-1)//2 if par==1 else (us-2)//2)  # used of parity par above us
    assert 2*Ostar==n+1-us, (n,Ostar,us)
    t=a+us; assert t>=3 and t%2==1
    k=np.searchsorted(primes,t)  # q_1 = primes[k]
    s=a+nxt; j=np.searchsorted(primes,s); assert primes[j]==s
    b=j-k
    for i in range(k,j): assert used[primes[i]-a] and primes[i]-a>us
    assert b<=Ostar
    dup=nxt-(n+1)
    cb=int(primes[k+Ostar])-t
    ref=cb-2*Ostar
    assert dup<=ref<=cb
    assert dup==int(primes[j])-t-2*Ostar
    assert n+1-nxt<=2*Ostar
    maxc=max(maxc,cb); maxref=max(maxref,ref); maxdup=max(maxdup,dup)
    # update
    used[nxt]=True; cnt[par]+=1
    if nxt==us:
        y=us
        while used[y]: y+=2
        low[par]=y
print('ok N',N,'max (c) bound',maxc,'max refined',maxref,'max dup',maxdup)
