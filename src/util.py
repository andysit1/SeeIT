
import pyqrcode
import io

#create randomizer id...
def next_bin_id():
    pass


#look into this function since buffer may not work intendedly with an async backend
def gen_qr_code(link : str):
    qr_code = pyqrcode.create(link)
    buffer = io.BytesIO()
    qr_code.png(buffer, scale=5)
    buffer.seek(0)
    return buffer
