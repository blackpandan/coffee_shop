import unittest
import json
from src.api import app
from src.database.models import setup_db, db_drop_and_create_all


class DrinksTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = app.test_client
        self.database_name = "test_database.db"
        setup_db(self.app, self.database_name)
        # db_drop_and_create_all()

    def tearDown(self):
        pass

    def test_get_drinks(self):
        response = self.client().get('/drinks')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("success"), True)
        self.assertIn("drinks", data)


if __name__ == "__main__":
    unittest.main()
