# for now, all in this folder
from repo.Repository import UserManager, GroupManager #serves formatted data...

"""
  Services
    user
      text/media
      basic filter for bad text

      types of impact?
      location impact?

    group
      custom way top sep. qr codes?

"""


class BaseService:
    #TODO // change the logic for permissions... not base in sql obj
    def has_permission(self, obj, permission: str) -> bool:
        return permission in obj.permissions

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
