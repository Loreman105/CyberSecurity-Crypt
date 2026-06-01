import sys
import os
import time
import json
import torch
import matplotlib.pyplot as plt
import random
from tkinter import Tk, filedialog

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from engine import LatticeEncryptionEngine

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

# Menu Workflows 
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
        encrypted_stream.append({
            "u": u.cpu().tolist(),
            "v": v.cpu().tolist()
        })

    # SEPARATED PAYLOADS
    # 1. The public ciphertext payload (No Secret Key)
    public_payload = {
        "parameters": {"k": k, "q": q, "error_bound": eb},
        "ciphertext": encrypted_stream
    }
    
    # 2. The private key payload
    private_key_payload = {
        "secret_key_s": s.cpu().tolist()
    }

    if is_file:
        # Save Ciphertext
        output_path = os.path.join(file_dir, f"{file_base}_encrypted.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(public_payload, f, indent=2)
            
        # Save Private Key
        key_path = os.path.join(file_dir, f"{file_base}_private_key.json")
        with open(key_path, "w", encoding="utf-8") as f:
            json.dump(private_key_payload, f, indent=2)
            
        print(f"[+] Security payload successfully compiled and saved to:\n    {output_path}")
        print(f"[+] PRIVATE KEY saved to:\n    {key_path}  <-- KEEP THIS SAFE!")
    else:
        root = Tk()
        root.withdraw()  # Hide tkinter window

        ciphertext_path = filedialog.asksaveasfilename(
            title="Save Encrypted Payload",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            initialfile="encrypted_payload.json"
        )

        if not ciphertext_path:
            print("[!] Save cancelled.")
            return

        key_path = filedialog.asksaveasfilename(
            title="Save Private Key",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            initialfile="private_key.json"
        )

        if not key_path:
            print("[!] Save cancelled.")
            return

        with open(ciphertext_path, "w", encoding="utf-8") as f:
            json.dump(public_payload, f, indent=2)

        with open(key_path, "w", encoding="utf-8") as f:
            json.dump(private_key_payload, f, indent=2)

        print(f"[+] Ciphertext saved to:\n    {ciphertext_path}")
        print(f"[+] Private key saved to:\n    {key_path}")

def handle_decryption():
    print("\n--- DECRYPTION MODE ---")
    print("1. Decrypt from encrypted JSON file")
    print("2. Decrypt paste raw JSON string token")
    sub_choice = input("Select an option (1-2): ").strip()

    payload_data = None
    key_data = None
    file_dir, file_base = "", ""
    is_file = False

    if sub_choice == "1":
        file_path = input("Enter the path to your encrypted .json file: ").strip()
        if not os.path.exists(file_path):
            print("[!] Error: Target file does not exist.")
            return
            
        key_path = input("Enter the path to your private key (.json) file: ").strip()
        if not os.path.exists(key_path):
            print("[!] Error: Private key file does not exist. Cannot decrypt.")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            payload_data = json.load(f)
        with open(key_path, "r", encoding="utf-8") as f:
            key_data = json.load(f)
            
        file_dir, file_name = os.path.split(file_path)
        file_base = file_name.replace("_encrypted.json", "")
        is_file = True
        
    elif sub_choice == "2":
        raw_json = input("Paste your raw JSON encrypted payload string: ").strip()
        raw_key = input("Paste your raw JSON private key string: ").strip()
        try:
            payload_data = json.loads(raw_json)
            key_data = json.loads(raw_key)
        except Exception as e:
            print(f"[!] Critical JSON parser fault: {e}")
            return
    else:
        print("[!] Invalid operation choice.")
        return

    # Extract original parameters
    params = payload_data.get("parameters", {})
    print(f"\n[Found Values] K: {params.get('k')}, Q: {params.get('q')}, Error Bound: {params.get('error_bound')}")
    
    use_override = input("Do you want to override these encryption values? (y/N): ").strip().lower()
    if use_override == 'y':
        k, q, eb = get_lattice_parameters()
    else:
        k, q, eb = params.get('k', 3), params.get('q', 3329), params.get('error_bound', 2)

    engine = LatticeEncryptionEngine(k=k, q=q, error_bound=eb)
    
    # Re-hydrate structural math keys using the separate key_data
    try:
        s = torch.tensor(key_data["secret_key_s"], device=engine.device, dtype=torch.float32)
    except KeyError:
        print("[!] Error: Invalid private key file. Missing 'secret_key_s'.")
        return
        
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
        print(f"[+] Plaintext recovered successfully. Saved to:\n    {output_path}")
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
    graph_points = []  # (q, eb, k, latency)

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
                        print(f"\n    [!] Integrity failure at K={k} ({accuracy*100:.1f}%)")
                        break

                    if latency_us > max_latency_us:
                        print(f"\n    [!] Latency limit hit at K={k} ({latency_us:.2f} μs)")
                        break

                    last_valid = {
                        "q": q,
                        "eb": eb,
                        "k": k,
                        "latency": latency_us
                    }

                    print(f"\r    K={k:<4} | {latency_us:.2f} μs", end="")

                    k += 1

                except Exception as e:
                    print(f"\n    [!] Failure at K={k}: {e}")
                    break

            if last_valid:
                results.append(last_valid)

    print("\n" + "=" * 60)
    print("           AUTO TUNE RESULT")
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
        print("         MODULAR LATTICE CRYPTOGRAPHY ENGINE UI")
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
            handle_auto_tune()   
        elif choice == "4":
            print("[*] Shutdown complete.")
            break
        else:
            print("[!] Invalid option.")


if __name__ == "__main__":
    main()