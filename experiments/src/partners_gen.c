/* Per-hole partner analysis for the Watts greedy sequence (A055265), used by partners.py.
 *
 * Reads the binaries written by k_survival_1e8_gen.c (seq.i32, fi.i32, h0.i16, h1.i16, isp.u8,
 * meta.txt) from WORKDIR and writes per-hole and per-partner arrays back into WORKDIR.
 *
 * Build:  gcc -O2 -o partners_gen partners_gen.c -lm
 * Run:    ./partners_gen WORKDIR R
 *   R = half-width (in same-parity slots) of the jitter window for the local null model.
 *
 * Hole v: 2 <= v <= N, fi(v) > v or fi(v) = 0 (open at N; then n = N). n = fi(v) - 1.
 * Slots: w = v+1, v+3, ..., <= n (parity 1-eps). Class of slot w (L009 Step 1):
 *   1 Ahead  fi(w) <= v-1;  2 steal-range  v <= fi(w) <= n-1;  3 fi(w) = n;  4 Late fi(w) > n or 0.
 * A slot is a partner iff w + v is prime.
 *
 * Per-hole outputs (index = hole number, increasing v):
 *   h_v.i32      v
 *   h_n.i32      n
 *   h_W.i8       5 bytes per hole: K, W1, W2, W3, W4
 *   h_S.i16      4 shorts per hole: S1..S4 = #slots of each class in (v, n]
 *   h_A.i16      3 shorts: Atot = #{x > v-1 used by v-1, parity 1-eps} (= H_{1-eps}(v-1)),
 *                          AP = #{such x with x+v prime} (any x, also x > n), Mv = max a(1..v-1) - v
 *   h_cut.i8     2 bytes: KbM = #partners w <= max a(1..v-1); Kbu = #partners w < u4,
 *                          u4 = smallest Late slot in (v, n] (n+1 if none)
 *   h_E.f32      6 floats: E1g, E4g (hypergeometric: K*S_i/M), E1j, E4j (jitter +-R slots),
 *                          E1p, E4p (random primes: sum over class slots of 2/ln(w+v))
 *   h_alive.i8   4 bytes: maxK over holes u<v alive at time v; #such holes (capped 127);
 *                         maxK over holes u != v alive at time n; #such (capped 127)
 *   K_by_v.i8    K for each v = 0..N (-1 if not a hole)
 * Per-partner outputs:
 *   p_hole.i32   hole index
 *   p_geo.i16    3 shorts: w - v, n - w, max a(1..v-1) - w
 *   p_cls.u8     class 1..4, plus 16 * chainflag for class 1 (see below)
 * chainflag (Ahead value w = a(k)): bit0: a(k-1) < k-1 (predecessor filled a hole),
 *   bit1: a(k-1) was the smallest unused value of its parity at time k-2 (frontier fill).
 * Also writes step_flags.u8 for k = 1..N: bit0 a(k) < k, bit1 a(k) = frontier of its parity
 *   at time k-1, bit2 a(k) > k.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

static void *rd(const char *dir, const char *name, size_t *cnt, size_t sz) {
    char path[4096]; snprintf(path, sizeof path, "%s/%s", dir, name);
    FILE *f = fopen(path, "rb"); if (!f) { perror(path); exit(1); }
    fseek(f, 0, SEEK_END); long len = ftell(f); fseek(f, 0, SEEK_SET);
    void *p = malloc(len); if (fread(p, 1, len, f) != (size_t)len) { perror("fread"); exit(1); }
    fclose(f); *cnt = len / sz; return p;
}
static FILE *op(const char *dir, const char *name) {
    char path[4096]; snprintf(path, sizeof path, "%s/%s", dir, name);
    FILE *f = fopen(path, "wb"); if (!f) { perror(path); exit(1); } return f;
}

#define MAXS 2048

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s WORKDIR R\n", argv[0]); return 1; }
    const char *dir = argv[1]; int R = atoi(argv[2]);
    long N, VMAX, PLIM, maxa;
    { char path[4096]; snprintf(path, sizeof path, "%s/meta.txt", dir); FILE *f = fopen(path, "r");
      if (fscanf(f, "%ld %ld %ld %ld", &N, &VMAX, &PLIM, &maxa) != 4) return 1;
      fclose(f); }
    size_t c;
    int32_t *seq = rd(dir, "seq.i32", &c, 4);       /* seq[k-1] = a(k) */
    int32_t *fi = rd(dir, "fi.i32", &c, 4);
    uint8_t *isp = rd(dir, "isp.u8", &c, 1);

    /* step flags */
    uint8_t *sf = calloc(N + 2, 1);
    {
        uint8_t *used = calloc(VMAX + 2, 1); long low[2] = {2, 1};
        for (long k = 1; k <= N; k++) {
            long x = seq[k - 1]; int p = x & 1;
            uint8_t fl = 0;
            if (x < k) fl |= 1;
            if (x == low[p]) fl |= 2;
            if (x > k) fl |= 4;
            sf[k] = fl; used[x] = 1;
            if (x == low[p]) { long y = x; while (used[y]) y += 2; low[p] = y; }
        }
        free(used);
        FILE *f = op(dir, "step_flags.u8"); fwrite(sf + 1, 1, N, f); fclose(f);
    }

    int8_t *Kv = malloc(N + 1); memset(Kv, -1, N + 1);
    FILE *fv = op(dir, "h_v.i32"), *fn = op(dir, "h_n.i32"), *fW = op(dir, "h_W.i8"), *fS = op(dir, "h_S.i16"),
         *fA = op(dir, "h_A.i16"), *fC = op(dir, "h_cut.i8"), *fE = op(dir, "h_E.f32"),
         *fph = op(dir, "p_hole.i32"), *fpg = op(dir, "p_geo.i16"), *fpc = op(dir, "p_cls.u8");
    static uint8_t cls[MAXS], ispart[MAXS];
    long nh = 0, np = 0, M = 0;  /* M = max a(1..v-1) */
    for (long v = 2; v <= N; v++) {
        if (seq[v - 2] > M) M = seq[v - 2];          /* include a(v-1) */
        long f = fi[v];
        if (!(f == 0 || f > v)) continue;
        long n = (f == 0) ? N : f - 1;
        int S[5] = {0}, W[5] = {0};
        int ns = 0;
        long u4 = n + 1;
        for (long w = v + 1; w <= n; w += 2) {
            long g = fi[w]; int cl;
            if (g == 0 || g > n) cl = 4; else if (g == n) cl = 3; else if (g >= v) cl = 2; else cl = 1;
            if (ns >= MAXS) { fprintf(stderr, "MAXS\n"); return 3; }
            cls[ns] = cl; ispart[ns] = isp[w + v]; S[cl]++;
            if (cl == 4 && u4 == n + 1) u4 = w;
            if (ispart[ns]) W[cl]++;
            ns++;
        }
        int K = W[1] + W[2] + W[3] + W[4];
        Kv[v] = K;
        /* Ahead set at time v-1 (whole, incl. > n) */
        int Atot = 0, AP = 0;
        for (long x = v + 1; x <= M; x += 2) {
            long g = fi[x];
            if (g >= 1 && g <= v - 1) { Atot++; if (isp[x + v]) AP++; }
        }
        int KbM = 0, Kbu = 0;
        double E1j = 0, E4j = 0, E1p = 0, E4p = 0;
        for (int j = 0; j < ns; j++) {
            long w = v + 1 + 2 * j;
            if (cls[j] == 1) E1p += 2.0 / log((double)(w + v));
            if (cls[j] == 4) E4p += 2.0 / log((double)(w + v));
            if (!ispart[j]) continue;
            if (w <= M) KbM++;
            if (w < u4) Kbu++;
            int lo = j - R < 0 ? 0 : j - R, hi = j + R >= ns ? ns - 1 : j + R;
            int c1 = 0, c4 = 0;
            for (int t = lo; t <= hi; t++) { c1 += cls[t] == 1; c4 += cls[t] == 4; }
            E1j += (double)c1 / (hi - lo + 1); E4j += (double)c4 / (hi - lo + 1);
            int32_t hi32 = (int32_t)nh; fwrite(&hi32, 4, 1, fph);
            int16_t geo[3] = {(int16_t)(w - v), (int16_t)(n - w), (int16_t)(M - w)}; fwrite(geo, 2, 3, fpg);
            uint8_t pc = cls[j];
            if (cls[j] == 1) { long k = fi[w]; uint8_t cf = (k >= 2) ? (sf[k - 1] & 3) : 0; pc |= cf << 4; }
            fwrite(&pc, 1, 1, fpc); np++;
        }
        int32_t v32 = v, n32 = n; fwrite(&v32, 4, 1, fv); fwrite(&n32, 4, 1, fn);
        int8_t Wb[5] = {K, W[1], W[2], W[3], W[4]}; fwrite(Wb, 1, 5, fW);
        int16_t Sb[4] = {S[1], S[2], S[3], S[4]}; fwrite(Sb, 2, 4, fS);
        int16_t Ab[3] = {Atot, AP, (int16_t)(M - v)}; fwrite(Ab, 2, 3, fA);
        int8_t Cb[2] = {KbM, Kbu}; fwrite(Cb, 1, 2, fC);
        float Eb[6] = {ns ? (float)K * S[1] / ns : 0, ns ? (float)K * S[4] / ns : 0, E1j, E4j, E1p, E4p};
        fwrite(Eb, 4, 6, fE);
        nh++;
    }
    fclose(fv); fclose(fn); fclose(fW); fclose(fS); fclose(fA); fclose(fC); fclose(fE);
    fclose(fph); fclose(fpg); fclose(fpc);
    { FILE *f = op(dir, "K_by_v.i8"); fwrite(Kv, 1, N + 1, f); fclose(f); }

    /* alive pass */
    FILE *fal = op(dir, "h_alive.i8");
    for (long v = 2; v <= N; v++) {
        long f = fi[v];
        if (!(f == 0 || f > v)) continue;
        long n = (f == 0) ? N : f - 1;
        int mk = -1, cnt = 0;
        for (long u = v - 1; u >= 2 && u >= v - 600; u--) {
            long g = fi[u];
            if (g == 0 || g > v) { if (Kv[u] > mk) mk = Kv[u]; cnt++; }
        }
        int mk2 = -1, cnt2 = 0;
        for (long u = n; u >= 2 && u >= n - 600; u--) {
            if (u == v) continue;
            long g = fi[u];
            if (u <= N && (g == 0 || g > n)) { if (Kv[u] > mk2) mk2 = Kv[u]; cnt2++; }
        }
        int8_t b[4] = {mk, cnt > 127 ? 127 : cnt, mk2, cnt2 > 127 ? 127 : cnt2};
        fwrite(b, 1, 4, fal);
    }
    fclose(fal);
    fprintf(stderr, "holes %ld partners %ld\n", nh, np);
    return 0;
}
