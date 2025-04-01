from cryptography.fernet import Fernet
import base64
import sys
from tqdm import tqdm
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

def get_key_from_qr_data(qr_bytes):
    """Extract and validate key from QR data (either format)."""
    # Try raw 32-byte binary first
    if len(qr_bytes) == 32:
        return qr_bytes
    
    # Try Base64 encoded string
    try:
        qr_str = qr_bytes.decode('utf-8').strip()
        if validate_key(qr_str):
            return base64.urlsafe_b64decode(qr_str)
    except:
        pass
    
    return None

def scan_qr_from_camera():
    """Camera scanner with better Linux device handling"""
    print("🔄 Initializing camera...")

    # Try common video devices
    for dev in ["/dev/video0", "/dev/video1", "/dev/video2"]:
        try:
            cap = cv2.VideoCapture(dev, cv2.CAP_V4L2)
            if cap.isOpened():
                print(f"✅ Using camera device: {dev}")
                break
        except:
            continue

    if not cap or not cap.isOpened():
        print("❌ No working camera found!")
        print("Try these fixes:")
        print("1. Run: sudo usermod -a -G video $USER")
        print("2. Reboot after running above command")
        print("3. Test camera with: guvcview")
        return None

    # Rest of camera scanning code...

    print("🔍 Looking for QR code... (Press Q to cancel)")
    cv2.namedWindow("QR Scanner", cv2.WINDOW_NORMAL)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Couldn't receive frame from camera")
                break

            # Show frame with QR detection area
            cv2.imshow("QR Scanner", frame)

            # Try decoding both color and grayscale versions
            decoded = decode(frame) or decode(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

            if decoded:
                print("🎯 QR Code Detected! Processing...")
                qr_bytes = decoded[0].data
                key = get_key_from_qr_data(qr_bytes)
                if key:
                    break

            # Exit on Q press
            if cv2.waitKey(1) in [ord('q'), ord('Q')]:
                print("⏹ User cancelled scanning")
                break

    except Exception as e:
        print(f"🚨 Camera error: {str(e)}")
        return None

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("🛑 Camera released")

    return key if 'key' in locals() else None

def get_key_from_clipboard():
    """Extract key from clipboard (supports both formats)."""
    try:
        # Check for image in clipboard
        img = ImageGrab.grabclipboard()
        if img:
            decoded = decode(img)
            if decoded:
                return get_key_from_qr_data(decoded[0].data)

        # Check for text in clipboard (either format)
        text = pyperclip.paste().strip()
        if text:
            # Try raw bytes if pasted as hex string
            if len(text) == 64 and all(c in '0123456789abcdefABCDEF' for c in text):
                try:
                    return bytes.fromhex(text)
                except:
                    pass
            # Try Base64 encoded string
            return get_key_from_qr_data(text.encode('utf-8'))
    except Exception as e:
        print(f"⚠️ Clipboard error: {str(e)}")
    return None

def scan_qr_from_file(file_path="key_qr.png"):
    """Read QR from image file (supports both formats)."""
    try:
        img = Image.open(file_path)
        decoded = decode(img)
        if decoded:
            return get_key_from_qr_data(decoded[0].data)
    except Exception as e:
        print(f"⚠️ File error: {str(e)}")
    return None

# Rest of the functions remain the same as in your original code
# (get_key_manual, get_encryption_key, encrypt_file, decrypt_file, main)

def get_key_manual():
    """Fallback: Manual key entry."""
    while True:
        key = input("⌨️ Enter key (44-char Base64 or 64-char hex): ").strip()
        
        # Try hex format first
        if len(key) == 64:
            try:
                return bytes.fromhex(key)
            except:
                print("❌ Invalid hex format!")
                continue
                
        # Try Base64 format
        if validate_key(key):
            return base64.urlsafe_b64decode(key)
        
        print("❌ Invalid key (must be 44-char Base64 or 64-char hex)")

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
