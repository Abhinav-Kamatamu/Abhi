import qrcode

data = 'zkcGTqVhTITuVn_tSXdLCtLfmGaPfocEG_wz-DUTz3I='

qr = qrcode.QRCode(
    version=2,  # Force version 7 (supports 32-byte binary)
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=4,
    border=2,
)
qr.add_data(data)  # ← CRITICAL: optimize=0 prevents UTF-8 conversion
qr.make(fit=True)  # ← Must use fit=False with explicit version

img = qr.make_image()
img.save("fixed_qr.png")