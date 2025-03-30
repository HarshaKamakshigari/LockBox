import os
import re
import itertools
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

IV = b"0000000000000000"  # Weak static IV
TEXT_PATTERN = re.compile(rb'[\x20-\x7E]{4,}')  # Detects printable ASCII text

def generate_weak_keys():
    """ Generates weak AES keys (both numeric & alphabetic) """
    # Numeric keys: "0000000000000000" to "9999999999999999"
    for i in range(10):
        yield bytes(str(i) * 16, 'utf-8')

    # Alphabetic keys: "AAAAAAAAAAAAAAAA" to "ZZZZZZZZZZZZZZZZ"
    for letter in "ABCDE":
        yield bytes(letter * 16, 'utf-8')

def brute_force_decrypt(file_path):
    """ Attempts to brute-force decrypt an AES-encrypted file """
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    with open(file_path, "rb") as f:
        encrypted_data = f.read()

    for key in generate_weak_keys():
        try:
            cipher = AES.new(key, AES.MODE_CBC, IV)
            decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

            if TEXT_PATTERN.search(decrypted_data):  # Check for readable content
                decrypted_file_path = file_path.replace(".enc_", ".dec_")
                with open(decrypted_file_path, "wb") as f:
                    f.write(decrypted_data)

                print(f"✅ SUCCESS! Key found: {key.decode()}")
                print(f"🔓 Decrypted file saved as: {decrypted_file_path}")
                return decrypted_file_path

        except Exception:
            pass  # Ignore errors, keep trying

    print("❌ No valid key found. Brute-force failed.")

if __name__ == "__main__":
    file_path = input("Enter the encrypted file path: ").strip()
    brute_force_decrypt(file_path)
