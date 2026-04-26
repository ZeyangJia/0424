import unittest
from app import app


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret"

    def test_index_returns_login_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Admin 登录".encode("utf-8"), response.data)

    def test_login_success(self):
        response = self.client.post(
            "/api/login",
            json={"username": "admin", "password": "admin123"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"success": True})

    def test_login_failure_wrong_password(self):
        response = self.client.post(
            "/api/login",
            json={"username": "admin", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "用户名或密码错误")

    def test_login_failure_nonexistent_user(self):
        response = self.client.post(
            "/api/login",
            json={"username": "notexist", "password": "admin123"},
        )
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "用户名或密码错误")

    def test_login_failure_empty_request(self):
        response = self.client.post("/api/login", json={})
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertFalse(data["success"])

    def test_admin_redirects_when_not_logged_in(self):
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/", response.headers.get("Location", ""))

    def test_admin_accessible_when_logged_in(self):
        self.client.post(
            "/api/login",
            json={"username": "admin", "password": "admin123"},
        )
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Admin 后台".encode("utf-8"), response.data)

    def test_logout_clears_session(self):
        self.client.post(
            "/api/login",
            json={"username": "admin", "password": "admin123"},
        )
        response = self.client.post("/api/logout")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"success": True})

        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
