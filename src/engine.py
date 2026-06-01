import torch
from tkinter import Tk, filedialog

class LatticeEncryptionEngine:
    def __init__(self, k=3, q=3329, error_bound=2):
        self.k = k
        self.q = q
        self.error_bound = error_bound

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

    def _sample_small(self, shape):
        return torch.randint(
            -self.error_bound,
            self.error_bound + 1,
            shape,
            device=self.device, 
            dtype=torch.float32
        )

    def keygen(self):
        A = torch.randint(
            0,
            self.q,
            (self.k, self.k),
            device=self.device,
            dtype=torch.float32
        )

        s = self._sample_small((self.k, 1))
        e = self._sample_small((self.k, 1))

        t = torch.remainder(torch.matmul(A, s) + e, self.q)

        return A, t, s

    def encrypt(self, A, t, bit):
        r = self._sample_small((self.k, 1))
        e1 = self._sample_small((self.k, 1))
        e2 = self._sample_small((1, 1))

        u = torch.remainder(torch.matmul(A.t(), r) + e1, self.q)

        encoded_bit = float(bit * (self.q // 2))

        v = torch.remainder(
            torch.matmul(t.t(), r) + e2 + encoded_bit,
            self.q
        )

        return u, v

    def decrypt(self, s, u, v):
        noisy_message = torch.remainder(
            v - torch.matmul(s.t(), u),
            self.q
        )

        target = self.q // 2
        diff = torch.abs(noisy_message - target)

        is_one = (
            (diff < (self.q // 4))
            | (torch.abs(diff - self.q) < (self.q // 4))
        )

        return int(is_one.int().item())