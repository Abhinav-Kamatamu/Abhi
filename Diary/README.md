### Instructions to decode Diary

**This is the encrypted file for my diary. You will find the KEY to unlocking this file in my physical diary.**

Here are all the required Python packages you need to install via `pip` for the complete QR code encryption/decryption tool to work:

### **Core Dependencies**
```bash
pip install cryptography opencv-python pyzbar pillow pyperclip
```

### **Detailed Breakdown**

| Library | Purpose | Version |
|---------|---------|---------|
| `cryptography` | Fernet encryption/decryption | >=3.0 |
| `opencv-python` | Webcam access & QR detection | >=4.5 |
| `pyzbar` | QR code decoding | >=0.1.9 |
| `pillow` | Image processing (for clipboard/file QR) | >=9.0 |
| `pyperclip` | Clipboard access (for pasting keys) | >=1.8 |

### **Platform-Specific Notes**

#### **Windows Users**
No additional requirements - the above packages work out-of-the-box.

#### **Mac Users**
```bash
# Additional system dependency for pyzbar
brew install zbar
```

#### **Linux (Debian/Ubuntu)**
```bash
# System dependencies
sudo apt install libzbar0 python3-tk

# For clipboard support (pyperclip)
sudo apt install xclip
```

### **Alternative Installation**
For a single-command install of all components:
```bash
pip install cryptography opencv-python pyzbar pillow pyperclip && \
sudo apt-get install -y libzbar0 xclip  # Linux only
```

### **Verification**
Check installed versions with:
```bash
pip list | grep -E "cryptography|opencv|pyzbar|pillow|pyperclip"
```

This ensures you have all components needed for:
- Webcam QR scanning
- Clipboard key pasting
- File encryption/decryption
- Manual key entry fallback

Let me know if you encounter any platform-specific issues!