import json
import math
import os
import random
import sys
from datetime import datetime
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from frequencies import QUADGRAM

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

_ = 0
GRID = [
    [_, _, _, _, _],
    ["I", _, _, _, _],
    ["T", "E", "B", _, _],
    ["F", "G", "H", _, _],
    ["R", "V", _, _, _]
]

class Solver:
    def freq_bigram(self, string: str) -> Dict:
        freq_data = {}
        total_ngrams = len(string) // 2
        for i in range(0, len(string), 2):
            ngram = string[i:i+2]
            freq_data[ngram] = freq_data.get(ngram, 0) + 1
        for ngram in freq_data:
            freq_data[ngram] = (freq_data[ngram] / total_ngrams * 100)
        return dict(sorted(freq_data.items(), key=lambda item: item[1], reverse=True))

    def find_pos(self, grid: List, letter: str) -> Tuple[int, int]:
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val == letter:
                    return r, c
        return None

    def decrypt_pair(self, grid: List, a: str, b: str) -> str:
        ra, ca = self.find_pos(grid, a)
        rb, cb = self.find_pos(grid, b)
        if ra == rb:
            return grid[ra][(ca - 1) % 5] + grid[rb][(cb - 1) % 5]
        if ca == cb:
            return grid[(ra - 1) % 5][ca] + grid[(rb - 1) % 5][cb]
        return grid[ra][cb] + grid[rb][ca]

    def build_mapping(self, grid: List, bigrams: List) -> Dict:
        return {bigram: self.decrypt_pair(grid, bigram[0], bigram[1]) for bigram in bigrams}

    def decrypt(self, string: str, mapping: Dict) -> str:
        return "".join(mapping[string[i:i+2]] for i in range(0, len(string), 2))

    def score(self, plain: str) -> float:
        total = 0.0
        for i in range(len(plain) - 3):
            total += math.log10(QUADGRAM.get(plain[i:i+4], 0.001))
        return total

    def random_grid(self, grid: List) -> List:
        used = [val for row in grid for val in row if val != 0]
        rest = [letter for letter in ALPHABET if letter not in used]
        random.shuffle(rest)
        return [[val if val != 0 else rest.pop() for val in row] for row in grid]

    def free_cells(self, grid: List) -> List:
        return [(r, c) for r in range(5) for c in range(5) if grid[r][c] == 0]

    def swap(self, grid: List, free: List) -> List:
        new_grid = [row[:] for row in grid]
        if len(free) == 25 and random.random() < 0.1:
            a, b = random.sample(range(5), 2)
            if random.random() < 0.5:
                new_grid[a], new_grid[b] = new_grid[b], new_grid[a]
            else:
                for row in new_grid:
                    row[a], row[b] = row[b], row[a]
            return new_grid
        (ra, ca), (rb, cb) = random.sample(free, 2)
        new_grid[ra][ca], new_grid[rb][cb] = new_grid[rb][cb], new_grid[ra][ca]
        return new_grid

    def anneal(self, string: str, bigrams: List, grid: List, temp: float = 20.0,
               step: float = 0.5, rounds: int = 2500) -> Tuple[List, float]:
        free = self.free_cells(grid)
        current = self.random_grid(grid)
        current_score = self.score(self.decrypt(string, self.build_mapping(current, bigrams)))
        best, best_score = current, current_score
        while temp > 0:
            for _ in range(rounds):
                trial = self.swap(current, free)
                trial_score = self.score(self.decrypt(string, self.build_mapping(trial, bigrams)))
                delta = trial_score - current_score
                if delta > 0 or random.random() < math.exp(delta / temp):
                    current, current_score = trial, trial_score
                    if current_score > best_score:
                        best, best_score = current, current_score
            temp -= step
        return best, best_score

    def solve(self, string: str, grid: List, restarts: int = 2) -> Tuple[List, float]:
        sample = string[:2400]
        bigrams = list(self.freq_bigram(sample))
        best, best_score = None, -math.inf
        for _ in range(restarts):
            result, result_score = self.anneal(sample, bigrams, grid)
            if result_score > best_score:
                best, best_score = result, result_score
        return best, best_score

def load_ciphertext(base_dir: str) -> str:
    with open(os.path.join(base_dir, "f.txt")) as f:
        return f.read().strip()

def write_plain(base_dir: str, timestamp: str, decrypted: str) -> str:
    path = os.path.join(base_dir, "log", "plain", timestamp + ".txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(decrypted)
    return path

def write_metadata(base_dir: str, timestamp: str, mapping: Dict, grid_manual: List,
                    grid_filled: List, freq: Dict, score: float) -> str:
    path = os.path.join(base_dir, "log", "metadata", timestamp + ".json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "mapping": mapping,
        "grid_manual": grid_manual,
        "grid_filled": grid_filled,
        "freq_ngram": freq,
        "score": score,
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    return path

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    content = load_ciphertext(base_dir)

    solver = Solver()
    freq = solver.freq_bigram(content)
    grid, score = solver.solve(content, GRID)

    mapping = solver.build_mapping(grid, freq)
    decrypted = solver.decrypt(content, mapping)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    plain_path = write_plain(base_dir, timestamp, decrypted)
    metadata_path = write_metadata(base_dir, timestamp, mapping, GRID, grid, freq, score)

    print(decrypted)