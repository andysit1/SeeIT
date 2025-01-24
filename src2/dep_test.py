from .db.DBManager import DatabaseManager
from .db.UserModels import User, UserResponse

if __name__ == "__main__":


    # Example usage:
    database_url = "sqlite:///test.db"
    db_manager = DatabaseManager(database_url)

    # Add a new user
    new_user = User(username="Alice", password="alicepass", email="alice@example.com")
    obj = db_manager.query(User, {"username": "Alice"})
    user_response = UserResponse.model_validate(obj=obj, from_attributes=True)
    print(user_response.model_dump_json(indent=4))
