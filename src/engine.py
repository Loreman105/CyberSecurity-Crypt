import torch

class LatticeEncryptionEngine:
    def __init__(self, k=3, q=3329, error_bound=2):
        self.k = k
        self.q = q
        self.error_bound = error_bound
        
        # Select CUDA if available, otherwise CPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def keygen(self):
        """Generates Public Key (A, t) and Secret Key (s)"""
        A = torch.randint(0, self.q, (self.k, self.k), device=self.device, dtype=torch.float32)
        s = torch.randint(-self.error_bound, self.error_bound + 1, (self.k, 1), device=self.device, dtype=torch.float32)
        e = torch.randint(-self.error_bound, self.error_bound + 1, (self.k, 1), device=self.device, dtype=torch.float32)
        
        t = torch.remainder(torch.matmul(A, s) + e, self.q)
        return A, t, s

    def encrypt(self, A, t, message_bit):
        """Encrypts a single 0 or 1 bit into ciphertext tuple (u, v)"""
        r = torch.randint(-self.error_bound, self.error_bound + 1, (self.k, 1), device=self.device, dtype=torch.float32)
        e1 = torch.randint(-self.error_bound, self.error_bound + 1, (self.k, 1), device=self.device, dtype=torch.float32)
        e2 = torch.randint(-self.error_bound, self.error_bound + 1, (1, 1), device=self.device, dtype=torch.float32)
        
        u = torch.remainder(torch.matmul(A.t(), r) + e1, self.q)
        scaled_message = float(message_bit * (self.q // 2))
        v = torch.remainder(torch.matmul(t.t(), r) + e2 + scaled_message, self.q)
        return u, v

    def decrypt(self, s, u, v):
        """Decrypts ciphertext tuple (u, v) back to a bit using pure tensor logic."""
        noisy_message = torch.remainder(v - torch.matmul(s.t(), u), self.q)
        target = self.q // 2
        diff = torch.abs(noisy_message - target)
        is_one = (diff < (self.q // 4)) | (torch.abs(diff - self.q) < (self.q // 4))
        return int(is_one.int().item())