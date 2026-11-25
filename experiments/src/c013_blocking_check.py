# Finite-time check of the blocking lemma used in C013:
# if m is unused at time n and k <= n-1 has a(k)+m prime, then a(k+1) < m.
# Hence for any set S of values unused at time n: #{k<=n-1 : exists m in S, a(k)+m prime} <= max(S)-1.
import numpy as np, sys
a=np.load('/home/user/erdos-watts/experiments/results/overshoot_1e7/sequence.npy')[:2_000_000]
assert list(a[:11])==[1,2,3,4,7,6,5,8,9,10,13]
N=len(a); lim=int(a.max())*2+10
isp=np.ones(lim+1,bool); isp[:2]=False
for i in range(2,int(lim**.5)+1):
    if isp[i]: isp[i*i::i]=False
fi=np.full(int(a.max())+2, 10**12, dtype=np.int64); fi[a]=np.arange(1,N+1)
viol=0; tested=0
for n in list(range(1000,2000000,99991))+[1999000]:
    # S = all values m <= n+300 unused at time n (holes plus unused values above n)
    S=np.array([m for m in range(1, n+1) if fi[m]>n])
    ak=a[:n-1]; ak1=a[1:n]   # a(k), a(k+1) for k=1..n-1
    blocked=np.zeros(n-1,bool)
    for m in S:
        hit=isp[ak+m]
        bad=hit & (ak1>=m)
        viol+=int(bad.sum()); blocked|=hit
        tested+=int(hit.sum())
    nb=int(blocked.sum())
    print(f"n={n}: |S|={len(S)}, maxS={S.max()}, #blocked k={nb} <= maxS-1: {nb<=S.max()-1}")
print("pairs (k,m) with a(k)+m prime tested:",tested,"violations of a(k+1)<m:",viol)
