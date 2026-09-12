import json
import os
import sys
from datetime import datetime
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from frequencies import MONOGRAM, MONOGRAM_ORDER

CORRECTIONS = [
    ("R", "T"), ("P", "H"), ("Q", "E"), ("I", "N"), ("C", "I"),
    ("U", "A"), ("Z", "U"), ("A", "R"), ("B", "Y"), ("M", "F"),
    ("O", "P"), ("W", "W"), ("N", "M"), ("D", "O"), ("T", "S"),
    ("X", "L"), ("G", "J"), ("F", "K"), ("S", "G"), ("J", "X"),
    ("Y", "Z"), ("E", "V"), ("L", "Q"),
]

class Solver:
    def count(self, string: str) -> Dict:
        data = {}
        for c in string:
            data[c] = data.get(c, 0) + 1
        return dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    def sort(self, string: str) -> List:
        return list(self.count(string).keys())

    def freq_ngram(self, string: str, n: int = 1) -> Dict:
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

    def replace_char(self, mapping: Dict, char0: str, char1: str) -> Dict:
        mapping[char0] = char1
        return mapping

    def decrypt(self, string: str, mapping: Dict) -> str:
        return "".join(mapping.get(c, c.lower()) for c in string)

    def table(self, string: str) -> str:
        cipher_freq = self.freq_ngram(string)
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

def load_ciphertext(base_dir: str) -> str:
    with open(os.path.join(base_dir, "s.txt")) as f:
        return f.read().strip()

def write_plain(base_dir: str, timestamp: str, decrypted: str) -> str:
    path = os.path.join(base_dir, "log", "plain", timestamp + ".txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(decrypted)
    return path

def write_metadata(base_dir: str, timestamp: str, mapping: Dict, freq: Dict) -> str:
    path = os.path.join(base_dir, "log", "metadata", timestamp + ".json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "mapping": mapping,
        "freq_ngram": {str(n): freq[n] for n in freq},
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    return path

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    content = load_ciphertext(base_dir)

    solver = Solver()
    mapping = solver.solve(content)
    for cipher_letter, plain_letter in CORRECTIONS:
        mapping = solver.replace_char(mapping, cipher_letter, plain_letter)

    decrypted = solver.decrypt(content, mapping)
    freq = {n: solver.freq_ngram(content, n) for n in (1, 2, 3)}

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    plain_path = write_plain(base_dir, timestamp, decrypted)
    metadata_path = write_metadata(base_dir, timestamp, mapping, freq)

    print("mapping (cipher -> plain):")
    print("".join(sorted(mapping)))
    print("".join(mapping[c] for c in sorted(mapping)))
    print()
    print("hasil dekripsi:")
    print(decrypted)
    print()
    print(f"[tersimpan ke {os.path.relpath(plain_path)} dan {os.path.relpath(metadata_path)}]")
