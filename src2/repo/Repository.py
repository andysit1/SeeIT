from src2.db.DBManager import DatabaseManager, User, Bin


#for now i'll keep the repo just a single repo instead of branching into user, groups... for simple
# i think i can get db_manager in crud and just call the models in crud operations for clearner impl.


#think of repository as doing the interactions...

class CrudOperations:
    def __init__(self):
      self.db_manager : DatabaseManager = DatabaseManager("sqlite:///test.db")

        #crud functions
    def create_model(self):
        #think of requirements before we create the user...
        # new_user = User()
        self.db_manager.add()

    def update_model(self):
        self.db_manager.update()

    def delete_model(self):
        self.db_manager.delete()



        

# create a user manager which handles the management system for all user
class UserManager(CrudOperations):
    #boolean oper.
    def is_user_exist_by_username(self, username: str) -> bool:
        user_response = self.db_manager.query_first(User, {"username": username})
        return bool(user_response)

    def is_user_exist_by_email(self, email: str) -> bool:
        user_response = self.db_manager.query_first(User, {"email": email})
        return bool(user_response)

    #more specific functions to the site
    def get_user_using_binid(self, binid: int):
        bin_response = self.db_manager.query_first(Bin, {"bin_id": binid})
        userid = bin_response.user_id
        return self.db_manager.query_first(User, {"id": userid})
        # pass


# create a user manager which handles the management system for all user
class GroupManager(CrudOperations):
    def __init__(self):
      self.db_manager : DatabaseManager = DatabaseManager()

    def append_user_to_group(self, userid: int , groupid: int):
        pass

    def get_list_of_users(self, groupid: int):
        pass



