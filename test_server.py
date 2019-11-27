import server
import unittest
import model


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
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    # def tearDown(self):

    def test_index(self):
        """Make sure homepage page returns correct HTML."""

        # create test client
        client = server.app.test_client()

        # make request to server
        result = client.get("/")

        # check that / route renders login page
        self.assertIn(b'<h1>Login:</h1>',result.data)

    def test_register(self):
        """Make sure registration page returns correct HTML."""

        # create test client
        client = server.app.test_client()

        # make request to server
        result = client.get("/register")

        # check that / route renders login page
        self.assertIn(b'<h1>Register for Roomies!</h1>',result.data)

    def test_login(self):
        """Test login page."""


        result = self.client.post("/login",
                                  data={"username": "julz", "password": "123"},
                                  follow_redirects=True)
        self.assertIn(b'<p>Your housemates: </p>', result.data)

    # def test_calendar_page(self):
    #     """Test homepage for users without a calendar"""
    #     # create test client
    #     client = server.app.test_client()

    #     test_user = model.User.query.filter_by(user_id=1).one()

    #     result = client.get("/calendar",data={'user':'test_user'})

    #     self.assertIn('<p>Search for and add housemates: </p>', result.data)


    def test_add_housemate(self):
        """Test that /add_housemate route processes form data correctly."""

        # create test client
        client = server.app.test_client()

        # make request to server with housemate name mona
        result = client.post("/add_housemates", data={'housemate_name':'mona'})
        self.assertIn(b'<h3>Users:</h3>', result.data)

if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()







