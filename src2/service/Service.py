# for now, all in this folder
from repo.Repository import UserManager, GroupManager #serves formatted data...

"""
  How codes are associated with an organization



  Services
    user -> easy per use pr code
      text/media
      basic filter for bad text

      types of impact?
      location impact?

    group -> how do we sep an organization codes?
      we want people in an organization to have codes
      we want codes to be spread per code

      location -> place
      email -> funding
      not every funding is in the same quantity
      funding per child



       custom way top sep. qr codes?

"""


class BaseService:
    #TODO // change the logic for permissions... not base in sql obj
    def has_permission(self, obj, permission: str) -> bool:
        return permission in obj.permissions

    #profanity checker
    def is_bad():
       pass

    #given binid over userid i think
    def add_media_to_bin(self, binid: int):
       pass

    def add_media_to_user(self, userid: int):
       pass

    def pull_media(self, binid):
       #later implement cause we dont want to pull all media randomly.. infact it should be user blocked
       pass

class UserService(BaseService):
  def __init__(self):
     super().__init__()
     self.user_manager : UserManager = UserManager()
    # pass  # User-specific logic

  def add_media_to_user(self, userid: int):
    # profanity checker https://lubna2004.medium.com/profanity-to-be-or-not-to-be-dd32d53648f7#:~:text=censor%20method%20is%20used%20to,library%20is%20profanity%2Dfilter%201.3.

    #  if self.user_manager.is_user_exist_by_email():
     pass

  # def


class GroupService(BaseService):
    def __init__(self):
       super().__init__()

    def add_user_to_group_id(self):
      pass  # Group-specific logic
