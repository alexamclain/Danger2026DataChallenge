// Exhaustive q=607 cubic K-line screen for p27 d3.
//
// The main q=1471/1607/1847 K-line screens kill degree <=2 and split
// degree <=4 branch divisors.  This small guard-field probe asks one narrower
// question exactly: on the balanced q=607 d3 K rows, is d3 the quadratic
// character of any monic cubic in K?
//
// This is not a proof over p27 and q=607 is not a promotion field.  It is a
// fast falsifier for the nearest elliptic-source subcase z^2=cubic(K).

#include <stdint.h>
#include <stdio.h>

#define Q 607
#define NROWS 32

static const int KROWS[NROWS] = {
    36, 38, 64, 91, 94, 107, 112, 135,
    144, 145, 208, 214, 247, 290, 309, 310,
    361, 386, 387, 390, 427, 454, 471, 482,
    489, 494, 527, 542, 572, 573, 580, 590,
};

static const int TARGETS[NROWS] = {
    -1, -1, 1, 1, -1, -1, 1, 1,
    1, 1, -1, 1, -1, 1, 1, 1,
    1, -1, -1, 1, -1, -1, -1, 1,
    -1, -1, -1, -1, 1, 1, 1, -1,
};

static int legendre[Q];

static int mod_pow(int a, int e) {
    int64_t out = 1;
    int64_t base = a % Q;
    while (e) {
        if (e & 1) out = (out * base) % Q;
        base = (base * base) % Q;
        e >>= 1;
    }
    return (int)out;
}

static int has_root_cubic(int a, int b, int c) {
    for (int x = 0; x < Q; ++x) {
        int v = (((x + a) * x + b) * x + c) % Q;
        if (v == 0) return 1;
    }
    return 0;
}

int main(void) {
    legendre[0] = 0;
    for (int a = 1; a < Q; ++a) {
        int r = mod_pow(a, (Q - 1) / 2);
        legendre[a] = (r == 1) ? 1 : -1;
    }

    int exact = 0;
    int exact_irreducible = 0;
    int best_good = -1;
    int best_zero = 0;
    int best_a = 0, best_b = 0, best_c = 0, best_polarity = 0;
    int64_t tested = 0;

    for (int a = 0; a < Q; ++a) {
        for (int b = 0; b < Q; ++b) {
            for (int c = 0; c < Q; ++c) {
                ++tested;
                int good_plus = 0;
                int good_minus = 0;
                int zeros = 0;
                for (int i = 0; i < NROWS; ++i) {
                    int k = KROWS[i];
                    int v = (((k + a) * k + b) * k + c) % Q;
                    int chi = legendre[v];
                    if (chi == 0) {
                        ++zeros;
                        continue;
                    }
                    if (chi == TARGETS[i]) ++good_plus;
                    if (chi == -TARGETS[i]) ++good_minus;
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
                if (zeros == 0 && good == NROWS) {
                    ++exact;
                    if (!has_root_cubic(a, b, c)) ++exact_irreducible;
                    printf(
                        "exact_cubic polarity=%d coeffs=K^3+%d*K^2+%d*K+%d irreducible=%d\n",
                        polarity, a, b, c, !has_root_cubic(a, b, c)
                    );
                }
            }
        }
    }

    printf("p27 K-line q607 monic cubic exhaustive probe\n");
    printf("q = %d\n", Q);
    printf("rows = %d\n", NROWS);
    printf("plus = 16\n");
    printf("minus = 16\n");
    printf("tested_monic_cubics = %lld\n", (long long)tested);
    printf("exact_cubics = %d\n", exact);
    printf("exact_irreducible_cubics = %d\n", exact_irreducible);
    printf(
        "best good=%d/%d zeros=%d polarity=%d coeffs=K^3+%d*K^2+%d*K+%d\n",
        best_good, NROWS, best_zero, best_polarity, best_a, best_b, best_c
    );
    printf("p27_kline_cubic_exhaustive_probe_rows=1/1\n");
    return 0;
}
