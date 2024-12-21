from datetime import datetime
from models.data_model import BinModel, TextMediaDecorator, Media
import firebase_admin
import pyqrcode

# could abstract into CacheDB vs FireBaseDB -> shall see when needed...
class DB:
  def __init__(self):
    self.email_to_model = {}

  def is_user_in_database(self, email : str):
    try:
      if self.email_to_model[email]:
        return True
    except:
      return False

  def get_user(self, email :str) -> BinModel:
    return self.email_to_model[email]

  def create_user(self, email: str, bin_description : str):
    #validation

    if not self.is_user_in_database(email=email):
      print(f"Saving email {email} into database")
      self.email_to_model[email] = BinModel(
        description=bin_description,
        bin_id=1,
        link=f"localhost:8000/{1}",
        bin_content=[]
      )


  def add_media(self, email: str, content: str):
    media= Media(
      date=datetime.now()
    )
    #base on content, wrap it in certain classes
    media = TextMediaDecorator(
      date=media.date,
      wrap_media=media,
      txt_content=content
    )

    self.email_to_model[email].bin_content.append(media) #probably abstract this into model logic... to validate
    print(f"Created Media Model: {media}")

class QRGenerator:
  def __init__(self):
    self.qr_cache = {}

  def is_qr_cached(self, email: str) -> bool:
    try:
      if self.qr_cache[email]:
        return True
    except:
      return False

  def build_qr(self, email: str, link: str):
    if self.is_qr_cached(email=email):
      return self.qr_cache[email]

    #other wise, make new qr code.
    path = f'E:\\projects\\2024\SeeIt\\cache\\{email}QR'
    url=pyqrcode.create(link)
    url.png(path, scale=10)

    self.qr_cache[email] = path
    print(f"Cached qr to {path}")


class Manager:
  def __init__(self):
    self.db : DB = DB()
    self.qr_builder : QRGenerator = QRGenerator()

  def create_user_and_return_qr_code(self, email: str, bin_description : str):
    #create user
    self.db.create_user(
      email=email,
      bin_description=bin_description
    )

    #if make qr code and put in cache
    if self.db.is_user_in_database(email=email):
      bin_model = self.db.get_user(email=email)
      self.qr_builder.build_qr(
        email=email,
        link=bin_model.link
      )
    else:
      print("Error in create_user(), not saving into DB.")

if __name__ == "__main__":

  """
    Inputs: andysit173@gmail.com
    NameDescription: "Andy's First Bin!"

    Someone wants to create a quick QR code...
    this give email.
      this should receive emails about thanks
  """
  manager = Manager()
  manager.create_user_and_return_qr_code(
    email="andysit173@gmail.com",
    bin_description="my first bin"
    )
