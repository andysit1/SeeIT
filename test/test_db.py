from src2.db.DBManager import DatabaseManager
from src2.db.UserModels import User

if __name__ == "__main__":
    # i think we should make this a singleton and have this in the init run time.
    # ask chatgpt after.
    # Example usage:
    database_url = "sqlite:///test.db"
    db_manager = DatabaseManager(database_url)
    # Add a new user
    new_user = User(username="Alice2", password="alicepass", email="alice2@example.com")
    # db_manager.add(new_user)
    user_response = db_manager.query_first(User, {"username": "Alice2"})
    print(user_response)