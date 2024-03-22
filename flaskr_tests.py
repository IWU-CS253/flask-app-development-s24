import os
import app as flaskr
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def test_messages(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
        assert b'A category' in rv.data

    def test_delete(self):
        # Add an entry
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)

        entry_id = id(rv)
        rv_delete = self.app.post('/delete', data=dict(
            id=id
        ), follow_redirects=True)

        assert b'Test Entry' not in rv_delete.data
        assert b'This is a test entry' not in rv_delete.data
        assert b'Test Category' not in rv_delete.data
        assert b'Entry deleted successfully' in rv_delete.data
        rv_delete_last_again = self.app.post('/delete', data=dict(
            id=entry_id
        ), follow_redirects=True)
        assert b'No entries found' in rv_delete_last_again


    def test_update_entry(self):
        # Add an entry
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)

        entry_id = id(rv)
        # Update the added entry
        updated_data = {
            'id': entry_id,
            'title': 'Updated Title',
            'text': 'Updated Text',
            'category': 'Updated Category'
        }
        rv_update = self.app.post('/update', data=updated_data, follow_redirects=True)

        # Check if the entry is successfully updated
        assert b'Entry updated successfully' in rv_update.data

    # def test_update_redir(self):
    #     # Add an entry to the database
    #     rv_add = self.app.post('/add', data=dict(
    #         title='<Hello>',
    #         text='<strong>HTML</strong> allowed here',
    #         category='A category'
    #     ), follow_redirects=True)
    #
    #     # Retrieve the entry ID from the response content
    #     entry_id = id(rv_add)  # You need to implement this function to extract the entry ID
    #
    #     # Simulate visiting the /update-redir route with the retrieved entry ID
    #     rv_redir = self.app.get(f'/update-redir?id={entry_id}', follow_redirects=False)
    #
    #     # Check if the response status code is a redirection status code (302)
    #     assert rv_redir.status_code == 302
    #
    #     # Check if the redirection URL is correct
    #     expected_url = f'http://localhost/update?id={entry_id}'  # Replace 'localhost' with the actual base URL of your application
    #     assert rv_redir.headers['Location'] == expected_url




if __name__ == '__main__':
    unittest.main()
