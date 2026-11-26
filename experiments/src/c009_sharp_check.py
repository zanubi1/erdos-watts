"""Checks for C009 sharpening (C009'), the frontier variant C009-t, and the K tail. Scratch-quality, 2026-11-25 (prover). Run: python experiments/src/c009_sharp_check.py  (~5 min, needs overshoot_1e7/sequence.npy)"""
import numpy as np, sys
a=np.load("/home/user/erdos-watts/experiments/results/overshoot_1e7/sequence.npy").astype(np.int64)
N=len(a); M=int(a.max())
isp=np.ones(2*M+10,bool); isp[:2]=False
for i in range(2,int((2*M+10)**.5)+1):
    if isp[i]: isp[i*i::i]=False
pi=np.cumsum(isp)
fi=np.full(M+2,N+1,np.int64); fi[a]=np.arange(1,N+1)
# H_p(m) for m in 1..N : x<=m, x≡p, fi(x)>m  -> x contributes on [x, fi(x)-1]
Hp=[None,None]
for p in (0,1):
    d=np.zeros(N+3,np.int64)
    xs=np.arange(1,N+1); xs=xs[(xs%2)==p]
    f=np.minimum(fi[xs],N+1)
    m=f>xs
    np.add.at(d,xs[m],1); np.add.at(d,f[m],-1)
    Hp[p]=np.cumsum(d)  # Hp[p][m]
H=Hp[0]+Hp[1]
# holes v with fi(v)<=N, v>=2, fi(v)>v
v=np.arange(2,N+1); f=fi[v]; sel=(f>v)&(f<=N); v=v[sel]; f=f[sel]; n=f-1
K=pi[n+v]-pi[2*v]
eps=v%2
rhs_old=1+(Hp[0][v]*(eps==0)+Hp[1][v]*(eps==1)-1)+ np.where(eps==0,Hp[1][v-1],Hp[0][v-1]) + np.where(eps==0,Hp[1][n],Hp[0][n])
rhs_new=H[v]+np.where(eps==0,Hp[1][n],Hp[0][n])
print("holes",len(v),"viol old",(K>rhs_old).sum(),"viol new",(K>rhs_new).sum(),"old==new",(rhs_old==rhs_new).all())
# identity checks H_{1-e}(v-1)==H_{1-e}(v)
o1=np.where(eps==0,Hp[1][v-1],Hp[1][v]); o2=np.where(eps==0,Hp[1][v],Hp[1][v])
print("H_{1-e}(v-1)==H_{1-e}(v):", (np.where(eps==0,Hp[1][v-1]==Hp[1][v],Hp[0][v-1]==Hp[0][v])).all())
print("K distribution:",np.bincount(K))
for lo,hi in [(1e3,1e4),(1e4,1e5),(1e5,1e6),(1e6,1e7)]:
    s=(v>=lo)&(v<hi); b=np.bincount(K[s],minlength=10)/s.sum()
    print(int(lo),"P(K>=k) k=3..8:",[f"{b[k:].sum():.2e}" for k in range(3,9)])
print("max K/H(v)+.. ratio K/rhs_new", (K/rhs_new).max())
eq=K==rhs_new
print("equality count",eq.sum(),"max K at equality",K[eq].max(), "examples", list(zip(v[eq][:5],n[eq][:5],K[eq][:5])))
big=eq&(K>=2); print("eq with K>=2:",big.sum(), list(zip(v[big][-5:],n[big][-5:],K[big][-5:])))
print("max v with equality", v[eq].max())
for lo,hi in [(1,3),(3,5),(5,10),(10,20),(20,40),(40,100)]:
    s=(rhs_new>=lo)&(rhs_new<hi)
    if s.sum(): print("rhs in",lo,hi,"count",s.sum(),"max K",K[s].max(),"max K/rhs %.3f"%(K[s]/rhs_new[s]).max(), "mean K %.2f"%K[s].mean())
print("H at equality max", rhs_new[eq].max())
# frontier version: T0 = max(v, s(v)), s(v)=max fi(w), w<v same parity
fiv=np.minimum(fi[:N+1],N+1).copy(); fiv[0]=0
s=np.zeros(N+1,np.int64)
for p in (0,1):
    idx=np.arange(p if p else 2,N+1,2) if p==0 else np.arange(1,N+1,2)
    if p==0: idx=np.arange(2,N+1,2)
    rm=np.maximum.accumulate(fiv[idx]); s[idx[1:]]=rm[:-1]
T0=np.maximum(v,s[v]); ok=T0<=n
vv,nn,tt,ee=v[ok],n[ok],T0[ok],eps[ok]
lhs=pi[nn+vv]-pi[tt+vv]
rhs=1+np.where(ee==0,Hp[1][tt-1],Hp[0][tt-1])+np.where(ee==0,Hp[1][nn],Hp[0][nn])
print("frontier holes",ok.sum(),"viol",(lhs>rhs).sum(),"max lhs",lhs.max(),"max rhs",rhs.max(), "eq count",(lhs==rhs).sum())
