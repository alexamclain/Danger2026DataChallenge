// Fast chunk oracle for p27 line-coordinate monic cubic exact-support screens.
//
// Input row file format:
//   # comments allowed
//   q n
//   X_0 sign_0
//   ...
//
// Scan family:
//   chi(X^3 + aX^2 + bX + c) = polarity * sign_i
// with both global polarities and zero values rejected.

#include <errno.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_Q 4096
#define MAX_ROWS 512
#define MAX_WORDS ((MAX_Q + 63) / 64)

typedef struct {
    int x;
    int sign;
    int x2;
    int x3;
} Row;

static int q_value = 0;
static int row_count = 0;
static Row rows[MAX_ROWS];
static int8_t chi_table[MAX_Q];
static uint64_t masks[2][MAX_Q][MAX_WORDS];
static uint64_t full_mask[MAX_WORDS];
static int word_count = 0;

static void die(const char *msg) {
    fprintf(stderr, "error: %s\n", msg);
    exit(2);
}

static uint64_t parse_u64(const char *raw, const char *name) {
    errno = 0;
    char *end = NULL;
    uint64_t value = strtoull(raw, &end, 10);
    if (errno != 0 || end == raw || *end != '\0') {
        fprintf(stderr, "bad %s: %s\n", name, raw);
        exit(2);
    }
    return value;
}

static int mod_q(int64_t value) {
    int out = (int)(value % q_value);
    return out < 0 ? out + q_value : out;
}

static bool next_data_line(FILE *fp, char *buf, size_t size) {
    while (fgets(buf, (int)size, fp)) {
        char *p = buf;
        while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') {
            p++;
        }
        if (*p == '\0' || *p == '#') {
            continue;
        }
        if (p != buf) {
            memmove(buf, p, strlen(p) + 1);
        }
        return true;
    }
    return false;
}

static void load_rows(const char *path) {
    FILE *fp = fopen(path, "r");
    if (!fp) {
        perror(path);
        exit(2);
    }
    char line[1024];
    if (!next_data_line(fp, line, sizeof(line))) {
        die("empty row file");
    }
    if (sscanf(line, "%d %d", &q_value, &row_count) != 2) {
        die("first data line must be: q n");
    }
    if (q_value <= 2 || q_value > MAX_Q) {
        die("q out of supported range");
    }
    if (row_count <= 0 || row_count > MAX_ROWS) {
        die("row count out of supported range");
    }
    for (int i = 0; i < row_count; i++) {
        if (!next_data_line(fp, line, sizeof(line))) {
            die("row file ended early");
        }
        int x = 0;
        int sign = 0;
        if (sscanf(line, "%d %d", &x, &sign) != 2) {
            die("row line must be: X sign");
        }
        if (sign != 1 && sign != -1) {
            die("row sign must be +1 or -1");
        }
        x = mod_q(x);
        int x2 = (int)((int64_t)x * x % q_value);
        int x3 = (int)((int64_t)x2 * x % q_value);
        rows[i] = (Row){.x = x, .sign = sign, .x2 = x2, .x3 = x3};
    }
    fclose(fp);
}

static void build_legendre(void) {
    for (int i = 0; i < q_value; i++) {
        chi_table[i] = -1;
    }
    chi_table[0] = 0;
    for (int x = 1; x < q_value; x++) {
        int square = (int)((int64_t)x * x % q_value);
        chi_table[square] = 1;
    }
}

static void build_masks(void) {
    word_count = (q_value + 63) / 64;
    memset(masks, 0, sizeof(masks));
    memset(full_mask, 0, sizeof(full_mask));
    for (int c = 0; c < q_value; c++) {
        full_mask[c >> 6] |= UINT64_C(1) << (c & 63);
    }
    for (int offset = 0; offset < q_value; offset++) {
        for (int c = 0; c < q_value; c++) {
            int sign = chi_table[(c + offset) % q_value];
            if (sign == 0) {
                continue;
            }
            int idx = sign == 1 ? 1 : 0;
            masks[idx][offset][c >> 6] |= UINT64_C(1) << (c & 63);
        }
    }
}

static void decode_index(uint64_t index, int *a, int *b) {
    uint64_t q = (uint64_t)q_value;
    *a = (int)(index / q);
    *b = (int)(index - (uint64_t)(*a) * q);
}

static bool is_zero_words(const uint64_t *words) {
    for (int w = 0; w < word_count; w++) {
        if (words[w]) {
            return false;
        }
    }
    return true;
}

static uint64_t popcount_words(const uint64_t *words) {
    uint64_t out = 0;
    for (int w = 0; w < word_count; w++) {
        out += (uint64_t)__builtin_popcountll(words[w]);
    }
    return out;
}

static int first_bit_words(const uint64_t *words) {
    for (int w = 0; w < word_count; w++) {
        if (words[w]) {
            return w * 64 + __builtin_ctzll(words[w]);
        }
    }
    return -1;
}

static double elapsed_seconds(struct timespec start, struct timespec end) {
    return (double)(end.tv_sec - start.tv_sec) + (double)(end.tv_nsec - start.tv_nsec) / 1.0e9;
}

int main(int argc, char **argv) {
    if (argc < 4 || argc > 5) {
        fprintf(stderr, "usage: %s rows.txt start count [sample_limit]\n", argv[0]);
        return 2;
    }
    const char *row_path = argv[1];
    uint64_t start = parse_u64(argv[2], "start");
    uint64_t count = parse_u64(argv[3], "count");
    uint64_t sample_limit = argc >= 5 ? parse_u64(argv[4], "sample_limit") : 8;

    load_rows(row_path);
    build_legendre();
    build_masks();

    uint64_t q = (uint64_t)q_value;
    uint64_t total = q * q;
    uint64_t end = start + count;
    if (end < start || end > total) {
        end = total;
    }

    uint64_t pairs_scanned = 0;
    uint64_t exact_cubics = 0;
    uint64_t polarity_hits[2] = {0, 0};
    uint64_t sample_count = 0;

    struct timespec t0;
    struct timespec t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    for (uint64_t index = start; index < end; index++) {
        int a = 0;
        int b = 0;
        decode_index(index, &a, &b);
        pairs_scanned++;
        for (int polarity_i = 0; polarity_i < 2; polarity_i++) {
            int polarity = polarity_i == 1 ? 1 : -1;
            uint64_t intersection[MAX_WORDS];
            for (int w = 0; w < word_count; w++) {
                intersection[w] = full_mask[w];
            }
            bool alive = true;
            for (int r = 0; r < row_count; r++) {
                Row row = rows[r];
                int desired = polarity * row.sign;
                int desired_i = desired == 1 ? 1 : 0;
                int offset = (int)(((int64_t)row.x3
                    + (int64_t)a * row.x2
                    + (int64_t)b * row.x) % q_value);
                bool any = false;
                for (int w = 0; w < word_count; w++) {
                    intersection[w] &= masks[desired_i][offset][w];
                    any = any || intersection[w] != 0;
                }
                if (!any) {
                    alive = false;
                    break;
                }
            }
            if (!alive || is_zero_words(intersection)) {
                continue;
            }
            uint64_t hit_count = popcount_words(intersection);
            exact_cubics += hit_count;
            polarity_hits[polarity_i] += hit_count;
            while (sample_count < sample_limit) {
                int c = first_bit_words(intersection);
                if (c < 0) {
                    break;
                }
                printf("hit_sample polarity=%d coeffs=%d,%d,%d\n", polarity, a, b, c);
                intersection[c >> 6] &= ~(UINT64_C(1) << (c & 63));
                sample_count++;
            }
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double seconds = elapsed_seconds(t0, t1);
    double throughput = seconds > 0.0 ? (double)pairs_scanned / seconds : 0.0;

    printf("p27 cubic fast chunk probe\n");
    printf("rows_file = %s\n", row_path);
    printf("field = %d\n", q_value);
    printf("rows = %d\n", row_count);
    printf("start = %" PRIu64 "\n", start);
    printf("end = %" PRIu64 "\n", end);
    printf("pairs_scanned = %" PRIu64 "\n", pairs_scanned);
    printf("polarity_-1_hits = %" PRIu64 "\n", polarity_hits[0]);
    printf("polarity_1_hits = %" PRIu64 "\n", polarity_hits[1]);
    printf("exact_cubics = %" PRIu64 "\n", exact_cubics);
    printf("elapsed_seconds = %.6f\n", seconds);
    printf("throughput_pairs_per_second = %.3f\n", throughput);
    printf("p27_cubic_chunk_fast_rows=1/1\n");
    return 0;
}
