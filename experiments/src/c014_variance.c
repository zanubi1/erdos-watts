// C014 numerical check of (G*): for every even h <= Z compute
//   R_Y(h) = sum_{n<=Y} Lambda(n) Lambda(n+h),  Y = floor(Z/(ln Z)^2),
// and compare with S(h) Y, S(h) = 2 C2 prod_{p|h, p>2} (p-1)/(p-2).
// Reports the normalised variance V/(Z Y^2/2) (mean over even h of ((R-SY)/Y)^2),
// max |R/(SY)-1|, counts of h with |R-SY| > Y/(ln Z)^A for A = 0.5,1,1.5,2,
// the same with the "count" r_Y(h) = #{p<=Y : p+h prime}, and min r_Y.
// Build: gcc -O3 -march=native -fopenmp c014_variance.c -o c014 -lm
// Run:   ./c014 Z
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <omp.h>
int main(int argc,char**argv){
  long Z=atol(argv[1]); double L=log((double)Z);
  long Y=(long)(Z/(L*L)); long N=Z+Y+2;
  // smallest prime factor sieve up to N
  unsigned *spf=calloc(N+1,sizeof(unsigned));
  for(long i=2;i<=N;i++) if(!spf[i]){ for(long j=i;j<=N;j+=i) if(!spf[j]) spf[j]=i; }
  float *lam=calloc(N+1,sizeof(float)); char *isp=calloc(N+1,1);
  for(long i=2;i<=N;i++){ long p=spf[i], m=i; while(m%p==0) m/=p; if(m==1) lam[i]=(float)log((double)p); if(spf[i]==i) isp[i]=1; }
  // list of prime powers <= Y
  long npp=0; long *pp=malloc(sizeof(long)*(Y+1)); for(long n=2;n<=Y;n++) if(lam[n]>0) pp[npp++]=n;
  long nh=Z/2; double *R=calloc(nh+1,sizeof(double)); int *r=calloc(nh+1,sizeof(int));
  long BLK=1<<14;
  #pragma omp parallel for schedule(dynamic)
  for(long b=1;b<=nh;b+=BLK){
    long e=b+BLK-1; if(e>nh) e=nh;
    for(long i=0;i<npp;i++){ long n=pp[i]; double ln=lam[n]; int prime=isp[n];
      for(long k=b;k<=e;k++){ long m=n+2*k; R[k]+=ln*lam[m]; if(prime && isp[m]) r[k]++; } }
  }
  const double C2=0.66016181584686957392781211;
  double As[4]={0.5,1,1.5,2}; long bad[4]={0}, badr[4]={0};
  double V=0,Vr=0, maxdev=0; long hmax=0; int minr=1<<30; long hminr=0; double sumS=0;
  for(long k=1;k<=nh;k++){ long h=2*k; double S=2*C2; long m=h; while(m%2==0) m/=2;
    while(m>1){ long p=spf[m]; S*=(double)(p-1)/(p-2); while(m%p==0) m/=p; }
    sumS+=S;
    double d=R[k]-S*Y; V+=d*d;
    // count-based analogue: r_Y(h) vs S(h) * sum_{p<=Y} 1/log(p+h) approx S*Y/(log Y log(h+Y/2))
    double main_r=S*Y/(log((double)Y)*log((double)h+Y/2.0));
    double dr=r[k]-main_r; Vr+=(dr/main_r)*(dr/main_r);
    double rel=fabs(R[k]/(S*Y)-1); if(rel>maxdev){maxdev=rel;hmax=h;}
    for(int a=0;a<4;a++){ if(fabs(d)>Y/pow(L,As[a])) bad[a]++; }
    if(r[k]<minr){minr=r[k];hminr=h;}
  }
  printf("Z=%ld Y=%ld lnZ=%.3f #primepowers<=Y=%ld #even h=%ld\n",Z,Y,L,npp,nh);
  printf("mean S(h) over even h = %.6f (theory: 2)\n",sumS/nh);
  printf("normalised variance  mean ((R-SY)/Y)^2 = %.6e   (sqrt = %.4e)\n",V/nh/((double)Y*Y),sqrt(V/nh)/Y);
  printf("  compare 1/(log Z)^2 = %.4e, log(Z)/Y (random model ~ S log^2/Y) = %.4e\n",1/(L*L),L/Y);
  printf("max |R/(SY)-1| = %.4f at h=%ld\n",maxdev,hmax);
  for(int a=0;a<4;a++) printf("  #{h: |R-SY| > Y/(lnZ)^%.1f = %.1f} = %ld\n",As[a],Y/pow(L,As[a]),bad[a]);
  printf("count version: mean ((r - S Y/(logY log h))/main)^2 = %.4e ; min r_Y(h) = %d at h=%ld\n",Vr/nh,minr,hminr);
  return 0;
}
