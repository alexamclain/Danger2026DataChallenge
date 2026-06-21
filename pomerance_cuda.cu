/*
 * pomerance_cuda.cu -- CUDA prototype for the p23/p25/p26 X1(16) nonsplit
 * first-branch halving search path from pomerance.c.
 *
 * This is deliberately narrow: it ports the production x16halvenonsplit path
 * for primes with the fast square-root cases p == 5 mod 8 or p == 3 mod 4,
 * with p < 2^127.  The generic 2-Sylow search and diagnostic modes remain in
 * pomerance.c.
 *
 * Compile on an Ada-generation NVIDIA GPU:
 *   nvcc -O3 -std=c++17 -arch=sm_89 -o pomerance_cuda pomerance_cuda.cu
 * Add -DPOM_CUDA_DETAILED_STATS=1 to keep the per-stage diagnostic counters.
 *
 * Usage:
 *   ./pomerance_cuda <p> [seed_offset] [max_trials]
 *     [x16halvenonsplit|x16stratumprobe|x16domainprobe|x16d2probe|x16d3probe|x16d4probe|x16tracenormab|x16tracenormfilter|x16uprecheckprobe|x16ecoverprobe|x16ecoverd2probe|x16ecoverd3probe|x16ecoverd4probe] [chunk_trials] [blocks]
 *     [threads] [claim_batch] [auto|generic|u96]
 *     [seed=mixed|identity|splitmix] [start_chunk=N] [start_trial=N]
 *     [target_depth=N] [bucket_bits=N] [focus_bucket=N]
 * The auto backend uses the specialized u96 path for p < 2^96 and the
 * generic u128 path otherwise.
 *
 * Example:
 *   ./pomerance_cuda 100000000000000000000117 0 1000000 x16halvenonsplit
 *   ./pomerance_cuda 100000000000000000000000067 121 550000000000 x16halvenonsplit 1000000000
 *   ./pomerance_cuda 100000000000000000000000067 121 65536 x16tracenormab 32768 1 64 1 u96
 *   ./pomerance_cuda 1000000000000000000000000103 0 1000000 x16ecoverprobe 1000000 0 128 64 u96 target_depth=26
 */

#include <cuda_runtime.h>

#include <chrono>
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

using u32 = uint32_t;
using u64 = unsigned long long;
using u128 = unsigned __int128;

#define HD __host__ __device__
#define DEV __device__

#ifndef POM_CUDA_DETAILED_STATS
#define POM_CUDA_DETAILED_STATS 0
#endif

#ifndef POM_CUDA_HIT_TELEMETRY
#define POM_CUDA_HIT_TELEMETRY 0
#endif

enum SeedMode {
    SEED_MIXED = 0,
    SEED_IDENTITY = 1,
    SEED_SPLITMIX = 2,
};

static constexpr int PROBE_MAX_BUCKET_BITS = 8;
static constexpr int PROBE_MAX_BUCKETS = 1 << (PROBE_MAX_BUCKET_BITS + 1);
static constexpr int PROBE_MAX_DEPTH = 64;
static constexpr int TRACE_AB_DEPTH_COUNT = 6;

struct u256 {
    u128 lo;
    u128 hi;
};

struct Mont128 {
    u128 p;
    u128 ni;
    u128 R2;
    u128 one;
};

struct Rng {
    u64 s0;
    u64 s1;
};

struct SearchParams {
    u128 p;
    u128 rand_mask;
    u128 sqrtm1;
    u128 sqrtm1_m;
    u128 sqrt_exp;
    u128 inv2_m;
    u128 two_m;
    u128 four_m;
    u128 eight_m;
    u128 c24_m;
    u128 c32_m;
    u128 c48_m;
    u128 inv4_m;
    Mont128 mt;
    int k;
    int sqrt_case;
};

struct U128Parts {
    u64 lo;
    u64 hi;
};

struct GpuStats {
    u64 claimed;
    u64 processed;
    u64 y_draws;
    u64 y_nonsplit;
    u64 y_with_sqrt_D;
    u64 roots_valid;
    u64 halve_calls;
    u64 chain_survivors;
};

struct GpuResult {
    int found;
    int root_index;
    int q_sheet;
    u64 trial_index;
    u64 chunk_nonce;
    u64 tid;
    u64 raw_draw_count;
    u64 local_draw_count;
    u64 compactD;
    U128Parts A;
    U128Parts x0;
    U128Parts y;
    U128Parts root_x;
    U128Parts xP16;
    U128Parts first_w;
    U128Parts V;
    U128Parts D;
};

struct ProbeStats {
    u64 claimed;
    u64 accepted_roots;
    u64 y_draws;
    u64 y_nonsplit;
    u64 y_with_sqrt_D;
    u64 roots_valid;
    u64 depth_exact[PROBE_MAX_DEPTH + 1];
    u64 bucket_total[PROBE_MAX_BUCKETS];
    u64 bucket_survive[PROBE_MAX_BUCKETS];
    u64 bucket_prefix_total[PROBE_MAX_BUCKETS];
    u64 bucket_prefix_survive[PROBE_MAX_BUCKETS];
    u64 bucket_held_total[PROBE_MAX_BUCKETS];
    u64 bucket_held_survive[PROBE_MAX_BUCKETS];
};

struct TraceNormLineClass {
    int valid;
    int domain_line;
    int d_class;
    int t_class;
    int t_line;
    int a_chi;
    int b_chi;
};

struct TraceNormABStats {
    u64 raw_y_draws;
    u64 nonsplit_y;
    u64 f_square;
    u64 d_plus;
    u64 d_minus;
    u64 d_zero;
    u64 t_line_plus;
    u64 t_line_minus;
    u64 t_line_inconsistent;
    u64 t_line_unusable;
    u64 branch_sqrt_y;
    u64 roots_valid;
    u64 ordinary_emitted_candidates;
    u64 candidate_emitted_candidates;
    u64 ordinary_survive[TRACE_AB_DEPTH_COUNT];
    u64 candidate_survive[TRACE_AB_DEPTH_COUNT];
};

struct UPrecheckCounters {
    u64 d_sqrt_calls;
    u64 d_sqrt_success;
    u64 uplus_checks;
    u64 uplus_pass;
    u64 uplus_reject;
    u64 w_sqrt_calls;
    u64 w_sqrt_success;
    u64 precheck_short_circuit;
};

struct UPrecheckStats {
    u64 claimed;
    u64 accepted_roots;
    u64 y_draws;
    u64 y_nonsplit;
    u64 y_with_sqrt_D;
    u64 roots_valid;
    u64 depth_exact[PROBE_MAX_DEPTH + 1];
    UPrecheckCounters counters;
};

HD static inline U128Parts pack128(u128 x) {
    U128Parts out;
    out.lo = (u64)x;
    out.hi = (u64)(x >> 64);
    return out;
}

static inline u128 unpack128(U128Parts x) {
    return ((u128)x.hi << 64) | (u128)x.lo;
}

HD static int trace_ab_depth_value(int idx) {
    switch (idx) {
        case 0: return 20;
        case 1: return 22;
        case 2: return 24;
        case 3: return 26;
        case 4: return 28;
        default: return 30;
    }
}

HD static inline u256 wide_mul(u128 a, u128 b) {
    u64 a0 = (u64)a;
    u64 a1 = (u64)(a >> 64);
    u64 b0 = (u64)b;
    u64 b1 = (u64)(b >> 64);
    u128 ll = (u128)a0 * b0;
    u128 lh = (u128)a0 * b1;
    u128 hl = (u128)a1 * b0;
    u128 hh = (u128)a1 * b1;
    u128 mid = lh + hl;
    u128 carry_mid = (mid < lh) ? 1 : 0;
    u128 lo = ll + (mid << 64);
    u128 carry_lo = (lo < ll) ? 1 : 0;
    return u256{lo, hh + (mid >> 64) + (carry_mid << 64) + carry_lo};
}

HD static inline u256 wide_add(u256 a, u256 b) {
    u128 lo = a.lo + b.lo;
    return u256{lo, a.hi + b.hi + ((lo < a.lo) ? 1 : 0)};
}

HD static inline u128 addmod128(u128 a, u128 b, u128 p) {
    u128 s = a + b;
    return s >= p ? s - p : s;
}

HD static inline u128 submod128(u128 a, u128 b, u128 p) {
    return a >= b ? a - b : p - b + a;
}

HD static inline u128 mred128(u256 T, const Mont128 *m) {
    u128 q = T.lo * m->ni;
    u256 s = wide_add(T, wide_mul(q, m->p));
    u128 t = s.hi;
    return t >= m->p ? t - m->p : t;
}

HD static inline u128 mm128(u128 a, u128 b, const Mont128 *m) {
    return mred128(wide_mul(a, b), m);
}

HD static inline u128 toM128(u128 a, const Mont128 *m) {
    return mm128(a % m->p, m->R2, m);
}

HD static inline u128 toM128_reduced(u128 a, const Mont128 *m) {
    return mm128(a, m->R2, m);
}

HD static inline u128 frM128(u128 a, const Mont128 *m) {
    return mred128(u256{a, 0}, m);
}

HD static inline u128 mulmod128_mont(u128 a, u128 b, const Mont128 *mt) {
    return frM128(mm128(toM128(a, mt), toM128(b, mt), mt), mt);
}

HD static u128 powmod128_mont(u128 a, u128 e, const Mont128 *mt) {
    u128 r = mt->one;
    u128 b = toM128(a, mt);
    while (e > 0) {
        if (e & 1) r = mm128(r, b, mt);
        e >>= 1;
        if (e) b = mm128(b, b, mt);
    }
    return frM128(r, mt);
}

HD static u128 powmod128_mont_raw(u128 a_m, u128 e, const Mont128 *mt) {
    u128 r = mt->one;
    u128 b = a_m;
    while (e > 0) {
        if (e & 1) r = mm128(r, b, mt);
        e >>= 1;
        if (e) b = mm128(b, b, mt);
    }
    return r;
}

HD static int sqrtmod_p5_128(u128 *root, u128 n, u128 p, u128 sqrtm1,
                             const Mont128 *mt) {
    n %= p;
    if (n == 0) {
        *root = 0;
        return 1;
    }
    if ((u64)(p & 3) == 3) {
        u128 x = powmod128_mont(n, (p + 1) >> 2, mt);
        if (mulmod128_mont(x, x, mt) == n) {
            *root = x;
            return 1;
        }
        return 0;
    }
    u128 x = powmod128_mont(n, (p + 3) >> 3, mt);
    if (mulmod128_mont(x, x, mt) == n) {
        *root = x;
        return 1;
    }
    x = mulmod128_mont(x, sqrtm1, mt);
    if (mulmod128_mont(x, x, mt) == n) {
        *root = x;
        return 1;
    }
    return 0;
}

HD static int sqrtmod_p5_128_mont(u128 *root_m, u128 n_m, u128 p,
                                  u128 sqrtm1_m, const Mont128 *mt) {
    if (n_m == 0) {
        *root_m = 0;
        return 1;
    }
    u128 x_m = powmod128_mont_raw(n_m,
                                  ((u64)(p & 3) == 3) ? ((p + 1) >> 2)
                                                      : ((p + 3) >> 3),
                                  mt);
    if (mm128(x_m, x_m, mt) == n_m) {
        *root_m = x_m;
        return 1;
    }
    if ((u64)(p & 3) == 3) return 0;
    x_m = mm128(x_m, sqrtm1_m, mt);
    if (mm128(x_m, x_m, mt) == n_m) {
        *root_m = x_m;
        return 1;
    }
    return 0;
}

HD static u128 invert128_mont(u128 a, u128 p, const Mont128 *mt) {
    return powmod128_mont(a, p - 2, mt);
}

HD static u128 invert128_mont_raw(u128 a_m, u128 p, const Mont128 *mt) {
    return powmod128_mont_raw(a_m, p - 2, mt);
}

HD static int invert_batch2_128(u128 out[2], const u128 vals[2], u128 p,
                                const Mont128 *mt) {
    if (vals[0] == 0 || vals[1] == 0) return 0;
    u128 prefix1 = vals[0];
    u128 prefix2 = mulmod128_mont(vals[0], vals[1], mt);
    u128 acc = invert128_mont(prefix2, p, mt);
    out[1] = mulmod128_mont(acc, prefix1, mt);
    out[0] = mulmod128_mont(acc, vals[1], mt);
    return 1;
}

HD static int invert_batch2_128_mont(u128 out[2], const u128 vals_m[2], u128 p,
                                     const Mont128 *mt) {
    if (vals_m[0] == 0 || vals_m[1] == 0) return 0;
    u128 prefix1 = vals_m[0];
    u128 prefix2 = mm128(vals_m[0], vals_m[1], mt);
    u128 acc = invert128_mont_raw(prefix2, p, mt);
    out[1] = mm128(acc, prefix1, mt);
    out[0] = mm128(acc, vals_m[1], mt);
    return 1;
}

HD static inline void xDBL128(u128 *Xo, u128 *Zo, u128 X, u128 Z,
                              u128 a24, const Mont128 *m) {
    u128 p = m->p;
    u128 u = addmod128(X, Z, p);
    u128 v = submod128(X, Z, p);
    u = mm128(u, u, m);
    v = mm128(v, v, m);
    *Xo = mm128(u, v, m);
    u128 w = submod128(u, v, p);
    *Zo = mm128(w, addmod128(v, mm128(a24, w, m), p), m);
}

HD static int verify128_mont(u128 p, u128 A, u128 x0, int k, const Mont128 *mt) {
    if (A % p == 2 || A % p == p - 2) return 0;
    u128 inv4_m = invert128_mont(4, p, mt);
    u128 a24m = mm128(toM128(addmod128(A, 2, p), mt), toM128(inv4_m, mt), mt);
    u128 X = toM128(x0 % p, mt);
    u128 Z = mt->one;
    for (int i = 1; i <= k; i++) {
        xDBL128(&X, &Z, X, Z, a24m, mt);
        if (i < k && Z == 0) return 0;
        if (i == k && Z != 0) return 0;
    }
    return 1;
}

HD static int verify128_mont_raw(u128 A_m, u128 x0_m, const SearchParams *params) {
    const u128 p = params->p;
    if (A_m == params->two_m || A_m == submod128(0, params->two_m, p)) return 0;

    const Mont128 *mt = &params->mt;
    u128 a24m = mm128(addmod128(A_m, params->two_m, p), params->inv4_m, mt);
    u128 X = x0_m;
    u128 Z = mt->one;
    for (int i = 1; i <= params->k; i++) {
        xDBL128(&X, &Z, X, Z, a24m, mt);
        if (i < params->k && Z == 0) return 0;
        if (i == params->k && Z != 0) return 0;
    }
    return 1;
}

HD static u128 x16_A_numerator_from_y128(u128 y, u128 p, const Mont128 *mt) {
    u128 num = 1;
    num = submod128(mulmod128_mont(num, y, mt), 8, p);
    num = addmod128(mulmod128_mont(num, y, mt), 24, p);
    num = submod128(mulmod128_mont(num, y, mt), 32, p);
    num = addmod128(mulmod128_mont(num, y, mt), 8, p);
    num = addmod128(mulmod128_mont(num, y, mt), 32, p);
    num = submod128(mulmod128_mont(num, y, mt), 48, p);
    num = addmod128(mulmod128_mont(num, y, mt), 32, p);
    num = submod128(mulmod128_mont(num, y, mt), 8, p);
    return num;
}

HD static u128 x16_A_numerator_from_y128_mont(u128 y_m, const SearchParams *params) {
    const u128 p = params->p;
    const Mont128 *mt = &params->mt;
    u128 num_m = mt->one;
    num_m = submod128(mm128(num_m, y_m, mt), params->eight_m, p);
    num_m = addmod128(mm128(num_m, y_m, mt), params->c24_m, p);
    num_m = submod128(mm128(num_m, y_m, mt), params->c32_m, p);
    num_m = addmod128(mm128(num_m, y_m, mt), params->eight_m, p);
    num_m = addmod128(mm128(num_m, y_m, mt), params->c32_m, p);
    num_m = submod128(mm128(num_m, y_m, mt), params->c48_m, p);
    num_m = addmod128(mm128(num_m, y_m, mt), params->c32_m, p);
    num_m = submod128(mm128(num_m, y_m, mt), params->eight_m, p);
    return num_m;
}

HD static int x16_y_predicts_nonsplit128(u128 p, u128 y, u128 y2,
                                         const Mont128 *mt) {
    u128 f1 = submod128(y2, 2, p);
    u128 two_y = addmod128(y, y, p);
    u128 four_y = addmod128(two_y, two_y, p);
    u128 f2 = addmod128(submod128(y2, four_y, p), 2, p);
    u128 f = mulmod128_mont(f1, f2, mt);
    if (f == 0) return 0;
    u128 leg = powmod128_mont(f, (p - 1) >> 1, mt);
    return leg != 1;
}

HD static int x16_y_predicts_nonsplit128_mont(u128 y_m, u128 y2_m,
                                              const SearchParams *params) {
    const u128 p = params->p;
    const Mont128 *mt = &params->mt;
    u128 f1_m = submod128(y2_m, params->two_m, p);
    u128 two_y_m = addmod128(y_m, y_m, p);
    u128 four_y_m = addmod128(two_y_m, two_y_m, p);
    u128 f2_m = addmod128(submod128(y2_m, four_y_m, p), params->two_m, p);
    u128 f_m = mm128(f1_m, f2_m, mt);
    if (f_m == 0) return 0;
    u128 leg_m = powmod128_mont_raw(f_m, (p - 1) >> 1, mt);
    return leg_m != mt->one;
}

HD static int chi128_mont(u128 f_m, const SearchParams *params) {
    if (f_m == 0) return 0;
    const u128 p = params->p;
    const Mont128 *mt = &params->mt;
    u128 chi_m = powmod128_mont_raw(f_m, (p - 1) >> 1, mt);
    if (chi_m == mt->one) return 1;
    if (chi_m == submod128(0, mt->one, p)) return -1;
    return 0;
}

HD static int x16_trace_norm_line_class128(TraceNormLineClass *out,
                                           u128 y_m, u128 y2_m,
                                           const SearchParams *params) {
    *out = TraceNormLineClass{0, 0, 0, 0, 0, 0, 0};
    const u128 p = params->p;
    const Mont128 *mt = &params->mt;
    u128 two_y_m = addmod128(y_m, y_m, p);
    u128 four_y_m = addmod128(two_y_m, two_y_m, p);
    u128 B_m = addmod128(submod128(y2_m, two_y_m, p), params->two_m, p);
    u128 C_m = submod128(y2_m, params->two_m, p);
    u128 R_m = addmod128(submod128(y2_m, four_y_m, p), params->two_m, p);
    u128 ym1_m = submod128(y_m, mt->one, p);
    if (ym1_m == 0) return 0;

    u128 F_m = mm128(mm128(ym1_m, C_m, mt), B_m, mt);
    int domain = chi128_mont(F_m, params);
    if (domain == 0) return 0;
    out->valid = 1;
    out->domain_line = domain;
    if (domain != 1) return 1;

    u128 K_m = submod128(0, mm128(C_m, R_m, mt), p);
    if (K_m == 0) return 1;
    u128 sqrt_K_m;
    if (!sqrtmod_p5_128_mont(&sqrt_K_m, K_m, p, params->sqrtm1_m, mt)) return 1;
    u128 sqrt_F_m;
    if (!sqrtmod_p5_128_mont(&sqrt_F_m, F_m, p, params->sqrtm1_m, mt)) return 1;

    u128 nh_scale_m = mm128(params->eight_m, ym1_m, mt);
    u128 sqrt_Nh_m = mm128(nh_scale_m, sqrt_F_m, mt);
    int nh_scale_chi = chi128_mont(nh_scale_m, params);
    if (nh_scale_chi == 0) return 1;
    if (nh_scale_chi < 0) sqrt_Nh_m = submod128(0, sqrt_Nh_m, p);

    u128 nv_factor_m = mm128(y_m, C_m, mt);
    int nv_scale_chi = chi128_mont(nv_factor_m, params);
    if (nv_scale_chi == 0) return 1;
    u128 sqrt_Nv_num_m = mm128(
        mm128(mm128(params->four_m, y_m, mt), sqrt_F_m, mt), sqrt_K_m, mt);
    if (nv_scale_chi < 0) sqrt_Nv_num_m = submod128(0, sqrt_Nv_num_m, p);

    u128 Ch_m = mm128(mm128(C_m, B_m, mt), params->four_m, mt);
    u128 h_arg_m = mm128(addmod128(Ch_m, sqrt_Nh_m, p), params->two_m, mt);
    int H = chi128_mont(h_arg_m, params);
    if (H == 0) return 1;

    u128 ym1_2_m = mm128(ym1_m, ym1_m, mt);
    u128 av_m = mm128(y_m, ym1_2_m, mt);
    av_m = mm128(av_m, params->eight_m, mt);
    u128 av_num_m = mm128(C_m, av_m, mt);
    u128 v_arg_num_m = addmod128(av_num_m, sqrt_Nv_num_m, p);
    int chi_C = chi128_mont(C_m, params);
    int chi_2B = chi128_mont(mm128(B_m, params->two_m, mt), params);
    int chi_v = chi128_mont(mm128(v_arg_num_m, params->two_m, mt), params);
    if (chi_C == 0 || chi_2B == 0 || chi_v == 0) return 1;
    chi_v *= chi_C;
    int VQ = chi_2B * chi_v;

    u128 y_minus_2_m = submod128(y_m, params->two_m, p);
    u128 neg_x_num_m = submod128(0, mm128(y_m, y_minus_2_m, mt), p);
    int X = chi128_mont(neg_x_num_m, params);
    if (X == 0) return 1;

    int d_class = -X * VQ * H;
    int y_chi = chi128_mont(y_m, params);
    if (y_chi == 0) return 1;

    u128 t_inv_m = invert128_mont_raw(ym1_m, p, mt);
    u128 a_m = submod128(ym1_m, t_inv_m, p);
    int a_chi = chi128_mont(a_m, params);
    int sqrt_K_chi = chi128_mont(sqrt_K_m, params);
    int B_chi = chi128_mont(B_m, params);
    if (a_chi == 0 || sqrt_K_chi == 0 || B_chi == 0) return 1;

    int b_chi = sqrt_K_chi * B_chi;
    int t_class = d_class * y_chi;
    int t_line = (a_chi == 1) ? t_class : t_class * b_chi;

    out->d_class = d_class;
    out->t_class = t_class;
    out->t_line = t_line;
    out->a_chi = a_chi;
    out->b_chi = b_chi;
    return 1;
}

HD static int x16_root_to_montgomery_A128(u128 *Ao, u128 *xPo,
                                          u128 p, u128 x, u128 y,
                                          const Mont128 *mt) {
    u128 num = x16_A_numerator_from_y128(y, p, mt);
    u128 ym1 = submod128(y, 1, p);
    u128 ym1_2 = mulmod128_mont(ym1, ym1, mt);
    u128 denA = mulmod128_mont(4, mulmod128_mont(ym1_2, ym1_2, mt), mt);
    u128 denx = submod128(x, y, p);
    u128 vals[2] = {denA, denx};
    u128 invs[2];
    if (!invert_batch2_128(invs, vals, p, mt)) return 0;

    u128 A = mulmod128_mont(num, invs[0], mt);
    u128 xP = mulmod128_mont(x, invs[1], mt);
    if (A <= 2 || A >= p - 2) return 0;
    *Ao = A;
    *xPo = xP;
    return 1;
}

HD static int x16_root_to_montgomery_A128_mont(u128 *Ao, u128 *Amo, u128 *xPmo,
                                               u128 x_m, u128 y_m,
                                               const SearchParams *params) {
    const u128 p = params->p;
    const Mont128 *mt = &params->mt;
    u128 num_m = x16_A_numerator_from_y128_mont(y_m, params);
    u128 ym1_m = submod128(y_m, mt->one, p);
    u128 ym1_2_m = mm128(ym1_m, ym1_m, mt);
    u128 denA_m = mm128(params->four_m, mm128(ym1_2_m, ym1_2_m, mt), mt);
    u128 denx_m = submod128(x_m, y_m, p);
    u128 vals_m[2] = {denA_m, denx_m};
    u128 invs_m[2];
    if (!invert_batch2_128_mont(invs_m, vals_m, p, mt)) return 0;

    u128 A_m = mm128(num_m, invs_m[0], mt);
    u128 xP_m = mm128(x_m, invs_m[1], mt);
    u128 A = frM128(A_m, mt);
    if (A <= 2 || A >= p - 2) return 0;
    *Ao = A;
    *Amo = A_m;
    *xPmo = xP_m;
    return 1;
}

HD static int halve_once_first128(u128 *xo, u128 p, u128 A, u128 x,
                                  u128 sqrtm1, const Mont128 *mt) {
    const u128 inv2 = (p + 1) >> 1;
    u128 x2 = mulmod128_mont(x, x, mt);
    u128 d = addmod128(addmod128(x2, mulmod128_mont(A, x, mt), p), 1, p);
    u128 sd;
    if (!sqrtmod_p5_128(&sd, d, p, sqrtm1, mt)) return 0;

    u128 roots_d[2] = {sd, submod128(0, sd, p)};
    for (int i = 0; i < 2; i++) {
        u128 u = addmod128(addmod128(x, x, p), addmod128(roots_d[i], roots_d[i], p), p);
        u128 w = submod128(mulmod128_mont(u, u, mt), 4, p);
        u128 sw;
        if (!sqrtmod_p5_128(&sw, w, p, sqrtm1, mt)) continue;
        u128 candidates[2] = {
            mulmod128_mont(addmod128(u, sw, p), inv2, mt),
            mulmod128_mont(submod128(u, sw, p), inv2, mt),
        };
        for (int j = 0; j < 2; j++) {
            if (candidates[j] != 0) {
                *xo = candidates[j];
                return 1;
            }
        }
    }
    return 0;
}

HD static int halve_once_first128_mont(u128 *xo_m, u128 A_m, u128 x_m,
                                       const SearchParams *params) {
    const u128 p = params->p;
    const Mont128 *mt = &params->mt;
    u128 x2_m = mm128(x_m, x_m, mt);
    u128 d_m = addmod128(addmod128(x2_m, mm128(A_m, x_m, mt), p), mt->one, p);
    u128 sd_m;
    if (!sqrtmod_p5_128_mont(&sd_m, d_m, p, params->sqrtm1_m, mt)) return 0;

    u128 roots_d[2] = {sd_m, submod128(0, sd_m, p)};
    for (int i = 0; i < 2; i++) {
        u128 u_m = addmod128(addmod128(x_m, x_m, p),
                             addmod128(roots_d[i], roots_d[i], p), p);
        u128 w_m = submod128(mm128(u_m, u_m, mt), params->four_m, p);
        u128 sw_m;
        if (!sqrtmod_p5_128_mont(&sw_m, w_m, p, params->sqrtm1_m, mt)) continue;
        u128 candidates[2] = {
            mm128(addmod128(u_m, sw_m, p), params->inv2_m, mt),
            mm128(submod128(u_m, sw_m, p), params->inv2_m, mt),
        };
        for (int j = 0; j < 2; j++) {
            if (candidates[j] != 0) {
                *xo_m = candidates[j];
                return 1;
            }
        }
    }
    return 0;
}

HD static int halve_once_first128_mont_trace(u128 *xo_m, u128 *first_w_m,
                                             u128 *first_v_m, u128 A_m,
                                             u128 x_m,
                                             const SearchParams *params) {
    const u128 p = params->p;
    const Mont128 *mt = &params->mt;
    u128 x2_m = mm128(x_m, x_m, mt);
    u128 d_m = addmod128(addmod128(x2_m, mm128(A_m, x_m, mt), p), mt->one, p);
    u128 sd_m;
    if (!sqrtmod_p5_128_mont(&sd_m, d_m, p, params->sqrtm1_m, mt)) return 0;

    u128 roots_d[2] = {sd_m, submod128(0, sd_m, p)};
    for (int i = 0; i < 2; i++) {
        u128 u_m = addmod128(addmod128(x_m, x_m, p),
                             addmod128(roots_d[i], roots_d[i], p), p);
        u128 w_m = submod128(mm128(u_m, u_m, mt), params->four_m, p);
        u128 sw_m;
        if (!sqrtmod_p5_128_mont(&sw_m, w_m, p, params->sqrtm1_m, mt)) continue;
        u128 candidates[2] = {
            mm128(addmod128(u_m, sw_m, p), params->inv2_m, mt),
            mm128(submod128(u_m, sw_m, p), params->inv2_m, mt),
        };
        for (int j = 0; j < 2; j++) {
            if (candidates[j] != 0) {
                *xo_m = candidates[j];
                *first_w_m = w_m;
                *first_v_m = u_m;
                return 1;
            }
        }
    }
    return 0;
}

HD static int halve_chain_from_depth128(u128 *xout, u128 p, u128 A, u128 x,
                                        int depth, int k, u128 sqrtm1,
                                        const Mont128 *mt) {
    for (; depth < k; depth++) {
        if (!halve_once_first128(&x, p, A, x, sqrtm1, mt)) return 0;
    }
    if (!verify128_mont(p, A, x, k, mt)) return 0;
    *xout = x;
    return 1;
}

HD static int halve_chain_from_depth128_mont(u128 *xout_m, u128 A_m, u128 x_m,
                                             int depth, const SearchParams *params) {
    for (; depth < params->k; depth++) {
        if (!halve_once_first128_mont(&x_m, A_m, x_m, params)) return 0;
    }
    if (!verify128_mont_raw(A_m, x_m, params)) return 0;
    *xout_m = x_m;
    return 1;
}

HD static int halve_chain_from_depth128_mont_trace(u128 *xout_m, u128 *first_w_m,
                                                   u128 *first_v_m, u128 A_m,
                                                   u128 x_m, int depth,
                                                   const SearchParams *params) {
    int first = 1;
    for (; depth < params->k; depth++) {
        if (first) {
            if (!halve_once_first128_mont_trace(&x_m, first_w_m, first_v_m,
                                                A_m, x_m, params)) return 0;
            first = 0;
        } else if (!halve_once_first128_mont(&x_m, A_m, x_m, params)) {
            return 0;
        }
    }
    if (!verify128_mont_raw(A_m, x_m, params)) return 0;
    *xout_m = x_m;
    return 1;
}

HD static int halve_prefix_depth128_mont_trace(u128 *xout_m, u128 *first_w_m,
                                               u128 *first_v_m, u128 A_m,
                                               u128 x_m, int depth,
                                               int target_depth,
                                               const SearchParams *params) {
    if (target_depth > params->k) target_depth = params->k;
    if (target_depth > PROBE_MAX_DEPTH) target_depth = PROBE_MAX_DEPTH;
    if (depth >= target_depth) {
        *xout_m = x_m;
        return depth;
    }

    if (!halve_once_first128_mont_trace(&x_m, first_w_m, first_v_m,
                                        A_m, x_m, params)) {
        *xout_m = x_m;
        return depth;
    }
    depth++;
    while (depth < target_depth) {
        if (!halve_once_first128_mont(&x_m, A_m, x_m, params)) break;
        depth++;
    }
    *xout_m = x_m;
    return depth;
}

HD static inline u64 rng64(Rng *r) {
    u64 s1 = r->s0;
    u64 s0 = r->s1;
    r->s0 = s0;
    s1 ^= s1 << 23;
    r->s1 = s1 ^ s0 ^ (s1 >> 17) ^ (s0 >> 26);
    return r->s1 + s0;
}

HD static inline u128 rand_below128(Rng *rng, u128 p, u128 mask) {
    for (;;) {
        u128 v = ((u128)rng64(rng) << 64) | (u128)rng64(rng);
        v &= mask;
        if (v < p) return v;
    }
}

HD static inline u128 rand_below128_counted(Rng *rng, u128 p, u128 mask,
                                            u64 *raw_draw_count) {
    for (;;) {
        (*raw_draw_count)++;
        u128 v = ((u128)rng64(rng) << 64) | (u128)rng64(rng);
        v &= mask;
        if (v < p) return v;
    }
}

HD static inline u64 splitmix64_next(u64 *x) {
    u64 z = (*x += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}

HD static inline u64 mix64_value(u64 x) {
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

HD static inline u64 compact128(u128 x) {
    return mix64_value((u64)x) ^ mix64_value((u64)(x >> 64));
}

HD static inline void init_rng(Rng *rng, u64 seed_offset, u64 chunk_nonce,
                               u64 tid, u64 total_threads, int seed_mode) {
    if (seed_mode == SEED_IDENTITY) {
        u64 stream = seed_offset + chunk_nonce * total_threads + tid;
        rng->s0 = 7364529176530163ULL ^ stream;
        rng->s1 = 1442695040888963407ULL ^ (stream << 1);
    } else if (seed_mode == SEED_SPLITMIX) {
        u64 seed = seed_offset + chunk_nonce * total_threads + tid;
        rng->s0 = splitmix64_next(&seed);
        rng->s1 = splitmix64_next(&seed);
    } else {
        u64 seed = seed_offset ^ (chunk_nonce * 0xd1342543de82ef95ULL) ^
                   (tid * 0x9e3779b97f4a7c15ULL) ^ 0x7364529176530163ULL;
        rng->s0 = splitmix64_next(&seed);
        rng->s1 = splitmix64_next(&seed);
    }
    if ((rng->s0 | rng->s1) == 0) rng->s1 = 1442695040888963407ULL;
    for (int i = 0; i < 200; i++) (void)rng64(rng);
}

DEV static inline int found_now(const GpuResult *result) {
    return *((volatile const int *)&result->found);
}

DEV static inline int probe_done_now(const ProbeStats *stats, u64 max_curves) {
    return *((volatile const u64 *)&stats->claimed) >= max_curves;
}

DEV static inline int uprecheck_done_now(const UPrecheckStats *stats,
                                         u64 max_curves) {
    return *((volatile const u64 *)&stats->claimed) >= max_curves;
}

DEV static inline void probe_record_candidate(ProbeStats *probe, u64 claim,
                                              u64 split_trial, int reached_depth,
                                              int target_depth, int root_index,
                                              u64 source_hash,
                                              int bucket_bits) {
    if (reached_depth < 0) reached_depth = 0;
    if (reached_depth > PROBE_MAX_DEPTH) reached_depth = PROBE_MAX_DEPTH;
    if (target_depth > PROBE_MAX_DEPTH) target_depth = PROBE_MAX_DEPTH;

    unsigned bucket_mask = (1u << bucket_bits) - 1u;
    int bucket = ((root_index & 1) << bucket_bits) |
                 (int)(source_hash & (u64)bucket_mask);
    int survived = reached_depth >= target_depth;

    atomicAdd(&probe->depth_exact[reached_depth], 1ULL);
    atomicAdd(&probe->bucket_total[bucket], 1ULL);
    if (survived) atomicAdd(&probe->bucket_survive[bucket], 1ULL);
    if (claim < split_trial) {
        atomicAdd(&probe->bucket_prefix_total[bucket], 1ULL);
        if (survived) atomicAdd(&probe->bucket_prefix_survive[bucket], 1ULL);
    } else {
        atomicAdd(&probe->bucket_held_total[bucket], 1ULL);
        if (survived) atomicAdd(&probe->bucket_held_survive[bucket], 1ULL);
    }
}

DEV static inline void uprecheck_record_candidate(UPrecheckStats *stats,
                                                  int reached_depth) {
    if (reached_depth < 0) reached_depth = 0;
    if (reached_depth > PROBE_MAX_DEPTH) reached_depth = PROBE_MAX_DEPTH;
    atomicAdd(&stats->depth_exact[reached_depth], 1ULL);
}

__global__ static void x16halvenonsplit_kernel(SearchParams params,
                                               u64 seed_offset,
                                               u64 chunk_nonce,
                                               u64 max_curves,
                                               u64 global_base,
                                               u64 claim_batch,
                                               int seed_mode,
                                               GpuStats *__restrict__ stats,
                                               GpuResult *__restrict__ result) {
    u64 tid = (u64)blockIdx.x * (u64)blockDim.x + (u64)threadIdx.x;
    u64 total_threads = (u64)gridDim.x * (u64)blockDim.x;
    Rng rng;
    init_rng(&rng, seed_offset, chunk_nonce, tid, total_threads, seed_mode);

    const u128 p = params.p;
    const Mont128 *mt = &params.mt;
    u64 local_processed = 0;
#if POM_CUDA_HIT_TELEMETRY
    u64 local_raw_draws = 0;
    u64 local_y_draws_for_result = 0;
#endif
#if POM_CUDA_DETAILED_STATS
    u64 local_y_draws = 0;
    u64 local_y_nonsplit = 0;
    u64 local_y_with_sqrt_D = 0;
    u64 local_roots_valid = 0;
    u64 local_halve_calls = 0;
    u64 local_chain_survivors = 0;
#endif
    u64 next_claim = 0;
    u64 claim_limit = 0;

    while (!found_now(result)) {
#if POM_CUDA_HIT_TELEMETRY
        u128 y = rand_below128_counted(&rng, p, params.rand_mask, &local_raw_draws);
        local_y_draws_for_result++;
#else
        u128 y = rand_below128(&rng, p, params.rand_mask);
#endif
#if POM_CUDA_DETAILED_STATS
        local_y_draws++;
#endif
        if (y == 0) continue;

        u128 y_m = toM128_reduced(y, mt);
        u128 y2_m = mm128(y_m, y_m, mt);
        if (!x16_y_predicts_nonsplit128_mont(y_m, y2_m, &params)) continue;
#if POM_CUDA_DETAILED_STATS
        local_y_nonsplit++;
#endif

        u128 y3_m = mm128(y2_m, y_m, mt);
        u128 two_y_m = addmod128(y_m, y_m, p);
        u128 qa_m = submod128(y2_m, two_y_m, p);
        if (qa_m == 0) continue;
        u128 qb_m = submod128(addmod128(y2_m, y2_m, p), y3_m, p);
        u128 qc_m = submod128(mt->one, y_m, p);
        u128 D_m = submod128(
            mm128(qb_m, qb_m, mt),
            mm128(addmod128(qa_m, qa_m, p), addmod128(qc_m, qc_m, p), mt),
            p);
        u128 sd_m;
        if (!sqrtmod_p5_128_mont(&sd_m, D_m, p, params.sqrtm1_m, mt)) continue;
#if POM_CUDA_DETAILED_STATS
        local_y_with_sqrt_D++;
#endif

        u128 inv_2qa_m = invert128_mont_raw(addmod128(qa_m, qa_m, p), p, mt);
        u128 roots_m[2] = {
            mm128(submod128(sd_m, qb_m, p), inv_2qa_m, mt),
            mm128(submod128(submod128(0, sd_m, p), qb_m, p), inv_2qa_m, mt),
        };

        int stop = 0;
        for (int ri = 0; ri < 2; ri++) {
            u128 A;
            u128 A_m;
            u128 xP16_m;
            if (!x16_root_to_montgomery_A128_mont(&A, &A_m, &xP16_m, roots_m[ri],
                                                  y_m, &params)) continue;
#if POM_CUDA_DETAILED_STATS
            local_roots_valid++;
#endif

            if (next_claim >= claim_limit) {
                next_claim = atomicAdd(&stats->claimed, claim_batch);
                claim_limit = next_claim + claim_batch;
            }
            u64 claim = next_claim++;
            if (claim >= max_curves || found_now(result)) {
                stop = 1;
                break;
            }

            local_processed++;
#if POM_CUDA_DETAILED_STATS
            local_halve_calls++;
#endif
            u128 xR_m;
#if POM_CUDA_HIT_TELEMETRY
            u128 first_w_m = 0;
            u128 first_v_m = 0;
            if (halve_chain_from_depth128_mont_trace(&xR_m, &first_w_m, &first_v_m,
                                                     A_m, xP16_m, 4, &params)) {
#else
            if (halve_chain_from_depth128_mont(&xR_m, A_m, xP16_m, 4, &params)) {
#endif
#if POM_CUDA_DETAILED_STATS
                local_chain_survivors++;
#endif
                if (atomicCAS(&result->found, 0, 1) == 0) {
                    result->trial_index = global_base + claim;
                    result->A = pack128(A);
                    result->x0 = pack128(frM128(xR_m, mt));
#if POM_CUDA_HIT_TELEMETRY
                    u128 D = frM128(D_m, mt);
                    result->chunk_nonce = chunk_nonce;
                    result->tid = tid;
                    result->raw_draw_count = local_raw_draws;
                    result->local_draw_count = local_y_draws_for_result;
                    result->root_index = ri;
                    result->q_sheet = ri;
                    result->compactD = compact128(D);
                    result->y = pack128(y);
                    result->root_x = pack128(frM128(roots_m[ri], mt));
                    result->xP16 = pack128(frM128(xP16_m, mt));
                    result->first_w = pack128(frM128(first_w_m, mt));
                    result->V = pack128(frM128(first_v_m, mt));
                    result->D = pack128(D);
#endif
                }
                stop = 1;
                break;
            }
        }
        if (stop) break;
    }

    atomicAdd(&stats->processed, local_processed);
#if POM_CUDA_DETAILED_STATS
    atomicAdd(&stats->y_draws, local_y_draws);
    atomicAdd(&stats->y_nonsplit, local_y_nonsplit);
    atomicAdd(&stats->y_with_sqrt_D, local_y_with_sqrt_D);
    atomicAdd(&stats->roots_valid, local_roots_valid);
    atomicAdd(&stats->halve_calls, local_halve_calls);
    atomicAdd(&stats->chain_survivors, local_chain_survivors);
#endif
}

__global__ static void x16stratumprobe_kernel(SearchParams params,
                                              u64 seed_offset,
                                              u64 chunk_nonce,
                                              u64 max_curves,
                                              u64 global_base,
                                              u64 split_trial,
                                              u64 claim_batch,
                                              int seed_mode,
                                              int first_gate_filter,
                                              int target_depth,
                                              int bucket_bits,
                                              ProbeStats *__restrict__ probe) {
    u64 tid = (u64)blockIdx.x * (u64)blockDim.x + (u64)threadIdx.x;
    u64 total_threads = (u64)gridDim.x * (u64)blockDim.x;
    Rng rng;
    init_rng(&rng, seed_offset, chunk_nonce, tid, total_threads, seed_mode);

    const u128 p = params.p;
    const Mont128 *mt = &params.mt;
    u64 local_accepted = 0;
    u64 local_y_draws = 0;
    u64 local_y_nonsplit = 0;
    u64 local_y_with_sqrt_D = 0;
    u64 local_roots_valid = 0;
    u64 next_claim = 0;
    u64 claim_limit = 0;

    while (!probe_done_now(probe, max_curves)) {
        u128 y = rand_below128(&rng, p, params.rand_mask);
        local_y_draws++;
        if (y == 0) continue;

        u128 y_m = toM128_reduced(y, mt);
        u128 y2_m = mm128(y_m, y_m, mt);
        if (!x16_y_predicts_nonsplit128_mont(y_m, y2_m, &params)) continue;
        local_y_nonsplit++;

        if (first_gate_filter) {
            u128 ym1_m = submod128(y_m, mt->one, p);
            if (ym1_m == 0) continue;
            u128 two_y_filter_m = addmod128(y_m, y_m, p);
            u128 B_m = addmod128(submod128(y2_m, two_y_filter_m, p),
                                 params.two_m, p);
            u128 C_m = submod128(y2_m, params.two_m, p);
            u128 F_m = mm128(mm128(ym1_m, C_m, mt), B_m, mt);
            if (chi128_mont(F_m, &params) != 1) continue;
        }

        u128 y3_m = mm128(y2_m, y_m, mt);
        u128 two_y_m = addmod128(y_m, y_m, p);
        u128 qa_m = submod128(y2_m, two_y_m, p);
        if (qa_m == 0) continue;
        u128 qb_m = submod128(addmod128(y2_m, y2_m, p), y3_m, p);
        u128 qc_m = submod128(mt->one, y_m, p);
        u128 D_m = submod128(
            mm128(qb_m, qb_m, mt),
            mm128(addmod128(qa_m, qa_m, p), addmod128(qc_m, qc_m, p), mt),
            p);
        u128 sd_m;
        if (!sqrtmod_p5_128_mont(&sd_m, D_m, p, params.sqrtm1_m, mt)) continue;
        local_y_with_sqrt_D++;

        u128 inv_2qa_m = invert128_mont_raw(addmod128(qa_m, qa_m, p), p, mt);
        u128 roots_m[2] = {
            mm128(submod128(sd_m, qb_m, p), inv_2qa_m, mt),
            mm128(submod128(submod128(0, sd_m, p), qb_m, p), inv_2qa_m, mt),
        };

        int stop = 0;
        for (int ri = 0; ri < 2; ri++) {
            u128 A;
            u128 A_m;
            u128 xP16_m;
            if (!x16_root_to_montgomery_A128_mont(&A, &A_m, &xP16_m, roots_m[ri],
                                                  y_m, &params)) continue;
            local_roots_valid++;

            if (next_claim >= claim_limit) {
                next_claim = atomicAdd(&probe->claimed, claim_batch);
                claim_limit = next_claim + claim_batch;
            }
            u64 claim = next_claim++;
            if (claim >= max_curves) {
                stop = 1;
                break;
            }

            local_accepted++;
            u128 x_probe_m;
            u128 first_w_m = 0;
            u128 first_v_m = 0;
            int reached_depth = halve_prefix_depth128_mont_trace(
                &x_probe_m, &first_w_m, &first_v_m, A_m, xP16_m, 4,
                target_depth, &params);
            u128 D = frM128(D_m, mt);
            u128 first_w = frM128(first_w_m, mt);
            u128 first_v = frM128(first_v_m, mt);
            u64 source_hash = compact128(D) ^
                              (compact128(first_w) * 0x9e3779b97f4a7c15ULL) ^
                              (compact128(first_v) * 0xd1342543de82ef95ULL) ^
                              (compact128(y) * 0x94d049bb133111ebULL);
            probe_record_candidate(probe, global_base + claim, split_trial,
                                   reached_depth, target_depth, ri, source_hash,
                                   bucket_bits);
        }
        if (stop) break;
    }

    atomicAdd(&probe->accepted_roots, local_accepted);
    atomicAdd(&probe->y_draws, local_y_draws);
    atomicAdd(&probe->y_nonsplit, local_y_nonsplit);
    atomicAdd(&probe->y_with_sqrt_D, local_y_with_sqrt_D);
    atomicAdd(&probe->roots_valid, local_roots_valid);
}

__global__ static void x16tracenormab_kernel(SearchParams params,
                                             u64 seed_offset,
                                             u64 chunk_nonce,
                                             u64 raw_y_draws,
                                             int seed_mode,
                                             int filter_only,
                                             TraceNormABStats *__restrict__ stats) {
    u64 tid = (u64)blockIdx.x * (u64)blockDim.x + (u64)threadIdx.x;
    u64 total_threads = (u64)gridDim.x * (u64)blockDim.x;
    Rng rng;
    init_rng(&rng, seed_offset, chunk_nonce, tid, total_threads, seed_mode);

    const u128 p = params.p;
    const Mont128 *mt = &params.mt;
    const int target_depth = trace_ab_depth_value(TRACE_AB_DEPTH_COUNT - 1);

    u64 local_raw_y_draws = 0;
    u64 local_nonsplit_y = 0;
    u64 local_f_square = 0;
    u64 local_d_plus = 0;
    u64 local_d_minus = 0;
    u64 local_d_zero = 0;
    u64 local_t_line_plus = 0;
    u64 local_t_line_minus = 0;
    u64 local_t_line_inconsistent = 0;
    u64 local_t_line_unusable = 0;
    u64 local_branch_sqrt_y = 0;
    u64 local_roots_valid = 0;
    u64 local_ordinary_emitted = 0;
    u64 local_candidate_emitted = 0;
    u64 local_ordinary_survive[TRACE_AB_DEPTH_COUNT] = {0, 0, 0, 0, 0, 0};
    u64 local_candidate_survive[TRACE_AB_DEPTH_COUNT] = {0, 0, 0, 0, 0, 0};

    u64 draws_per_thread = (raw_y_draws + total_threads - 1) / total_threads;
    for (u64 i = 0; i < draws_per_thread; i++) {
        u64 draw_index = i * total_threads + tid;
        if (draw_index >= raw_y_draws) break;

        u128 y = rand_below128(&rng, p, params.rand_mask);
        local_raw_y_draws++;
        if (y == 0) continue;

        u128 y_m = toM128_reduced(y, mt);
        u128 y2_m = mm128(y_m, y_m, mt);
        if (!x16_y_predicts_nonsplit128_mont(y_m, y2_m, &params)) continue;
        local_nonsplit_y++;

        TraceNormLineClass line{};
        x16_trace_norm_line_class128(&line, y_m, y2_m, &params);
        int candidate_gate = 0;
        if (line.valid && line.domain_line == 1) {
            local_f_square++;
            if (line.d_class == 1) {
                local_d_plus++;
                candidate_gate = 1;
            } else if (line.d_class == -1) {
                local_d_minus++;
            } else {
                local_d_zero++;
            }

            if (line.t_line == 1) {
                local_t_line_plus++;
            } else if (line.t_line == -1) {
                local_t_line_minus++;
            } else {
                local_t_line_unusable++;
            }
            if (line.t_line != 0 && line.a_chi != 0 && line.b_chi != 0) {
                int expected = (line.a_chi == 1) ? line.t_class
                                                 : line.t_class * line.b_chi;
                if (line.t_line != expected) local_t_line_inconsistent++;
            }
        }
        if (filter_only && !candidate_gate) continue;

        u128 y3_m = mm128(y2_m, y_m, mt);
        u128 two_y_m = addmod128(y_m, y_m, p);
        u128 qa_m = submod128(y2_m, two_y_m, p);
        if (qa_m == 0) continue;
        u128 qb_m = submod128(addmod128(y2_m, y2_m, p), y3_m, p);
        u128 qc_m = submod128(mt->one, y_m, p);
        u128 D_m = submod128(
            mm128(qb_m, qb_m, mt),
            mm128(addmod128(qa_m, qa_m, p), addmod128(qc_m, qc_m, p), mt),
            p);
        u128 sd_m;
        if (!sqrtmod_p5_128_mont(&sd_m, D_m, p, params.sqrtm1_m, mt)) continue;
        local_branch_sqrt_y++;

        u128 inv_2qa_m = invert128_mont_raw(addmod128(qa_m, qa_m, p), p, mt);
        u128 roots_m[2] = {
            mm128(submod128(sd_m, qb_m, p), inv_2qa_m, mt),
            mm128(submod128(submod128(0, sd_m, p), qb_m, p), inv_2qa_m, mt),
        };

        for (int ri = 0; ri < 2; ri++) {
            u128 A;
            u128 A_m;
            u128 xP16_m;
            if (!x16_root_to_montgomery_A128_mont(&A, &A_m, &xP16_m, roots_m[ri],
                                                  y_m, &params)) {
                continue;
            }
            local_roots_valid++;
            if (!filter_only) local_ordinary_emitted++;

            u128 x_probe_m;
            u128 first_w_m = 0;
            u128 first_v_m = 0;
            int reached_depth = halve_prefix_depth128_mont_trace(
                &x_probe_m, &first_w_m, &first_v_m, A_m, xP16_m, 4,
                target_depth, &params);
            for (int di = 0; di < TRACE_AB_DEPTH_COUNT; di++) {
                if (reached_depth >= trace_ab_depth_value(di)) {
                    if (!filter_only) local_ordinary_survive[di]++;
                    if (candidate_gate) local_candidate_survive[di]++;
                }
            }
            if (candidate_gate) local_candidate_emitted++;
        }
    }

    atomicAdd(&stats->raw_y_draws, local_raw_y_draws);
    atomicAdd(&stats->nonsplit_y, local_nonsplit_y);
    atomicAdd(&stats->f_square, local_f_square);
    atomicAdd(&stats->d_plus, local_d_plus);
    atomicAdd(&stats->d_minus, local_d_minus);
    atomicAdd(&stats->d_zero, local_d_zero);
    atomicAdd(&stats->t_line_plus, local_t_line_plus);
    atomicAdd(&stats->t_line_minus, local_t_line_minus);
    atomicAdd(&stats->t_line_inconsistent, local_t_line_inconsistent);
    atomicAdd(&stats->t_line_unusable, local_t_line_unusable);
    atomicAdd(&stats->branch_sqrt_y, local_branch_sqrt_y);
    atomicAdd(&stats->roots_valid, local_roots_valid);
    atomicAdd(&stats->ordinary_emitted_candidates, local_ordinary_emitted);
    atomicAdd(&stats->candidate_emitted_candidates, local_candidate_emitted);
    for (int di = 0; di < TRACE_AB_DEPTH_COUNT; di++) {
        atomicAdd(&stats->ordinary_survive[di], local_ordinary_survive[di]);
        atomicAdd(&stats->candidate_survive[di], local_candidate_survive[di]);
    }
}

struct U96 {
    u32 v[3];
};

struct Field96 {
    U96 p;
    U96 r2;
    U96 one;
    u32 nprime;
};

struct SearchParams96 {
    Field96 f;
    U96 rand_mask;
    U96 sqrtm1_m;
    U96 inv2_m;
    U96 two_m;
    U96 four_m;
    U96 eight_m;
    U96 c24_m;
    U96 c32_m;
    U96 c48_m;
    U96 inv4_m;
    u128 leg_exp;
    u128 sqrt_exp;
    u128 inv_exp;
    int k;
    int sqrt_case;
};

HD static inline U96 u96_from_u64(u64 x) {
    U96 out{{(u32)x, (u32)(x >> 32), 0}};
    return out;
}

HD static inline U96 u96_from_u128(u128 x) {
    U96 out{{(u32)x, (u32)(x >> 32), (u32)(x >> 64)}};
    return out;
}

HD static inline u128 u96_to_u128(U96 x) {
    return (u128)x.v[0] | ((u128)x.v[1] << 32) | ((u128)x.v[2] << 64);
}

HD static inline U128Parts pack96(U96 x) {
    return pack128(u96_to_u128(x));
}

HD static inline int cmp96(U96 a, U96 b) {
    if (a.v[2] < b.v[2]) return -1;
    if (a.v[2] > b.v[2]) return 1;
    if (a.v[1] < b.v[1]) return -1;
    if (a.v[1] > b.v[1]) return 1;
    if (a.v[0] < b.v[0]) return -1;
    if (a.v[0] > b.v[0]) return 1;
    return 0;
}

HD static inline int is_zero96(U96 a) {
    return (a.v[0] | a.v[1] | a.v[2]) == 0;
}

HD static inline int eq96(U96 a, U96 b) {
    return ((a.v[0] ^ b.v[0]) | (a.v[1] ^ b.v[1]) | (a.v[2] ^ b.v[2])) == 0;
}

HD static inline U96 and96(U96 a, U96 b) {
    U96 out{{a.v[0] & b.v[0], a.v[1] & b.v[1], a.v[2] & b.v[2]}};
    return out;
}

HD static U96 sub96_raw(U96 a, U96 b, u32 *borrow_out = nullptr) {
    U96 out;
    u64 bi = b.v[0];
    out.v[0] = (u32)((u64)a.v[0] - bi);
    u64 borrow = ((u64)a.v[0] < bi) ? 1 : 0;
    bi = (u64)b.v[1] + borrow;
    out.v[1] = (u32)((u64)a.v[1] - bi);
    borrow = ((u64)a.v[1] < bi) ? 1 : 0;
    bi = (u64)b.v[2] + borrow;
    out.v[2] = (u32)((u64)a.v[2] - bi);
    borrow = ((u64)a.v[2] < bi) ? 1 : 0;
    if (borrow_out) *borrow_out = (u32)borrow;
    return out;
}

HD static U96 add96_raw(U96 a, U96 b, u32 *carry_out = nullptr) {
    U96 out;
    u64 s = (u64)a.v[0] + b.v[0];
    out.v[0] = (u32)s;
    u64 carry = s >> 32;
    s = (u64)a.v[1] + b.v[1] + carry;
    out.v[1] = (u32)s;
    carry = s >> 32;
    s = (u64)a.v[2] + b.v[2] + carry;
    out.v[2] = (u32)s;
    carry = s >> 32;
    if (carry_out) *carry_out = (u32)carry;
    return out;
}

HD static U96 addmod96(U96 a, U96 b, U96 p) {
    u32 carry = 0;
    U96 s = add96_raw(a, b, &carry);
    if (carry || cmp96(s, p) >= 0) s = sub96_raw(s, p);
    return s;
}

HD static U96 submod96(U96 a, U96 b, U96 p) {
    u32 borrow = 0;
    U96 d = sub96_raw(a, b, &borrow);
    if (borrow) d = add96_raw(d, p);
    return d;
}

HD static u32 inv32_odd(u32 p0) {
    u32 x = 1;
    for (int i = 0; i < 5; i++) x *= 2u - p0 * x;
    return 0u - x;
}

HD static U96 mont_red96(const u32 in[6], const Field96 *f) {
    u32 t[7] = {in[0], in[1], in[2], in[3], in[4], in[5], 0};
    for (int i = 0; i < 3; i++) {
        u32 m = t[i] * f->nprime;
        u64 carry = 0;
        for (int j = 0; j < 3; j++) {
            u64 uv = (u64)t[i + j] + (u64)m * f->p.v[j] + carry;
            t[i + j] = (u32)uv;
            carry = uv >> 32;
        }
        int k = i + 3;
        while (carry) {
            u64 uv = (u64)t[k] + carry;
            t[k] = (u32)uv;
            carry = uv >> 32;
            k++;
        }
    }

    U96 r{{t[3], t[4], t[5]}};
    u32 high = t[6];
    if (high || cmp96(r, f->p) >= 0) {
        u32 borrow = 0;
        U96 s = sub96_raw(r, f->p, &borrow);
        high -= borrow;
        r = s;
    }
    return r;
}

HD static U96 mont_mul96(U96 a, U96 b, const Field96 *f) {
    const u32 a0 = a.v[0], a1 = a.v[1], a2 = a.v[2];
    const u32 b0 = b.v[0], b1 = b.v[1], b2 = b.v[2];

    u64 uv = (u64)a0 * b0;
    u32 t0 = (u32)uv;
    u64 carry = uv >> 32;
    uv = (u64)a0 * b1 + carry;
    u32 t1 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)a0 * b2 + carry;
    u32 t2 = (u32)uv;
    u32 t3 = (u32)(uv >> 32);

    uv = (u64)t1 + (u64)a1 * b0;
    t1 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t2 + (u64)a1 * b1 + carry;
    t2 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t3 + (u64)a1 * b2 + carry;
    t3 = (u32)uv;
    u32 t4 = (u32)(uv >> 32);

    uv = (u64)t2 + (u64)a2 * b0;
    t2 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t3 + (u64)a2 * b1 + carry;
    t3 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t4 + (u64)a2 * b2 + carry;
    t4 = (u32)uv;
    u32 t5 = (u32)(uv >> 32);
    u32 t6 = 0;

    const u32 p0 = f->p.v[0], p1 = f->p.v[1], p2 = f->p.v[2];
    const u32 nprime = f->nprime;

    u32 m = t0 * nprime;
    uv = (u64)t0 + (u64)m * p0;
    carry = uv >> 32;
    uv = (u64)t1 + (u64)m * p1 + carry;
    t1 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t2 + (u64)m * p2 + carry;
    t2 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t3 + carry;
    t3 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t4 + carry;
    t4 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t5 + carry;
    t5 = (u32)uv;
    t6 = (u32)(uv >> 32);

    m = t1 * nprime;
    uv = (u64)t1 + (u64)m * p0;
    carry = uv >> 32;
    uv = (u64)t2 + (u64)m * p1 + carry;
    t2 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t3 + (u64)m * p2 + carry;
    t3 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t4 + carry;
    t4 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t5 + carry;
    t5 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t6 + carry;
    t6 = (u32)uv;

    m = t2 * nprime;
    uv = (u64)t2 + (u64)m * p0;
    carry = uv >> 32;
    uv = (u64)t3 + (u64)m * p1 + carry;
    t3 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t4 + (u64)m * p2 + carry;
    t4 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t5 + carry;
    t5 = (u32)uv;
    carry = uv >> 32;
    uv = (u64)t6 + carry;
    t6 = (u32)uv;

    U96 r{{t3, t4, t5}};
    if (t6 || cmp96(r, f->p) >= 0) r = sub96_raw(r, f->p);
    return r;
}

HD static U96 to_mont96(U96 a, const Field96 *f) {
    return mont_mul96(a, f->r2, f);
}

HD static U96 from_mont96(U96 a, const Field96 *f) {
    return mont_mul96(a, u96_from_u64(1), f);
}

HD static U96 mulmod96(U96 a, U96 b, const Field96 *f) {
    return from_mont96(mont_mul96(to_mont96(a, f), to_mont96(b, f), f), f);
}

HD static U96 mulmod96_to_mont(U96 a, U96 b, const Field96 *f) {
    return mont_mul96(to_mont96(a, f), to_mont96(b, f), f);
}

HD static U96 powmod96_mont(U96 a_m, u128 e, const Field96 *f) {
    U96 r = f->one;
    U96 b = a_m;
    while (e > 0) {
        if (e & 1) r = mont_mul96(r, b, f);
        e >>= 1;
        if (e) b = mont_mul96(b, b, f);
    }
    return r;
}

HD static int sqrtmod_p5_96_mont(U96 *root_m, U96 n_m, const SearchParams96 *params) {
    if (is_zero96(n_m)) {
        *root_m = u96_from_u64(0);
        return 1;
    }
    U96 x_m = powmod96_mont(n_m, params->sqrt_exp, &params->f);
    if (eq96(mont_mul96(x_m, x_m, &params->f), n_m)) {
        *root_m = x_m;
        return 1;
    }
    if (params->sqrt_case == 3) return 0;
    x_m = mont_mul96(x_m, params->sqrtm1_m, &params->f);
    if (eq96(mont_mul96(x_m, x_m, &params->f), n_m)) {
        *root_m = x_m;
        return 1;
    }
    return 0;
}

HD static U96 invert96_mont(U96 a_m, const SearchParams96 *params) {
    return powmod96_mont(a_m, params->inv_exp, &params->f);
}

HD static int invert_batch2_96_mont(U96 out[2], const U96 vals_m[2],
                                    const SearchParams96 *params) {
    if (is_zero96(vals_m[0]) || is_zero96(vals_m[1])) return 0;
    U96 prefix1 = vals_m[0];
    U96 prefix2 = mont_mul96(vals_m[0], vals_m[1], &params->f);
    U96 acc = invert96_mont(prefix2, params);
    out[1] = mont_mul96(acc, prefix1, &params->f);
    out[0] = mont_mul96(acc, vals_m[1], &params->f);
    return 1;
}

HD static inline void xDBL96(U96 *Xo, U96 *Zo, U96 X, U96 Z, U96 a24,
                             const Field96 *f) {
    U96 u = addmod96(X, Z, f->p);
    U96 v = submod96(X, Z, f->p);
    u = mont_mul96(u, u, f);
    v = mont_mul96(v, v, f);
    *Xo = mont_mul96(u, v, f);
    U96 w = submod96(u, v, f->p);
    *Zo = mont_mul96(w, addmod96(v, mont_mul96(a24, w, f), f->p), f);
}

HD static int verify96_mont(U96 A_m, U96 x0_m, const SearchParams96 *params) {
    U96 pm2_m = submod96(u96_from_u64(0), params->two_m, params->f.p);
    if (eq96(A_m, params->two_m) || eq96(A_m, pm2_m)) return 0;

    U96 a24m = mont_mul96(addmod96(A_m, params->two_m, params->f.p),
                          params->inv4_m, &params->f);
    U96 X = x0_m;
    U96 Z = params->f.one;
    for (int i = 1; i <= params->k; i++) {
        xDBL96(&X, &Z, X, Z, a24m, &params->f);
        if (i < params->k && is_zero96(Z)) return 0;
        if (i == params->k && !is_zero96(Z)) return 0;
    }
    return 1;
}

HD static U96 x16_A_numerator_from_y96_mont(U96 y_m, const SearchParams96 *params) {
    U96 num_m = params->f.one;
    num_m = submod96(mont_mul96(num_m, y_m, &params->f), params->eight_m, params->f.p);
    num_m = addmod96(mont_mul96(num_m, y_m, &params->f), params->c24_m, params->f.p);
    num_m = submod96(mont_mul96(num_m, y_m, &params->f), params->c32_m, params->f.p);
    num_m = addmod96(mont_mul96(num_m, y_m, &params->f), params->eight_m, params->f.p);
    num_m = addmod96(mont_mul96(num_m, y_m, &params->f), params->c32_m, params->f.p);
    num_m = submod96(mont_mul96(num_m, y_m, &params->f), params->c48_m, params->f.p);
    num_m = addmod96(mont_mul96(num_m, y_m, &params->f), params->c32_m, params->f.p);
    num_m = submod96(mont_mul96(num_m, y_m, &params->f), params->eight_m, params->f.p);
    return num_m;
}

HD static int x16_y_predicts_nonsplit96(U96 y, U96 y2, const SearchParams96 *params) {
    U96 f1 = submod96(y2, u96_from_u64(2), params->f.p);
    U96 two_y = addmod96(y, y, params->f.p);
    U96 four_y = addmod96(two_y, two_y, params->f.p);
    U96 f2 = addmod96(submod96(y2, four_y, params->f.p), u96_from_u64(2), params->f.p);
    U96 f_m = mulmod96_to_mont(f1, f2, &params->f);
    if (is_zero96(f_m)) return 0;
    U96 leg_m = powmod96_mont(f_m, params->leg_exp, &params->f);
    return !eq96(leg_m, params->f.one);
}

HD static int x16_y_predicts_nonsplit96_mont(U96 y_m, U96 y2_m,
                                             const SearchParams96 *params) {
    U96 f1_m = submod96(y2_m, params->two_m, params->f.p);
    U96 two_y_m = addmod96(y_m, y_m, params->f.p);
    U96 four_y_m = addmod96(two_y_m, two_y_m, params->f.p);
    U96 f2_m = addmod96(submod96(y2_m, four_y_m, params->f.p),
                        params->two_m, params->f.p);
    U96 f_m = mont_mul96(f1_m, f2_m, &params->f);
    if (is_zero96(f_m)) return 0;
    U96 leg_m = powmod96_mont(f_m, params->leg_exp, &params->f);
    return !eq96(leg_m, params->f.one);
}

HD static int chi96_mont(U96 f_m, const SearchParams96 *params) {
    if (is_zero96(f_m)) return 0;
    U96 chi_m = powmod96_mont(f_m, params->leg_exp, &params->f);
    if (eq96(chi_m, params->f.one)) return 1;
    if (eq96(chi_m, submod96(u96_from_u64(0), params->f.one, params->f.p))) return -1;
    return 0;
}

HD static int x16_trace_norm_line_class96(TraceNormLineClass *out,
                                          U96 y_m, U96 y2_m,
                                          const SearchParams96 *params) {
    *out = TraceNormLineClass{0, 0, 0, 0, 0, 0, 0};
    U96 two_y_m = addmod96(y_m, y_m, params->f.p);
    U96 four_y_m = addmod96(two_y_m, two_y_m, params->f.p);
    U96 B_m = addmod96(submod96(y2_m, two_y_m, params->f.p),
                       params->two_m, params->f.p);
    U96 C_m = submod96(y2_m, params->two_m, params->f.p);
    U96 R_m = addmod96(submod96(y2_m, four_y_m, params->f.p),
                       params->two_m, params->f.p);
    U96 ym1_m = submod96(y_m, params->f.one, params->f.p);
    if (is_zero96(ym1_m)) return 0;

    U96 F_m = mont_mul96(mont_mul96(ym1_m, C_m, &params->f), B_m, &params->f);
    int domain = chi96_mont(F_m, params);
    if (domain == 0) return 0;
    out->valid = 1;
    out->domain_line = domain;
    if (domain != 1) return 1;

    U96 K_m = submod96(u96_from_u64(0),
                       mont_mul96(C_m, R_m, &params->f), params->f.p);
    if (is_zero96(K_m)) return 1;
    U96 sqrt_K_m;
    if (!sqrtmod_p5_96_mont(&sqrt_K_m, K_m, params)) return 1;
    U96 sqrt_F_m;
    if (!sqrtmod_p5_96_mont(&sqrt_F_m, F_m, params)) return 1;

    U96 nh_scale_m = mont_mul96(params->eight_m, ym1_m, &params->f);
    U96 sqrt_Nh_m = mont_mul96(nh_scale_m, sqrt_F_m, &params->f);
    int nh_scale_chi = chi96_mont(nh_scale_m, params);
    if (nh_scale_chi == 0) return 1;
    if (nh_scale_chi < 0) {
        sqrt_Nh_m = submod96(u96_from_u64(0), sqrt_Nh_m, params->f.p);
    }

    U96 nv_factor_m = mont_mul96(y_m, C_m, &params->f);
    int nv_scale_chi = chi96_mont(nv_factor_m, params);
    if (nv_scale_chi == 0) return 1;
    U96 sqrt_Nv_num_m = mont_mul96(
        mont_mul96(mont_mul96(params->four_m, y_m, &params->f), sqrt_F_m, &params->f),
        sqrt_K_m, &params->f);
    if (nv_scale_chi < 0) {
        sqrt_Nv_num_m = submod96(u96_from_u64(0), sqrt_Nv_num_m, params->f.p);
    }

    U96 Ch_m = mont_mul96(mont_mul96(C_m, B_m, &params->f),
                          params->four_m, &params->f);
    U96 h_arg_m = mont_mul96(addmod96(Ch_m, sqrt_Nh_m, params->f.p),
                             params->two_m, &params->f);
    int H = chi96_mont(h_arg_m, params);
    if (H == 0) return 1;

    U96 ym1_2_m = mont_mul96(ym1_m, ym1_m, &params->f);
    U96 av_m = mont_mul96(y_m, ym1_2_m, &params->f);
    av_m = mont_mul96(av_m, params->eight_m, &params->f);
    U96 av_num_m = mont_mul96(C_m, av_m, &params->f);
    U96 v_arg_num_m = addmod96(av_num_m, sqrt_Nv_num_m, params->f.p);
    int chi_C = chi96_mont(C_m, params);
    int chi_2B = chi96_mont(mont_mul96(B_m, params->two_m, &params->f), params);
    int chi_v = chi96_mont(mont_mul96(v_arg_num_m, params->two_m, &params->f),
                           params);
    if (chi_C == 0 || chi_2B == 0 || chi_v == 0) return 1;
    chi_v *= chi_C;
    int VQ = chi_2B * chi_v;

    U96 y_minus_2_m = submod96(y_m, params->two_m, params->f.p);
    U96 neg_x_num_m = submod96(u96_from_u64(0),
                               mont_mul96(y_m, y_minus_2_m, &params->f),
                               params->f.p);
    int X = chi96_mont(neg_x_num_m, params);
    if (X == 0) return 1;

    int d_class = -X * VQ * H;
    int y_chi = chi96_mont(y_m, params);
    if (y_chi == 0) return 1;

    U96 t_inv_m = invert96_mont(ym1_m, params);
    U96 a_m = submod96(ym1_m, t_inv_m, params->f.p);
    int a_chi = chi96_mont(a_m, params);
    int sqrt_K_chi = chi96_mont(sqrt_K_m, params);
    int B_chi = chi96_mont(B_m, params);
    if (a_chi == 0 || sqrt_K_chi == 0 || B_chi == 0) return 1;

    int b_chi = sqrt_K_chi * B_chi;
    int t_class = d_class * y_chi;
    int t_line = (a_chi == 1) ? t_class : t_class * b_chi;

    out->d_class = d_class;
    out->t_class = t_class;
    out->t_line = t_line;
    out->a_chi = a_chi;
    out->b_chi = b_chi;
    return 1;
}

HD static int x16_root_to_montgomery_A96_mont(U96 *Ao, U96 *Amo, U96 *xPmo,
                                              U96 x_m, U96 y_m,
                                              const SearchParams96 *params) {
    U96 num_m = x16_A_numerator_from_y96_mont(y_m, params);
    U96 ym1_m = submod96(y_m, params->f.one, params->f.p);
    U96 ym1_2_m = mont_mul96(ym1_m, ym1_m, &params->f);
    U96 denA_m = mont_mul96(params->four_m,
                            mont_mul96(ym1_2_m, ym1_2_m, &params->f),
                            &params->f);
    U96 denx_m = submod96(x_m, y_m, params->f.p);
    U96 vals_m[2] = {denA_m, denx_m};
    U96 invs_m[2];
    if (!invert_batch2_96_mont(invs_m, vals_m, params)) return 0;

    U96 A_m = mont_mul96(num_m, invs_m[0], &params->f);
    U96 xP_m = mont_mul96(x_m, invs_m[1], &params->f);
    U96 A = from_mont96(A_m, &params->f);
    U96 two = u96_from_u64(2);
    U96 pm2 = submod96(params->f.p, two, params->f.p);
    if (cmp96(A, two) <= 0 || cmp96(A, pm2) >= 0) return 0;
    *Ao = A;
    *Amo = A_m;
    *xPmo = xP_m;
    return 1;
}

HD static int x16_root_to_montgomery_xP96_mont(U96 *xPmo, U96 x_m, U96 y_m,
                                               const SearchParams96 *params) {
    U96 denx_m = submod96(x_m, y_m, params->f.p);
    if (is_zero96(denx_m)) return 0;
    U96 inv_denx_m = invert96_mont(denx_m, params);
    *xPmo = mont_mul96(x_m, inv_denx_m, &params->f);
    return 1;
}

HD static int halve_once_first96_mont(U96 *xo_m, U96 A_m, U96 x_m,
                                      const SearchParams96 *params) {
    U96 x2_m = mont_mul96(x_m, x_m, &params->f);
    U96 d_m = addmod96(addmod96(x2_m, mont_mul96(A_m, x_m, &params->f),
                                params->f.p),
                       params->f.one, params->f.p);
    U96 sd_m;
    if (!sqrtmod_p5_96_mont(&sd_m, d_m, params)) return 0;

    U96 roots_d[2] = {sd_m, submod96(u96_from_u64(0), sd_m, params->f.p)};
    for (int i = 0; i < 2; i++) {
        U96 u_m = addmod96(addmod96(x_m, x_m, params->f.p),
                           addmod96(roots_d[i], roots_d[i], params->f.p),
                           params->f.p);
        U96 w_m = submod96(mont_mul96(u_m, u_m, &params->f), params->four_m,
                           params->f.p);
        U96 sw_m;
        if (!sqrtmod_p5_96_mont(&sw_m, w_m, params)) continue;
        U96 candidates[2] = {
            mont_mul96(addmod96(u_m, sw_m, params->f.p), params->inv2_m, &params->f),
            mont_mul96(submod96(u_m, sw_m, params->f.p), params->inv2_m, &params->f),
        };
        for (int j = 0; j < 2; j++) {
            if (!is_zero96(candidates[j])) {
                *xo_m = candidates[j];
                return 1;
            }
        }
    }
    return 0;
}

HD static int halve_once_first96_mont_trace(U96 *xo_m, U96 *first_w_m,
                                            U96 *first_v_m, U96 A_m, U96 x_m,
                                            const SearchParams96 *params) {
    U96 x2_m = mont_mul96(x_m, x_m, &params->f);
    U96 d_m = addmod96(addmod96(x2_m, mont_mul96(A_m, x_m, &params->f),
                                params->f.p),
                       params->f.one, params->f.p);
    U96 sd_m;
    if (!sqrtmod_p5_96_mont(&sd_m, d_m, params)) return 0;

    U96 roots_d[2] = {sd_m, submod96(u96_from_u64(0), sd_m, params->f.p)};
    for (int i = 0; i < 2; i++) {
        U96 u_m = addmod96(addmod96(x_m, x_m, params->f.p),
                           addmod96(roots_d[i], roots_d[i], params->f.p),
                           params->f.p);
        U96 w_m = submod96(mont_mul96(u_m, u_m, &params->f), params->four_m,
                           params->f.p);
        U96 sw_m;
        if (!sqrtmod_p5_96_mont(&sw_m, w_m, params)) continue;
        U96 candidates[2] = {
            mont_mul96(addmod96(u_m, sw_m, params->f.p), params->inv2_m, &params->f),
            mont_mul96(submod96(u_m, sw_m, params->f.p), params->inv2_m, &params->f),
        };
        for (int j = 0; j < 2; j++) {
            if (!is_zero96(candidates[j])) {
                *xo_m = candidates[j];
                *first_w_m = w_m;
                *first_v_m = u_m;
                return 1;
            }
        }
    }
    return 0;
}

HD static int halve_once_first96_mont_uprecheck(U96 *xo_m, U96 A_m, U96 x_m,
                                                int need_next_gate,
                                                const SearchParams96 *params,
                                                UPrecheckCounters *counters) {
    U96 x2_m = mont_mul96(x_m, x_m, &params->f);
    U96 d_m = addmod96(addmod96(x2_m, mont_mul96(A_m, x_m, &params->f),
                                params->f.p),
                       params->f.one, params->f.p);
    U96 sd_m;
    counters->d_sqrt_calls++;
    if (!sqrtmod_p5_96_mont(&sd_m, d_m, params)) return 0;
    counters->d_sqrt_success++;

    int rejected_possible_w_branch = 0;
    U96 roots_d[2] = {sd_m, submod96(u96_from_u64(0), sd_m, params->f.p)};
    for (int i = 0; i < 2; i++) {
        U96 u_m = addmod96(addmod96(x_m, x_m, params->f.p),
                           addmod96(roots_d[i], roots_d[i], params->f.p),
                           params->f.p);
        if (need_next_gate) {
            counters->uplus_checks++;
            int uplus_chi = chi96_mont(addmod96(u_m, params->two_m,
                                                params->f.p),
                                       params);
            if (uplus_chi != 1) {
                counters->uplus_reject++;
                rejected_possible_w_branch = 1;
                continue;
            }
            counters->uplus_pass++;
        }

        U96 w_m = submod96(mont_mul96(u_m, u_m, &params->f), params->four_m,
                           params->f.p);
        U96 sw_m;
        counters->w_sqrt_calls++;
        if (!sqrtmod_p5_96_mont(&sw_m, w_m, params)) continue;
        counters->w_sqrt_success++;

        U96 candidates[2] = {
            mont_mul96(addmod96(u_m, sw_m, params->f.p), params->inv2_m, &params->f),
            mont_mul96(submod96(u_m, sw_m, params->f.p), params->inv2_m, &params->f),
        };
        for (int j = 0; j < 2; j++) {
            if (!is_zero96(candidates[j])) {
                *xo_m = candidates[j];
                return 1;
            }
        }
    }
    if (need_next_gate && rejected_possible_w_branch) {
        counters->precheck_short_circuit++;
        return 2;
    }
    return 0;
}

HD static int halve_chain_from_depth96_mont(U96 *xout_m, U96 A_m, U96 x_m,
                                            int depth, const SearchParams96 *params) {
    for (; depth < params->k; depth++) {
        if (!halve_once_first96_mont(&x_m, A_m, x_m, params)) return 0;
    }
    if (!verify96_mont(A_m, x_m, params)) return 0;
    *xout_m = x_m;
    return 1;
}

HD static int halve_chain_from_depth96_mont_trace(U96 *xout_m, U96 *first_w_m,
                                                  U96 *first_v_m, U96 A_m,
                                                  U96 x_m, int depth,
                                                  const SearchParams96 *params) {
    int first = 1;
    for (; depth < params->k; depth++) {
        if (first) {
            if (!halve_once_first96_mont_trace(&x_m, first_w_m, first_v_m,
                                               A_m, x_m, params)) return 0;
            first = 0;
        } else if (!halve_once_first96_mont(&x_m, A_m, x_m, params)) {
            return 0;
        }
    }
    if (!verify96_mont(A_m, x_m, params)) return 0;
    *xout_m = x_m;
    return 1;
}

HD static int halve_prefix_depth96_mont_trace(U96 *xout_m, U96 *first_w_m,
                                              U96 *first_v_m, U96 A_m,
                                              U96 x_m, int depth,
                                              int target_depth,
                                              const SearchParams96 *params) {
    if (target_depth > params->k) target_depth = params->k;
    if (target_depth > PROBE_MAX_DEPTH) target_depth = PROBE_MAX_DEPTH;
    if (depth >= target_depth) {
        *xout_m = x_m;
        return depth;
    }

    if (!halve_once_first96_mont_trace(&x_m, first_w_m, first_v_m,
                                       A_m, x_m, params)) {
        *xout_m = x_m;
        return depth;
    }
    depth++;
    while (depth < target_depth) {
        if (!halve_once_first96_mont(&x_m, A_m, x_m, params)) break;
        depth++;
    }
    *xout_m = x_m;
    return depth;
}

HD static int halve_prefix_depth96_mont(U96 *xout_m, U96 A_m, U96 x_m,
                                        int depth, int target_depth,
                                        const SearchParams96 *params) {
    if (target_depth > params->k) target_depth = params->k;
    if (target_depth > PROBE_MAX_DEPTH) target_depth = PROBE_MAX_DEPTH;
    while (depth < target_depth) {
        if (!halve_once_first96_mont(&x_m, A_m, x_m, params)) break;
        depth++;
    }
    *xout_m = x_m;
    return depth;
}

HD static int halve_prefix_depth96_mont_uprecheck(U96 *xout_m, U96 A_m,
                                                  U96 x_m, int depth,
                                                  int target_depth,
                                                  const SearchParams96 *params,
                                                  UPrecheckCounters *counters) {
    if (target_depth > params->k) target_depth = params->k;
    if (target_depth > PROBE_MAX_DEPTH) target_depth = PROBE_MAX_DEPTH;
    while (depth < target_depth) {
        int need_next_gate = (depth + 1) < target_depth;
        int step = halve_once_first96_mont_uprecheck(&x_m, A_m, x_m,
                                                     need_next_gate, params,
                                                     counters);
        if (step == 1) {
            depth++;
            continue;
        }
        if (step == 2) {
            *xout_m = x_m;
            return depth + 1;
        }
        break;
    }
    *xout_m = x_m;
    return depth;
}

DEV static U96 rand_below96(Rng *rng, const SearchParams96 *params) {
    for (;;) {
        u64 a = rng64(rng);
        u64 b = rng64(rng);
        U96 v{{(u32)a, (u32)(a >> 32), (u32)b}};
        v = and96(v, params->rand_mask);
        if (cmp96(v, params->f.p) < 0) return v;
    }
}

DEV static U96 rand_below96_counted(Rng *rng, const SearchParams96 *params,
                                    u64 *raw_draw_count) {
    for (;;) {
        (*raw_draw_count)++;
        u64 a = rng64(rng);
        u64 b = rng64(rng);
        U96 v{{(u32)a, (u32)(a >> 32), (u32)b}};
        v = and96(v, params->rand_mask);
        if (cmp96(v, params->f.p) < 0) return v;
    }
}

__global__ static void x16halvenonsplit_kernel96(SearchParams96 params,
                                                 u64 seed_offset,
                                                 u64 chunk_nonce,
                                                 u64 max_curves,
                                                 u64 global_base,
                                                 u64 claim_batch,
                                                 int seed_mode,
                                                 GpuStats *__restrict__ stats,
                                                 GpuResult *__restrict__ result) {
    u64 tid = (u64)blockIdx.x * (u64)blockDim.x + (u64)threadIdx.x;
    u64 total_threads = (u64)gridDim.x * (u64)blockDim.x;
    Rng rng;
    init_rng(&rng, seed_offset, chunk_nonce, tid, total_threads, seed_mode);

    u64 local_processed = 0;
#if POM_CUDA_HIT_TELEMETRY
    u64 local_raw_draws = 0;
    u64 local_y_draws_for_result = 0;
#endif
#if POM_CUDA_DETAILED_STATS
    u64 local_y_draws = 0;
    u64 local_y_nonsplit = 0;
    u64 local_y_with_sqrt_D = 0;
    u64 local_roots_valid = 0;
    u64 local_halve_calls = 0;
    u64 local_chain_survivors = 0;
#endif
    u64 next_claim = 0;
    u64 claim_limit = 0;

    while (!found_now(result)) {
#if POM_CUDA_HIT_TELEMETRY
        U96 y = rand_below96_counted(&rng, &params, &local_raw_draws);
        local_y_draws_for_result++;
#else
        U96 y = rand_below96(&rng, &params);
#endif
#if POM_CUDA_DETAILED_STATS
        local_y_draws++;
#endif
        if (is_zero96(y)) continue;

        U96 y_m = to_mont96(y, &params.f);
        U96 y2_m = mont_mul96(y_m, y_m, &params.f);
        if (!x16_y_predicts_nonsplit96_mont(y_m, y2_m, &params)) continue;
#if POM_CUDA_DETAILED_STATS
        local_y_nonsplit++;
#endif

        U96 y3_m = mont_mul96(y2_m, y_m, &params.f);
        U96 two_y_m = addmod96(y_m, y_m, params.f.p);
        U96 qa_m = submod96(y2_m, two_y_m, params.f.p);
        if (is_zero96(qa_m)) continue;
        U96 qb_m = submod96(addmod96(y2_m, y2_m, params.f.p), y3_m, params.f.p);
        U96 qc_m = submod96(params.f.one, y_m, params.f.p);
        U96 D_m = submod96(
            mont_mul96(qb_m, qb_m, &params.f),
            mont_mul96(addmod96(qa_m, qa_m, params.f.p),
                       addmod96(qc_m, qc_m, params.f.p), &params.f),
            params.f.p);
        U96 sd_m;
        if (!sqrtmod_p5_96_mont(&sd_m, D_m, &params)) continue;
#if POM_CUDA_DETAILED_STATS
        local_y_with_sqrt_D++;
#endif

        U96 inv_2qa_m = invert96_mont(addmod96(qa_m, qa_m, params.f.p), &params);
        U96 roots_m[2] = {
            mont_mul96(submod96(sd_m, qb_m, params.f.p), inv_2qa_m, &params.f),
            mont_mul96(submod96(submod96(u96_from_u64(0), sd_m, params.f.p), qb_m,
                                params.f.p),
                       inv_2qa_m, &params.f),
        };

        U96 A;
        U96 A_m;
        U96 xP16_m[2];
        int root_valid[2] = {0, 0};
        root_valid[0] = x16_root_to_montgomery_A96_mont(&A, &A_m, &xP16_m[0],
                                                        roots_m[0], y_m, &params);
        if (root_valid[0]) {
            root_valid[1] = x16_root_to_montgomery_xP96_mont(&xP16_m[1],
                                                             roots_m[1], y_m,
                                                             &params);
        } else {
            root_valid[1] = x16_root_to_montgomery_A96_mont(&A, &A_m, &xP16_m[1],
                                                            roots_m[1], y_m,
                                                            &params);
        }

        int stop = 0;
        for (int ri = 0; ri < 2; ri++) {
            if (!root_valid[ri]) continue;
#if POM_CUDA_DETAILED_STATS
            local_roots_valid++;
#endif

            if (next_claim >= claim_limit) {
                next_claim = atomicAdd(&stats->claimed, claim_batch);
                claim_limit = next_claim + claim_batch;
            }
            u64 claim = next_claim++;
            if (claim >= max_curves || found_now(result)) {
                stop = 1;
                break;
            }

            local_processed++;
#if POM_CUDA_DETAILED_STATS
            local_halve_calls++;
#endif
            U96 xR_m;
#if POM_CUDA_HIT_TELEMETRY
            U96 first_w_m = u96_from_u64(0);
            U96 first_v_m = u96_from_u64(0);
            if (halve_chain_from_depth96_mont_trace(&xR_m, &first_w_m, &first_v_m,
                                                    A_m, xP16_m[ri], 4, &params)) {
#else
            if (halve_chain_from_depth96_mont(&xR_m, A_m, xP16_m[ri], 4, &params)) {
#endif
#if POM_CUDA_DETAILED_STATS
                local_chain_survivors++;
#endif
                if (atomicCAS(&result->found, 0, 1) == 0) {
                    result->trial_index = global_base + claim;
                    result->A = pack96(A);
                    result->x0 = pack96(from_mont96(xR_m, &params.f));
#if POM_CUDA_HIT_TELEMETRY
                    U96 D = from_mont96(D_m, &params.f);
                    result->chunk_nonce = chunk_nonce;
                    result->tid = tid;
                    result->raw_draw_count = local_raw_draws;
                    result->local_draw_count = local_y_draws_for_result;
                    result->root_index = ri;
                    result->q_sheet = ri;
                    result->compactD = compact128(u96_to_u128(D));
                    result->y = pack96(y);
                    result->root_x = pack96(from_mont96(roots_m[ri], &params.f));
                    result->xP16 = pack96(from_mont96(xP16_m[ri], &params.f));
                    result->first_w = pack96(from_mont96(first_w_m, &params.f));
                    result->V = pack96(from_mont96(first_v_m, &params.f));
                    result->D = pack96(D);
#endif
                }
                stop = 1;
                break;
            }
        }
        if (stop) break;
    }

    atomicAdd(&stats->processed, local_processed);
#if POM_CUDA_DETAILED_STATS
    atomicAdd(&stats->y_draws, local_y_draws);
    atomicAdd(&stats->y_nonsplit, local_y_nonsplit);
    atomicAdd(&stats->y_with_sqrt_D, local_y_with_sqrt_D);
    atomicAdd(&stats->roots_valid, local_roots_valid);
    atomicAdd(&stats->halve_calls, local_halve_calls);
    atomicAdd(&stats->chain_survivors, local_chain_survivors);
#endif
}

__global__ static void x16stratumprobe_kernel96(SearchParams96 params,
                                                u64 seed_offset,
                                                u64 chunk_nonce,
                                                u64 max_curves,
                                                u64 global_base,
                                                u64 split_trial,
                                                u64 claim_batch,
                                                int seed_mode,
                                                int first_gate_filter,
                                                int prefix_filter_depth,
                                                int target_depth,
                                                int bucket_bits,
                                                ProbeStats *__restrict__ probe) {
    u64 tid = (u64)blockIdx.x * (u64)blockDim.x + (u64)threadIdx.x;
    u64 total_threads = (u64)gridDim.x * (u64)blockDim.x;
    Rng rng;
    init_rng(&rng, seed_offset, chunk_nonce, tid, total_threads, seed_mode);

    u64 local_accepted = 0;
    u64 local_y_draws = 0;
    u64 local_y_nonsplit = 0;
    u64 local_y_with_sqrt_D = 0;
    u64 local_roots_valid = 0;
    u64 next_claim = 0;
    u64 claim_limit = 0;

    while (!probe_done_now(probe, max_curves)) {
        U96 y = rand_below96(&rng, &params);
        local_y_draws++;
        if (is_zero96(y)) continue;

        U96 y_m = to_mont96(y, &params.f);
        U96 y2_m = mont_mul96(y_m, y_m, &params.f);
        if (!x16_y_predicts_nonsplit96_mont(y_m, y2_m, &params)) continue;
        local_y_nonsplit++;

        if (first_gate_filter) {
            U96 ym1_m = submod96(y_m, params.f.one, params.f.p);
            if (is_zero96(ym1_m)) continue;
            U96 two_y_filter_m = addmod96(y_m, y_m, params.f.p);
            U96 B_m = addmod96(submod96(y2_m, two_y_filter_m, params.f.p),
                               params.two_m, params.f.p);
            U96 C_m = submod96(y2_m, params.two_m, params.f.p);
            U96 F_m = mont_mul96(mont_mul96(ym1_m, C_m, &params.f),
                                 B_m, &params.f);
            if (chi96_mont(F_m, &params) != 1) continue;
        }

        U96 y3_m = mont_mul96(y2_m, y_m, &params.f);
        U96 two_y_m = addmod96(y_m, y_m, params.f.p);
        U96 qa_m = submod96(y2_m, two_y_m, params.f.p);
        if (is_zero96(qa_m)) continue;
        U96 qb_m = submod96(addmod96(y2_m, y2_m, params.f.p), y3_m, params.f.p);
        U96 qc_m = submod96(params.f.one, y_m, params.f.p);
        U96 D_m = submod96(
            mont_mul96(qb_m, qb_m, &params.f),
            mont_mul96(addmod96(qa_m, qa_m, params.f.p),
                       addmod96(qc_m, qc_m, params.f.p), &params.f),
            params.f.p);
        U96 sd_m;
        if (!sqrtmod_p5_96_mont(&sd_m, D_m, &params)) continue;
        local_y_with_sqrt_D++;

        U96 inv_2qa_m = invert96_mont(addmod96(qa_m, qa_m, params.f.p), &params);
        U96 roots_m[2] = {
            mont_mul96(submod96(sd_m, qb_m, params.f.p), inv_2qa_m, &params.f),
            mont_mul96(submod96(submod96(u96_from_u64(0), sd_m, params.f.p), qb_m,
                                params.f.p),
                       inv_2qa_m, &params.f),
        };

        U96 A;
        U96 A_m;
        U96 xP16_m[2];
        int root_valid[2] = {0, 0};
        root_valid[0] = x16_root_to_montgomery_A96_mont(&A, &A_m, &xP16_m[0],
                                                        roots_m[0], y_m, &params);
        if (root_valid[0]) {
            root_valid[1] = x16_root_to_montgomery_xP96_mont(&xP16_m[1],
                                                             roots_m[1], y_m,
                                                             &params);
        } else {
            root_valid[1] = x16_root_to_montgomery_A96_mont(&A, &A_m, &xP16_m[1],
                                                            roots_m[1], y_m,
                                                            &params);
        }

        int stop = 0;
        for (int ri = 0; ri < 2; ri++) {
            if (!root_valid[ri]) continue;
            local_roots_valid++;

            U96 x_start_m = xP16_m[ri];
            U96 first_w_m = u96_from_u64(0);
            U96 first_v_m = u96_from_u64(0);
            int effective_prefix_depth = prefix_filter_depth;
            if (effective_prefix_depth < 4) effective_prefix_depth = 4;
            if (effective_prefix_depth > target_depth) {
                effective_prefix_depth = target_depth;
            }
            if (effective_prefix_depth > 4) {
                int prefix_reached = halve_prefix_depth96_mont_trace(
                    &x_start_m, &first_w_m, &first_v_m, A_m, x_start_m, 4,
                    effective_prefix_depth, &params);
                if (prefix_reached < effective_prefix_depth) continue;
            }

            if (next_claim >= claim_limit) {
                next_claim = atomicAdd(&probe->claimed, claim_batch);
                claim_limit = next_claim + claim_batch;
            }
            u64 claim = next_claim++;
            if (claim >= max_curves) {
                stop = 1;
                break;
            }

            local_accepted++;
            U96 x_probe_m;
            int reached_depth;
            if (effective_prefix_depth > 4) {
                reached_depth = halve_prefix_depth96_mont(
                    &x_probe_m, A_m, x_start_m, effective_prefix_depth,
                    target_depth, &params);
            } else {
                reached_depth = halve_prefix_depth96_mont_trace(
                    &x_probe_m, &first_w_m, &first_v_m, A_m, x_start_m, 4,
                    target_depth, &params);
            }
            U96 D = from_mont96(D_m, &params.f);
            U96 first_w = from_mont96(first_w_m, &params.f);
            U96 first_v = from_mont96(first_v_m, &params.f);
            u64 source_hash = compact128(u96_to_u128(D)) ^
                              (compact128(u96_to_u128(first_w)) *
                               0x9e3779b97f4a7c15ULL) ^
                              (compact128(u96_to_u128(first_v)) *
                               0xd1342543de82ef95ULL) ^
                              (compact128(u96_to_u128(y)) *
                               0x94d049bb133111ebULL);
            probe_record_candidate(probe, global_base + claim, split_trial,
                                   reached_depth, target_depth, ri, source_hash,
                                   bucket_bits);
        }
        if (stop) break;
    }

    atomicAdd(&probe->accepted_roots, local_accepted);
    atomicAdd(&probe->y_draws, local_y_draws);
    atomicAdd(&probe->y_nonsplit, local_y_nonsplit);
    atomicAdd(&probe->y_with_sqrt_D, local_y_with_sqrt_D);
    atomicAdd(&probe->roots_valid, local_roots_valid);
}

__global__ static void x16ecoverprobe_kernel96(SearchParams96 params,
                                               u64 seed_offset,
                                               u64 chunk_nonce,
                                               u64 max_curves,
                                               u64 global_base,
                                               u64 split_trial,
                                               u64 claim_batch,
                                               int seed_mode,
                                               int prefix_filter_depth,
                                               int target_depth,
                                               int bucket_bits,
                                               ProbeStats *__restrict__ probe) {
    u64 tid = (u64)blockIdx.x * (u64)blockDim.x + (u64)threadIdx.x;
    u64 total_threads = (u64)gridDim.x * (u64)blockDim.x;
    Rng rng;
    init_rng(&rng, seed_offset, chunk_nonce, tid, total_threads, seed_mode);

    u64 local_accepted = 0;
    u64 local_x_draws = 0;
    u64 local_y_nonsplit = 0;
    u64 local_y_with_sqrt_D = 0;
    u64 local_roots_valid = 0;
    u64 next_claim = 0;
    u64 claim_limit = 0;

    while (!probe_done_now(probe, max_curves)) {
        U96 X = rand_below96(&rng, &params);
        local_x_draws++;

        U96 X_m = to_mont96(X, &params.f);
        U96 X2_m = mont_mul96(X_m, X_m, &params.f);
        U96 rhs_m = submod96(mont_mul96(X2_m, X_m, &params.f), X_m,
                             params.f.p);
        U96 W_m;
        if (!sqrtmod_p5_96_mont(&W_m, rhs_m, &params)) continue;

        U96 y_m = addmod96(X_m, params.f.one, params.f.p);
        if (is_zero96(y_m)) continue;
        U96 y2_m = mont_mul96(y_m, y_m, &params.f);
        if (!x16_y_predicts_nonsplit96_mont(y_m, y2_m, &params)) continue;
        local_y_nonsplit++;

        U96 y3_m = mont_mul96(y2_m, y_m, &params.f);
        U96 two_y_m = addmod96(y_m, y_m, params.f.p);
        U96 qa_m = submod96(y2_m, two_y_m, params.f.p);
        if (is_zero96(qa_m)) continue;
        U96 qb_m = submod96(addmod96(y2_m, y2_m, params.f.p), y3_m, params.f.p);
        U96 qc_m = submod96(params.f.one, y_m, params.f.p);
        U96 D_m = submod96(
            mont_mul96(qb_m, qb_m, &params.f),
            mont_mul96(addmod96(qa_m, qa_m, params.f.p),
                       addmod96(qc_m, qc_m, params.f.p), &params.f),
            params.f.p);
        U96 sd_m;
        if (!sqrtmod_p5_96_mont(&sd_m, D_m, &params)) continue;
        local_y_with_sqrt_D++;

        U96 inv_2qa_m = invert96_mont(addmod96(qa_m, qa_m, params.f.p), &params);
        U96 roots_m[2] = {
            mont_mul96(submod96(sd_m, qb_m, params.f.p), inv_2qa_m, &params.f),
            mont_mul96(submod96(submod96(u96_from_u64(0), sd_m, params.f.p), qb_m,
                                params.f.p),
                       inv_2qa_m, &params.f),
        };

        U96 A;
        U96 A_m;
        U96 xP16_m[2];
        int root_valid[2] = {0, 0};
        root_valid[0] = x16_root_to_montgomery_A96_mont(&A, &A_m, &xP16_m[0],
                                                        roots_m[0], y_m, &params);
        if (root_valid[0]) {
            root_valid[1] = x16_root_to_montgomery_xP96_mont(&xP16_m[1],
                                                             roots_m[1], y_m,
                                                             &params);
        } else {
            root_valid[1] = x16_root_to_montgomery_A96_mont(&A, &A_m, &xP16_m[1],
                                                            roots_m[1], y_m,
                                                            &params);
        }

        U96 y = from_mont96(y_m, &params.f);
        int stop = 0;
        for (int ri = 0; ri < 2; ri++) {
            if (!root_valid[ri]) continue;
            local_roots_valid++;

            U96 x_start_m = xP16_m[ri];
            U96 first_w_m = u96_from_u64(0);
            U96 first_v_m = u96_from_u64(0);
            int effective_prefix_depth = prefix_filter_depth;
            if (effective_prefix_depth < 4) effective_prefix_depth = 4;
            if (effective_prefix_depth > target_depth) {
                effective_prefix_depth = target_depth;
            }
            if (effective_prefix_depth > 4) {
                int prefix_reached = halve_prefix_depth96_mont_trace(
                    &x_start_m, &first_w_m, &first_v_m, A_m, x_start_m, 4,
                    effective_prefix_depth, &params);
                if (prefix_reached < effective_prefix_depth) continue;
            }

            if (next_claim >= claim_limit) {
                next_claim = atomicAdd(&probe->claimed, claim_batch);
                claim_limit = next_claim + claim_batch;
            }
            u64 claim = next_claim++;
            if (claim >= max_curves) {
                stop = 1;
                break;
            }

            local_accepted++;
            U96 x_probe_m;
            int reached_depth;
            if (effective_prefix_depth > 4) {
                reached_depth = halve_prefix_depth96_mont(
                    &x_probe_m, A_m, x_start_m, effective_prefix_depth,
                    target_depth, &params);
            } else {
                reached_depth = halve_prefix_depth96_mont_trace(
                    &x_probe_m, &first_w_m, &first_v_m, A_m, x_start_m, 4,
                    target_depth, &params);
            }
            U96 D = from_mont96(D_m, &params.f);
            U96 first_w = from_mont96(first_w_m, &params.f);
            U96 first_v = from_mont96(first_v_m, &params.f);
            u64 source_hash = compact128(u96_to_u128(D)) ^
                              (compact128(u96_to_u128(first_w)) *
                               0x9e3779b97f4a7c15ULL) ^
                              (compact128(u96_to_u128(first_v)) *
                               0xd1342543de82ef95ULL) ^
                              (compact128(u96_to_u128(X)) *
                               0x94d049bb133111ebULL) ^
                              (compact128(u96_to_u128(y)) *
                               0x2545f4914f6cdd1dULL);
            probe_record_candidate(probe, global_base + claim, split_trial,
                                   reached_depth, target_depth, ri, source_hash,
                                   bucket_bits);
        }
        if (stop) break;
    }

    atomicAdd(&probe->accepted_roots, local_accepted);
    atomicAdd(&probe->y_draws, local_x_draws);
    atomicAdd(&probe->y_nonsplit, local_y_nonsplit);
    atomicAdd(&probe->y_with_sqrt_D, local_y_with_sqrt_D);
    atomicAdd(&probe->roots_valid, local_roots_valid);
}

__global__ static void x16uprecheckprobe_kernel96(SearchParams96 params,
                                                  u64 seed_offset,
                                                  u64 chunk_nonce,
                                                  u64 max_curves,
                                                  u64 claim_batch,
                                                  int seed_mode,
                                                  int target_depth,
                                                  UPrecheckStats *__restrict__ stats) {
    u64 tid = (u64)blockIdx.x * (u64)blockDim.x + (u64)threadIdx.x;
    u64 total_threads = (u64)gridDim.x * (u64)blockDim.x;
    Rng rng;
    init_rng(&rng, seed_offset, chunk_nonce, tid, total_threads, seed_mode);

    u64 local_accepted = 0;
    u64 local_y_draws = 0;
    u64 local_y_nonsplit = 0;
    u64 local_y_with_sqrt_D = 0;
    u64 local_roots_valid = 0;
    UPrecheckCounters local_counters{};
    u64 next_claim = 0;
    u64 claim_limit = 0;

    while (!uprecheck_done_now(stats, max_curves)) {
        U96 y = rand_below96(&rng, &params);
        local_y_draws++;
        if (is_zero96(y)) continue;

        U96 y_m = to_mont96(y, &params.f);
        U96 y2_m = mont_mul96(y_m, y_m, &params.f);
        if (!x16_y_predicts_nonsplit96_mont(y_m, y2_m, &params)) continue;
        local_y_nonsplit++;

        U96 y3_m = mont_mul96(y2_m, y_m, &params.f);
        U96 two_y_m = addmod96(y_m, y_m, params.f.p);
        U96 qa_m = submod96(y2_m, two_y_m, params.f.p);
        if (is_zero96(qa_m)) continue;
        U96 qb_m = submod96(addmod96(y2_m, y2_m, params.f.p), y3_m, params.f.p);
        U96 qc_m = submod96(params.f.one, y_m, params.f.p);
        U96 D_m = submod96(
            mont_mul96(qb_m, qb_m, &params.f),
            mont_mul96(addmod96(qa_m, qa_m, params.f.p),
                       addmod96(qc_m, qc_m, params.f.p), &params.f),
            params.f.p);
        U96 sd_m;
        if (!sqrtmod_p5_96_mont(&sd_m, D_m, &params)) continue;
        local_y_with_sqrt_D++;

        U96 inv_2qa_m = invert96_mont(addmod96(qa_m, qa_m, params.f.p), &params);
        U96 roots_m[2] = {
            mont_mul96(submod96(sd_m, qb_m, params.f.p), inv_2qa_m, &params.f),
            mont_mul96(submod96(submod96(u96_from_u64(0), sd_m, params.f.p), qb_m,
                                params.f.p),
                       inv_2qa_m, &params.f),
        };

        U96 A;
        U96 A_m;
        U96 xP16_m[2];
        int root_valid[2] = {0, 0};
        root_valid[0] = x16_root_to_montgomery_A96_mont(&A, &A_m, &xP16_m[0],
                                                        roots_m[0], y_m, &params);
        if (root_valid[0]) {
            root_valid[1] = x16_root_to_montgomery_xP96_mont(&xP16_m[1],
                                                             roots_m[1], y_m,
                                                             &params);
        } else {
            root_valid[1] = x16_root_to_montgomery_A96_mont(&A, &A_m, &xP16_m[1],
                                                            roots_m[1], y_m,
                                                            &params);
        }

        int stop = 0;
        for (int ri = 0; ri < 2; ri++) {
            if (!root_valid[ri]) continue;
            local_roots_valid++;

            if (next_claim >= claim_limit) {
                next_claim = atomicAdd(&stats->claimed, claim_batch);
                claim_limit = next_claim + claim_batch;
            }
            u64 claim = next_claim++;
            if (claim >= max_curves) {
                stop = 1;
                break;
            }

            local_accepted++;
            U96 x_probe_m;
            int reached_depth = halve_prefix_depth96_mont_uprecheck(
                &x_probe_m, A_m, xP16_m[ri], 4, target_depth, &params,
                &local_counters);
            uprecheck_record_candidate(stats, reached_depth);
        }
        if (stop) break;
    }

    atomicAdd(&stats->accepted_roots, local_accepted);
    atomicAdd(&stats->y_draws, local_y_draws);
    atomicAdd(&stats->y_nonsplit, local_y_nonsplit);
    atomicAdd(&stats->y_with_sqrt_D, local_y_with_sqrt_D);
    atomicAdd(&stats->roots_valid, local_roots_valid);
    atomicAdd(&stats->counters.d_sqrt_calls, local_counters.d_sqrt_calls);
    atomicAdd(&stats->counters.d_sqrt_success, local_counters.d_sqrt_success);
    atomicAdd(&stats->counters.uplus_checks, local_counters.uplus_checks);
    atomicAdd(&stats->counters.uplus_pass, local_counters.uplus_pass);
    atomicAdd(&stats->counters.uplus_reject, local_counters.uplus_reject);
    atomicAdd(&stats->counters.w_sqrt_calls, local_counters.w_sqrt_calls);
    atomicAdd(&stats->counters.w_sqrt_success, local_counters.w_sqrt_success);
    atomicAdd(&stats->counters.precheck_short_circuit,
              local_counters.precheck_short_circuit);
}

__global__ static void x16tracenormab_kernel96(SearchParams96 params,
                                               u64 seed_offset,
                                               u64 chunk_nonce,
                                               u64 raw_y_draws,
                                               int seed_mode,
                                               int filter_only,
                                               TraceNormABStats *__restrict__ stats) {
    u64 tid = (u64)blockIdx.x * (u64)blockDim.x + (u64)threadIdx.x;
    u64 total_threads = (u64)gridDim.x * (u64)blockDim.x;
    Rng rng;
    init_rng(&rng, seed_offset, chunk_nonce, tid, total_threads, seed_mode);

    const int target_depth = trace_ab_depth_value(TRACE_AB_DEPTH_COUNT - 1);

    u64 local_raw_y_draws = 0;
    u64 local_nonsplit_y = 0;
    u64 local_f_square = 0;
    u64 local_d_plus = 0;
    u64 local_d_minus = 0;
    u64 local_d_zero = 0;
    u64 local_t_line_plus = 0;
    u64 local_t_line_minus = 0;
    u64 local_t_line_inconsistent = 0;
    u64 local_t_line_unusable = 0;
    u64 local_branch_sqrt_y = 0;
    u64 local_roots_valid = 0;
    u64 local_ordinary_emitted = 0;
    u64 local_candidate_emitted = 0;
    u64 local_ordinary_survive[TRACE_AB_DEPTH_COUNT] = {0, 0, 0, 0, 0, 0};
    u64 local_candidate_survive[TRACE_AB_DEPTH_COUNT] = {0, 0, 0, 0, 0, 0};

    u64 draws_per_thread = (raw_y_draws + total_threads - 1) / total_threads;
    for (u64 i = 0; i < draws_per_thread; i++) {
        u64 draw_index = i * total_threads + tid;
        if (draw_index >= raw_y_draws) break;

        U96 y = rand_below96(&rng, &params);
        local_raw_y_draws++;
        if (is_zero96(y)) continue;

        U96 y_m = to_mont96(y, &params.f);
        U96 y2_m = mont_mul96(y_m, y_m, &params.f);
        if (!x16_y_predicts_nonsplit96_mont(y_m, y2_m, &params)) continue;
        local_nonsplit_y++;

        TraceNormLineClass line{};
        x16_trace_norm_line_class96(&line, y_m, y2_m, &params);
        int candidate_gate = 0;
        if (line.valid && line.domain_line == 1) {
            local_f_square++;
            if (line.d_class == 1) {
                local_d_plus++;
                candidate_gate = 1;
            } else if (line.d_class == -1) {
                local_d_minus++;
            } else {
                local_d_zero++;
            }

            if (line.t_line == 1) {
                local_t_line_plus++;
            } else if (line.t_line == -1) {
                local_t_line_minus++;
            } else {
                local_t_line_unusable++;
            }
            if (line.t_line != 0 && line.a_chi != 0 && line.b_chi != 0) {
                int expected = (line.a_chi == 1) ? line.t_class
                                                 : line.t_class * line.b_chi;
                if (line.t_line != expected) local_t_line_inconsistent++;
            }
        }
        if (filter_only && !candidate_gate) continue;

        U96 y3_m = mont_mul96(y2_m, y_m, &params.f);
        U96 two_y_m = addmod96(y_m, y_m, params.f.p);
        U96 qa_m = submod96(y2_m, two_y_m, params.f.p);
        if (is_zero96(qa_m)) continue;
        U96 qb_m = submod96(addmod96(y2_m, y2_m, params.f.p), y3_m, params.f.p);
        U96 qc_m = submod96(params.f.one, y_m, params.f.p);
        U96 D_m = submod96(
            mont_mul96(qb_m, qb_m, &params.f),
            mont_mul96(addmod96(qa_m, qa_m, params.f.p),
                       addmod96(qc_m, qc_m, params.f.p), &params.f),
            params.f.p);
        U96 sd_m;
        if (!sqrtmod_p5_96_mont(&sd_m, D_m, &params)) continue;
        local_branch_sqrt_y++;

        U96 inv_2qa_m = invert96_mont(addmod96(qa_m, qa_m, params.f.p), &params);
        U96 roots_m[2] = {
            mont_mul96(submod96(sd_m, qb_m, params.f.p), inv_2qa_m, &params.f),
            mont_mul96(submod96(submod96(u96_from_u64(0), sd_m, params.f.p), qb_m,
                                params.f.p),
                       inv_2qa_m, &params.f),
        };

        U96 A;
        U96 A_m;
        U96 xP16_m[2];
        int root_valid[2] = {0, 0};
        root_valid[0] = x16_root_to_montgomery_A96_mont(&A, &A_m, &xP16_m[0],
                                                        roots_m[0], y_m, &params);
        if (root_valid[0]) {
            root_valid[1] = x16_root_to_montgomery_xP96_mont(&xP16_m[1],
                                                             roots_m[1], y_m,
                                                             &params);
        } else {
            root_valid[1] = x16_root_to_montgomery_A96_mont(&A, &A_m, &xP16_m[1],
                                                            roots_m[1], y_m,
                                                            &params);
        }

        for (int ri = 0; ri < 2; ri++) {
            if (!root_valid[ri]) continue;
            local_roots_valid++;
            if (!filter_only) local_ordinary_emitted++;

            U96 x_probe_m;
            U96 first_w_m = u96_from_u64(0);
            U96 first_v_m = u96_from_u64(0);
            int reached_depth = halve_prefix_depth96_mont_trace(
                &x_probe_m, &first_w_m, &first_v_m, A_m, xP16_m[ri], 4,
                target_depth, &params);
            for (int di = 0; di < TRACE_AB_DEPTH_COUNT; di++) {
                if (reached_depth >= trace_ab_depth_value(di)) {
                    if (!filter_only) local_ordinary_survive[di]++;
                    if (candidate_gate) local_candidate_survive[di]++;
                }
            }
            if (candidate_gate) local_candidate_emitted++;
        }
    }

    atomicAdd(&stats->raw_y_draws, local_raw_y_draws);
    atomicAdd(&stats->nonsplit_y, local_nonsplit_y);
    atomicAdd(&stats->f_square, local_f_square);
    atomicAdd(&stats->d_plus, local_d_plus);
    atomicAdd(&stats->d_minus, local_d_minus);
    atomicAdd(&stats->d_zero, local_d_zero);
    atomicAdd(&stats->t_line_plus, local_t_line_plus);
    atomicAdd(&stats->t_line_minus, local_t_line_minus);
    atomicAdd(&stats->t_line_inconsistent, local_t_line_inconsistent);
    atomicAdd(&stats->t_line_unusable, local_t_line_unusable);
    atomicAdd(&stats->branch_sqrt_y, local_branch_sqrt_y);
    atomicAdd(&stats->roots_valid, local_roots_valid);
    atomicAdd(&stats->ordinary_emitted_candidates, local_ordinary_emitted);
    atomicAdd(&stats->candidate_emitted_candidates, local_candidate_emitted);
    for (int di = 0; di < TRACE_AB_DEPTH_COUNT; di++) {
        atomicAdd(&stats->ordinary_survive[di], local_ordinary_survive[di]);
        atomicAdd(&stats->candidate_survive[di], local_candidate_survive[di]);
    }
}

static void die_cuda(cudaError_t err, const char *what) {
    if (err == cudaSuccess) return;
    std::fprintf(stderr, "CUDA error at %s: %s\n", what, cudaGetErrorString(err));
    std::exit(1);
}

static u128 parse128(const char *s) {
    u128 v = 0;
    while (*s >= '0' && *s <= '9') {
        v = v * 10 + (unsigned)(*s - '0');
        s++;
    }
    return v;
}

static std::string sprint128(u128 v) {
    if (v == 0) return "0";
    char tmp[50];
    int i = 49;
    tmp[i] = '\0';
    while (v > 0) {
        tmp[--i] = char('0' + (int)(v % 10));
        v /= 10;
    }
    return std::string(tmp + i);
}

static int bitlen128(u128 x) {
    u64 hi = (u64)(x >> 64);
    if (hi) return 64 + (64 - __builtin_clzll(hi));
    u64 lo = (u64)x;
    return lo ? 64 - __builtin_clzll(lo) : 0;
}

static void m128_init(Mont128 *m, u128 p) {
    m->p = p;
    u128 x = 1;
    for (int i = 0; i < 7; i++) x *= 2 - p * x;
    m->ni = (u128)0 - x;
    u128 r = 1;
    for (int i = 0; i < 128; i++) {
        r <<= 1;
        if (r >= p) r -= p;
    }
    m->one = r;
    for (int i = 0; i < 128; i++) {
        r <<= 1;
        if (r >= p) r -= p;
    }
    m->R2 = r;
}

static U96 u96_mask_bits(int bits) {
    U96 mask{{0, 0, 0}};
    if (bits >= 96) {
        mask.v[0] = mask.v[1] = mask.v[2] = 0xffffffffu;
        return mask;
    }
    for (int i = 0; i < 3; i++) {
        int limb_bits = bits - 32 * i;
        if (limb_bits >= 32) mask.v[i] = 0xffffffffu;
        else if (limb_bits > 0) mask.v[i] = (1u << limb_bits) - 1u;
        else mask.v[i] = 0;
    }
    return mask;
}

static Field96 field96_init(u128 p128) {
    Field96 f{};
    f.p = u96_from_u128(p128);
    f.nprime = inv32_odd(f.p.v[0]);

    U96 r = u96_from_u64(1);
    for (int i = 0; i < 96; i++) r = addmod96(r, r, f.p);
    f.one = r;
    for (int i = 0; i < 96; i++) r = addmod96(r, r, f.p);
    f.r2 = r;
    return f;
}

static SearchParams96 search_params96_init(u128 p, int k, int pbits) {
    SearchParams96 params{};
    params.f = field96_init(p);
    params.rand_mask = u96_mask_bits(pbits);
    params.leg_exp = (p - 1) >> 1;
    params.sqrt_case = ((u64)(p & 3) == 3) ? 3 : 5;
    params.sqrt_exp = params.sqrt_case == 3 ? ((p + 1) >> 2) : ((p + 3) >> 3);
    params.inv_exp = p - 2;
    params.k = k;
    params.two_m = to_mont96(u96_from_u64(2), &params.f);
    params.four_m = to_mont96(u96_from_u64(4), &params.f);
    params.eight_m = to_mont96(u96_from_u64(8), &params.f);
    params.c24_m = to_mont96(u96_from_u64(24), &params.f);
    params.c32_m = to_mont96(u96_from_u64(32), &params.f);
    params.c48_m = to_mont96(u96_from_u64(48), &params.f);
    params.sqrtm1_m = params.sqrt_case == 5
        ? powmod96_mont(params.two_m, (p - 1) >> 2, &params.f)
        : u96_from_u64(0);
    params.inv2_m = to_mont96(u96_from_u128((p + 1) >> 1), &params.f);
    params.inv4_m = invert96_mont(params.four_m, &params);
    return params;
}

static int compute_k(u128 p) {
    u64 q = (u64)std::sqrt((long double)p);
    while ((u128)(q + 1) * (q + 1) <= p) q++;
    while ((u128)q * q > p) q--;
    u64 sq = (u64)std::sqrt((long double)q);
    while ((sq + 1) * (sq + 1) <= q) sq++;
    while (sq * sq > q) sq--;
    u64 bound = q + 1 + 2 * sq;
    int k = 0;
    u64 v = 1;
    while (v <= bound) {
        k++;
        v <<= 1;
    }
    return k;
}

static u64 parse_u64_arg(const char *s, u64 fallback) {
    if (!s || !*s) return fallback;
    return std::strtoull(s, nullptr, 10);
}

static int starts_with(const char *s, const char *prefix) {
    return std::strncmp(s, prefix, std::strlen(prefix)) == 0;
}

static int parse_seed_mode(const char *s, int fallback) {
    if (!s || !*s) return fallback;
    if (std::strcmp(s, "mixed") == 0) return SEED_MIXED;
    if (std::strcmp(s, "identity") == 0) return SEED_IDENTITY;
    if (std::strcmp(s, "splitmix") == 0) return SEED_SPLITMIX;
    return fallback;
}

static const char *seed_mode_name(int seed_mode) {
    if (seed_mode == SEED_IDENTITY) return "identity";
    if (seed_mode == SEED_SPLITMIX) return "splitmix";
    return "mixed";
}

static void usage(const char *argv0) {
    std::fprintf(stderr,
                 "Usage: %s <p> [seed_offset] [max_trials] "
                 "[x16halvenonsplit|x16stratumprobe|x16domainprobe|"
                 "x16d2probe|x16d3probe|x16d4probe|x16tracenormab|"
                 "x16tracenormfilter|x16uprecheckprobe|x16ecoverprobe|"
                 "x16ecoverd2probe|x16ecoverd3probe|x16ecoverd4probe] "
                 "[chunk_trials] [blocks] "
                 "[threads] [claim_batch] [auto|generic|u96] "
                 "[seed=mixed|identity|splitmix] [start_chunk=N] "
                 "[start_trial=N] [target_depth=N] [bucket_bits=N] "
                 "[focus_bucket=N]\n",
                 argv0);
}

static void add_probe_stats(ProbeStats *dst, const ProbeStats *src) {
    dst->claimed += src->claimed;
    dst->accepted_roots += src->accepted_roots;
    dst->y_draws += src->y_draws;
    dst->y_nonsplit += src->y_nonsplit;
    dst->y_with_sqrt_D += src->y_with_sqrt_D;
    dst->roots_valid += src->roots_valid;
    for (int i = 0; i <= PROBE_MAX_DEPTH; i++) {
        dst->depth_exact[i] += src->depth_exact[i];
    }
    for (int i = 0; i < PROBE_MAX_BUCKETS; i++) {
        dst->bucket_total[i] += src->bucket_total[i];
        dst->bucket_survive[i] += src->bucket_survive[i];
        dst->bucket_prefix_total[i] += src->bucket_prefix_total[i];
        dst->bucket_prefix_survive[i] += src->bucket_prefix_survive[i];
        dst->bucket_held_total[i] += src->bucket_held_total[i];
        dst->bucket_held_survive[i] += src->bucket_held_survive[i];
    }
}

static void add_trace_norm_ab_stats(TraceNormABStats *dst,
                                    const TraceNormABStats *src) {
    dst->raw_y_draws += src->raw_y_draws;
    dst->nonsplit_y += src->nonsplit_y;
    dst->f_square += src->f_square;
    dst->d_plus += src->d_plus;
    dst->d_minus += src->d_minus;
    dst->d_zero += src->d_zero;
    dst->t_line_plus += src->t_line_plus;
    dst->t_line_minus += src->t_line_minus;
    dst->t_line_inconsistent += src->t_line_inconsistent;
    dst->t_line_unusable += src->t_line_unusable;
    dst->branch_sqrt_y += src->branch_sqrt_y;
    dst->roots_valid += src->roots_valid;
    dst->ordinary_emitted_candidates += src->ordinary_emitted_candidates;
    dst->candidate_emitted_candidates += src->candidate_emitted_candidates;
    for (int i = 0; i < TRACE_AB_DEPTH_COUNT; i++) {
        dst->ordinary_survive[i] += src->ordinary_survive[i];
        dst->candidate_survive[i] += src->candidate_survive[i];
    }
}

static void add_uprecheck_stats(UPrecheckStats *dst, const UPrecheckStats *src) {
    dst->claimed += src->claimed;
    dst->accepted_roots += src->accepted_roots;
    dst->y_draws += src->y_draws;
    dst->y_nonsplit += src->y_nonsplit;
    dst->y_with_sqrt_D += src->y_with_sqrt_D;
    dst->roots_valid += src->roots_valid;
    for (int i = 0; i <= PROBE_MAX_DEPTH; i++) {
        dst->depth_exact[i] += src->depth_exact[i];
    }
    dst->counters.d_sqrt_calls += src->counters.d_sqrt_calls;
    dst->counters.d_sqrt_success += src->counters.d_sqrt_success;
    dst->counters.uplus_checks += src->counters.uplus_checks;
    dst->counters.uplus_pass += src->counters.uplus_pass;
    dst->counters.uplus_reject += src->counters.uplus_reject;
    dst->counters.w_sqrt_calls += src->counters.w_sqrt_calls;
    dst->counters.w_sqrt_success += src->counters.w_sqrt_success;
    dst->counters.precheck_short_circuit +=
        src->counters.precheck_short_circuit;
}

static u64 uprecheck_depth_survive_ge(const UPrecheckStats *stats, int depth) {
    if (depth < 0) depth = 0;
    if (depth > PROBE_MAX_DEPTH) depth = PROBE_MAX_DEPTH;
    u64 total = 0;
    for (int d = depth; d <= PROBE_MAX_DEPTH; d++) total += stats->depth_exact[d];
    return total;
}

static void print_uprecheck_summary(const UPrecheckStats *stats, u128 p,
                                    const char *backend_name,
                                    const char *gpu_name, int seed_mode,
                                    u64 seed_offset, int target_depth,
                                    double elapsed) {
    double accepted_rate = elapsed > 0.0
        ? (double)stats->accepted_roots / elapsed / 1e6
        : 0.0;
    u64 target_survive = uprecheck_depth_survive_ge(stats, target_depth);
    double target_rate = stats->accepted_roots
        ? (double)target_survive / (double)stats->accepted_roots
        : 0.0;
    const UPrecheckCounters *c = &stats->counters;

    std::printf("\nU+2 precheck probe summary:\n");
    std::printf("  backend=%s GPU=\"%s\" seed_mode=%s seed_offset=%llu\n",
                backend_name, gpu_name, seed_mode_name(seed_mode), seed_offset);
    std::printf("  accepted_roots=%llu y_draws=%llu nonsplit_y=%llu "
                "sqrtD_y=%llu roots_valid=%llu\n",
                stats->accepted_roots, stats->y_draws, stats->y_nonsplit,
                stats->y_with_sqrt_D, stats->roots_valid);
    std::printf("  target_depth=%d survivors=%llu rate=%.9f "
                "elapsed=%.6f accepted_rate_Mps=%.6f\n",
                target_depth, target_survive, target_rate, elapsed,
                accepted_rate);
    std::printf("  precheck counters: d_sqrt=%llu/%llu uplus=%llu "
                "pass=%llu reject=%llu short_circuit=%llu "
                "w_sqrt=%llu/%llu\n",
                c->d_sqrt_success, c->d_sqrt_calls, c->uplus_checks,
                c->uplus_pass, c->uplus_reject,
                c->precheck_short_circuit,
                c->w_sqrt_success, c->w_sqrt_calls);
    std::printf("  depth survival checkpoints:\n");
    for (int d = 4; d <= target_depth; d++) {
        if (d == 4 || d == target_depth || (d % 2) == 0) {
            u64 ge = uprecheck_depth_survive_ge(stats, d);
            double rate = stats->accepted_roots
                ? (double)ge / (double)stats->accepted_roots
                : 0.0;
            std::printf("    depth>=%d count=%llu rate=%.9f\n", d, ge, rate);
        }
    }
    std::printf("uprecheck_jsonl={\"mode\":\"x16uprecheckprobe\","
                "\"p\":\"%s\",\"backend\":\"%s\",\"gpu\":\"%s\","
                "\"seed_mode\":\"%s\",\"seed_offset\":%llu,"
                "\"target_depth\":%d,\"elapsed\":%.6f,"
                "\"accepted_roots\":%llu,\"y_draws\":%llu,"
                "\"target_survivors\":%llu,\"uplus_checks\":%llu,"
                "\"uplus_pass\":%llu,\"uplus_reject\":%llu,"
                "\"short_circuit\":%llu,\"w_sqrt_calls\":%llu,"
                "\"w_sqrt_success\":%llu}\n",
                sprint128(p).c_str(), backend_name, gpu_name,
                seed_mode_name(seed_mode), seed_offset, target_depth, elapsed,
                stats->accepted_roots, stats->y_draws, target_survive,
                c->uplus_checks, c->uplus_pass, c->uplus_reject,
                c->precheck_short_circuit, c->w_sqrt_calls,
                c->w_sqrt_success);
}

static void print_trace_norm_ab_summary(const TraceNormABStats *stats,
                                        const char *mode_name, u128 p,
                                        const char *backend_name,
                                        const char *gpu_name, int seed_mode,
                                        u64 seed_offset, double elapsed) {
    double raw_rate = elapsed > 0.0 ? (double)stats->raw_y_draws / elapsed : 0.0;
    double ordinary_rate = elapsed > 0.0
        ? (double)stats->ordinary_emitted_candidates / elapsed
        : 0.0;
    double candidate_rate = elapsed > 0.0
        ? (double)stats->candidate_emitted_candidates / elapsed
        : 0.0;

    std::printf("\nTrace/norm %s summary:\n",
                std::strcmp(mode_name, "x16tracenormfilter") == 0
                    ? "filter-only"
                    : "same-stream A/B");
    std::printf("  backend=%s GPU=\"%s\" seed_mode=%s seed_offset=%llu\n",
                backend_name, gpu_name, seed_mode_name(seed_mode), seed_offset);
    std::printf("  raw_y_draws=%llu elapsed=%.6f raw_y_per_sec=%.3f\n",
                stats->raw_y_draws, elapsed, raw_rate);
    std::printf("  nonsplit_y=%llu F_square=%llu branch_sqrt_y=%llu roots_valid=%llu\n",
                stats->nonsplit_y, stats->f_square, stats->branch_sqrt_y,
                stats->roots_valid);
    std::printf("  D_trace: plus=%llu minus=%llu zero_or_unusable=%llu\n",
                stats->d_plus, stats->d_minus, stats->d_zero);
    std::printf("  T_line: plus=%llu minus=%llu inconsistent=%llu unusable=%llu\n",
                stats->t_line_plus, stats->t_line_minus,
                stats->t_line_inconsistent, stats->t_line_unusable);
    std::printf("  emitted_candidates: ordinary=%llu candidate=%llu "
                "ordinary_per_sec=%.3f candidate_per_sec=%.3f\n",
                stats->ordinary_emitted_candidates,
                stats->candidate_emitted_candidates,
                ordinary_rate, candidate_rate);
    std::printf("  depth ordinary_survive ordinary_rate candidate_survive "
                "candidate_rate lift survivor_per_sec_candidate\n");
    for (int i = 0; i < TRACE_AB_DEPTH_COUNT; i++) {
        int d = trace_ab_depth_value(i);
        double ordinary_survive_rate = stats->ordinary_emitted_candidates
            ? (double)stats->ordinary_survive[i] /
              (double)stats->ordinary_emitted_candidates
            : 0.0;
        double candidate_survive_rate = stats->candidate_emitted_candidates
            ? (double)stats->candidate_survive[i] /
              (double)stats->candidate_emitted_candidates
            : 0.0;
        double lift = ordinary_survive_rate > 0.0
            ? candidate_survive_rate / ordinary_survive_rate
            : 0.0;
        double candidate_survivor_sec = elapsed > 0.0
            ? (double)stats->candidate_survive[i] / elapsed
            : 0.0;
        std::printf("    %d %llu %.9f %llu %.9f %.3f %.6f\n",
                    d, stats->ordinary_survive[i], ordinary_survive_rate,
                    stats->candidate_survive[i], candidate_survive_rate,
                    lift, candidate_survivor_sec);
    }

    std::printf("trace_norm_ab_jsonl={\"mode\":\"%s\","
                "\"p\":\"%s\",\"backend\":\"%s\",\"gpu\":\"%s\","
                "\"seed_mode\":\"%s\",\"seed_offset\":%llu,"
                "\"elapsed\":%.6f,\"raw_y_draws\":%llu,"
                "\"nonsplit_y\":%llu,\"F_square\":%llu,"
                "\"D_plus\":%llu,\"D_minus\":%llu,\"D_zero\":%llu,"
                "\"T_line_plus\":%llu,\"T_line_minus\":%llu,"
                "\"T_line_inconsistent\":%llu,\"T_line_unusable\":%llu,"
                "\"ordinary_emitted_candidates\":%llu,"
                "\"candidate_emitted_candidates\":%llu",
                mode_name, sprint128(p).c_str(), backend_name, gpu_name,
                seed_mode_name(seed_mode), seed_offset, elapsed,
                stats->raw_y_draws, stats->nonsplit_y, stats->f_square,
                stats->d_plus, stats->d_minus, stats->d_zero,
                stats->t_line_plus, stats->t_line_minus,
                stats->t_line_inconsistent, stats->t_line_unusable,
                stats->ordinary_emitted_candidates,
                stats->candidate_emitted_candidates);
    for (int i = 0; i < TRACE_AB_DEPTH_COUNT; i++) {
        std::printf(",\"ordinary_survive_%d\":%llu,\"candidate_survive_%d\":%llu",
                    trace_ab_depth_value(i), stats->ordinary_survive[i],
                    trace_ab_depth_value(i), stats->candidate_survive[i]);
    }
    std::printf("}\n");
}

static u64 depth_survive_ge(const ProbeStats *stats, int depth) {
    if (depth < 0) depth = 0;
    if (depth > PROBE_MAX_DEPTH) depth = PROBE_MAX_DEPTH;
    u64 total = 0;
    for (int d = depth; d <= PROBE_MAX_DEPTH; d++) total += stats->depth_exact[d];
    return total;
}

static void print_bucket_row(const ProbeStats *stats, int bucket_bits, int bucket,
                             double prefix_rate, double held_rate) {
    double pr = stats->bucket_prefix_total[bucket]
        ? (double)stats->bucket_prefix_survive[bucket] /
          (double)stats->bucket_prefix_total[bucket]
        : 0.0;
    double hr = stats->bucket_held_total[bucket]
        ? (double)stats->bucket_held_survive[bucket] /
          (double)stats->bucket_held_total[bucket]
        : 0.0;
    double plift = prefix_rate > 0.0 ? pr / prefix_rate : 0.0;
    double hlift = held_rate > 0.0 ? hr / held_rate : 0.0;
    const char *promotion =
        (stats->bucket_held_survive[bucket] >= 100 && hlift >= 1.25) ? "yes" : "no";
    int q_sheet = bucket >> bucket_bits;
    int key = bucket & ((1 << bucket_bits) - 1);
    std::printf("    %d %d %d %llu %llu %.3f %llu %llu %.3f %s\n",
                bucket, q_sheet, key,
                stats->bucket_prefix_total[bucket],
                stats->bucket_prefix_survive[bucket], plift,
                stats->bucket_held_total[bucket],
                stats->bucket_held_survive[bucket], hlift,
                promotion);
}

static void print_probe_summary(const ProbeStats *stats, const char *mode_name,
                                u128 p, const char *backend_name,
                                const char *gpu_name, int seed_mode,
                                u64 seed_offset, int target_depth,
                                int prefix_filter_depth, int bucket_bits,
                                int focus_bucket, double elapsed) {
    int bucket_count = 1 << (bucket_bits + 1);
    u64 target_survive = depth_survive_ge(stats, target_depth);
    double target_rate = stats->accepted_roots
        ? (double)target_survive / (double)stats->accepted_roots
        : 0.0;
    double accepted_rate = elapsed > 0.0
        ? (double)stats->accepted_roots / elapsed / 1e6
        : 0.0;
    double source_per_accepted = stats->accepted_roots
        ? (double)stats->y_draws / (double)stats->accepted_roots
        : 0.0;
    double target_per_source_draw = stats->y_draws
        ? (double)target_survive / (double)stats->y_draws
        : 0.0;
    double target_survivor_per_sec = elapsed > 0.0
        ? (double)target_survive / elapsed
        : 0.0;
    const int ecover_prefix =
        std::strcmp(mode_name, "x16ecoverprefixprobe") == 0 ||
        std::strcmp(mode_name, "x16ecoverd2probe") == 0 ||
        std::strcmp(mode_name, "x16ecoverd3probe") == 0 ||
        std::strcmp(mode_name, "x16ecoverd4probe") == 0;
    const int raw_prefix =
        std::strcmp(mode_name, "x16prefixprobe") == 0 ||
        std::strcmp(mode_name, "x16d2probe") == 0 ||
        std::strcmp(mode_name, "x16d3probe") == 0 ||
        std::strcmp(mode_name, "x16d4probe") == 0;
    const int source_sampler = std::strcmp(mode_name, "x16ecoverprobe") == 0 ||
                               ecover_prefix;
    const int scope_narrowing = source_sampler || raw_prefix ||
                                std::strcmp(mode_name, "x16domainprobe") == 0;
    const char *source_kind = source_sampler
        ? (ecover_prefix ? "ecover_random_affine_xplus1_prefix_d"
                         : "ecover_random_affine_xplus1")
        : (raw_prefix
               ? "raw_x16_domain_plus_prefix_d"
               : (std::strcmp(mode_name, "x16domainprobe") == 0
               ? "raw_x16_domain_line_plus_y"
                  : "raw_x16_nonsplit_y"));

    u64 prefix_total = 0;
    u64 prefix_survive = 0;
    u64 held_total = 0;
    u64 held_survive = 0;
    for (int b = 0; b < bucket_count; b++) {
        prefix_total += stats->bucket_prefix_total[b];
        prefix_survive += stats->bucket_prefix_survive[b];
        held_total += stats->bucket_held_total[b];
        held_survive += stats->bucket_held_survive[b];
    }
    double prefix_rate = prefix_total ? (double)prefix_survive / (double)prefix_total : 0.0;
    double held_rate = held_total ? (double)held_survive / (double)held_total : 0.0;

    std::printf("\nStratum probe summary:\n");
    std::printf("  mode=%s source_kind=%s backend=%s GPU=\"%s\" "
                "seed_mode=%s seed_offset=%llu\n",
                mode_name, source_kind, backend_name, gpu_name,
                seed_mode_name(seed_mode), seed_offset);
    std::printf("  prefix_filter_depth=%d\n", prefix_filter_depth);
    std::printf("  accepted_roots=%llu y_draws=%llu nonsplit_y=%llu sqrtD_y=%llu roots_valid=%llu\n",
                stats->accepted_roots, stats->y_draws, stats->y_nonsplit,
                stats->y_with_sqrt_D, stats->roots_valid);
    std::printf("  target_depth=%d survivors=%llu rate=%.9f "
                "elapsed=%.6f accepted_rate_Mps=%.6f "
                "source_draws_per_accepted=%.6f target_per_source_draw=%.12f "
                "target_survivor_per_sec=%.6f\n",
                target_depth, target_survive, target_rate, elapsed,
                accepted_rate, source_per_accepted, target_per_source_draw,
                target_survivor_per_sec);
    std::printf("  prefix total=%llu survivors=%llu rate=%.9f\n",
                prefix_total, prefix_survive, prefix_rate);
    std::printf("  heldout total=%llu survivors=%llu rate=%.9f\n",
                held_total, held_survive, held_rate);
    std::printf("  depth survival checkpoints:\n");
    for (int d = 4; d <= target_depth; d++) {
        if (d == 4 || d == target_depth || (d % 2) == 0) {
            u64 ge = depth_survive_ge(stats, d);
            double rate = stats->accepted_roots
                ? (double)ge / (double)stats->accepted_roots
                : 0.0;
            std::printf("    depth>=%d count=%llu rate=%.9f\n", d, ge, rate);
        }
    }

    std::vector<int> buckets;
    buckets.reserve(bucket_count);
    for (int b = 0; b < bucket_count; b++) {
        if (stats->bucket_prefix_total[b] >= 100) buckets.push_back(b);
    }
    std::sort(buckets.begin(), buckets.end(), [&](int a, int b) {
        double ar = (double)stats->bucket_prefix_survive[a] /
                    (double)stats->bucket_prefix_total[a];
        double br = (double)stats->bucket_prefix_survive[b] /
                    (double)stats->bucket_prefix_total[b];
        double al = prefix_rate > 0.0 ? ar / prefix_rate : 0.0;
        double bl = prefix_rate > 0.0 ? br / prefix_rate : 0.0;
        if (al != bl) return al > bl;
        return stats->bucket_prefix_survive[a] > stats->bucket_prefix_survive[b];
    });

    std::printf("  top buckets selected by prefix lift (min prefix total 100):\n");
    std::printf("    bucket q_sheet key prefix_total prefix_surv prefix_lift "
                "held_total held_surv held_lift promotion\n");
    int rows = 0;
    for (int b : buckets) {
        if (rows >= 12) break;
        print_bucket_row(stats, bucket_bits, b, prefix_rate, held_rate);
        rows++;
    }
    if (rows == 0) {
        std::printf("    no buckets reached the minimum prefix total\n");
    }
    if (focus_bucket >= 0 && focus_bucket < bucket_count) {
        std::printf("  focus bucket:\n");
        std::printf("    bucket q_sheet key prefix_total prefix_surv prefix_lift "
                    "held_total held_surv held_lift promotion\n");
        print_bucket_row(stats, bucket_bits, focus_bucket, prefix_rate, held_rate);
    }

    std::printf("scope_probe_jsonl={\"mode\":\"%s\","
                "\"source_kind\":\"%s\",\"narrowing_source\":%s,"
                "\"scope_narrowing\":%s,"
                "\"p\":\"%s\",\"backend\":\"%s\",\"gpu\":\"%s\","
                "\"seed_mode\":\"%s\",\"seed_offset\":%llu,"
                "\"target_depth\":%d,\"prefix_filter_depth\":%d,"
                "\"bucket_bits\":%d,"
                "\"elapsed\":%.6f,\"accepted_rate_Mps\":%.6f,"
                "\"accepted_roots\":%llu,\"source_draws\":%llu,"
                "\"nonsplit_y\":%llu,\"sqrtD_y\":%llu,"
                "\"roots_valid\":%llu,\"target_survivors\":%llu,"
                "\"target_rate\":%.12f,\"source_draws_per_accepted\":%.12f,"
                "\"target_per_source_draw\":%.12f,"
                "\"target_survivor_per_sec\":%.6f,"
                "\"prefix_total\":%llu,\"prefix_survive\":%llu,"
                "\"held_total\":%llu,\"held_survive\":%llu",
                mode_name, source_kind, source_sampler ? "true" : "false",
                scope_narrowing ? "true" : "false",
                sprint128(p).c_str(), backend_name, gpu_name,
                seed_mode_name(seed_mode), seed_offset, target_depth,
                prefix_filter_depth, bucket_bits, elapsed, accepted_rate,
                stats->accepted_roots,
                stats->y_draws, stats->y_nonsplit, stats->y_with_sqrt_D,
                stats->roots_valid, target_survive, target_rate,
                source_per_accepted, target_per_source_draw,
                target_survivor_per_sec, prefix_total, prefix_survive,
                held_total, held_survive);
    for (int d = 4; d <= target_depth; d++) {
        if (d == 4 || d == target_depth || (d % 2) == 0) {
            std::printf(",\"survive_%d\":%llu", d, depth_survive_ge(stats, d));
        }
    }
    if (focus_bucket >= 0 && focus_bucket < bucket_count) {
        std::printf(",\"focus_bucket\":%d,"
                    "\"focus_prefix_total\":%llu,"
                    "\"focus_prefix_survive\":%llu,"
                    "\"focus_held_total\":%llu,"
                    "\"focus_held_survive\":%llu",
                    focus_bucket, stats->bucket_prefix_total[focus_bucket],
                    stats->bucket_prefix_survive[focus_bucket],
                    stats->bucket_held_total[focus_bucket],
                    stats->bucket_held_survive[focus_bucket]);
    }
    std::printf("}\n");
}

int main(int argc, char **argv) {
    if (argc < 2) {
        usage(argv[0]);
        return 1;
    }

    const char *mode = argc >= 5 ? argv[4] : "x16halvenonsplit";
    bool probe_mode = std::strcmp(mode, "x16stratumprobe") == 0;
    bool domain_probe_mode = std::strcmp(mode, "x16domainprobe") == 0;
    bool prefix_probe_mode = std::strcmp(mode, "x16prefixprobe") == 0 ||
                             std::strcmp(mode, "x16d2probe") == 0 ||
                             std::strcmp(mode, "x16d3probe") == 0 ||
                             std::strcmp(mode, "x16d4probe") == 0;
    bool trace_ab_mode = std::strcmp(mode, "x16tracenormab") == 0;
    bool trace_filter_mode = std::strcmp(mode, "x16tracenormfilter") == 0;
    bool uprecheck_mode = std::strcmp(mode, "x16uprecheckprobe") == 0;
    bool ecover_probe_mode = std::strcmp(mode, "x16ecoverprobe") == 0;
    bool ecover_prefix_probe_mode =
        std::strcmp(mode, "x16ecoverprefixprobe") == 0 ||
        std::strcmp(mode, "x16ecoverd2probe") == 0 ||
        std::strcmp(mode, "x16ecoverd3probe") == 0 ||
        std::strcmp(mode, "x16ecoverd4probe") == 0;
    bool scope_probe_mode = probe_mode || domain_probe_mode || prefix_probe_mode ||
                            ecover_probe_mode || ecover_prefix_probe_mode;
    if (std::strcmp(mode, "x16halvenonsplit") != 0 && !probe_mode &&
        !domain_probe_mode && !prefix_probe_mode && !trace_ab_mode &&
        !trace_filter_mode && !uprecheck_mode && !ecover_probe_mode &&
        !ecover_prefix_probe_mode) {
        std::fprintf(stderr,
                     "Only x16halvenonsplit, x16stratumprobe/x16domainprobe, and "
                     "x16tracenormab/x16tracenormfilter/x16uprecheckprobe/"
                     "x16ecoverprobe plus d-prefix probe aliases "
                     "are implemented in this CUDA prototype.\n");
        return 1;
    }

    u128 p = parse128(argv[1]);
    u64 seed_offset = argc >= 3 ? parse_u64_arg(argv[2], 0) : 0;
    u64 max_trials = argc >= 4 ? parse_u64_arg(argv[3], 1000000ULL) : 1000000ULL;
    u64 default_chunk = max_trials < 1000000000ULL ? max_trials : 1000000000ULL;
    u64 chunk_trials = argc >= 6 ? parse_u64_arg(argv[5], default_chunk) : default_chunk;
    if (max_trials == 0) max_trials = 1000000ULL;
    if (chunk_trials == 0) chunk_trials = max_trials;

    u64 p_mod8 = (u64)(p & 7);
    if (p_mod8 != 5 && (p_mod8 & 3) != 3) {
        std::fprintf(stderr,
                     "x16halvenonsplit requires p == 5 mod 8 or p == 3 mod 4 "
                     "for fast square roots.\n");
        return 1;
    }

    int device = 0;
    die_cuda(cudaSetDevice(device), "cudaSetDevice");
    cudaDeviceProp prop{};
    die_cuda(cudaGetDeviceProperties(&prop, device), "cudaGetDeviceProperties");

    int blocks = argc >= 7 ? (int)parse_u64_arg(argv[6], 0) : 0;
    int threads = argc >= 8 ? (int)parse_u64_arg(argv[7], 0) : 128;
    if (threads <= 0) threads = 128;
    u64 claim_batch = argc >= 9 ? parse_u64_arg(argv[8], 1ULL) : 1ULL;
    if (claim_batch == 0) claim_batch = 1ULL;
    const char *backend_arg = argc >= 10 ? argv[9] : "auto";
    int seed_mode = SEED_MIXED;
    u64 start_chunk_nonce = 0;
    u64 start_trial_base = 0;
    bool start_trial_set = false;
    int probe_target_depth = 26;
    int probe_bucket_bits = 6;
    int probe_focus_bucket = -1;
    int probe_prefix_depth = 4;
    if (prefix_probe_mode || ecover_prefix_probe_mode) probe_prefix_depth = 6;
    if (std::strcmp(mode, "x16d3probe") == 0 ||
        std::strcmp(mode, "x16ecoverd3probe") == 0) {
        probe_prefix_depth = 7;
    } else if (std::strcmp(mode, "x16d4probe") == 0 ||
               std::strcmp(mode, "x16ecoverd4probe") == 0) {
        probe_prefix_depth = 8;
    }
    for (int i = 10; i < argc; i++) {
        const char *arg = argv[i];
        if (starts_with(arg, "seed=")) {
            int parsed = parse_seed_mode(arg + 5, -1);
            if (parsed < 0) {
                std::fprintf(stderr, "Unknown seed mode: %s\n", arg + 5);
                return 1;
            }
            seed_mode = parsed;
        } else if (std::strcmp(arg, "mixed") == 0 ||
                   std::strcmp(arg, "identity") == 0 ||
                   std::strcmp(arg, "splitmix") == 0) {
            seed_mode = parse_seed_mode(arg, SEED_MIXED);
        } else if (starts_with(arg, "start_chunk=")) {
            start_chunk_nonce = parse_u64_arg(arg + 12, 0);
        } else if (starts_with(arg, "start_trial=")) {
            start_trial_base = parse_u64_arg(arg + 12, 0);
            start_trial_set = true;
        } else if (starts_with(arg, "target_depth=")) {
            probe_target_depth = (int)parse_u64_arg(arg + 13, 26);
        } else if (starts_with(arg, "prefix_depth=")) {
            probe_prefix_depth = (int)parse_u64_arg(arg + 13, 4);
        } else if (starts_with(arg, "bucket_bits=")) {
            probe_bucket_bits = (int)parse_u64_arg(arg + 12, 6);
        } else if (starts_with(arg, "focus_bucket=")) {
            probe_focus_bucket = (int)parse_u64_arg(arg + 13, 0);
        } else if (starts_with(arg, "bucket=")) {
            probe_focus_bucket = (int)parse_u64_arg(arg + 7, 0);
        } else {
            std::fprintf(stderr, "Unknown option: %s\n", arg);
            usage(argv[0]);
            return 1;
        }
    }
    if (!start_trial_set) start_trial_base = start_chunk_nonce * chunk_trials;
    if (probe_target_depth < 4) probe_target_depth = 4;
    if (probe_target_depth > PROBE_MAX_DEPTH) probe_target_depth = PROBE_MAX_DEPTH;
    if (probe_prefix_depth < 4) probe_prefix_depth = 4;
    if (probe_prefix_depth > PROBE_MAX_DEPTH) probe_prefix_depth = PROBE_MAX_DEPTH;
    if (probe_prefix_depth > probe_target_depth) probe_prefix_depth = probe_target_depth;
    if (probe_bucket_bits < 0) probe_bucket_bits = 0;
    if (probe_bucket_bits > PROBE_MAX_BUCKET_BITS) {
        std::fprintf(stderr, "bucket_bits must be <= %d.\n", PROBE_MAX_BUCKET_BITS);
        return 1;
    }
    if (probe_focus_bucket >= (1 << (probe_bucket_bits + 1))) {
        std::fprintf(stderr, "focus_bucket is outside the selected bucket range.\n");
        return 1;
    }
    if (start_trial_base > max_trials) {
        std::fprintf(stderr, "start_trial must be <= max_trials.\n");
        return 1;
    }

    SearchParams params{};
    params.p = p;
    m128_init(&params.mt, p);
    int pbits = bitlen128(p);
    params.rand_mask = pbits >= 128 ? (u128)0 - 1 : (((u128)1 << pbits) - 1);
    params.sqrt_case = ((u64)(p & 3) == 3) ? 3 : 5;
    params.sqrt_exp = params.sqrt_case == 3 ? ((p + 1) >> 2) : ((p + 3) >> 3);
    params.sqrtm1 = params.sqrt_case == 5
        ? powmod128_mont(2, (p - 1) >> 2, &params.mt)
        : 0;
    params.two_m = toM128(2, &params.mt);
    params.four_m = toM128(4, &params.mt);
    params.eight_m = toM128(8, &params.mt);
    params.c24_m = toM128(24, &params.mt);
    params.c32_m = toM128(32, &params.mt);
    params.c48_m = toM128(48, &params.mt);
    params.sqrtm1_m = params.sqrt_case == 5
        ? powmod128_mont_raw(params.two_m, (p - 1) >> 2, &params.mt)
        : 0;
    params.inv2_m = toM128((p + 1) >> 1, &params.mt);
    params.inv4_m = invert128_mont_raw(params.four_m, p, &params.mt);
    params.k = compute_k(p);

    bool use_u96 = false;
    if (std::strcmp(backend_arg, "auto") == 0) {
        use_u96 = pbits <= 96;
    } else if (std::strcmp(backend_arg, "u96") == 0) {
        if (pbits > 96) {
            std::fprintf(stderr, "u96 backend requires p < 2^96.\n");
            return 1;
        }
        use_u96 = true;
    } else if (std::strcmp(backend_arg, "generic") == 0) {
        use_u96 = false;
    } else {
        std::fprintf(stderr, "Unknown backend: %s\n", backend_arg);
        return 1;
    }
    if (blocks <= 0) blocks = prop.multiProcessorCount * (use_u96 ? 8 : 4);
    SearchParams96 params96{};
    if (use_u96) params96 = search_params96_init(p, params.k, pbits);

    std::printf("Pomerance CUDA x16halvenonsplit prototype\n\n");
    std::printf("p = %s\n", sprint128(p).c_str());
    std::printf("mode = %s\n", mode);
    std::printf("seed_offset = %llu\n", seed_offset);
    std::printf("seed_mode = %s\n", seed_mode_name(seed_mode));
    std::printf("max_trials = %llu\n", max_trials);
    std::printf("chunk_trials = %llu\n", chunk_trials);
    if (start_trial_base || start_chunk_nonce) {
        std::printf("start_chunk = %llu\n", start_chunk_nonce);
        std::printf("start_trial = %llu\n", start_trial_base);
    }
    if (scope_probe_mode) {
        std::printf("probe_target_depth = %d\n", probe_target_depth);
        std::printf("probe_prefix_filter_depth = %d\n", probe_prefix_depth);
        std::printf("probe_bucket_bits = %d\n", probe_bucket_bits);
        if (probe_focus_bucket >= 0) {
            std::printf("probe_focus_bucket = %d\n", probe_focus_bucket);
        }
    }
    if (uprecheck_mode) {
        std::printf("uprecheck_target_depth = %d\n", probe_target_depth);
    }
    std::printf("k = %d\n", params.k);
    std::printf("backend = %s\n", use_u96 ? "u96" : "generic-u128");
    std::printf("GPU = %s  SMs=%d  blocks=%d  threads=%d  claim_batch=%llu\n\n",
                prop.name, prop.multiProcessorCount, blocks, threads, claim_batch);

    if (trace_ab_mode || trace_filter_mode) {
        TraceNormABStats *d_trace = nullptr;
        die_cuda(cudaMalloc(&d_trace, sizeof(TraceNormABStats)),
                 "cudaMalloc trace/norm A/B stats");

        TraceNormABStats cumulative{};
        u64 total = start_trial_base;
        u64 chunk_nonce = start_chunk_nonce;
        auto t0 = std::chrono::steady_clock::now();

        while (total < max_trials) {
            u64 remaining = max_trials - total;
            u64 this_chunk = remaining < chunk_trials ? remaining : chunk_trials;
            die_cuda(cudaMemset(d_trace, 0, sizeof(TraceNormABStats)),
                     "cudaMemset trace/norm A/B stats");

            if (use_u96) {
                x16tracenormab_kernel96<<<blocks, threads>>>(
                    params96, seed_offset, chunk_nonce, this_chunk, seed_mode,
                    trace_filter_mode ? 1 : 0, d_trace);
            } else {
                x16tracenormab_kernel<<<blocks, threads>>>(
                    params, seed_offset, chunk_nonce, this_chunk, seed_mode,
                    trace_filter_mode ? 1 : 0, d_trace);
            }
            die_cuda(cudaGetLastError(), "trace/norm A/B kernel launch");
            die_cuda(cudaDeviceSynchronize(), "trace/norm A/B kernel synchronize");

            TraceNormABStats stats{};
            die_cuda(cudaMemcpy(&stats, d_trace, sizeof(stats), cudaMemcpyDeviceToHost),
                     "copy trace/norm A/B stats");
            add_trace_norm_ab_stats(&cumulative, &stats);

            u64 done = stats.raw_y_draws;
            if (done > this_chunk) done = this_chunk;
            total += done;
            auto now = std::chrono::steady_clock::now();
            double elapsed = std::chrono::duration<double>(now - t0).count();
            double raw_rate = elapsed > 0.0
                ? (double)(total - start_trial_base) / elapsed / 1e6
                : 0.0;
            std::printf("  raw_y_draws=%llu elapsed=%.3f raw_y_Mps=%.6f "
                        "nonsplit=%llu F_square=%llu D_plus=%llu "
                        "ordinary_emit=%llu candidate_emit=%llu "
                        "candidate_survive_26=%llu\n",
                        total, elapsed, raw_rate, cumulative.nonsplit_y,
                        cumulative.f_square, cumulative.d_plus,
                        cumulative.ordinary_emitted_candidates,
                        cumulative.candidate_emitted_candidates,
                        cumulative.candidate_survive[3]);
            std::fflush(stdout);

            if (done == 0) {
                std::fprintf(stderr,
                             "Trace/norm A/B kernel made no raw-y progress; stopping.\n");
                break;
            }
            chunk_nonce++;
        }

        auto t1 = std::chrono::steady_clock::now();
        double elapsed = std::chrono::duration<double>(t1 - t0).count();
        print_trace_norm_ab_summary(&cumulative, mode, p,
                                    use_u96 ? "u96" : "generic-u128",
                                    prop.name, seed_mode, seed_offset, elapsed);
        cudaFree(d_trace);
        return 0;
    }

    if (uprecheck_mode) {
        if (!use_u96) {
            std::fprintf(stderr, "x16uprecheckprobe currently requires the u96 backend.\n");
            return 1;
        }

        UPrecheckStats *d_uprecheck = nullptr;
        die_cuda(cudaMalloc(&d_uprecheck, sizeof(UPrecheckStats)),
                 "cudaMalloc U+2 precheck stats");

        UPrecheckStats cumulative{};
        u64 total = start_trial_base;
        u64 chunk_nonce = start_chunk_nonce;
        auto t0 = std::chrono::steady_clock::now();

        while (total < max_trials) {
            u64 remaining = max_trials - total;
            u64 this_chunk = remaining < chunk_trials ? remaining : chunk_trials;
            die_cuda(cudaMemset(d_uprecheck, 0, sizeof(UPrecheckStats)),
                     "cudaMemset U+2 precheck stats");

            x16uprecheckprobe_kernel96<<<blocks, threads>>>(
                params96, seed_offset, chunk_nonce, this_chunk, claim_batch,
                seed_mode, probe_target_depth, d_uprecheck);
            die_cuda(cudaGetLastError(), "U+2 precheck kernel launch");
            die_cuda(cudaDeviceSynchronize(), "U+2 precheck kernel synchronize");

            UPrecheckStats stats{};
            die_cuda(cudaMemcpy(&stats, d_uprecheck, sizeof(stats),
                                cudaMemcpyDeviceToHost),
                     "copy U+2 precheck stats");
            add_uprecheck_stats(&cumulative, &stats);

            u64 done = stats.accepted_roots;
            if (done > this_chunk) done = this_chunk;
            total += done;
            auto now = std::chrono::steady_clock::now();
            double elapsed = std::chrono::duration<double>(now - t0).count();
            double rate = elapsed > 0.0
                ? (double)(total - start_trial_base) / elapsed / 1e6
                : 0.0;
            u64 target_survive =
                uprecheck_depth_survive_ge(&cumulative, probe_target_depth);
            std::printf("  uprecheck_trials=%llu elapsed=%.3f rate_Mps=%.6f "
                        "target_survivors=%llu uplus_reject=%llu "
                        "w_sqrt_calls=%llu\n",
                        total, elapsed, rate, target_survive,
                        cumulative.counters.uplus_reject,
                        cumulative.counters.w_sqrt_calls);
            std::fflush(stdout);

            if (done == 0) {
                std::fprintf(stderr,
                             "U+2 precheck kernel made no candidate progress; stopping.\n");
                break;
            }
            chunk_nonce++;
        }

        auto t1 = std::chrono::steady_clock::now();
        double elapsed = std::chrono::duration<double>(t1 - t0).count();
        print_uprecheck_summary(&cumulative, p, use_u96 ? "u96" : "generic-u128",
                                prop.name, seed_mode, seed_offset,
                                probe_target_depth, elapsed);
        cudaFree(d_uprecheck);
        return 0;
    }

    if (scope_probe_mode) {
        if ((ecover_probe_mode || ecover_prefix_probe_mode || prefix_probe_mode) &&
            !use_u96) {
            std::fprintf(stderr,
                         "ecover and d-prefix scope probes currently require "
                         "the u96 backend.\n");
            return 1;
        }

        ProbeStats *d_probe = nullptr;
        die_cuda(cudaMalloc(&d_probe, sizeof(ProbeStats)), "cudaMalloc probe stats");

        ProbeStats cumulative{};
        u64 total = start_trial_base;
        u64 chunk_nonce = start_chunk_nonce;
        u64 split_trial = start_trial_base + (max_trials - start_trial_base) / 2;
        auto t0 = std::chrono::steady_clock::now();

        while (total < max_trials) {
            u64 remaining = max_trials - total;
            u64 this_chunk = remaining < chunk_trials ? remaining : chunk_trials;
            die_cuda(cudaMemset(d_probe, 0, sizeof(ProbeStats)),
                     "cudaMemset probe stats");

            if (use_u96) {
                if (ecover_probe_mode || ecover_prefix_probe_mode) {
                    x16ecoverprobe_kernel96<<<blocks, threads>>>(
                        params96, seed_offset, chunk_nonce, this_chunk, total,
                        split_trial, claim_batch, seed_mode,
                        ecover_prefix_probe_mode ? probe_prefix_depth : 4,
                        probe_target_depth, probe_bucket_bits, d_probe);
                } else {
                    x16stratumprobe_kernel96<<<blocks, threads>>>(
                        params96, seed_offset, chunk_nonce, this_chunk, total,
                        split_trial, claim_batch, seed_mode,
                        (domain_probe_mode || prefix_probe_mode) ? 1 : 0,
                        prefix_probe_mode ? probe_prefix_depth : 4,
                        probe_target_depth, probe_bucket_bits, d_probe);
                }
            } else {
                x16stratumprobe_kernel<<<blocks, threads>>>(
                    params, seed_offset, chunk_nonce, this_chunk, total,
                    split_trial, claim_batch, seed_mode,
                    domain_probe_mode ? 1 : 0, probe_target_depth,
                    probe_bucket_bits, d_probe);
            }
            die_cuda(cudaGetLastError(), "probe kernel launch");
            die_cuda(cudaDeviceSynchronize(), "probe kernel synchronize");

            ProbeStats stats{};
            die_cuda(cudaMemcpy(&stats, d_probe, sizeof(stats), cudaMemcpyDeviceToHost),
                     "copy probe stats");
            add_probe_stats(&cumulative, &stats);

            u64 done = stats.accepted_roots;
            if (done > this_chunk) done = this_chunk;
            total += done;
            auto now = std::chrono::steady_clock::now();
            double elapsed = std::chrono::duration<double>(now - t0).count();
            u64 interval_done = total - start_trial_base;
            double rate = elapsed > 0.0 ? (double)interval_done / elapsed / 1e6 : 0.0;
            u64 target_survive = depth_survive_ge(&cumulative, probe_target_depth);
            std::printf("  probe_trials=%llu elapsed=%.3f rate_Mps=%.6f "
                        "target_survivors=%llu y_draws=%llu\n",
                        total, elapsed, rate, target_survive, cumulative.y_draws);
            std::fflush(stdout);

            if (done == 0) {
                std::fprintf(stderr,
                             "Scope probe kernel made no candidate progress; stopping.\n");
                break;
            }
            chunk_nonce++;
        }

        auto t1 = std::chrono::steady_clock::now();
        double elapsed = std::chrono::duration<double>(t1 - t0).count();
        u64 interval_done = total - start_trial_base;
        double rate = elapsed > 0.0 ? (double)interval_done / elapsed / 1e6 : 0.0;
        print_probe_summary(&cumulative, mode, p, use_u96 ? "u96" : "generic-u128",
                            prop.name, seed_mode, seed_offset, probe_target_depth,
                            (prefix_probe_mode || ecover_prefix_probe_mode)
                                ? probe_prefix_depth : 4,
                            probe_bucket_bits, probe_focus_bucket, elapsed);
        std::printf("\nProbe completed in %.2fs. trials=%llu interval_trials=%llu "
                    "rate_Mps=%.6f\n",
                    elapsed, total, interval_done, rate);
        cudaFree(d_probe);
        return 0;
    }

    GpuStats *d_stats = nullptr;
    GpuResult *d_result = nullptr;
    die_cuda(cudaMalloc(&d_stats, sizeof(GpuStats)), "cudaMalloc stats");
    die_cuda(cudaMalloc(&d_result, sizeof(GpuResult)), "cudaMalloc result");

    u64 total = start_trial_base;
    u64 chunk_nonce = start_chunk_nonce;
    GpuResult final_result{};
    auto t0 = std::chrono::steady_clock::now();

    while (total < max_trials && !final_result.found) {
        u64 remaining = max_trials - total;
        u64 this_chunk = remaining < chunk_trials ? remaining : chunk_trials;
        die_cuda(cudaMemset(d_stats, 0, sizeof(GpuStats)), "cudaMemset stats");
        die_cuda(cudaMemset(d_result, 0, sizeof(GpuResult)), "cudaMemset result");

        if (use_u96) {
            x16halvenonsplit_kernel96<<<blocks, threads>>>(params96, seed_offset, chunk_nonce,
                                                           this_chunk, total, claim_batch,
                                                           seed_mode,
                                                           d_stats, d_result);
        } else {
            x16halvenonsplit_kernel<<<blocks, threads>>>(params, seed_offset, chunk_nonce,
                                                         this_chunk, total, claim_batch,
                                                         seed_mode,
                                                         d_stats, d_result);
        }
        die_cuda(cudaGetLastError(), "kernel launch");
        die_cuda(cudaDeviceSynchronize(), "kernel synchronize");

        GpuStats stats{};
        GpuResult result{};
        die_cuda(cudaMemcpy(&stats, d_stats, sizeof(stats), cudaMemcpyDeviceToHost),
                 "copy stats");
        die_cuda(cudaMemcpy(&result, d_result, sizeof(result), cudaMemcpyDeviceToHost),
                 "copy result");

        u64 done = stats.processed;
        if (done > this_chunk) done = this_chunk;
        total += done;
        auto now = std::chrono::steady_clock::now();
        double elapsed = std::chrono::duration<double>(now - t0).count();
        u64 interval_done = total - start_trial_base;
        double rate = elapsed > 0.0 ? (double)interval_done / elapsed / 1e6 : 0.0;
#if POM_CUDA_DETAILED_STATS
        std::printf("  trials=%llu elapsed=%.3f rate_Mps=%.6f y_draws=%llu "
                    "nonsplit_y=%llu sqrtD_y=%llu roots=%llu\n",
                    total, elapsed, rate,
                    stats.y_draws, stats.y_nonsplit, stats.y_with_sqrt_D,
                    stats.roots_valid);
#else
        std::printf("  trials=%llu elapsed=%.3f rate_Mps=%.6f claimed=%llu\n",
                    total, elapsed, rate, stats.claimed);
#endif
        std::fflush(stdout);

        if (result.found) {
            final_result = result;
            total = result.trial_index + 1;
            break;
        }
        if (done == 0) {
            std::fprintf(stderr, "Kernel made no candidate progress; stopping.\n");
            break;
        }
        chunk_nonce++;
    }

    auto t1 = std::chrono::steady_clock::now();
    double elapsed = std::chrono::duration<double>(t1 - t0).count();
    std::printf("\n");
    if (final_result.found) {
        u128 A = unpack128(final_result.A);
        u128 x0 = unpack128(final_result.x0);
        std::printf("Found after %.2fs (~%llu X1(16) curves)\n\n",
                    elapsed, final_result.trial_index + 1);
        std::printf("%s %s %s\n\n",
                    sprint128(p).c_str(), sprint128(A).c_str(), sprint128(x0).c_str());
#if POM_CUDA_HIT_TELEMETRY
        std::printf("Hit telemetry:\n");
        std::printf("  seed_offset=%llu chunk_nonce=%llu tid=%llu "
                    "raw_draw_count=%llu local_draw_count=%llu\n",
                    seed_offset, final_result.chunk_nonce, final_result.tid,
                    final_result.raw_draw_count, final_result.local_draw_count);
        std::printf("  root_index=%d q_sheet=%d compactD=%016llx\n",
                    final_result.root_index, final_result.q_sheet,
                    final_result.compactD);
        std::printf("  y=%s\n", sprint128(unpack128(final_result.y)).c_str());
        std::printf("  root_x=%s\n", sprint128(unpack128(final_result.root_x)).c_str());
        std::printf("  xP16=%s\n", sprint128(unpack128(final_result.xP16)).c_str());
        std::printf("  first_w=%s\n", sprint128(unpack128(final_result.first_w)).c_str());
        std::printf("  V=%s\n", sprint128(unpack128(final_result.V)).c_str());
        std::printf("  D=%s\n\n", sprint128(unpack128(final_result.D)).c_str());
#else
        std::printf("Hit telemetry: disabled in this build "
                    "(-DPOM_CUDA_HIT_TELEMETRY=1 enables it)\n\n");
#endif
        std::printf("Verified: %s  (%.2fs)\n",
                    verify128_mont(p, A, x0, params.k, &params.mt) ? "PASS" : "FAIL",
                    elapsed);
    } else {
        u64 interval_done = total - start_trial_base;
        double rate = elapsed > 0.0 ? (double)interval_done / elapsed / 1e6 : 0.0;
        std::printf("Not found in %.2fs. trials=%llu interval_trials=%llu rate_Mps=%.6f\n",
                    elapsed, total, interval_done, rate);
    }

    cudaFree(d_stats);
    cudaFree(d_result);
    return final_result.found ? 0 : 1;
}
