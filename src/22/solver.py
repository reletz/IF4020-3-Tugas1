import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from frequencies import MONOGRAM

class VigenereSolver:
    def __init__(self):
        self.english_freq = {c: pct / 100.0 for c, pct in MONOGRAM.items()}

    def find_repeated_sequences(self, text: str, min_len: int = 3, max_len: int = 6) -> Dict[str, List[int]]:
        seq_positions = {}
        for length in range(min_len, max_len + 1):
            for i in range(len(text) - length + 1):
                seq = text[i:i+length]
                if seq not in seq_positions:
                    seq_positions[seq] = []
                seq_positions[seq].append(i)
        
        repeated_seqs = {seq: pos for seq, pos in seq_positions.items() if len(pos) > 1}
        return repeated_seqs

    def get_kasiski_factors(self, text: str, max_factor: int = 20) -> List[Tuple[int, int]]:
        repeated_seqs = self.find_repeated_sequences(text)
        distances = []
        for seq, pos in repeated_seqs.items():
            for i in range(len(pos) - 1):
                distances.append(pos[i+1] - pos[i])
        
        factor_counts = Counter()
        for dist in distances:
            for factor in range(2, max_factor + 1):
                if dist % factor == 0:
                    factor_counts[factor] += 1
                    
        return factor_counts.most_common(10)

    def guess_key(self, text: str, key_length: int) -> str:
        key = ""
        for i in range(key_length):
            subtext = text[i::key_length]
            counts = Counter(subtext)
            N = len(subtext)
            
            best_shift = 0
            max_dot_product = -1
            
            for shift in range(26):
                dot_product = 0
                for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    shifted_c = chr((ord(c) - 65 + shift) % 26 + 65)
                    observed_freq = counts[shifted_c] / N if N > 0 else 0
                    expected_freq = self.english_freq.get(c, 0.0)
                    
                    dot_product += observed_freq * expected_freq
                
                if dot_product > max_dot_product:
                    max_dot_product = dot_product
                    best_shift = shift
            
            key += chr(best_shift + 65)
        return key

    def decrypt(self, text: str, key: str) -> str:
        decrypted = []
        key_len = len(key)
        key_idx = 0
        for char in text:
            if char.isalpha():
                shift = ord(key[key_idx % key_len].upper()) - 65
                decrypted_char = chr((ord(char.upper()) - 65 - shift) % 26 + 65)
                decrypted.append(decrypted_char)
                key_idx += 1
            else:
                decrypted.append(char)
        return "".join(decrypted)

def load_ciphertext(base_dir: str) -> str:
    with open(os.path.join(base_dir, "v.txt")) as f:
        return f.read().strip().replace('\n', '').replace(' ', '')

def write_plain(base_dir: str, timestamp: str, decrypted: str) -> str:
    path = os.path.join(base_dir, "log", "plain", timestamp + ".txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(decrypted)
    return path

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    content = load_ciphertext(base_dir)

    solver = VigenereSolver()
    
    print("1. Kasiski Examination")
    factors = solver.get_kasiski_factors(content)
    print(f"Faktor yang paling sering muncul dari jarak antar substring berulang:")
    for factor, count in factors:
        print(f"Faktor {factor}: {count} kali")
    
    # Ambil nilai maksimum dari 3 faktor yang paling sering muncul
    best_key_length = max([factor for factor, count in factors[:3]])
    print(f"\nPanjang Kunci yang Ditebak (dari Kasiski): {best_key_length}")
    
    print("\n2. Frequency Analysis")
    guessed_key = solver.guess_key(content, best_key_length)
    print(f"Kunci yang Ditebak: {guessed_key}")

    decrypted = solver.decrypt(content, guessed_key)
    
    print("\n3. Plaintext Preview")
    print(decrypted[:200] + "...")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    plain_path = write_plain(base_dir, timestamp, decrypted)
    
    print(f"\n[tersimpan ke {os.path.relpath(plain_path)}]")
