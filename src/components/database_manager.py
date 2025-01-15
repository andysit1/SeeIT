from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from typing import Callable, TypeVar, Optional, Any

T = TypeVar("T")

class DatabaseManager:
    """
    A class to manage database operations using SQLAlchemy.
    Provides utility methods for common tasks like session management,
    error handling, and CRUD operations.
    """

    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> sessionmaker:
        """Returns a new session object."""
        return self.SessionLocal()


    # uses a design patterns. I cant remember the name..
    def execute_with_session(self, operation: Callable[[Any], T]) -> Optional[T]:
        """
        Executes a database operation within a managed session.

        :param operation: A callable that takes a session and returns a result.
        :return: The result of the operation, or None if an exception occurs.
        """
        session = self.get_session()
        try:
            result = operation(session)
            session.commit()
            return result
        except exc.SQLAlchemyError as e:
            session.rollback()
            print(f"Database operation failed: {e}")
            return None
        finally:
            session.close()

    def add(self, instance: Any) -> bool:
        """
        Adds a new instance to the database.

        :param instance: The instance to add.
        :return: True if successful, False otherwise.
        """
        return self.execute_with_session(lambda session: session.add(instance) or True) is not None

    def delete(self, instance: Any) -> bool:
        """
        Deletes an instance from the database.

        :param instance: The instance to delete.
        :return: True if successful, False otherwise.
        """
        return self.execute_with_session(lambda session: session.delete(instance) or True) is not None

    def query_all(self, model: Any, filter_by: Optional[dict] = None) -> list:
        """
        Queries the database for all instances of a model.

        :param model: The model to query.
        :param filter_by: Optional dictionary of filter criteria.
        :return: A list of results.
        """
        def operation(session):
            query = session.query(model)
            if filter_by:
                query = query.filter_by(**filter_by)
            return query.all()

        return self.execute_with_session(operation) or []

    def query_first(self, model: Any, filter_by: Optional[dict] = None) -> list:
        """
        Queries the database for first instances of a model.

        :param model: The model to query.
        :param filter_by: Optional dictionary of filter criteria.
        :return: A list of results.
        """
        def operation(session):
            query = session.query(model)
            if filter_by:
                query = query.filter_by(**filter_by)
            return query.first()

        return self.execute_with_session(operation) or []

    def get(self, model: Any, **filters) -> Optional[Any]:
        """
        Retrieves a single instance of a model matching the given filters.

        :param model: The model to query.
        :param filters: Filter criteria as keyword arguments.
        :return: The matching instance, or None if not found.
        """
        def operation(session):
            return session.query(model).filter_by(**filters).first()

        return self.execute_with_session(operation)

    def update(self, model: Any, filter_by: dict, update_data: dict) -> bool:
        """
        Updates an instance in the database.

        :param model: The model to update.
        :param filter_by: Dictionary to identify the instance.
        :param update_data: Dictionary of fields to update.
        :return: True if successful, False otherwise.
        """
        def operation(session):
            instance = session.query(model).filter_by(**filter_by).first()
            if not instance:
                return None
            for key, value in update_data.items():
                setattr(instance, key, value)
            return True

        return self.execute_with_session(operation) is not None

# Example usage:
# database_url = "sqlite:///test.db"
# db_manager = DatabaseManager(database_url)

# Define your Base.metadata.create_all(bind=engine) elsewhere for initial setup.

# Add a new user:
# user = User(username="new_user", password="password", email="new_user@example.com")
# db_manager.add(user)

# Query for users:
# users = db_manager.query(User, {"email": "new_user@example.com"})
# print(users)


from database import User, UserResponse
if __name__ == "__main__":
    # Example usage:
    database_url = "sqlite:///test.db"
    db_manager = DatabaseManager(database_url)

    # Add a new user
    # new_user = User(username="Alice", password="alicepass", email="alice@example.com")
    obj = db_manager.query(User, {"username": "Alice"})
    user_response = UserResponse.model_validate(obj=obj, from_attributes=True)
    print(user_response.model_dump_json(indent=4))
