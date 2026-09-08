import os
import sys
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from frequencies import MONOGRAM, MONOGRAM_ORDER

class Solver:
    def count(self, string: str) -> Dict:
        data = {}
        for c in string:
            data[c] = data.get(c, 0) + 1
        return dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    def sort(self, string: str) -> List:
        return list(self.count(string).keys())

    def freq_ngram(self, string: str, n: int) -> Dict:
        freq_data = {}
        total_ngrams = len(string) - n + 1
        for i in range(total_ngrams):
            ngram = string[i:i+n]
            freq_data[ngram] = (freq_data.get(ngram, 0) + 1)
        for ngram in freq_data:
            freq_data[ngram] = (freq_data[ngram] / total_ngrams * 100)
        return dict(sorted(freq_data.items(), key=lambda item: item[1], reverse=True))

    def solve(self, string: str) -> Dict:
        cipher_order = [c for c in self.sort(string) if c.isalpha()]
        mapping = {}
        for cipher_letter, plain_letter in zip(cipher_order, MONOGRAM_ORDER):
            mapping[cipher_letter] = plain_letter
        return mapping

    def decrypt(self, string: str, mapping: Dict) -> str:
        return "".join(mapping.get(c, c.lower()) for c in string)

    def table(self, string: str) -> str:
        cipher_freq = self.freq_ngram(string, 1)
        rows = ["rank  cipher  cipher%   ->  plain  plain%"]
        for i, cipher_letter in enumerate(cipher_freq):
            if not cipher_letter.isalpha():
                continue
            plain_letter = MONOGRAM_ORDER[i] if i < len(MONOGRAM_ORDER) else "-"
            plain_pct = MONOGRAM.get(plain_letter, 0.0)
            rows.append(
                f"{i+1:>4}  {cipher_letter:^6}  {cipher_freq[cipher_letter]:>6.2f}   ->  "
                f"{plain_letter:^5}  {plain_pct:>5.2f}"
            )
        return "\n".join(rows)


if __name__ == "__main__":
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "s.txt")
    with open(path, "r") as f:
        content = f.read().strip()

    solver = Solver()
    mapping = solver.solve(content)

    print(solver.table(content))
    print()
    print("mapping (cipher -> plain):")
    print("".join(sorted(mapping)))
    print("".join(mapping[c] for c in sorted(mapping)))
    print()
    print("hasil dekripsi (tebakan frekuensi monogram):")
    print(solver.decrypt(content, mapping))
