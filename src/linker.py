import pyqrcode
# will represent the data logic
# class QRGENERATOR:
if __name__ == "__main__":
  url = pyqrcode.create('http://uca.edu')
  print(url.terminal())
  # with open('code.png', 'w') as fstream:
    # url.png(fstream, scale=5)

