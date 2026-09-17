import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from frequencies import BIGRAM, TRIGRAM, QUADGRAM

class AffineSolver:
    def calculate_fitness(self, text: str) -> float:
        score = 0.0
        for i in range(len(text) - 1):
            bg = text[i:i+2]
            if bg in BIGRAM:
                score += BIGRAM[bg]
        for i in range(len(text) - 2):
            tg = text[i:i+3]
            if tg in TRIGRAM:
                score += TRIGRAM[tg]
        for i in range(len(text) - 3):
            qg = text[i:i+4]
            if qg in QUADGRAM:
                score += QUADGRAM[qg]
        return score

    def count(self, string: str) -> Dict:
        data = {}
        for c in string:
            if c.isalpha():
                data[c] = data.get(c, 0) + 1
        return dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    def sort(self, string: str) -> List:
        return list(self.count(string).keys())

    def mod_inverse(self, a: int, m: int) -> int:
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return -1

    def is_coprime(self, a: int, m: int) -> bool:
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
        return gcd(a, m) == 1

    def solve_keys(self, c1_char: str, c2_char: str, p1_char: str = 'E', p2_char: str = 'T') -> Tuple[int, int]:
        c1 = ord(c1_char) - ord('A')
        c2 = ord(c2_char) - ord('A')
        p1 = ord(p1_char) - ord('A')
        p2 = ord(p2_char) - ord('A')

        
        diff_c = (c1 - c2) % 26
        diff_p = (p1 - p2) % 26
        
        inv_diff_p = self.mod_inverse(diff_p, 26)
        if inv_diff_p == -1:
            return -1, -1
            
        m = (diff_c * inv_diff_p) % 26
        
        if not self.is_coprime(m, 26):
            return -1, -1
            
        b = (c1 - m * p1) % 26
        return m, b

    def decrypt(self, string: str, m: int, b: int) -> str:
        m_inv = self.mod_inverse(m, 26)
        if m_inv == -1:
            return ""
            
        result = []
        for c in string:
            if c.isalpha():
                y = ord(c) - ord('A')
                x = (m_inv * (y - b)) % 26
                result.append(chr(x + ord('A')))
            else:
                result.append(c)
        return "".join(result)

    def brute_force_fallback(self, string: str) -> List[Tuple[int, int, int, str]]:
        possible_m = [m for m in range(1, 26) if self.is_coprime(m, 26)]
        results = []
        for m in possible_m:
            for b in range(26):
                decrypted = self.decrypt(string, m, b)
                score = self.calculate_fitness(decrypted)
                results.append((score, m, b, decrypted))
        
        return sorted(results, key=lambda x: x[0], reverse=True)


def load_ciphertext(base_dir: str) -> str:
    with open(os.path.join(base_dir, "t.txt")) as f:
        return f.read().strip()

def write_plain(base_dir: str, timestamp: str, decrypted: str) -> str:
    path = os.path.join(base_dir, "log", "plain", timestamp + ".txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(decrypted)
    return path

def write_metadata(base_dir: str, timestamp: str, m: int, b: int) -> str:
    path = os.path.join(base_dir, "log", "metadata", timestamp + ".json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "key": {
            "m": m,
            "b": b
        }
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    return path

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    content = load_ciphertext(base_dir)

    solver = AffineSolver()
    
    sorted_chars = solver.sort(content)
    print("Karakter paling sering muncul di ciphertext:", sorted_chars[:5])
    c1_char = sorted_chars[0]
    c2_char = sorted_chars[1]
    print(f"Mencoba memetakan {c1_char} -> E dan {c2_char} -> T")
    
    m, b = solver.solve_keys(c1_char, c2_char, 'E', 'T')
    
    decrypted = ""
    if m != -1:
        print(f"Ditemukan kunci: m = {m}, b = {b}")
        decrypted = solver.decrypt(content, m, b)
        print("Preview hasil dekripsi:")
        print(decrypted[:100] + "...")
    else:
        print("Pemetaan E dan T tidak menghasilkan m yang valid. Mencoba Brute-force Fallback...")
        results = solver.brute_force_fallback(content)
        top_result = results[0]
        m, b = top_result[1], top_result[2]
        print(f"Hasil terbaik dari brute-force: m = {m}, b = {b}")
        decrypted = solver.decrypt(content, m, b)
        print("Preview hasil dekripsi:")
        print(decrypted[:100] + "...")
        
    if decrypted:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        plain_path = write_plain(base_dir, timestamp, decrypted)
        metadata_path = write_metadata(base_dir, timestamp, m, b)
        print(f"\n[Teks lengkap tersimpan ke {os.path.relpath(plain_path)}]")
        print(f"[Metadata tersimpan ke {os.path.relpath(metadata_path)}]")
