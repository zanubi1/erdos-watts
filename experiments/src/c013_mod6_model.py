# Q-greedy with a pseudo-prime set Q inside 1 mod 6, spaced ~ log t (stronger than Cramer).
import math
LIM=4_000_000
Q=bytearray(LIM+1)
t=7.0
while t<LIM:
    s=int(t); s+= (1-s)%6   # next s >= t with s = 1 mod 6
    if s<=LIM: Q[s]=1
    t+=math.log(t)
# interval statistics check
import random
worst=0
for _ in range(2000):
    x=random.randrange(10**5,LIM-20000); y=int(math.log(x)**2.5)
    cnt=sum(Q[x+1:x+y+1]); exp=y/math.log(x)
    worst=max(worst,abs(cnt/exp-1))
gaps=[]; last=None
for s in range(LIM+1):
    if Q[s]:
        if last: gaps.append((s-last)/math.log(s)**1)
        last=s
print("max |count/expected - 1| on random intervals of length log^2.5 x:",round(worst,3),"; max gap/log x:",round(max(gaps[100:]),2))
N=20000
used=set([1]); a=1; seq=[1]
for n in range(N-1):
    x=1
    while x in used or not Q[a+x]: x+=1
    used.add(x); seq.append(x); a=x
miss=[v for v in range(1,60) if v not in used]
print("first terms:",seq[:20])
print("values < 60 missing after",N,"terms:",miss)
print("residues mod 6 of used values:",sorted(set(v%6 for v in used)))
