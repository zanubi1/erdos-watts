// For even h <= Z, count r_Y(h) = #{p prime <= Y : h+p prime}, capped at CAP.
// Report histogram of min(r,CAP) and the worst h, for Y = Z/(ln Z)^2 and Y = (ln Z)^3.
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
int main(int argc,char**argv){
  long Z=atol(argv[1]); int CAP=atoi(argv[2]); double ymode=atof(argv[3]);
  double L=log((double)Z);
  long Y = ymode<=0 ? (long)(Z/(L*L)) : (long)pow(L,ymode);
  long lim=Z+Y+10; char*c=calloc(lim+1,1);
  for(long i=2;i<=lim;i++) c[i]=1;
  for(long i=2;i*i<=lim;i++) if(c[i]) for(long j=i*i;j<=lim;j+=i) c[j]=0;
  long np=0; long*P=malloc(sizeof(long)*(Y+1));
  for(long p=3;p<=Y;p++) if(c[p]) P[np++]=p;
  long hist[1000]; memset(hist,0,sizeof hist); long worst=-1; int wr=1<<30;
  for(long h=2;h<=Z;h+=2){ int r=0; for(long i=0;i<np && r<CAP;i++) if(c[h+P[i]]) r++;
    hist[r]++; if(r<wr){wr=r;worst=h;} }
  printf("Z=%ld Y=%ld (#odd primes<=Y = %ld) CAP=%d\n",Z,Y,np,CAP);
  for(int r=0;r<=CAP;r++) if(hist[r]) printf("  r=%d%s : %ld h\n",r,r==CAP?"+":"",hist[r]);
  printf("  min r = %d at h=%ld\n",wr,worst);
}
