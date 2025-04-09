from pyzbar.pyzbar import decode
from PIL import Image
import hashlib

original_data = b'\xd5\xa4\x99\xdaj\x1eJV\x8d\xd8\x86\xd6\xb8\x05\xac\xeb\xe4\xdf\xf4\xeah\xc3r7\x0c\x1a3\x02\xae\xc6x '

def verify_qr(file_path):
    # Read QR code
    decoded = decode(Image.open(file_path))
    if not decoded:
        print("❌ No QR code found")
        return

    # Get raw bytes
    qr_bytes = decoded[0].data

    # Verification check
    print("QR contains:", qr_bytes)
    print("Length:", len(qr_bytes))
    print("SHA-256:", hashlib.sha256(qr_bytes).hexdigest())

    if qr_bytes == original_data:
        print("✅ Exact binary match!")
    else:
        print("❌ Data mismatch!")


verify_qr("debug_qr.png")