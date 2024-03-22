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

    # def test_delete(self):
    #     # Add an entry
    #     rv = self.app.post('/add', data=dict(
    #         title='<Hello>',
    #         text='<strong>HTML</strong> allowed here',
    #         category='A category'
    #     ), follow_redirects=True)
    #
    #     entry_id = id(rv)
    #     rv_delete = self.app.post('/delete', data=dict(
    #         id=id
    #     ), follow_redirects=True)
    #
    #     assert b'Test Entry' not in rv_delete.data
    #     assert b'This is a test entry' not in rv_delete.data
    #     assert b'Test Category' not in rv_delete.data
    #     assert b'Entry deleted successfully' in rv_delete.data

    def test_delete(self):
        # Test deleting an existing entry
        rv_add = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)

        entry_id = id(rv_add)

        rv_delete_existing = self.app.post('/delete', data=dict(
            id=entry_id
        ), follow_redirects=True)
        assert b'Entry deleted successfully' in rv_delete_existing.data

        # Test deleting a non-existing entry
        rv_delete_non_existing = self.app.post('/delete', data=dict(
            id='non_existing_id'
        ), follow_redirects=True)
        assert b'Entry not found' in rv_delete_non_existing.data

        # Test deleting the last entry
        rv_delete_last = self.app.post('/delete', data=dict(
            id=entry_id
        ), follow_redirects=True)
        assert b'Entry deleted successfully' in rv_delete_last.data

        # Test deleting entry without specifying ID
        rv_delete_no_id = self.app.post('/delete', follow_redirects=True)
        assert b'Invalid request' in rv_delete_no_id.data

        # Test deleting entry with invalid ID format
        rv_delete_invalid_id = self.app.post('/delete', data=dict(
            id='invalid_id_format'
        ), follow_redirects=True)
        assert b'Invalid entry ID' in rv_delete_invalid_id.data






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

    def test_update_redirect(self):
        test_id = 123
        response = self.app.get(f'/update-redir?id={test_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes(str(test_id), 'utf-8'), response.data)


if __name__ == '__main__':
    unittest.main()
