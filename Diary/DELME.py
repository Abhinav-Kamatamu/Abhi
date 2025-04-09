import qrcode

data = b'\xd5\xa4\x99\xdaj\x1eJV\x8d\xd8\x86\xd6\xb8\x05\xac\xeb\xe4\xdf\xf4\xeah\xc3r7\x0c\x1a3\x02\xae\xc6x '

qr = qrcode.QRCode(
    version=7,  # Force version 7 (supports 32-byte binary)
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=4,
    border=2,
)
qr.add_data(data, optimize=0)  # ← CRITICAL: optimize=0 prevents UTF-8 conversion
qr.make(fit=False)  # ← Must use fit=False with explicit version

img = qr.make_image()
img.save("fixed_qr.png")