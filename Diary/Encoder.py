from cryptography.fernet import Fernet
import base64
import os

os.environ['GST_DEBUG'] = '0'
import cv2
from pyzbar.pyzbar import decode
# ---
import subprocess
# ---
from PIL import Image, ImageGrab
import pyperclip
from tqdm import tqdm
import platform


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
    """Scan QR codes containing either:
    - Raw 32-byte Fernet key (for compact QR)
    - 44-character URL-safe base64 Fernet key (human-readable)
    """

    os_type =  platform.system()

    # Determine appropriate backend
    if os_type == "Linux":
        backends = [cv2.CAP_V4L2]
    elif os_type == "Windows":
        backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
    else:
        backends = [cv2.CAP_ANY]

    # Initialize camera (same as before)

    # Try devices 0 through 2 with available backends
    for dev in [0, 1, 2]:
        for backend in backends:
            cap = cv2.VideoCapture(dev, backend)
            if cap.isOpened():
                print(f"✅ Using camera device: {dev} with backend: {backend}")
                break
        else:
            continue
        break
    else:
        print("❌ No working camera found!")
        return None

    print("📷 Looking for QR code (Press Q to cancel)...")
    cv2.namedWindow("QR Scanner", cv2.WINDOW_NORMAL)

    # Auto-size the window to the actual camera resolution
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cv2.resizeWindow("QR Scanner", width, height)

    detected_key = None

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("QR Scanner", frame)
            if cv2.waitKey(1) in (27, ord('q'), ord('Q')):
                print("⏹ Scanning cancelled")
                break

            decoded = decode(frame)
            if not decoded:
                continue

            qr_data = decoded[0].data

            # Handle both bytes and string responses
            try:
                # First attempt to decode as UTF-8 (common implicit conversion)
                raw_data = qr_data.encode('latin1')  # Get raw bytes regardless of type
                if len(raw_data) != 32:
                    # If length mismatch, try direct bytes access
                    raw_data = bytes(qr_data)  # Alternative access for binary data
            except:
                raw_data = bytes(qr_data)

            # Case 1: 32 raw bytes → Convert to Fernet key
            if len(raw_data) == 32:
                detected_key = base64.urlsafe_b64encode(raw_data).decode('utf-8')
                print(
                    "✅ Detected 32-byte key → Fernet key")  # Ask to print detected_key if you want to see what the 44-char key is
                break

            # Case 2: 44-character base64 → Validate as Fernet key
            elif len(raw_data) == 44:
                try:
                    # Ensure it's valid base64 and 32 bytes when decoded
                    decoded_bytes = base64.urlsafe_b64decode(raw_data)
                    if len(decoded_bytes) == 32:
                        detected_key = raw_data.decode('utf-8')
                        print("✅ Detected valid 44-char Fernet key.")
                        break
                    else:
                        print(f"⚠️ Base64 decoded to {len(decoded_bytes)} bytes (expected 32)")
                except:
                    print("⚠️ Invalid base64 encoding")

            else:
                print(f"⚠️ Unsupported data length: {len(raw_data)} bytes")

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


def get_file_path():
    choice = input('Would you want folder (f) or document (d)? ').strip().lower()
    home_dir = os.path.expanduser("~")

    if choice == 'f':
        result = subprocess.run(
            ['zenity', '--file-selection', '--directory', f'--filename={home_dir}/'],
            stdout=subprocess.PIPE
        )
        folder_path = result.stdout.decode().strip()
        print("You selected:", folder_path)
        return folder_path

    elif choice == 'd':
        result = subprocess.run(
            ['zenity', '--file-selection', f'--filename={home_dir}/'],
            stdout=subprocess.PIPE
        )
        file_path = result.stdout.decode().strip()
        print("You selected:", file_path)
        return file_path

    else:
        print("Invalid choice. Please enter 'f' or 'd'.")
        return None


def main():
    """Main application flow."""
    action = input("(E)ncrypt or (D)ecrypt? ").strip().lower()
    path = input("File/directory path: ").strip()
    #path = get_file_path()
    if not os.path.exists(path):
        print("❌ Path not found!")
        return

    key = get_encryption_key()
    try:
        cipher = Fernet(key)
    except:
        pass

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
