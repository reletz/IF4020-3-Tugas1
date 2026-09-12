import json
import os
import sys
from datetime import datetime
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_ = 0
GRID = [
    [_, "D", _, _, _],
    [_, "I", _, _, _],
    ["E", "T", "R", "B", "V"],
    ["G", "F", _, "H", _],
    [_, _, _, _, _]
]

class Solver:
    def count(self, string: str) -> Dict:
        data = {}
        for i in range(0, len(string), 2):
            bigram = string[i:i+2]
            data[bigram] = data.get(bigram, 0) + 1
        return dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    def sort(self, string: str) -> List:
        return list(self.count(string).keys())

    def freq_bigram(self, string: str) -> Dict:
        freq_data = {}
        total_ngrams = len(string) // 2
        for i in range(0, len(string), 2):
            ngram = string[i:i+2]
            freq_data[ngram] = (freq_data.get(ngram, 0) + 1)
        for ngram in freq_data:
            freq_data[ngram] = (freq_data[ngram] / total_ngrams * 100)
        return dict(sorted(freq_data.items(), key=lambda item: item[1], reverse=True))

    def decrypt(self, string: str, mapping: Dict) -> str:
        decrypted = ""
        for i in range(0, len(string), 2):
            bigram = string[i:i+2]
            decrypted += (mapping[bigram] if bigram in mapping else bigram)
        return decrypted

    def find_pos(self, grid: List, letter: str):
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val == letter:
                    return r, c
        return None

    def playfair_decrypt_pair(self, grid: List, a: str, b: str) -> str | None:
        pos_a, pos_b = self.find_pos(grid, a), self.find_pos(grid, b)
        if pos_a is None or pos_b is None:
            return None
        ra, ca = pos_a
        rb, cb = pos_b
        if ra == rb:
            da, db = grid[ra][(ca - 1) % 5], grid[rb][(cb - 1) % 5]
        elif ca == cb:
            da, db = grid[(ra - 1) % 5][ca], grid[(rb - 1) % 5][cb]
        else:
            da, db = grid[ra][cb], grid[rb][ca]
        if da == 0 or db == 0:
            return None
        return da + db

    def build_corrections(self, grid: List, bigrams: List) -> Dict:
        mapping = {}
        for bigram in bigrams:
            result = self.playfair_decrypt_pair(grid, bigram[0], bigram[1])
            if result:
                mapping[bigram] = result
        return mapping

def load_ciphertext(base_dir: str) -> str:
    with open(os.path.join(base_dir, "f.txt")) as f:
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
    mapping = solver.build_corrections(GRID, solver.sort(content))

    decrypted = solver.decrypt(content, mapping)
    freq = solver.freq_bigram(content)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    plain_path = write_plain(base_dir, timestamp, decrypted)
    metadata_path = write_metadata(base_dir, timestamp, mapping, freq)

    print("mapping (cipher -> plain):")
    print("".join(sorted(mapping)))
    print("".join(mapping[c] for c in sorted(mapping)))
    print()
    print(decrypted)
    print()
    print(f"[tersimpan ke {os.path.relpath(plain_path)} dan {os.path.relpath(metadata_path)}]")
