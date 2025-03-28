from cryptography.fernet import Fernet
import os
import base64

# Function to get a user-defined Base64 key
def get_user_key():
    while True:
        key = input("Enter your 44-character Base64 encryption key: ").strip()
        if len(key) == 44:
            try:
                return base64.urlsafe_b64decode(key)  # Convert from Base64
            except Exception:
                print("❌ Invalid Base64 key! Try again.")
        else:
            print("❌ Key must be exactly 44 characters long!")

# Encrypt function
def encrypt_file(file_name):
    key = Fernet.generate_key()  # Generate a valid key
    print(f"🔑 Your encryption key (SAVE THIS SAFELY!): {key.decode()}")

    cipher = Fernet(key)

    with open(file_name, "rb") as file:
        file_data = file.read()

    encrypted_data = cipher.encrypt(file_data)

    with open(file_name + ".enc", "wb") as file:
        file.write(encrypted_data)

    os.remove(file_name)
    print(f"🔐 Encrypted: {file_name} → {file_name}.enc")
    print("⚠️ REMEMBER YOUR KEY! Without it, you can't decrypt!")

# Decrypt function
def decrypt_file(file_name):
    key = get_user_key()
    cipher = Fernet(base64.urlsafe_b64encode(key))  # Convert back to valid key

    try:
        with open(file_name, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = cipher.decrypt(encrypted_data)
        original_name = file_name.replace(".enc", "")

        with open(original_name, "wb") as file:
            file.write(decrypted_data)

        os.remove(file_name)
        print(f"🔓 Decrypted: {file_name} → {original_name}")
    except Exception:
        print("❌ Decryption failed. Incorrect key!")

# Ask user for action
if __name__ == "__main__":
    action = input("Do you want to (E)ncrypt or (D)ecrypt a file? ").strip().lower()
    file_name = input("Enter the file name: ").strip()

    if action == "e":
        encrypt_file(file_name)
    elif action == "d":
        decrypt_file(file_name)
    else:
        print("❌ Invalid choice! Use 'E' for encrypt or 'D' for decrypt.")
