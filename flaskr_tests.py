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
        assert b'Updated Title' in rv_update.data
        assert b'Updated Text' in rv_update.data
        assert b'Updated Category' in rv_update.data
        assert b'Entry updated successfully' in rv_update.data


    def test_update_redir_after_adding_entry(self):
        # Add an entry
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)

        entry_id = id(rv)
        rv_update_redir = self.app.get(f'/update-redir?id={entry_id}', follow_redirects=False)

        assert rv_update_redir.status_code == 302  # 302 is the HTTP status code for redirection

        # Check if the redirection URL is as expected
        assert rv_update_redir.headers['Location'] == f'http://localhost/update?id={entry_id}'


if __name__ == '__main__':
    unittest.main()
