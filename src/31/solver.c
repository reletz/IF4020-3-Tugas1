#include "enigma.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 16384
#define TOP 10

static const char *NAMES[] = {"I", "II", "III", "IV", "V", "VI", "VII", "VIII"};

typedef struct { double ci; int l, c, r; char pos[4]; } Result;

static double ci(const int *text, int n) {
  long freq[26] = {0};
  for (int i = 0; i < n; ++i) ++freq[text[i]];
  long sum = 0;
  for (int i = 0; i < 26; ++i) sum += freq[i] * (freq[i] - 1);
  return (double) sum / ((double) n * (n - 1));
}

/* Dekripsi dengan ring AAA tanpa plugboard, lalu hitung CI hasilnya. */
static double score(int l, int c, int r, const char *pos, const int *cipher, int n, int *buf) {
  Enigma m = plain(NAMES[l], NAMES[c], NAMES[r], "AAA", pos);
  for (int i = 0; i < n; ++i) buf[i] = run(&m, cipher[i]);
  return ci(buf, n);
}

static void insert(Result *top, Result r) {
  for (int i = 0; i < TOP; ++i) {
    if (r.ci > top[i].ci) {
      memmove(&top[i + 1], &top[i], (TOP - i - 1) * sizeof(Result));
      top[i] = r;
      return;
    }
  }
}

int main(int argc, char **argv) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <ciphertext>\n", argv[0]);
    return 1;
  }
  FILE *f = fopen(argv[1], "r");
  if (!f) { perror(argv[1]); return 1; }
  static int cipher[MAX_LEN];
  int n = 0, ch;
  while ((ch = fgetc(f)) != EOF && n < MAX_LEN)
    if (ch >= 'A' && ch <= 'Z') cipher[n++] = ch - 'A';
  fclose(f);
  printf("Panjang ciphertext: %d huruf, CI ciphertext: %.5f\n\n", n, ci(cipher, n));

  /*
   * Buat daftar semua cara memasang 3 dari 8 rotor ke slot kiri, tengah, dan kanan.
   * Indeks 0..7 mewakili rotor I..VIII (lihat NAMES). Urutan diperhatikan karena
   * (VI, II, IV) dan (IV, II, VI) menghasilkan enkripsi yang berbeda, sedangkan satu
   * rotor tidak boleh dipakai dua kali (sama seperti validasi di cli()).
   * Jumlahnya 8 x 7 x 6 = 336 urutan, misalnya orders[0] = {0, 1, 2} = I II III.
   */
  int orders[336][3], count = 0;
  for (int l = 0; l < 8; ++l)
    for (int c = 0; c < 8; ++c)
      for (int r = 0; r < 8; ++r)
        if (l != c && c != r && l != r) {
          orders[count][0] = l; orders[count][1] = c; orders[count][2] = r;
          ++count;
        }

  Result best_per_order[336];
  #pragma omp parallel for schedule(dynamic)
  for (int o = 0; o < count; ++o) {
    int *buf = malloc(n * sizeof(int));
    Result best = {0};
    char pos[4] = {0};
    for (int p = 0; p < 26 * 26 * 26; ++p) {
      pos[0] = 'A' + p / 676; pos[1] = 'A' + p / 26 % 26; pos[2] = 'A' + p % 26;
      double s = score(orders[o][0], orders[o][1], orders[o][2], pos, cipher, n, buf);
      if (s > best.ci) {
        best = (Result) {s, orders[o][0], orders[o][1], orders[o][2], {0}};
        memcpy(best.pos, pos, 4);
      }
    }
    best_per_order[o] = best;
    free(buf);
  }

  /* print "best so far" sesuai urutan rotor yang dicoba */
  Result top[TOP] = {0}, so_far = {0};
  for (int o = 0; o < count; ++o) {
    Result r = best_per_order[o];
    insert(top, r);
    if (r.ci > so_far.ci) {
      so_far = r;
      printf("Terbaik sejauh ini: rotor %s %s %s posisi %s CI %.5f\n",
             NAMES[r.l], NAMES[r.c], NAMES[r.r], r.pos, r.ci);
    }
  }

  printf("\n%d kandidat terbaik:\n", TOP);
  for (int i = 0; i < TOP; ++i)
    printf("%2d. rotor %-4s %-4s %-4s posisi %s CI %.5f\n", i + 1,
           NAMES[top[i].l], NAMES[top[i].c], NAMES[top[i].r], top[i].pos, top[i].ci);

  printf("\nKonfigurasi terbaik: rotor %s %s %s, ring AAA, posisi %s, tanpa plugboard (CI %.5f)\n",
         NAMES[top[0].l], NAMES[top[0].c], NAMES[top[0].r], top[0].pos, top[0].ci);
  return 0;
}
