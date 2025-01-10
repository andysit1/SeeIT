from database import *

# This file handles the communication between db, qr and more.
# Note
  # should really only handle movement of data, from db - users or user -> db
  # Auth will be handled in auth folder

# Note 2
  # might be better to just keep it as functions since Im not really using any type of inheritance

class ManagerSingleton:
    _instance = None  # Class-level attribute to store the single instance

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to control instance creation.
        If an instance already exists, return it; otherwise, create one.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, *args, **kwargs):
        """
        Internal initialization method for the singleton instance.
        This method is called only once for the singleton.
        """
        self.data = {}  # Example attribute to hold shared state

    def get_value(self, key):
        """Retrieve a value from the shared data."""
        return self.data.get(key)

    def set_value(self, key, value):
        """Set a value in the shared data."""
        self.data[key] = value


    def create_media_in_bin_id(self, bin_id, media : list):
        try:
          bin_response : BinResponse = fetch_bin_with_media(bin_id=bin_id)
          if bin_response:
            add_more_media_to_bin(bin_id=bin_id, new_media_items=media)
        except:
           print(f"Error saving media to bin_id {bin_id}")

    #requires user to make bin
    def create_bin(self, user_id):
        session = SessionLocal()

        try:
          user_response : UserResponse = get_user(user_id=user_id)
          if user_response:
            # Create a bin associated with the user
            new_bin = Bin(description="User's Bin", bin_id=101, link="http://example.com", user_id=user_response.id)
            session.add(new_bin)
            session.commit()

        finally:
            session.close()



if __name__ == "__main__":
  pass





