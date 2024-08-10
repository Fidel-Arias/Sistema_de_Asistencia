from django.shortcuts import render
import qrcode
import json
# Create your views here.

data = {
    'AP_PATERNO': 'HERRERA',
    'AP_MATERNO': 'HERRERA',
    'CORREO': 'piero.herrera@ucsm.edu.pe',
    'CONGRESO': 5
}

json_data = json.dumps(data)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(json_data)
qr.make(fit=True)

img = qr.make_image(fill_color='black', back_color='white')

#save img
file_path = "tipoDocumento/qr_code.png"
img.save(file_path)

file_path