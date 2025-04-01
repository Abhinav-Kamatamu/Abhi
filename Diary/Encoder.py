from cryptography.fernet import Fernet
import base64
import sys
from tqdm import tqdm  # For progress bar (install with pip install tqdm)
import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageGrab
import pyperclip
import os


def validate_key(key):
    """Check if key is valid (44-char URL-safe Base64)."""
    try:
        if len(key) == 44 and all(
                c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_=' for c in key):
            base64.urlsafe_b64decode(key)
            return True
    except:
        pass
    return False


def get_key_from_qr_data(qr_data):
    """Extract and validate key from QR data."""
    qr_data = qr_data.strip()
    if validate_key(qr_data):
        return base64.urlsafe_b64decode(qr_data)
    return None


def scan_qr_from_camera():
    """Capture QR code from webcam with guaranteed 'Q' key exit."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open camera!")
        return None

    print("📷 Looking for QR in camera (Press 'Q' to skip)...")

    # Create window first and force focus
    cv2.namedWindow("QR Scanner", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("QR Scanner", 800, 600)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Could not read from camera!")
            break

        # Show the frame
        cv2.imshow("QR Scanner", frame)

        # MUST use waitKey for proper event processing
        key = cv2.waitKey(1)

        # Check for ESC or Q key (ASCII 27 or 113/81)
        if key in (27, ord('q'), ord('Q')):
            print("⏹ Camera scanning cancelled by user")
            break

        # Check for QR codes
        decoded = decode(frame)
        if decoded:
            try:
                qr_data = decoded[0].data.decode('utf-8')
                key = get_key_from_qr_data(qr_data)
                if key:
                    break
            except Exception as e:
                print(f"⚠️ QR decode error: {str(e)}")
                continue

    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    # Ensure all windows are closed
    for i in range(5):
        cv2.waitKey(1)
    return key if 'key' in locals() else None

def get_key_from_clipboard():
    """Extract key from clipboard (image or text)."""
    try:
        # Check for image in clipboard
        img = ImageGrab.grabclipboard()
        if img:
            decoded = decode(img)
            if decoded:
                qr_data = decoded[0].data.decode('utf-8')
                return get_key_from_qr_data(qr_data)

        # Check for text in clipboard
        text = pyperclip.paste().strip()
        return get_key_from_qr_data(text)
    except:
        return None


def scan_qr_from_file(file_path="key_qr.png"):
    """Read QR from image file."""
    try:
        img = Image.open(file_path)
        decoded = decode(img)
        if decoded:
            qr_data = decoded[0].data.decode('utf-8')
            return get_key_from_qr_data(qr_data)
    except:
        return None


def get_key_manual():
    """Fallback: Manual key entry."""
    while True:
        key = input("⌨️ Enter 44-character key manually: ").strip()
        if validate_key(key):
            return base64.urlsafe_b64decode(key)
        print("❌ Invalid key (must be 44 chars, URL-safe Base64)")


def get_encryption_key():
    """Get key from QR (webcam/image), clipboard, or manual input."""
    print("\n🔑 Getting encryption key...")

    # 1. Try clipboard first (quickest if available)
    key = get_key_from_clipboard()
    if key:
        print("✓ Key found in clipboard")
        return key

    # 2. Try scanning QR from webcam
    print("No key in clipboard. Trying camera...")
    key = scan_qr_from_camera()
    if key:
        print("✓ Key scanned from camera")
        return key

    # 3. Try reading QR from file
    key = scan_qr_from_file()
    if key:
        print("✓ Key loaded from QR file")
        return key

    # 4. Fallback to manual entry
    return get_key_manual()


def encrypt_file(file_name, cipher):
    """Encrypt file and save with .enc extension."""
    try:
        with open(file_name, "rb") as file:
            encrypted = cipher.encrypt(file.read())

        encrypted_name = file_name + ".enc"
        with open(encrypted_name, "wb") as file:
            file.write(encrypted)

        os.remove(file_name)
        print(f"🔐 Encrypted: {file_name} → {encrypted_name}")
        return True
    except Exception as e:
        print(f"❌ Encryption failed: {str(e)}")
        return False


def decrypt_file(file_name, cipher):
    """Decrypt .enc file and remove extension."""
    try:
        if not file_name.endswith(".enc"):
            print("⚠️ Warning: Trying to decrypt non-.enc file")

        with open(file_name, "rb") as file:
            decrypted = cipher.decrypt(file.read())

        original_name = file_name[:-4]  # Safer extension removal
        with open(original_name, "wb") as file:
            file.write(decrypted)

        os.remove(file_name)
        print(f"🔓 Decrypted: {file_name} → {original_name}")
        return True
    except Exception as e:
        print(f"❌ Decryption failed: {str(e)}")
        return False


def main():
    """Main program flow."""
    action = input("(E)ncrypt or (D)ecrypt? ").strip().lower()
    path = input("File or directory path: ").strip()

    if not os.path.exists(path):
        print("❌ Path not found!")
        return

    key = get_encryption_key()
    cipher = Fernet(base64.urlsafe_b64encode(key))

    if os.path.isdir(path):
        # Build file list first for accurate progress tracking
        target_files = []
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if (action == "e" and not file_path.endswith(".enc")) or \
                        (action == "d" and file_path.endswith(".enc")):
                    target_files.append(file_path)

        if not target_files:
            print("⚠️ No matching files found!")
            return

        # Process files with progress bar
        success_count = 0
        progress_desc = "Encrypting" if action == "e" else "Decrypting"

        for file_path in tqdm(target_files,
                              desc=progress_desc,
                              unit="file",
                              colour='green' if action == 'e' else 'blue'):
            if action == "e":
                success_count += encrypt_file(file_path, cipher)
            else:
                success_count += decrypt_file(file_path, cipher)

        print(f"\n{'🔐' if action == 'e' else '🔓'} "
              f"Processed {success_count}/{len(target_files)} files successfully!")

    else:  # Single file processing
        if action == "e":
            encrypt_file(path, cipher)
        elif action == "d":
            decrypt_file(path, cipher)
        else:
            print("❌ Invalid choice! Use 'E' or 'D'.")


if __name__ == "__main__":
    main()