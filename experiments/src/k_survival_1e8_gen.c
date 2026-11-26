/* Fast generator for the Watts greedy sequence (OEIS A055265), used by k_survival_1e8.py.
 *
 *   a(1) = 1, a(n+1) = min { x >= 1 unused : a(n) + x prime }.
 *
 * Build:  gcc -O2 -o k_survival_1e8_gen k_survival_1e8_gen.c
 * Run:    ./k_survival_1e8_gen N OUTDIR
 *
 * Writes raw little-endian binaries into OUTDIR:
 *   seq.i32    a(1..N)                         (int32, N entries)
 *   fi.i32     fi[v] for v = 0..VMAX           (int32; 0 = not seen by N; VMAX = N + SLACK)
 *   h0.i16     H_0(m) for m = 1..N             (int16; even holes x <= m, x not in U_m)
 *   h1.i16     H_1(m) for m = 1..N             (int16; odd holes)
 *   isp.u8     isprime[x] for x = 0..PLIM      (uint8)
 *   meta.txt   N VMAX PLIM max_a
 * Aborts if a value > VMAX is ever needed (never happens: |a(n) - n| < 400 up to 1e8).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define SLACK 100000L

static void wr(const char *dir, const char *name, const void *p, size_t sz, size_t cnt) {
    char path[4096];
    snprintf(path, sizeof path, "%s/%s", dir, name);
    FILE *f = fopen(path, "wb");
    if (!f) { perror(path); exit(1); }
    if (fwrite(p, sz, cnt, f) != cnt) { perror("fwrite"); exit(1); }
    fclose(f);
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s N OUTDIR\n", argv[0]); return 1; }
    long N = atol(argv[1]);
    const char *dir = argv[2];
    long VMAX = N + SLACK;
    long PLIM = 2 * VMAX + 10;

    uint8_t *isp = malloc(PLIM + 1);
    memset(isp, 1, PLIM + 1);
    isp[0] = isp[1] = 0;
    for (long i = 2; i * i <= PLIM; i++)
        if (isp[i]) for (long j = i * i; j <= PLIM; j += i) isp[j] = 0;

    uint8_t *used = calloc(VMAX + 2, 1);
    int32_t *seq = malloc(sizeof(int32_t) * N);
    int32_t *fi = calloc(VMAX + 1, sizeof(int32_t));
    int16_t *h0 = malloc(sizeof(int16_t) * N);
    int16_t *h1 = malloc(sizeof(int16_t) * N);

    long lowest[2] = {2, 1};
    long a = 1, maxa = 1;
    seq[0] = 1; used[1] = 1; fi[1] = 1; lowest[1] = 3;
    /* usedle[p] = #{x <= m : x = p mod 2, x used}; holes H_p(m) = #{x<=m, parity p} - usedle[p] */
    long usedle[2] = {0, 1};          /* at m = 1: value 1 used */
    h0[0] = 0; h1[0] = 0;
    for (long i = 1; i < N; i++) {
        long m = i + 1;               /* we are computing a(m) */
        long par = 1 - (a & 1);
        long x = lowest[par];
        for (;;) {
            if (x > VMAX) { fprintf(stderr, "VMAX exceeded at m=%ld\n", m); return 2; }
            if (!used[x] && isp[a + x]) break;
            x += 2;
        }
        seq[i] = (int32_t)x; used[x] = 1; fi[x] = (int32_t)m;
        if (x > maxa) maxa = x;
        if (x == lowest[par]) { long y = x; while (used[y]) y += 2; lowest[par] = y; }
        a = x;
        /* update usedle for time m: value m enters the window [1, m], value x is now used */
        if (used[m]) usedle[m & 1]++;           /* m itself used by time m (incl. x == m) */
        if (x < m) usedle[x & 1]++;             /* x < m newly used, was a hole */
        long n0 = m / 2, n1 = (m + 1) / 2;
        h0[i] = (int16_t)(n0 - usedle[0]);
        h1[i] = (int16_t)(n1 - usedle[1]);
    }
    wr(dir, "seq.i32", seq, sizeof(int32_t), N);
    wr(dir, "fi.i32", fi, sizeof(int32_t), VMAX + 1);
    wr(dir, "h0.i16", h0, sizeof(int16_t), N);
    wr(dir, "h1.i16", h1, sizeof(int16_t), N);
    wr(dir, "isp.u8", isp, 1, PLIM + 1);
    char path[4096]; snprintf(path, sizeof path, "%s/meta.txt", dir);
    FILE *f = fopen(path, "w"); fprintf(f, "%ld %ld %ld %ld\n", N, VMAX, PLIM, maxa); fclose(f);
    return 0;
}
