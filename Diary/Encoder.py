from cryptography.fernet import Fernet
import base64
import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageGrab
import pyperclip
import os
from tqdm import tqdm


def validate_key(key):
    """Check if key is valid (32-byte binary or 44-char Base64)."""
    try:
        if len(key) == 32:
            Fernet(base64.urlsafe_b64encode(key))
            return True
        if len(key) == 44 and all(
                c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_=' for c in key):
            Fernet(key)
            return True
    except:
        pass
    return False


def get_key_from_qr_data(qr_bytes):
    """Extract key from QR data (32-byte binary or Base64)."""
    # Try raw 32-byte key first
    if len(qr_bytes) == 32:
        try:
            Fernet(base64.urlsafe_b64encode(qr_bytes))
            return qr_bytes
        except:
            pass

    # Try Base64 decoding
    try:
        qr_str = qr_bytes.decode('utf-8').strip()
        decoded = base64.urlsafe_b64decode(qr_str)
        if len(decoded) == 32:
            return decoded
    except:
        pass

    return None


def scan_qr_from_camera():
    """Capture QR code from webcam with multi-format support."""
    # Try different camera devices
    for dev in ["/dev/video0", "/dev/video1", 0, 1]:
        try:
            cap = cv2.VideoCapture(dev)
            if cap.isOpened():
                print(f"✅ Using camera device: {dev}")
                break
        except:
            continue
    else:
        print("❌ No working camera found!")
        return None

    print("📷 Looking for QR code (Press Q to cancel)...")
    cv2.namedWindow("QR Scanner", cv2.WINDOW_NORMAL)
    detected_key = None

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("QR Scanner", frame)
            key = cv2.waitKey(1)

            if key in (27, ord('q'), ord('Q')):
                print("⏹ Scanning cancelled")
                break

            decoded = decode(frame)
            if decoded:
                qr_bytes = decoded[0].data
                detected_key = get_key_from_qr_data(qr_bytes)
                if detected_key:
                    break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return detected_key


def get_key_from_clipboard():
    """Get key from clipboard (image/text in any format)."""
    try:
        # Check for image
        img = ImageGrab.grabclipboard()
        if img:
            decoded = decode(img)
            if decoded:
                return get_key_from_qr_data(decoded[0].data)

        # Check for text
        text = pyperclip.paste().strip()
        if text:
            # Try hex (64 characters)
            if len(text) == 64:
                try:
                    return bytes.fromhex(text)
                except:
                    pass
            # Try Base64
            return get_key_from_qr_data(text.encode())
    except Exception as e:
        print(f"⚠️ Clipboard error: {str(e)}")
    return None


def scan_qr_from_file(file_path="key_qr.png"):
    """Read QR from file (supports both formats)."""
    try:
        img = Image.open(file_path)
        decoded = decode(img)
        if decoded:
            return get_key_from_qr_data(decoded[0].data)
    except Exception as e:
        print(f"⚠️ File error: {str(e)}")
    return None


def get_key_manual():
    """Manual entry for both key formats."""
    while True:
        key = input("⌨️ Enter key (44-char Base64 or 64-char hex): ").strip()

        # Try hex format
        if len(key) == 64:
            try:
                return bytes.fromhex(key)
            except:
                print("❌ Invalid hex format!")
                continue

        # Try Base64 format
        if validate_key(key):
            return base64.urlsafe_b64decode(key)

        print("❌ Invalid key format!")


def get_encryption_key():
    """Get key through all available methods."""
    print("\n🔑 Getting encryption key...")

    # Try clipboard first
    key = get_key_from_clipboard()
    if key:
        print("✓ Key from clipboard")
        return key

    # Try camera
    print("No clipboard key. Trying camera...")
    key = scan_qr_from_camera()
    if key:
        print("✓ Key from camera")
        return key

    # Try file
    key = scan_qr_from_file()
    if key:
        print("✓ Key from file")
        return key

    # Manual entry
    return get_key_manual()


def encrypt_file(file_path, cipher):
    """Encrypt file with progress tracking."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()

        encrypted = cipher.encrypt(data)
        with open(file_path + ".enc", "wb") as f:
            f.write(encrypted)

        os.remove(file_path)
        return True
    except Exception as e:
        print(f"❌ Error encrypting {file_path}: {str(e)}")
        return False


def decrypt_file(file_path, cipher):
    """Decrypt file with validation."""
    try:
        if not file_path.endswith(".enc"):
            print(f"⚠️ Decrypting non-.enc file: {file_path}")

        with open(file_path, "rb") as f:
            data = cipher.decrypt(f.read())

        output_path = file_path[:-4] if file_path.endswith(".enc") else file_path + ".dec"
        with open(output_path, "wb") as f:
            f.write(data)

        os.remove(file_path)
        return True
    except Exception as e:
        print(f"❌ Error decrypting {file_path}: {str(e)}")
        return False


def main():
    """Main application flow."""
    action = input("(E)ncrypt or (D)ecrypt? ").strip().lower()
    path = input("File/directory path: ").strip()

    if not os.path.exists(path):
        print("❌ Path not found!")
        return

    key = get_encryption_key()
    cipher = Fernet(base64.urlsafe_b64encode(key))

    if os.path.isdir(path):
        files = []
        for root, _, filenames in os.walk(path):
            for f in filenames:
                full_path = os.path.join(root, f)
                if (action == "e" and not f.endswith(".enc")) or (action == "d" and f.endswith(".enc")):
                    files.append(full_path)

        if not files:
            print("⚠️ No files to process!")
            return

        success = 0
        for file in tqdm(files, desc="Processing", unit="file"):
            if action == "e":
                success += encrypt_file(file, cipher)
            else:
                success += decrypt_file(file, cipher)

        print(f"\n✅ Successfully processed {success}/{len(files)} files")
    else:
        if action == "e":
            encrypt_file(path, cipher)
        elif action == "d":
            decrypt_file(path, cipher)
        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()