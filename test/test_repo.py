# ai , gotta write my own / review unittest
import unittest
from unittest.mock import MagicMock
from src2.db.DBManager import DatabaseManager, User, Bin
from src2.repo.Repository import CrudOperations, UserManager

class TestCrudOperations(unittest.TestCase):
    def setUp(self):
        self.db_manager_mock = MagicMock(spec=DatabaseManager)
        self.crud = CrudOperations()
        self.crud.db_manager = self.db_manager_mock

    def test_create_user(self):
        self.crud.create_user()
        self.db_manager_mock.add.assert_called_once()

    def test_update_user(self):
        self.crud.update_user()
        self.db_manager_mock.update.assert_called_once()

    def test_delete_user(self):
        self.crud.delete_user()
        self.db_manager_mock.delete.assert_called_once()

class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.db_manager_mock = MagicMock(spec=DatabaseManager)
        self.user_manager = UserManager()
        self.user_manager.db_manager = self.db_manager_mock

    def test_is_user_exist_by_username(self):
        self.db_manager_mock.query_first.return_value = User(username="test_user")
        self.assertTrue(self.user_manager.is_user_exist_by_username("test_user"))

        self.db_manager_mock.query_first.return_value = None
        self.assertFalse(self.user_manager.is_user_exist_by_username("nonexistent_user"))

    def test_is_user_exist_by_email(self):
        self.db_manager_mock.query_first.return_value = User(email="test@example.com")
        self.assertTrue(self.user_manager.is_user_exist_by_email("test@example.com"))

        self.db_manager_mock.query_first.return_value = None
        self.assertFalse(self.user_manager.is_user_exist_by_email("noemail@example.com"))

    def test_get_user_using_binid(self):
        mock_bin = MagicMock()
        mock_bin.user_id = 1
        mock_user = MagicMock()

        self.db_manager_mock.query_first.side_effect = [mock_bin, mock_user]
        result = self.user_manager.get_user_using_binid(100)

        self.db_manager_mock.query_first.assert_any_call(Bin, {"bin_id": 100})
        self.db_manager_mock.query_first.assert_any_call(User, {"id": mock_bin.user_id})
        self.assertEqual(result, mock_user)

if __name__ == "__main__":
    unittest.main()


