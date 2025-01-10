
import pyqrcode
import io
import requests


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

def generate_user_id():
  url = "https://www.random.org/strings/?num=1&len=15&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new"
  response = requests.get(url)

  if response.status_code == 200:
      response = response.text.strip()
  return response

def generate_bin_id():
  url = "https://www.random.org/strings/?num=1&len=5&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new"
  response = requests.get(url)

  if response.status_code == 200:
      response = response.text.strip()
  return response

# if __name__ == "__main__":
#     print(generate_bin_id())
#     print(generate_user_id())
