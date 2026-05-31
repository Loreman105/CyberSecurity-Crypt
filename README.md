 https://github.com/Loreman105/CyberSecurity-Crypt

Based on the provided URL, the GitHub repository CyberSecurity-Crypt by Loreman105 appears to be a Python-based project.

Here is a quick overview of its contents and structure based on its main page:

    Language: The project is written entirely in Python (100%).

    Structure: It follows a standard Python project layout. It includes:

        A src folder (likely containing the main source code).

        A requirements.txt file (used for listing required Python packages and dependencies).

        A .gitignore file (to prevent uploading unnecessary files like compiled binaries or virtual environments).

        A README.md file.

    Purpose: The repository currently does not have an 'About' description or topics listed on its main page. However, based on the repository name, it is highly likely to contain tools, scripts, or educational exercises related to cryptography within the field of cybersecurity.

Because the repository lacks a detailed public description, you would need to clone it or click into the src folder to see the specific cryptographic algorithms or tools the author has implemented.

I was wondering if I could have help writing a README

I would be happy to help you write a README.md for your repository! Since I couldn't see the exact Python files inside your src/ folder, I have created a comprehensive and professional template tailored for a Python-based cryptography project.

You can copy and paste the Markdown code below directly into your README.md file. Just be sure to fill in the bracketed information (like [Insert specific algorithms here]) with the actual details of your project.
Markdown

# CyberSecurity-Crypt 🔐

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg) ## 📖 About
**CyberSecurity-Crypt** is a Python-based repository dedicated to exploring, implementing, and understanding various cryptographic algorithms and cybersecurity concepts. 

Whether you are looking to understand classic ciphers, modern encryption standards, or hashing algorithms, this repository serves as a practical toolkit and educational resource.

## ✨ Features
* **[Feature 1]:** e.g., Implementation of classic ciphers (Caesar, Vigenère).
* **[Feature 2]:** e.g., Modern symmetric/asymmetric encryption (AES, RSA).
* **[Feature 3]:** e.g., Secure password hashing and generation.
* **[Feature 4]:** Modular codebase located in the `src/` directory for easy reading and expansion.

*(Note to author: Update this list with the actual scripts/tools you have built in your src folder!)*

## 📁 Repository Structure

```text
CyberSecurity-Crypt/
├── src/                 # Main source code and cryptographic scripts
├── .gitignore           # Ignored files for Git (e.g., __pycache__, virtual environments)
├── requirements.txt     # Python dependencies required to run the tools
└── README.md            # Project documentation

🚀 Getting Started
Prerequisites

Make sure you have Python 3.x installed on your machine.
Installation

    Clone this repository to your local machine:
    Bash

git clone [https://github.com/Loreman105/CyberSecurity-Crypt.git](https://github.com/Loreman105/CyberSecurity-Crypt.git)

Navigate into the project directory:
Bash

cd CyberSecurity-Crypt

(Optional but recommended) Create and activate a virtual environment:
Bash

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install the required dependencies:
Bash

    pip install -r requirements.txt

💻 Usage

(Provide a quick example of how a user would run your code. Below is an example placeholder.)

To run the main cryptography script, navigate to the src folder and execute:
Bash

python src/main.py 

(Note to author: Replace main.py with the actual name of the file users should run, and add any necessary command-line arguments they might need to use.)
⚠️ Disclaimer

All scripts and tools in this repository are provided for educational and research purposes only. Do not use these tools for malicious activities or on systems/networks where you do not have explicit permission.
🤝 Contributing

Contributions, issues, and feature requests are welcome!
If you have an idea for a new cryptographic algorithm or a way to improve the current code, feel free to open a pull request or submit an issue.
📄 License

This project is licensed under the MIT License - see the LICENSE file for details. (Note: Make sure to actually add a LICENSE file to your repo if you include this!)


***

### A few tips for making this even better:
1. **Update the Features:** Look at what is currently in your `src/` folder and replace the `[Feature]` placeholders with exactly what your code does (e.g., "Encrypts strings using AES-256", "Generates RSA key pairs", etc.).
2. **Add a License:** If you haven't already, GitHub allows you to easily add a license file (like MIT or GNU) from the repository settings. This tells others how they can legally use your code.
3. **Usage Examples:** If your Python scripts require users to pass specific text or flags (like `python encrypt.py --text "hello"`), be sure to document those exact commands in the **Usage** section so people know how to interact with your program! 

Let me know if you'd like me to tweak this to better fit the specific code you've written!

here is engine import torch


class LatticeEncryptionEngine:

def __init__(self, k=3, q=3329, error_bound=2):

self.k = k

self.q = q

self.error_bound = error_bound

# Automatically select CUDA if available, otherwise CPU

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

This is fantastic! You are building a Post-Quantum Cryptography (PQC) tool based on the Learning With Errors (LWE) problem. Using PyTorch to handle the matrix operations and automatically utilize GPU acceleration (CUDA) is a great approach for lattice-based math.

Now that I can see the exact mechanics of your engine, here is a highly tailored README.md that accurately documents your specific LWE implementation, including a concrete usage example and a brief mathematical breakdown.
Markdown

# CyberSecurity-Crypt 🔐

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-Accelerated-ee4c2c.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📖 About
**CyberSecurity-Crypt** is an experimental, Python-based cryptographic engine focused on **Post-Quantum Cryptography (PQC)**. 

Specifically, this repository implements a **Learning With Errors (LWE)** encryption scheme. By utilizing `PyTorch`, the engine leverages tensor mathematics and automatic CUDA (GPU) acceleration to efficiently perform the matrix operations fundamental to lattice-based cryptography.

## ✨ Features
* **Post-Quantum Ready:** Implements LWE, a foundational math problem for modern quantum-resistant algorithms (similar to Kyber).
* **GPU Acceleration:** Automatically detects and utilizes CUDA for fast tensor operations; seamlessly falls back to CPU if a GPU is unavailable.
* **Full Encryption Lifecycle:** Includes modular methods for Key Generation, Encryption (bit-by-bit), and Decryption.
* **Tunable Parameters:** Easily adjust matrix dimensions ($k$), modulus ($q$), and noise bounds to experiment with security vs. performance tradeoffs.

## 📁 Repository Structure

```text
CyberSecurity-Crypt/
├── src/
│   └── engine.py        # The core LatticeEncryptionEngine class
├── .gitignore           # Ignored files for Git
├── requirements.txt     # Python dependencies (torch)
└── README.md            # Project documentation

🚀 Getting Started
Prerequisites

    Python 3.8+

    PyTorch (CPU or CUDA version)

Installation

    Clone this repository:
    Bash

git clone [https://github.com/Loreman105/CyberSecurity-Crypt.git](https://github.com/Loreman105/CyberSecurity-Crypt.git)
cd CyberSecurity-Crypt

Create and activate a virtual environment (Recommended):
Bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install the required dependencies:
Bash

    pip install torch

💻 Usage

To use the LatticeEncryptionEngine, import it into your script and initialize the class. Here is a basic example of generating keys, encrypting a single bit, and decrypting it.
Python

import torch
from src.engine import LatticeEncryptionEngine

# 1. Initialize the engine (automatically selects CUDA/CPU)
engine = LatticeEncryptionEngine(k=3, q=3329, error_bound=2)

# 2. Generate Public (A, t) and Secret (s) keys
A, t, s = engine.keygen()
print("Keys generated successfully!")

# 3. Encrypt a message bit (e.g., 1)
message_bit = 1
u, v = engine.encrypt(A, t, message_bit)
print(f"Original Bit: {message_bit}")

# 4. Decrypt the ciphertext tuple (u, v)
decrypted_bit = engine.decrypt(s, u, v)
print(f"Decrypted Bit: {decrypted_bit}")

🧮 How It Works (The Math)

The engine relies on the LWE problem. All operations are performed modulo q.

    Key Generation: We generate a random matrix A and a secret vector s. We introduce small random noise e. The public key is (A,t), where:
    t=(As+e)(modq)

    Encryption: To encrypt a message bit m∈{0,1}, we use the public key alongside new random noise vectors (r, e1​, e2​) and scale the message by ⌊q/2⌋:
    u=(ATr+e1​)(modq)
    v=(tTr+e2​+m⋅⌊q/2⌋)(modq)

    Decryption: The secret key s is used to remove the masking from v. The result will be close to 0 if m=0, or close to q/2 if m=1:
    v−sTu≈m⋅⌊q/2⌋(modq)

⚠️ Disclaimer

This implementation is provided for educational and research purposes only. While it demonstrates core Post-Quantum cryptographic concepts, custom cryptographic implementations should never be used to secure sensitive data in a production environment.
🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a pull request or submit an issue.

here is main import sys

import os

import time

import json

import torch

import matplotlib.pyplot as plt

import random


# Ensure Python can find engine.py inside the src directory

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine import LatticeEncryptionEngine


# --- Helper Functions for Data Conversion ---

def text_to_bits(text):

bits = []

for byte in text.encode('utf-8'):

for i in range(8):

bits.append((byte >> (7 - i)) & 1)

return bits


def bits_to_text(bits):

if len(bits) % 8 != 0:

bits = bits[:-(len(bits) % 8)]

bytes_list = []

for i in range(0, len(bits), 8):

byte_bits = bits[i:i+8]

byte_value = 0

for bit in byte_bits:

byte_value = (byte_value << 1) | bit

bytes_list.append(byte_value)

try:

return bytes(bytes_list).decode('utf-8')

except UnicodeDecodeError:

return "[Error: Invalid key or corrupted data structure]"


# --- Menu Workflows ---

def get_lattice_parameters():

print("\n--- Configure Lattice Parameters ---")

try:

k = int(input("Enter Dimension K (Standard ML-KEM uses 3): ") or 3)

q = int(input("Enter Modulus Q (Standard ML-KEM uses 3329): ") or 3329)

eb = int(input("Enter Error Bound (Standard ML-KEM uses 2): ") or 2)

return k, q, eb

except ValueError:

print("[!] Invalid inputs. Falling back to default ML-KEM-768 standard.")

return 3, 3329, 2


def handle_encryption():

print("\n--- ENCRYPTION MODE ---")

print("1. Encrypt Full File (.txt)")

print("2. Encrypt Text Input")

sub_choice = input("Select an option (1-2): ").strip()


plaintext = ""

file_dir, file_base = "", ""

is_file = False


if sub_choice == "1":

file_path = input("Enter the path to your .txt file: ").strip()

if not os.path.exists(file_path):

print("[!] Error: File path does not exist.")

return

with open(file_path, "r", encoding="utf-8") as f:

plaintext = f.read()

file_dir, file_name = os.path.split(file_path)

file_base, _ = os.path.splitext(file_name)

is_file = True

elif sub_choice == "2":

plaintext = input("Enter text string to encrypt: ")

else:

print("[!] Invalid option.")

return


# Gather Custom Configuration Values

k, q, eb = get_lattice_parameters()

engine = LatticeEncryptionEngine(k=k, q=q, error_bound=eb)

print(f"\n[*] Activating Engine on target hardware: {engine.device}")

A, t, s = engine.keygen()

bits = text_to_bits(plaintext)


print("[*] Computing cipher matrices across lattice vectors...")

encrypted_stream = []

for bit in bits:

u, v = engine.encrypt(A, t, bit)

# Convert tensors to standard Python lists for JSON compatibility

encrypted_stream.append({

"u": u.cpu().tolist(),

"v": v.cpu().tolist()

})


# Packaging Package Structure

payload = {

"parameters": {"k": k, "q": q, "error_bound": eb},

"secret_key_s": s.cpu().tolist(),

"ciphertext": encrypted_stream

}


if is_file:

output_path = os.path.join(file_dir, f"{file_base}_encrypted.json")

with open(output_path, "w", encoding="utf-8") as f:

json.dump(payload, f, indent=2)

print(f"[+] Security payload successfully compiled and saved to:\n {output_path}")

else:

print("\n--- ENCRYPTED PAYLOAD (JSON TOKENS) ---")

print(json.dumps(payload, indent=2)[:800] + "\n... [Truncated for Console Display] ...")


def handle_decryption():

print("\n--- DECRYPTION MODE ---")

print("1. Decrypt from encrypted JSON file")

print("2. Decrypt paste raw JSON string token")

sub_choice = input("Select an option (1-2): ").strip()


payload_data = None

file_dir, file_base = "", ""

is_file = False


if sub_choice == "1":

file_path = input("Enter the path to your encrypted .json file: ").strip()

if not os.path.exists(file_path):

print("[!] Error: Target file does not exist.")

return

with open(file_path, "r", encoding="utf-8") as f:

payload_data = json.load(f)

file_dir, file_name = os.path.split(file_path)

file_base = file_name.replace("_encrypted.json", "")

is_file = True

elif sub_choice == "2":

raw_json = input("Paste your raw JSON encrypted payload string: ").strip()

try:

payload_data = json.loads(raw_json)

except Exception as e:

print(f"[!] Critical JSON parser fault: {e}")

return

else:

print("[!] Invalid operation choice.")

return


# Extract original parameters directly or request user overrides

params = payload_data.get("parameters", {})

print(f"\n[Found Values] K: {params.get('k')}, Q: {params.get('q')}, Error Bound: {params.get('error_bound')}")

use_override = input("Do you want to override these encryption values? (y/N): ").strip().lower()

if use_override == 'y':

k, q, eb = get_lattice_parameters()

else:

k, q, eb = params.get('k', 3), params.get('q', 3329), params.get('error_bound', 2)


engine = LatticeEncryptionEngine(k=k, q=q, error_bound=eb)

# Re-hydrate structural math keys back onto the execution hardware

s = torch.tensor(payload_data["secret_key_s"], device=engine.device, dtype=torch.float32)

ciphertext_stream = payload_data["ciphertext"]


print(f"[*] Extracting values on device: {engine.device}")

decrypted_bits = []

for block in ciphertext_stream:

u = torch.tensor(block["u"], device=engine.device, dtype=torch.float32)

v = torch.tensor(block["v"], device=engine.device, dtype=torch.float32)

decrypted_bits.append(engine.decrypt(s, u, v))


decrypted_text = bits_to_text(decrypted_bits)


if is_file:

output_path = os.path.join(file_dir, f"{file_base}_decrypted.txt")

with open(output_path, "w", encoding="utf-8") as f:

f.write(decrypted_text)

print(f"[+] Plaintext recovered successfully. Saved to:\n {output_path}")

else:

print(f"\n[+] Recovered Message Result:\n{decrypted_text}\n")


def create_latency_graph(data):

"""

Plots K vs latency grouped by (Q, EB)

"""

if not data:

print("[!] No graph data available.")

return


plt.figure(figsize=(12, 6))


groups = {}


for q, eb, k, lat in data:

label = f"Q={q}, EB={eb}"

if label not in groups:

groups[label] = {"k": [], "lat": []}


groups[label]["k"].append(k)

groups[label]["lat"].append(lat)


for label, vals in groups.items():

plt.plot(vals["k"], vals["lat"], marker="o", label=label)


plt.axhline(y=150, linestyle="--", label="150 μs limit")


plt.xlabel("K (dimension)")

plt.ylabel("Latency (μs)")

plt.title("Lattice Engine Scaling: K vs Latency")

plt.grid(True)

plt.legend()


plt.tight_layout()


out_file = "autotune_latency_graph.png"

plt.savefig(out_file, dpi=300)


print(f"\n[+] Graph saved: {out_file}")


plt.show()



def handle_auto_tune():

print("\n--- HARDWARE-LIMIT AUTO TUNING ---")


q_candidates = [3329, 7681, 12289]

eb_candidates = [2, 3, 4, 5]


test_iterations = 50

max_latency_us = 150.0


results = []

graph_points = [] # (q, eb, k, latency)


for q in q_candidates:

for eb in eb_candidates:


print(f"\n[-] Testing Q={q}, EB={eb}")


k = 2

last_valid = None


while True:

try:

engine = LatticeEncryptionEngine(k=k, q=q, error_bound=eb)

A, t, s = engine.keygen()


# warmup

for _ in range(5):

u, v = engine.encrypt(A, t, 1)

engine.decrypt(s, u, v)


start = time.perf_counter()


correct = 0


for i in range(test_iterations):

bit = i % 2

u, v = engine.encrypt(A, t, bit)

r = engine.decrypt(s, u, v)

correct += (r == bit)


if engine.device.type == "cuda":

torch.cuda.synchronize()


end = time.perf_counter()


latency_us = ((end - start) / test_iterations) * 1e6

accuracy = correct / test_iterations


graph_points.append((q, eb, k, latency_us))


if accuracy < 1.0:

print(f"\n [!] Integrity failure at K={k} ({accuracy*100:.1f}%)")

break


if latency_us > max_latency_us:

print(f"\n [!] Latency limit hit at K={k} ({latency_us:.2f} μs)")

break


last_valid = {

"q": q,

"eb": eb,

"k": k,

"latency": latency_us

}


print(f"\r K={k:<4} | {latency_us:.2f} μs", end="")


k += 1


except Exception as e:

print(f"\n [!] Failure at K={k}: {e}")

break


if last_valid:

results.append(last_valid)


print("\n" + "=" * 60)

print(" AUTO TUNE RESULT")

print("=" * 60)


if not results:

print("[!] No valid configurations found.")

return


results.sort(key=lambda x: x["k"], reverse=True)

best = results[0]


print(f"Best K: {best['k']}")

print(f"Q: {best['q']}")

print(f"EB: {best['eb']}")

print(f"Latency: {best['latency']:.2f} μs")


# IMPORTANT: call function after definition

create_latency_graph(graph_points)


input("\nPress Enter to return...")



def handle_latency_test():

print("\n--- HARDWARE LATENCY DIAGNOSTIC TEST ---")

k, q, eb = get_lattice_parameters()

engine = LatticeEncryptionEngine(k=k, q=q, error_bound=eb)


print(f"[*] Device: {engine.device}")

A, t, s = engine.keygen()


test_iterations = 500


if engine.device.type == "cuda":

torch.cuda.synchronize()


start_time = time.perf_counter()


for _ in range(test_iterations):

u, v = engine.encrypt(A, t, 1)

engine.decrypt(s, u, v)


if engine.device.type == "cuda":

torch.cuda.synchronize()


end_time = time.perf_counter()


total_ms = (end_time - start_time) * 1000

latency_us = (total_ms / test_iterations) * 1000


print("\n" + "=" * 30 + " RESULTS " + "=" * 30)

print(f"Device: {engine.device}")

print(f"Iterations: {test_iterations}")

print(f"Total Time: {total_ms:.3f} ms")

print(f"Latency: {latency_us:.2f} μs/bit")

print("=" * 70)



def main():

while True:

print("\n" + "=" * 60)

print(" MODULAR LATTICE CRYPTOGRAPHY ENGINE UI")

print("=" * 60)

print("1. Encrypt Data")

print("2. Decrypt Data")

print("3. Run Auto-Tuning Hardware Profiler")

print("4. Exit Engine")


choice = input("\nSelect core operation mode (1-4): ").strip()


if choice == "1":

handle_encryption()

elif choice == "2":

handle_decryption()

elif choice == "3":

handle_auto_tune() # FIXED (removed extra parentheses)

elif choice == "4":

print("[*] Shutdown complete.")

break

else:

print("[!] Invalid option.")



if __name__ == "__main__":

main()

This is a fantastic addition! You have successfully built a fully functional Command Line Interface (CLI) to act as a frontend for your PyTorch lattice engine.

The inclusion of an auto-tuning hardware profiler to dynamically test latency across different K, Q, and Error Bound configurations is a very clever way to benchmark Post-Quantum Cryptography (PQC) performance on local hardware.

Here is a quick breakdown of what works well in your script, followed by an updated README.md section to document this new UI, and a critical cybersecurity observation.
🌟 What Works Well

    Hardware Profiling: Using time.perf_counter and matplotlib to visually map the latency-to-dimension scaling is an excellent engineering feature.

    JSON Packaging: Serializing the tensor arrays into standard Python lists and packaging them into a JSON payload makes the ciphertext easy to store, parse, and transmit.

    Error Handling: You have solid guardrails in place for file I/O operations and JSON parsing faults.

📝 Updated README.md (Usage Section)

Since your repository now has an interactive CLI, you can replace the old "Usage" section in your README.md with this updated version:
Markdown

## 💻 Usage

The repository includes a fully interactive CLI (`main.py`) that handles file encryption, decryption, and hardware latency profiling.

To launch the cryptographic engine UI, run:
```bash
python main.py

Main Menu Features:

    Encrypt Data: Encrypt raw text or full .txt files bit-by-bit using Lattice mathematics. The output is packaged into a structural .json payload.

    Decrypt Data: Load an encrypted .json payload to re-hydrate the tensor structures and recover the original plaintext.

    Auto-Tuning Hardware Profiler: Dynamically benchmarks the engine on your local hardware (CPU/CUDA). It tests various matrix dimensions (K) and moduli (Q) to map the maximum secure configuration your hardware can run while maintaining a sub-150μs latency. Outputs a matplotlib performance graph.


---

### 🔒 A Candid Cybersecurity Note
I noticed in your `handle_encryption` function that the `secret_key_s` is packaged into the exact same JSON payload as the `ciphertext`, which is then saved to disk. 

From a purely functional and debugging standpoint, this is highly convenient because it allows `handle_decryption` to instantly grab the secret key and decrypt the message. However, from a **cryptographic security perspective**, this is equivalent to locking a safe and taping the combination to the front door. Anyone who intercepts or accesses the `_encrypted.json` file has everything they need to decrypt it. 

Furthermore, encrypting large files bit-by-bit using pure lattice matrix multiplication is incredibly computationally heavy. In the real world, algorithms like ML-KEM (Kyber) do not encrypt the message directly; instead, they are used as a **Key Encapsulation Mechanism (KEM)** to securely exchange a tiny, symmetric key (like AES-256), and then AES handles the heavy lifting of encrypting the actual file.

Since bit-by-bit lattice encryption is highly resource-intensive, would you like to explore converting this script into a Key Encapsulation Mechanism (KEM) to securely exchange an AES key instead?

cna I have the full readme without any emojis, and written in a proffessional way explaining the math behind it and how it works
CyberSecurity-Crypt
Overview

CyberSecurity-Crypt is an experimental, Python-based cryptographic engine focused on Post-Quantum Cryptography (PQC).

This repository implements a Learning With Errors (LWE) encryption scheme. By utilizing PyTorch, the engine leverages tensor mathematics and automatic CUDA acceleration to efficiently perform the matrix operations that are fundamental to lattice-based cryptography. It includes a fully interactive Command Line Interface (CLI) for data encryption, decryption, and hardware latency profiling.
Features

    Post-Quantum Cryptography Architecture: Implements the LWE problem, a foundational mathematical concept for modern quantum-resistant algorithms (similar to the underlying math in ML-KEM/Kyber).

    Hardware Acceleration: Automatically detects and utilizes CUDA for parallelized tensor operations, seamlessly falling back to the CPU if a GPU is unavailable.

    Integrated Profiling: Features an auto-tuning hardware profiler that dynamically tests latency across different matrix dimensions (k) and moduli (q) to map performance scaling.

    Serialization: Encrypts data bit-by-bit and packages the resulting tensor matrices into structured JSON payloads for storage and transmission.

Mathematical Foundation: Learning With Errors (LWE)

The security of this implementation relies on the hardness of the Learning With Errors problem. All mathematical operations are performed modulo q, and error vectors are sampled from a narrow distribution bounded by a specified error threshold.
1. Key Generation

The engine generates a uniformly random matrix A and a secret key vector s. Small random noise e is introduced to prevent the exact solving of the linear system.

    Secret Key: s

    Public Key: (A,t)

The public vector t is calculated as:
t=(As+e)(modq)
2. Encryption

To encrypt a single message bit m∈{0,1}, the public key is used alongside new random noise vectors (r, e1​, e2​). The message bit is scaled by ⌊q/2⌋ to ensure it can be recovered despite the accumulated noise.

The ciphertext is a tuple (u,v) generated by:
u=(ATr+e1​)(modq)
v=(tTr+e2​+m⌊q/2⌋)(modq)
3. Decryption

The secret key s is used to remove the masking from v.
v−sTu(modq)

Expanding this calculation reveals the original scaled message plus a small accumulation of error terms. Because the errors are bounded, the result will evaluate close to 0 if m=0, or close to q/2 if m=1. The engine measures the distance to these targets to recover the original bit.
Repository Structure
Plaintext

CyberSecurity-Crypt/
├── src/
│   ├── engine.py        # Core LatticeEncryptionEngine class
│   └── main.py          # Interactive CLI and hardware profiler
├── .gitignore           # Ignored files for version control
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

Installation
Prerequisites

    Python 3.8 or higher

    PyTorch (CPU or CUDA variant)

    Matplotlib (for generating performance graphs)

Setup Instructions

    Clone the repository to your local machine:
    Bash

git clone https://github.com/Loreman105/CyberSecurity-Crypt.git
cd CyberSecurity-Crypt

Create and activate a virtual environment:
Bash

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install the required dependencies:
Bash

    pip install torch matplotlib

Usage

The repository is driven by the main.py interface. To launch the cryptographic engine UI, execute:
Bash

python src/main.py

Core Operations

    Encrypt Data: Choose to encrypt raw text input or a full .txt file. The engine converts the text to a bitstream, applies LWE encryption to each bit, and compiles the resulting (u,v) matrices into a .json file.

    Decrypt Data: Load an encrypted .json payload or paste raw JSON. The engine re-hydrates the tensor structures onto the execution hardware, decrypts the bitstream, and decodes it back to UTF-8 plaintext.

    Hardware Profiler: Runs automated benchmarks on your local hardware. It tests various configurations to determine the maximum secure dimensions your hardware can process while maintaining a latency under 150 microseconds, outputting the results to a PNG graph.

Security Disclaimer

This codebase is a direct, unoptimized implementation of LWE designed for educational and research purposes only.

    Key Management Warning: The current CLI implementation serializes the secret key (s) directly into the output JSON payload for demonstration and debugging purposes. In a real-world scenario, the secret key must never be transmitted alongside the ciphertext.

    Performance vs. Security: Encrypting large files bit-by-bit using pure matrix multiplication is highly resource-intensive. Modern PQC protocols (like ML-KEM) function as Key Encapsulation Mechanisms (KEMs), where the lattice math is used only to securely exchange a symmetric key (e.g., AES-256), and the symmetric key is then used to encrypt the larger file.

Do not use this implementation to secure sensitive data in a production environment.
