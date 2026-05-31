import sys
import os
import time
import json
import torch

# Ensure Python can find engine.py inside the src directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from engine import LatticeEncryptionEngine

# --- Byte & Bitstream Management with Chunking Support ---
def bytes_to_bits(byte_data):
    """Converts raw bytes into a flat list of 0s and 1s."""
    bits = []
    for byte in byte_data:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)
    return bits

def bits_to_bytes(bits):
    """Converts a list of 0s and 1s back into raw bytes."""
    if len(bits) % 8 != 0:
        bits = bits[:-(len(bits) % 8)]
    bytes_list = bytearray()
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        byte_value = 0
        for bit in byte_bits:
            byte_value = (byte_value << 1) | bit
        bytes_list.append(byte_value)
    return bytes(bytes_list)

def get_lattice_parameters():
    print("\n--- Configure Lattice Parameters ---")
    try:
        k = int(input("Enter Dimension K (Standard ML-KEM uses 3): ") or 3)
        q = int(input("Enter Modulus Q (Standard ML-KEM uses 3329): ") or 3329)
        eb = int(input("Enter Error Bound (Standard ML-KEM uses 2): ") or 2)
        return k, q, eb
    except ValueError:
        print("[!] Invalid inputs. Falling back to default ML-KEM standard.")
        return 3, 3329, 2

def get_chunk_size():
    print("\n--- Configure Interpretation Block Size ---")
    try:
        chunk_size = int(input("Enter number of bytes to interpret at once (e.g., 1, 4, 16): ") or 1)
        if chunk_size < 1:
            chunk_size = 1
        return chunk_size
    except ValueError:
        return 1

# --- Operational Modes ---
def handle_encryption():
    print("\n--- ENCRYPTION MODE ---")
    print("1. Encrypt Any File (Binary Mode)")
    print("2. Encrypt Text Input")
    sub_choice = input("Select an option (1-2): ").strip()

    raw_input_bytes = b""
    file_dir, file_base, file_ext = "", "", ""
    is_file = False

    if sub_choice == "1":
        file_path = input("Enter the path to your file: ").strip()
        if not os.path.exists(file_path):
            print("[!] Error: File path does not exist.")
            return
        with open(file_path, "rb") as f:
            raw_input_bytes = f.read()
        file_dir, file_name = os.path.split(file_path)
        file_base, file_ext = os.path.splitext(file_name)
        is_file = True
    elif sub_choice == "2":
        plaintext = input("Enter text string to encrypt: ")
        raw_input_bytes = plaintext.encode('utf-8')
    else:
        print("[!] Invalid option.")
        return

    # Gather Configuration Metrics & Variable Chunk Size
    k, q, eb = get_lattice_parameters()
    chunk_bytes = get_chunk_size()
    
    engine = LatticeEncryptionEngine(k=k, q=q, error_bound=eb)
    print(f"\n[*] Activating Engine on node: {engine.device}")
    A, t, s = engine.keygen()

    # Process data in chunks of specified bytes
    print(f"[*] Processing data stream in {chunk_bytes}-byte blocks...")
    encrypted_stream = []
    
    start_enc = time.perf_counter()
    
    # Loop over the file bytes by the chosen chunk step size
    for i in range(0, len(raw_input_bytes), chunk_bytes):
        chunk = raw_input_bytes[i:i+chunk_bytes]
        chunk_bits = bytes_to_bits(chunk)
        
        block_ciphertexts = []
        for bit in chunk_bits:
            u, v = engine.encrypt(A, t, bit)
            block_ciphertexts.append({"u": u.cpu().tolist(), "v": v.cpu().tolist()})
            
        encrypted_stream.append(block_ciphertexts)

    if engine.device.type == 'cuda':
        torch.cuda.synchronize()
    end_enc = time.perf_counter()

    # Package structure including variable metadata
    payload = {
        "parameters": {"k": k, "q": q, "error_bound": eb},
        "chunk_bytes": chunk_bytes,
        "original_extension": file_ext if is_file else None,
        "secret_key_s": s.cpu().tolist(),
        "ciphertext_blocks": encrypted_stream
    }

    enc_time_ms = (end_enc - start_enc) * 1000
    print(f"[+] Encryption sequence finalized in {enc_time_ms:.2f} ms")

    if is_file:
        output_path = os.path.join(file_dir, f"{file_base}_encrypted.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f)
        print(f"[+] Security payload saved to: {output_path}")
    else:
        print("\n--- ENCRYPTED PAYLOAD ---")
        print(json.dumps(payload)[:500] + "\n... [Truncated]")

def handle_decryption():
    print("\n--- DECRYPTION MODE ---")
    print("1. Decrypt from encrypted JSON file")
    print("2. Decrypt via pasted JSON token string")
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
        raw_json = input("Paste your raw JSON encrypted payload: ").strip()
        try:
            payload_data = json.loads(raw_json)
        except Exception as e:
            print(f"[!] JSON parsing fault: {e}")
            return

    params = payload_data.get("parameters", {})
    chunk_bytes = payload_data.get("chunk_bytes", 1)
    orig_ext = payload_data.get("original_extension", ".bin") or ".bin"
    
    print(f"\n[Metadata Found] Chunk Size: {chunk_bytes} Byte(s) | K: {params.get('k')} | Q: {params.get('q')}")
    
    k, q, eb = params.get('k', 3), params.get('q', 3329), params.get('error_bound', 2)
    engine = LatticeEncryptionEngine(k=k, q=q, error_bound=eb)
    
    s = torch.tensor(payload_data["secret_key_s"], device=engine.device, dtype=torch.float32)
    ciphertext_blocks = payload_data["ciphertext_blocks"]

    print(f"[*] Reconstructing block signatures across hardware registers...")
    all_recovered_bits = []
    
    start_dec = time.perf_counter()
    
    for block in ciphertext_blocks:
        for bit_cipher in block:
            u = torch.tensor(bit_cipher["u"], device=engine.device, dtype=torch.float32)
            v = torch.tensor(bit_cipher["v"], device=engine.device, dtype=torch.float32)
            all_recovered_bits.append(engine.decrypt(s, u, v))
            
    if engine.device.type == 'cuda':
        torch.cuda.synchronize()
    end_dec = time.perf_counter()

    decrypted_bytes = bits_to_bytes(all_recovered_bits)
    dec_time_ms = (end_dec - start_dec) * 1000
    print(f"[+] Decryption sequence finalized in {dec_time_ms:.2f} ms")

    if is_file:
        output_path = os.path.join(file_dir, f"{file_base}_decrypted{orig_ext}")
        with open(output_path, "wb") as f:
            f.write(decrypted_bytes)
        print(f"[+] File recovered natively. Saved to:\n    {output_path}")
    else:
        try:
            print(f"\n[+] Recovered Message Result:\n{decrypted_bytes.decode('utf-8')}\n")
        except UnicodeDecodeError:
            print(f"\n[+] Recovered Binary Hexstream:\n{decrypted_bytes.hex()[:200]}...\n")

def handle_auto_tune():
    print("\n" + "="*70)
    print("      HARDWARE-LIMIT AUTO-TUNING PROFILER")
    print("="*70)
    print("[*] Searching for the largest stable K value...")
    print("[*] Stopping only when latency exceeds 150 μs or hardware fails.\n")

    q_candidates = [3329, 7681, 12289]
    eb_candidates = [2, 3, 4, 5]

    test_iterations = 100
    target_latency_us = 150.0

    results = []

    for q in q_candidates:
        for eb in eb_candidates:

            print(f"\n[-] Testing Q={q} | Error Bound={eb}")

            k_val = 2
            last_valid = None

            while True:

                try:
                    engine = LatticeEncryptionEngine(
                        k=k_val,
                        q=q,
                        error_bound=eb
                    )

                    A, t, s = engine.keygen()

                    # Warm-up
                    for _ in range(10):
                        u, v = engine.encrypt(A, t, 1)
                        engine.decrypt(s, u, v)

                    start_time = time.perf_counter()

                    integrity_passes = 0

                    for i in range(test_iterations):

                        test_bit = i % 2

                        u, v = engine.encrypt(A, t, test_bit)
                        recovered_bit = engine.decrypt(s, u, v)

                        if recovered_bit == test_bit:
                            integrity_passes += 1

                    if engine.device.type == "cuda":
                        torch.cuda.synchronize()

                    end_time = time.perf_counter()

                    latency_us = (
                        ((end_time - start_time) * 1000)
                        / test_iterations
                    ) * 1000

                    integrity_rate = (
                        integrity_passes / test_iterations
                    ) * 100

                    if integrity_rate < 100:
                        print(
                            f"\n    [!] Integrity failure at K={k_val}"
                            f" ({integrity_rate:.1f}%)"
                        )
                        break

                    if latency_us > target_latency_us:
                        print(
                            f"\n    [!] Latency limit reached at "
                            f"K={k_val} ({latency_us:.2f} μs)"
                        )
                        break

                    security_score = ((k_val * eb) / q) * 1000

                    last_valid = {
                        "q": q,
                        "eb": eb,
                        "k": k_val,
                        "latency": latency_us,
                        "score": security_score
                    }

                    print(
                        f"\r    K={k_val:<5} | "
                        f"Latency={latency_us:.2f} μs",
                        end=""
                    )

                    k_val += 1

                except Exception as e:
                    print(
                        f"\n    [!] Hardware limit encountered "
                        f"at K={k_val}: {e}"
                    )
                    break

            if last_valid:
                results.append(last_valid)

    print("\n" + "="*70)
    print("                    PROFILER VERDICT")
    print("="*70)

    if not results:
        print("[!] No valid configurations found.")
        return

    results.sort(key=lambda x: x["k"], reverse=True)

    best = results[0]

    print("MAXIMUM STABLE CONFIGURATION:")
    print(f"  -> Dimension K:    {best['k']}")
    print(f"  -> Modulus Q:      {best['q']}")
    print(f"  -> Error Bound:    {best['eb']}")
    print(f"  -> Latency:        {best['latency']:.2f} μs")
    print(f"  -> Security Score: {best['score']:.2f}")

    print("="*70)
    input("\n[Press Enter to return to the Main Menu...]")

def main():
    while True:
        print("\n" + "="*60)
        print("         MODULAR CHUNK-BASED LATTICE CRYPTO ENGINE")
        print("="*60)
        print("1. Encrypt Data (Any File or String)")
        print("2. Decrypt Data")
        print("3. Run Auto-Tuning Hardware Profiler")
        print("4. Educational Mode: Technical Architecture Breakdown")
        print("5. Exit Engine")
        
        choice = input("\nSelect core operation mode (1-5): ").strip()
        
        if choice == "1":
            handle_encryption()
        elif choice == "2":
            handle_decryption()
        elif choice == "3":
            handle_auto_tune()
        elif choice == "4":
            handle_education_mode()
        elif choice == "5":
            print("[*] De-allocating vectors. Goodbye.")
            break
        else:
            print("[!] Invalid option selection.")

if __name__ == "__main__":
    main()