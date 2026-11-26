/* Level crossings of the Watts greedy sequence (A055265), used by crossings.py.
 *
 * Reads seq.i32, fi.i32, h0.i16, h1.i16, isp.u8, meta.txt (written by k_survival_1e8_gen.c) from WORKDIR.
 *
 * Build:  gcc -O2 -o crossings_gen crossings_gen.c
 * Run:    ./crossings_gen WORKDIR
 *
 * Down-crossing of level v at time j (2 <= j <= N):  a(j-1) > v > a(j).   Up-crossing: a(j-1) < v < a(j).
 * Levels v = 2..N are tracked.
 *
 * Per-level outputs (index v = 0..N, int16):
 *   L_Xd.i16  total down-crossings X_v(N)       L_Xu.i16  total up-crossings
 *   L_dmin.i16 / L_dmax.i16   min / max of (j - v) over down-crossings (32767 / -32768 if none)
 *   L_fmin.i16 / L_fmax.i16   min / max of (j - fi(v)) over down-crossings (only if fi(v) > 0)
 *   L_Xpre.i16 down-crossings with j < fi(v) (j <= N if fi(v) = 0)
 * Per-time outputs (index j-1 for j = 1..N, int16):
 *   T_ostar.i16  O*(j) = (j + 1 - u*(j)) / 2 (L006), u*(j) = smallest unused value of parity j+1 at time j
 *   T_gap.i16    j - umin(j), umin(j) = smallest unused value at time j
 * Per-time down-crossing class (uint8, index j-1): 0 not a down step; 1 a(j) < a(j-1) and a(j) <= j-1
 *   (hole fill); 2 a(j) < a(j-1) and a(j) >= j (frontier value).  -> T_down.u8
 * Per-hole outputs (hole: 2 <= v <= N, fi(v) > v or fi(v) = 0; n = fi(v) - 1 or N):
 *   H_v.i32, H_n.i32
 *   H_rec.i16  NF shorts per hole, see FIELDS below.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static void *rd(const char *dir, const char *name, size_t *cnt, size_t sz) {
    char path[4096]; snprintf(path, sizeof path, "%s/%s", dir, name);
    FILE *f = fopen(path, "rb"); if (!f) { perror(path); exit(1); }
    fseek(f, 0, SEEK_END); long len = ftell(f); fseek(f, 0, SEEK_SET);
    void *p = malloc(len); if (!p) { perror("malloc"); exit(1); }
    if (fread(p, 1, len, f) != (size_t)len) { perror("fread"); exit(1); }
    fclose(f); *cnt = len / sz; return p;
}
static FILE *op(const char *dir, const char *name) {
    char path[4096]; snprintf(path, sizeof path, "%s/%s", dir, name);
    FILE *f = fopen(path, "wb"); if (!f) { perror(path); exit(1); } return f;
}
static void wr(const char *dir, const char *name, const void *p, size_t sz, size_t cnt) {
    FILE *f = op(dir, name); fwrite(p, sz, cnt, f); fclose(f);
}

enum { F_K, F_W1, F_W2, F_W3, F_W4, F_X, F_XEPS, F_E, F_EEPS, F_L, F_FFRONT,
       F_HV, F_HV1, F_H1EN, F_H1EV1, F_BV, F_AV, F_LFILL, F_LFILLEPS, F_U, F_NVN,
       F_MAXO, F_XTOT, F_NMV, F_MMV, F_HFILLE, NF };
/* FIELDS:
 *  K, W1..W4         partner classes of L009 (as in partners_gen.c)
 *  X                 X_v(n);  XEPS = those with a(j) = v (mod 2)
 *  E                 down-crossings with j <= v;  EEPS = those with a(j) = v (mod 2)
 *  L                 down-crossings with v < j <= n
 *  FFRONT            down-crossings j <= n with a(j) >= j (lands on a frontier value in [j, v))
 *  HV, HV1           H(v), H(v-1);  H1EN = H_{1-eps}(n);  H1EV1 = H_{1-eps}(v-1);  BV = B(v) = H_eps(v) - 1
 *  AV                #{k <= v-1 : a(k) > v}
 *  LFILL             #{x < v : x unused at time v, v < fi(x) <= n};  LFILLEPS same with x = v (mod 2)
 *  U                 up-crossings with j <= n
 *  NVN               #{k <= n : a(k) > v}
 *  MAXO              max O*(j-1) over down-crossing times j <= n (-1 if none)
 *  XTOT              X_v(N)
 *  NMV               n - v;  MMV = max a(1..v-1) - v
 *  HFILLE            early (j <= v) down-crossings that are hole fills (a(j) <= j-1)
 */

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s WORKDIR\n", argv[0]); return 1; }
    const char *dir = argv[1];
    long N, VMAX, PLIM, maxa;
    { char p[4096]; snprintf(p, sizeof p, "%s/meta.txt", dir); FILE *f = fopen(p, "r");
      if (fscanf(f, "%ld %ld %ld %ld", &N, &VMAX, &PLIM, &maxa) != 4) return 1; fclose(f); }
    size_t c;
    int32_t *seq = rd(dir, "seq.i32", &c, 4);
    int32_t *fi = rd(dir, "fi.i32", &c, 4);
    int16_t *h0 = rd(dir, "h0.i16", &c, 2), *h1 = rd(dir, "h1.i16", &c, 2);
    uint8_t *isp = rd(dir, "isp.u8", &c, 1);
#define A(j) ((long)seq[(j) - 1])
#define HP(p, m) ((p) ? h1[(m) - 1] : h0[(m) - 1])

    /* per-time: O*(j), gap, down class */
    int16_t *ostar = malloc(2 * N), *gap = malloc(2 * N);
    uint8_t *dcl = calloc(N, 1);
    {
        uint8_t *used = calloc(VMAX + 2, 1);
        long low[2] = {2, 1};
        for (long j = 1; j <= N; j++) {
            long x = A(j); used[x] = 1;
            if (x == low[x & 1]) { long y = x; while (used[y]) y += 2; low[x & 1] = y; }
            long par = (j + 1) & 1;
            ostar[j - 1] = (int16_t)((j + 1 - low[par]) / 2);
            long um = low[0] < low[1] ? low[0] : low[1];
            gap[j - 1] = (int16_t)(j - um);
            if (j >= 2 && x < A(j - 1)) dcl[j - 1] = (x <= j - 1) ? 1 : 2;
        }
        free(used);
    }
    wr(dir, "T_ostar.i16", ostar, 2, N);
    wr(dir, "T_gap.i16", gap, 2, N);
    wr(dir, "T_down.u8", dcl, 1, N);

    size_t L1 = N + 1;
    int16_t *Xd = calloc(L1, 2), *Xu = calloc(L1, 2), *Xpre = calloc(L1, 2);
    int16_t *dmin = malloc(2 * L1), *dmax = malloc(2 * L1), *fmin = malloc(2 * L1), *fmax = malloc(2 * L1);
    for (size_t v = 0; v < L1; v++) { dmin[v] = fmin[v] = 32767; dmax[v] = fmax[v] = -32768; }
    /* hole-only per-level counters */
    int16_t *hXe = calloc(L1, 2), *hE = calloc(L1, 2), *hEe = calloc(L1, 2), *hFf = calloc(L1, 2),
            *hU = calloc(L1, 2), *hMO = malloc(2 * L1), *hHF = calloc(L1, 2);
    for (size_t v = 0; v < L1; v++) hMO[v] = -1;
    long histd[4001] = {0}, histf[8001] = {0};

    for (long j = 2; j <= N; j++) {
        long p = A(j - 1), x = A(j);
        if (p > x) {           /* down step: levels v in (x, p) */
            long hi = p - 1 < N ? p - 1 : N;
            for (long v = x + 1; v <= hi; v++) {
                if (v < 2) continue;
                Xd[v]++;
                long d = j - v; if (d < dmin[v]) dmin[v] = d; if (d > dmax[v]) dmax[v] = d;
                long hd = d + 2000; if (hd < 0) hd = 0; if (hd > 4000) hd = 4000; histd[hd]++;
                long f = fi[v];
                if (f > 0) { long e = j - f; if (e < fmin[v]) fmin[v] = e; if (e > fmax[v]) fmax[v] = e;
                             long he = e + 4000; if (he < 0) he = 0; if (he > 8000) he = 8000; histf[he]++; }
                if (f == 0 || j < f) {
                    Xpre[v]++;
                    if (f == 0 || f > v) {   /* hole, and j <= n */
                        int ep = ((x & 1) == (v & 1));
                        if (ep) hXe[v]++;
                        if (j <= v) { hE[v]++; if (ep) hEe[v]++; if (x <= j - 1) hHF[v]++; }
                        if (x >= j) hFf[v]++;
                        if (ostar[j - 2] > hMO[v]) hMO[v] = ostar[j - 2];
                    }
                }
            }
        } else {               /* up step: levels v in (p, x) */
            long hi = x - 1 < N ? x - 1 : N;
            for (long v = p + 1; v <= hi; v++) {
                if (v < 2) continue;
                Xu[v]++;
                long f = fi[v];
                if ((f == 0 || f > v) && (f == 0 || j < f)) hU[v]++;
            }
        }
    }
    wr(dir, "L_Xd.i16", Xd, 2, L1); wr(dir, "L_Xu.i16", Xu, 2, L1); wr(dir, "L_Xpre.i16", Xpre, 2, L1);
    wr(dir, "L_dmin.i16", dmin, 2, L1); wr(dir, "L_dmax.i16", dmax, 2, L1);
    wr(dir, "L_fmin.i16", fmin, 2, L1); wr(dir, "L_fmax.i16", fmax, 2, L1);
    { FILE *f = op(dir, "hist_jmv.i64"); fwrite(histd, 8, 4001, f); fclose(f); }
    { FILE *f = op(dir, "hist_jmfi.i64"); fwrite(histf, 8, 8001, f); fclose(f); }
    free(dmin); free(dmax); free(fmin); free(fmax); free(Xu);

    FILE *fv = op(dir, "H_v.i32"), *fn = op(dir, "H_n.i32"), *fr = op(dir, "H_rec.i16");
    long M = 0, nh = 0;
    for (long v = 2; v <= N; v++) {
        if (A(v - 1) > M) M = A(v - 1);
        long f = fi[v];
        if (!(f == 0 || f > v)) continue;
        long n = (f == 0) ? N : f - 1;
        int eps = v & 1;
        int W[5] = {0};
        for (long w = v + 1; w <= n; w += 2) {
            if (!isp[w + v]) continue;
            long g = fi[w]; int cl;
            if (g == 0 || g > n) cl = 4; else if (g == n) cl = 3; else if (g >= v) cl = 2; else cl = 1;
            W[cl]++;
        }
        int16_t r[NF];
        r[F_K] = W[1] + W[2] + W[3] + W[4]; r[F_W1] = W[1]; r[F_W2] = W[2]; r[F_W3] = W[3]; r[F_W4] = W[4];
        r[F_X] = Xpre[v]; r[F_XEPS] = hXe[v]; r[F_E] = hE[v]; r[F_EEPS] = hEe[v]; r[F_L] = Xpre[v] - hE[v];
        r[F_FFRONT] = hFf[v];
        r[F_HV] = h0[v - 1] + h1[v - 1]; r[F_HV1] = h0[v - 2] + h1[v - 2];
        r[F_H1EN] = HP(1 - eps, n); r[F_H1EV1] = HP(1 - eps, v - 1); r[F_BV] = HP(eps, v) - 1;
        int av = 0;
        for (long k = (v - 1 > 3000 ? v - 3000 : 1); k <= v - 1; k++) if (A(k) > v) av++;
        r[F_AV] = av;
        /* holes x < v at time v: x >= umin(v) */
        long um = v - gap[v - 1];
        int lf = 0, lfe = 0, und = 0;
        for (long x = um; x <= v; x++) {
            long g = fi[x];
            if (x < v && (g == 0 || g > v) && g != 0 && g <= n) { lf++; if ((x & 1) == eps) lfe++; }
            if (g == 0 || g > n) und++;   /* x <= v unused at time n (umin(n) >= umin(v)) */
        }
        r[F_LFILL] = lf; r[F_LFILLEPS] = lfe; r[F_U] = hU[v];
        r[F_NVN] = (int16_t)(n - v + und);
        r[F_MAXO] = hMO[v]; r[F_XTOT] = Xd[v]; r[F_NMV] = (int16_t)(n - v); r[F_MMV] = (int16_t)(M - v);
        r[F_HFILLE] = hHF[v];
        int32_t v32 = v, n32 = n; fwrite(&v32, 4, 1, fv); fwrite(&n32, 4, 1, fn); fwrite(r, 2, NF, fr);
        nh++;
    }
    fclose(fv); fclose(fn); fclose(fr);
    fprintf(stderr, "[crossings_gen] N=%ld holes=%ld NF=%d\n", N, nh, NF);
    return 0;
}
