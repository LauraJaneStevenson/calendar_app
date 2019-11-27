import server
import unittest
import model
import helper_functions


class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes."""
    def setUp(self):
        """Code to run before every test."""

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        server.app.config['SECRET_KEY'] = "123"

        # Connect to test database
        model.connect_to_db(server.app, "postgresql:///testdb")

        # Create tables and add sample data
        model.db.create_all()
        # example_data()

        with self.client as c:
            with c.session_transaction() as session:
                session['user_id'] = 1
                session['username'] = 'j'
                session['name'] = 'l'
                session['cal_id'] = 1

    # def tearDown(self):

    def test_index(self):
        """Make sure homepage page returns correct HTML."""

        # make request to server
        result = self.client.get("/")

        # check that / route renders login page
        self.assertIn(b'<h1>Login:</h1>',result.data)

    def test_register(self):
        """Make sure registration page returns correct HTML."""

        # make request to server
        result = self.client.get("/register")

        # check that / route renders login page
        self.assertIn(b'<h1>Register for Roomies!</h1>',result.data)

    def test_login(self):
        """Test login page."""


        result = self.client.post("/login",
                                  data={"username": "julz", "password": "123"},
                                  follow_redirects=True)
        self.assertIn(b'<p>Your housemates: </p>', result.data)

    # make users without calendar in different class
    # def test_calendar_page(self):
    #     """Test homepage for users without a calendar"""


    #     result = self.client.get("/calendar")

    #     self.assertIn(b'Create New Calendar', result.data)


    def test_add_housemate(self):
        """Test that /add_housemate route processes form data correctly."""

        # make request to server with housemate name mona
        result = self.client.post("/add_housemates", data={'housemate_name':'mona'})
        self.assertIn(b'<h3>Users:</h3>', result.data)

    def test_user_profiles(self):
        """Test that user profiles render correct HTML"""

        result = self.client.get("/profile/1")
        self.assertIn(b'In house:',result.data)

    def test_logout(self):
        """Test that check if logout works correctly"""

        result = self.client.get("/logout_process",follow_redirects=True)
        self.assertIn(b'Login:',result.data)


if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()







