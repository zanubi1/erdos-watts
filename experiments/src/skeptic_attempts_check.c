/* Skeptic checker (independent of prover scripts).
   ./chk N A1 MODE   MODE=0: all (v,n) hole pairs; MODE=1: only n=fi(v)-1 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#define INF 0x7fffffff
static long N; static int A1, MODE;
static int32_t *a, *fi, *pic, *primes, *Mpre; static uint8_t *isp; static int16_t *H0,*H1;
static long PLIM;
static inline int Hp(int p,long m){ return m<1?0:(p?H1[m]:H0[m]); }
static inline long PI(long x){ return x<0?0:pic[x]; }
int main(int argc,char**argv){
  N=atol(argv[1]); A1=atoi(argv[2]); MODE=atoi(argv[3]);
  long VMAX=N+200000+A1; PLIM=3*N+1000000+2*A1;
  isp=calloc(PLIM+1,1); for(long i=2;i<=PLIM;i++)isp[i]=1;
  for(long i=2;i*i<=PLIM;i++) if(isp[i]) for(long j=i*i;j<=PLIM;j+=i) isp[j]=0;
  pic=malloc(4*(PLIM+1)); long np=0; for(long i=0;i<=PLIM;i++){ if(isp[i])np++; pic[i]=np; }
  primes=malloc(4*np); np=0; for(long i=0;i<=PLIM;i++) if(isp[i]) primes[np++]=i;
  a=malloc(4*(N+2)); fi=calloc(VMAX+1,4); uint8_t*used=calloc(VMAX+1,1);
  int32_t *ustar=malloc(4*(N+2));
  long low[2]={2,1}; a[1]=A1; used[A1]=1; fi[A1]=1;
  for(int p=0;p<2;p++) while(used[low[p]]) low[p]+=2;
  for(long n=1;n<N+1;n++){ long cur=a[n]; int par=1-(cur&1); ustar[n]=low[par];
    long x=low[par]; while(used[x]||!isp[cur+x]){ x+=2; if(x>=VMAX){fprintf(stderr,"VMAX\n");exit(1);} }
    a[n+1]=x; used[x]=1; fi[x]=n+1; while(used[low[par]]) low[par]+=2; }
  /* a[1..N+1] known; treat fi>N as infinity for hole purposes up to time N */
  for(long v=0;v<=VMAX;v++) if(fi[v]==0||fi[v]>N) fi[v]=INF;
  /* ---- R1 / R2 ---- */
  long r1A_last=0,r1A_cnt=0,r1B_last=0,r1B_cnt=0,r1C_last=0,r1C_cnt=0,r1D_last=0,r1D_cnt=0; long r2i_bad=0,r2ii_bad=0,r2ii_n=0,cp_bad=0,parbad=0;
  long maxO=0,maxDlo=0,maxDup=0; double maxratioA=0; long ratioA_n=0;
  for(long n=1;n<=N;n++){ long u=ustar[n]; if(((n+1-u)&1)!=0||u>n+1) parbad++;
    long O=(n+1-u)/2, t=a[n]+u, K=O+1; long q=primes[pic[t-1]+K-1];
    long dup=a[n+1]-(n+1), dlo=-dup; if(O>maxO)maxO=O; if(dlo>maxDlo)maxDlo=dlo; if(dup>maxDup)maxDup=dup;
    if(dup> q-t-2*O) cp_bad++;
    if(n>=3){ double ln=log((double)n); double bnd=pow(n,0.61)+3.0*K*ln, b53=pow(n,0.53)+3.0*K*ln;
      if(dup>bnd){r1A_cnt++;r1A_last=n;} if(q-t>bnd){r1B_cnt++;r1B_last=n;}
      if(q-t>b53){r1C_cnt++;r1C_last=n;}
      double r=(q-t)/bnd; if(r>maxratioA){maxratioA=r;ratioA_n=n;}
      double Z=3.0*fmax(fmax((double)t,2.0*n*log((double)(t+n))),1e6); double d=pow(Z,0.6)+2.0*K*log(Z);
      if(q-t>d){r1D_cnt++;r1D_last=n;} }
    if(dlo>2*O) r2i_bad++;
    long k=fi[u]; if(k!=INF){ r2ii_n++; if(!(k>n && k-u>=2*O)) r2ii_bad++; } }
  printf("N=%ld a1=%d\n(b') parity/frontier failures: %ld\nL006(c') failures: %ld\n",N,A1,parbad,cp_bad);
  printf("R1 Dup(n+1) > n^.61+3K ln n: count %ld last n %ld\nR1 q_K-t_n > n^.61+3K ln n: count %ld last n %ld; max ratio (q_K-t)/bound %.3f at n=%ld\n",r1A_cnt,r1A_last,r1B_cnt,r1B_last,maxratioA,ratioA_n);
  printf("R1(0.53) q_K-t_n > n^.53+3K ln n: count %ld last %ld\nR1 step2 q_K-t > Z^.6+2K lnZ: count %ld last %ld\n",r1C_cnt,r1C_last,r1D_cnt,r1D_last);
  printf("R2(i) Dlo(n+1)>2O*(n): %ld\nR2(ii) checked %ld, failures %ld\nmax O*=%ld 2maxO*=%ld maxDlo=%ld maxDup=%ld\n",r2i_bad,r2ii_n,r2ii_bad,maxO,2*maxO,maxDlo,maxDup);
  /* ---- holes sweep ---- */
  H0=calloc(N+2,2); H1=calloc(N+2,2); Mpre=malloc(4*(N+2)); Mpre[0]=0; for(long m=1;m<=N;m++) Mpre[m]= a[m]>Mpre[m-1]?a[m]:Mpre[m-1];
  int32_t *off=malloc(4*(N+2)); uint8_t *len=calloc(N+2,1); long poolcap=1<<20, pooln=0; int32_t *pool=malloc(4*poolcap);
  int hs[4096]; int hn=0; /* hole set at current time */
  long l9bad=0,pairs=0, p2bad[5]={0},p2eq[5]={0},p2cnt[5]={0}; long p2maxdiff[5]; for(int i=0;i<5;i++)p2maxdiff[i]=-1000000;
  long p2maxL[5]={0}, p6bad=0,p6cnt=0,p6eq=0,p6maxL=0, bidbad=0;
  long p5gen=0,p5bad=0, lossF_bound=0, lossF_inner=0, loss_total=0; long maxH=0;
  for(long m=1;m<=N;m++){
    /* transition from time m-1 to m: a[m] is used at time m. P5 checks use holes at time m-1 */
    long w=a[m];
    if(m>=2){ for(int i=0;i<hn;i++){ long v=hs[i]; if(v==w||v<2) continue; if(!isp[v+w]) continue;
        /* v hole at time m, v+a(m) prime */
        p5gen++; long nx=a[m+1]; if(nx>v) p5bad++; else if(nx!=v){ if(!(nx<v && ((nx^v)&1)==0 && nx<=m)) p5bad++; }
        if(w<=m-1 && v<w){ /* w left Late(v,.) at step m-1 -> m */ loss_total++;
          int B=0; for(int j=0;j<len[v];j++) if(pool[off[v]+j]>m-1) B++;
          if(B==0){ if(a[m+1]==v) lossF_bound++; else { lossF_inner++; printf("inner loss: m=%ld v=%ld w=%ld a(m+1)=%d fi(v)=%d\n",m,v,w,a[m+1],fi[v]); } } } } }
    /* update hole set */
    if(w<m){ for(int i=0;i<hn;i++) if(hs[i]==w){ hs[i]=hs[--hn]; break; } }
    if(fi[m]>m){ hs[hn++]=m; long v=m; int e=v&1; off[v]=pooln; int c=0;
      for(int i=0;i<hn;i++){ long x=hs[i]; if(x<v && (x&1)==e){ if(pooln>=poolcap){poolcap*=2;pool=realloc(pool,4*poolcap);} pool[pooln++]=fi[x]; c++; } }
      len[v]=c; }
    int h0=0,h1=0; for(int i=0;i<hn;i++){ if(hs[i]&1)h1++; else h0++; } H0[m]=h0;H1[m]=h1; if(hn>maxH)maxH=hn;
    /* pair checks at time n=m */
    long n=m; if(n<2) continue;
    long uopp[2]={n+1,n+1}; for(int i=0;i<hn;i++){ int p=hs[i]&1; if(hs[i]<uopp[p]) uopp[p]=hs[i]; }
    for(int i=0;i<hn;i++){ long v=hs[i]; if(v<2) continue; if(MODE==1 && fi[v]!=n+1) continue; int e=v&1; pairs++;
      long K=PI(n+v)-PI(2*v); if(K> (Hp(0,v)+Hp(1,v)) + Hp(1-e,n)) l9bad++;
      if(len[v]+1 != Hp(e,v)) bidbad++;
      long tau=v; for(int j=0;j<len[v];j++){ long f=pool[off[v]+j]; if(f>tau) tau=f; }
      long ts[5]={v,(v+n)/2,n-1,tau, v+ (long)((((unsigned long)(v*2654435761u))^n) % (unsigned long)(n-v+1))};
      for(int s=0;s<5;s++){ long t=ts[s]; if(t<v||t>n) continue; int B=0; for(int j=0;j<len[v];j++) if(pool[off[v]+j]>t) B++;
        if(s==3 && B!=0){ printf("tau B!=0 ??\n"); }
        long L=PI(n+v)-PI(t+v), R=Hp(1-e,t-1)+B+1+Hp(1-e,n); p2cnt[s]++;
        if(L>R) p2bad[s]++; if(L==R) p2eq[s]++; if(L-R>p2maxdiff[s]) p2maxdiff[s]=L-R; if(L>p2maxL[s]) p2maxL[s]=L; }
      long lo=2*v; if(v+Mpre[v-1]>lo) lo=v+Mpre[v-1]; long hi=v+uopp[1-e]-1; if(n+v<hi) hi=n+v;
      long L6= hi>lo? PI(hi)-PI(lo):0; p6cnt++; if(L6>Hp(e,v)) p6bad++; if(L6==Hp(e,v)) p6eq++; if(L6>p6maxL) p6maxL=L6; }
  }
  printf("maxH=%ld pairs=%ld L009' failures=%ld  B(v)+1!=H_e(v): %ld\n",maxH,pairs,l9bad,bidbad);
  const char*nm[5]={"t=v","t=mid","t=n-1","t=tau(frontier)","t=pseudo-random"};
  for(int s=0;s<5;s++) printf("P2 %-16s checked %ld fail %ld equal %ld max(L-R) %ld maxL %ld\n",nm[s],p2cnt[s],p2bad[s],p2eq[s],p2maxdiff[s],p2maxL[s]);
  printf("P6 checked %ld fail %ld equal %ld maxL %ld\n",p6cnt,p6bad,p6eq,p6maxL);
  printf("P5 generic events %ld failures %ld\nLate losses %ld; with v frontier: at last step (fi(v)=step+1) %ld, strictly inside %ld\n",p5gen,p5bad,loss_total,lossF_bound,lossF_inner);
  return 0; }
