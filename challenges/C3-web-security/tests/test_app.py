import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("FLASK_SECRET_KEY", "test-only-session-key")
os.environ.setdefault("C3_FLAG", "TEST_FLAG_FOR_UNIT_TESTS")

import app as c3_app


class C3ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_dir.name) / "test.db")
        c3_app.DB_PATH = self.db_path
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
            )
            connection.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                ("researcher", "test-password-not-for-production"),
            )
        c3_app.app.config.update(TESTING=True, SECRET_KEY="test-only-session-key")
        self.client = c3_app.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "running")

    def test_archive_requires_session(self):
        response = self.client.get("/archive")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/", response.headers["Location"])

    def test_normal_invalid_login_is_rejected(self):
        response = self.client.post(
            "/", data={"username": "not-a-user", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Access denied", response.data)

    def test_intended_sql_injection_reaches_archive(self):
        # Demonstrates the intentional flaw only against the temporary test DB.
        response = self.client.post(
            "/",
            data={"username": "' OR '1'='1' -- ", "password": "irrelevant"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Research Archive", response.data)
        self.assertIn(b"TEST_FLAG_FOR_UNIT_TESTS", response.data)

    def test_logout_clears_session(self):
        self.client.post(
            "/", data={"username": "researcher", "password": "test-password-not-for-production"}
        )
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)
        archive = self.client.get("/archive")
        self.assertEqual(archive.status_code, 302)


if __name__ == "__main__":
    unittest.main()
