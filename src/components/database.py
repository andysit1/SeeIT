


# assume only one bin per person for now
class DB:
  def __init__(self):
    pass

  def is_user_in_database(self, email: str):
    pass

  def create_user(self, email: str, bin_description: str):
    pass

  def add_media(self, email: str):
    pass


class CacheDB(DB):
  def __init__(self):
    super().__init__()
    self.cache = {} # specific parts of the cache?

  def handle_cache(self):
    return


class FireBaseDB(DB):
  def __init__(self):
    super().__init__()

    # credentials...

  #validators...

