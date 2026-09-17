import json
import os
from datetime import datetime
import numpy as np

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Invers modular tidak ada')
    else:
        return x % m

def matrix_mod_inv(matrix, modulus):
    det = int(round(np.linalg.det(matrix)))
    det_inv = modinv(det % modulus, modulus)
    matrix_modulum = det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    return matrix_modulum

class HillSolver:
    def __init__(self, m: int = 3):
        self.m = m

    def solve_key(self, plain: str, cipher: str) -> np.ndarray:
        P_list = [ord(c) - ord('A') for c in plain[:self.m * self.m]]
        C_list = [ord(c) - ord('A') for c in cipher[:self.m * self.m]]
        
        P = np.array(P_list).reshape((self.m, self.m)).T
        C = np.array(C_list).reshape((self.m, self.m)).T
        
        try:
            P_inv = matrix_mod_inv(P, 26)
            K = np.dot(C, P_inv) % 26
            return K
        except Exception as e:
            print("Gagal mencari invers matriks Plaintext:", e)
            return None

    def decrypt(self, cipher: str, K: np.ndarray) -> str:
        K_inv = matrix_mod_inv(K, 26)
        
        C_nums = [ord(c) - ord('A') for c in cipher if c.isalpha()]
        
        pad_len = (self.m - len(C_nums) % self.m) % self.m
        if pad_len > 0:
            C_nums.extend([0] * pad_len)
            
        P_nums = []
        for i in range(0, len(C_nums), self.m):
            C_block = np.array(C_nums[i:i+self.m])
            P_block = np.dot(K_inv, C_block) % 26
            P_nums.extend(P_block.tolist())
            
        if pad_len > 0:
            P_nums = P_nums[:-pad_len]
            
        result = []
        idx = 0
        for c in cipher:
            if c.isalpha():
                result.append(chr(int(P_nums[idx]) + ord('A')))
                idx += 1
            else:
                result.append(c)
                
        return "".join(result)

def load_ciphertext(base_dir: str) -> str:
    with open(os.path.join(base_dir, "h.txt")) as f:
        return f.read().strip()

def write_plain(base_dir: str, timestamp: str, decrypted: str) -> str:
    path = os.path.join(base_dir, "log", "plain", timestamp + ".txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(decrypted)
    return path

def write_metadata(base_dir: str, timestamp: str, K: np.ndarray) -> str:
    path = os.path.join(base_dir, "log", "metadata", timestamp + ".json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "key": {
            "matrix": K.tolist()
        }
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    return path

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    content = load_ciphertext(base_dir)

    solver = HillSolver(m=3)
    
    known_plain = "EXPLOSIVESCOOP" # dari spek
    K = solver.solve_key(known_plain, content.replace(' ', '')[:9])
    
    if K is not None:
        print("Ditemukan matriks kunci K:")
        print(K)
        decrypted = solver.decrypt(content, K)
        print("\nPreview hasil dekripsi:")
        print(decrypted[:100] + "...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        plain_path = write_plain(base_dir, timestamp, decrypted)
        metadata_path = write_metadata(base_dir, timestamp, K)
        print(f"\n[Teks lengkap tersimpan ke {os.path.relpath(plain_path)}]")
        print(f"[Metadata tersimpan ke {os.path.relpath(metadata_path)}]")
    else:
        print("Gagal menemukan kunci.")
