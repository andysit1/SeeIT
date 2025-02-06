# this file represents the lower level db interactions...

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from typing import Callable, TypeVar, Optional, Any
from src2.db.UserModels import User, UserResponse, Media, MediaResponse, Bin, BinResponse

T = TypeVar("T")
import logging

class DatabaseManager:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.logger = logging.getLogger(__name__)

        self.model_response = {
            User : UserResponse,
            Bin : BinResponse,
            Media : MediaResponse
        }

    def get_session(self) -> sessionmaker:
        return self.SessionLocal()

    def execute_with_session(self, operation: Callable[[Any], T]) -> Optional[T]:
        session = self.get_session()
        try:
            result = operation(session)
            session.commit()
            return result
        except exc.SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database operation failed: {e}")
            return None
        finally:
            session.close()

    def add(self, instance: Any) -> bool:
        return bool(self.execute_with_session(lambda session: (session.add(instance), True)[1]))

    def delete(self, instance: Any) -> bool:
        return bool(self.execute_with_session(lambda session: (session.delete(instance), True)[1]))



    # more specific functions

    def query_all(self, model: Any, filter_by: Optional[dict] = None) -> list:
        def operation(session):
            query = session.query(model)
            if filter_by:
                query = query.filter_by(**filter_by)
            return query.all()
        return self.execute_with_session(operation) or []


    #main query choice
    def query_first(self, model: Any, filter_by: Optional[dict] = None) -> Optional[Any]:
        def operation(session):
            query = session.query(model)
            if filter_by:
                query = query.filter_by(**filter_by)

            obj = query.first()

            try:
                if obj:
                    response = self.model_response[type(obj)].model_validate(obj=obj, from_attributes=True)
                return response
            except Exception as e:
                print(f"Validation failed: {e}")

        return self.execute_with_session(operation)

    def update(self, model: Any, filter_by: dict, update_data: dict) -> bool:
        def operation(session):
            instance = session.query(model).filter_by(**filter_by).first()
            if not instance:
                return False
            for key, value in update_data.items():
                setattr(instance, key, value)
            return True
        return bool(self.execute_with_session(operation))
