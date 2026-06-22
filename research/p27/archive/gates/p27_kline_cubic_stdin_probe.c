// Generic monic-cubic K-line character screen for p27 finite-field rows.
//
// Input format on stdin:
//   q nrows
//   K_0 target_0
//   ...
//   K_{n-1} target_{n-1}
//
// It exhausts monic cubics K^3 + a*K^2 + b*K + c over F_q and asks whether
// chi(f(K_i)) matches the target signs up to global polarity.  This is the
// exact local genus-1 subcase z^2=cubic(K), not a production search.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX_ROWS 512

static int q;
static int nrows;
static int krows[MAX_ROWS];
static int targets[MAX_ROWS];
static int *legendre_table;

static int mod_pow(int a, int e) {
    int64_t out = 1;
    int64_t base = a % q;
    while (e) {
        if (e & 1) out = (out * base) % q;
        base = (base * base) % q;
        e >>= 1;
    }
    return (int)out;
}

static int has_root_cubic(int a, int b, int c) {
    for (int x = 0; x < q; ++x) {
        int64_t v = x;
        v = (v + a) % q;
        v = (v * x + b) % q;
        v = (v * x + c) % q;
        if (v == 0) return 1;
    }
    return 0;
}

int main(void) {
    if (scanf("%d %d", &q, &nrows) != 2) {
        fprintf(stderr, "expected q nrows\n");
        return 2;
    }
    if (q <= 2 || nrows <= 0 || nrows > MAX_ROWS) {
        fprintf(stderr, "invalid q/nrows\n");
        return 2;
    }
    for (int i = 0; i < nrows; ++i) {
        if (scanf("%d %d", &krows[i], &targets[i]) != 2) {
            fprintf(stderr, "expected row %d\n", i);
            return 2;
        }
        krows[i] %= q;
        if (targets[i] != 1 && targets[i] != -1) {
            fprintf(stderr, "invalid target at row %d\n", i);
            return 2;
        }
    }

    legendre_table = calloc((size_t)q, sizeof(int));
    if (!legendre_table) {
        fprintf(stderr, "calloc failed\n");
        return 2;
    }
    legendre_table[0] = 0;
    for (int a = 1; a < q; ++a) {
        int r = mod_pow(a, (q - 1) / 2);
        legendre_table[a] = (r == 1) ? 1 : -1;
    }

    int exact = 0;
    int exact_irreducible = 0;
    int best_good = -1;
    int best_zero = 0;
    int best_a = 0, best_b = 0, best_c = 0, best_polarity = 0;
    int64_t tested = 0;

    for (int a = 0; a < q; ++a) {
        for (int b = 0; b < q; ++b) {
            for (int c = 0; c < q; ++c) {
                ++tested;
                int good_plus = 0;
                int good_minus = 0;
                int zeros = 0;
                for (int i = 0; i < nrows; ++i) {
                    int k = krows[i];
                    int64_t v = k;
                    v = (v + a) % q;
                    v = (v * k + b) % q;
                    v = (v * k + c) % q;
                    int chi = legendre_table[v];
                    if (chi == 0) {
                        ++zeros;
                        continue;
                    }
                    if (chi == targets[i]) ++good_plus;
                    if (chi == -targets[i]) ++good_minus;
                }
                int polarity = (good_plus >= good_minus) ? 1 : -1;
                int good = (good_plus >= good_minus) ? good_plus : good_minus;
                if (good > best_good || (good == best_good && zeros < best_zero)) {
                    best_good = good;
                    best_zero = zeros;
                    best_a = a;
                    best_b = b;
                    best_c = c;
                    best_polarity = polarity;
                }
                if (zeros == 0 && good == nrows) {
                    ++exact;
                    int irreducible = !has_root_cubic(a, b, c);
                    if (irreducible) ++exact_irreducible;
                    printf(
                        "exact_cubic q=%d polarity=%d coeffs=K^3+%d*K^2+%d*K+%d irreducible=%d\n",
                        q, polarity, a, b, c, irreducible
                    );
                }
            }
        }
    }

    int plus = 0;
    int minus = 0;
    for (int i = 0; i < nrows; ++i) {
        if (targets[i] == 1) ++plus;
        if (targets[i] == -1) ++minus;
    }

    printf("p27 K-line monic cubic stdin probe\n");
    printf("q = %d\n", q);
    printf("rows = %d\n", nrows);
    printf("plus = %d\n", plus);
    printf("minus = %d\n", minus);
    printf("tested_monic_cubics = %lld\n", (long long)tested);
    printf("exact_cubics = %d\n", exact);
    printf("exact_irreducible_cubics = %d\n", exact_irreducible);
    printf(
        "best good=%d/%d zeros=%d polarity=%d coeffs=K^3+%d*K^2+%d*K+%d\n",
        best_good, nrows, best_zero, best_polarity, best_a, best_b, best_c
    );
    printf("p27_kline_cubic_stdin_probe_rows=1/1\n");

    free(legendre_table);
    return 0;
}
