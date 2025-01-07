import firebase_admin
from firebase_admin import credentials, auth

#Base functions, needs verification and authentication with tokens but for now it's okay!
class FirebaseAuthFacade:
    def __init__(self, credentials_path: str):
        """
        Initializes the Firebase app with the given credentials.
        """
        cred = credentials.Certificate(credentials_path)
        firebase_admin.initialize_app(cred)
        print("Firebase Auth initialized.")

    def create_user(self, email: str, password: str):
        """
        Creates a new user with the given email and password.
        """
        try:
            user = auth.create_user(email=email, password=password)
            print(f"User {email} created with UID: {user.uid}")
            return user
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def get_user_by_email(self, email: str):
        """
        Retrieves a user by email.
        """
        try:
            user = auth.get_user_by_email(email)
            print(f"User retrieved: {user.email} (UID: {user.uid})")
            return user
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None

    def get_user_by_uid(self, uid: str):
        """
        Retrieves a user by UID.
        """
        try:
            user = auth.get_user(uid)
            print(f"User retrieved: {user.email} (UID: {uid})")
            return user
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None

    def delete_user(self, uid: str):
        """
        Deletes a user by UID.
        """
        try:
            auth.delete_user(uid)
            print(f"User with UID {uid} deleted.")
        except Exception as e:
            print(f"Error deleting user: {e}")

    def update_user(self, uid: str, email: str = None, password: str = None, display_name: str = None):
        """
        Updates user information. Pass only the fields you want to update.
        """
        try:
            user = auth.update_user(
                uid,
                email=email,
                password=password,
                display_name=display_name,
            )
            print(f"User with UID {uid} updated: {user.email}")
            return user
        except Exception as e:
            print(f"Error updating user: {e}")
            return None

# Example Usage
if __name__ == "__main__":
    # Initialize facade with your credentials
    facade = FirebaseAuthFacade(r"E:\projects\2024\SeeIt\src\serviceAccountKey.json")

    # Create a user
    new_user = facade.create_user("testuser@example.com", "securepassword123")

    # Retrieve user by email
    if new_user:
        retrieved_user = facade.get_user_by_email("testuser@example.com")

    # Update user (if needed)
    if retrieved_user:
        facade.update_user(retrieved_user.uid, display_name="Test User")

    # # Delete the user
    # if retrieved_user:
    #     facade.delete_user(retrieved_user.uid)
