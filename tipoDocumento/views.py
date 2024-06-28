from django.shortcuts import render
import qrcode
import json
# Create your views here.

data={
    'name':'Fidel',
    'apellido':'Arias',
    'cedula':'123456789',
    'telefono':'3123456789',
    'email':'fidel@gmail.com',
    'direccion':'Carrera 123 # 456, Barrio San Francisco'
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