from db.DBManager import DatabaseManager

#for now i'll keep the repo just a single repo instead of branching into user, groups... for simple
# i think i can get db_manager in crud and just call the models in crud operations for clearner impl.
class CrudOperations:
        #crud functions
    def create_user(self):
        pass

    def read_user(self):
        pass

    def update_user(self):
        pass

    def delete_user(self):
        pass


# create a user manager which handles the management system for all user
class UserManager(CrudOperations):
    def __init__(self):
      self.db_manager : DatabaseManager = DatabaseManager()


    #boolean oper.
    def is_user_exist_by_username(self, username: str) -> bool:
        """
        Check if a user with the given username already exists in the database.

        :param email: The username to check.
        :return: True if the user exists, False otherwise.
        """
        # session = SessionLocal()
        # try:
        #     # Query the database for a user with the given email
        #     user = session.query(User).filter(User.username == username).first()
        #     return user is not None
        # finally:
        #     session.close()
        pass

    def is_user_exist_by_email(self, email: str) -> bool:
        pass
        """
        Check if a user with the given email already exists in the database.

        :param email: The email to check.
        :return: True if the user exists, False otherwise.
        """
        # session = SessionLocal()
        # try:
        #     # Query the database for a user with the given email
        #     user = session.query(User).filter(User.email == email).first()
        #     return user is not None
        # finally:
        #     session.close()

    #more specific functions to the site
    def get_user_using_binid(self, binid: int):
        pass


# create a user manager which handles the management system for all user
class GroupManager(CrudOperations):
    def __init__(self):
      self.db_manager : DatabaseManager = DatabaseManager()

    def append_user_to_group(self, userid: int , groupid: int):
        pass

    def get_list_of_users(self, groupid: int):
        pass



