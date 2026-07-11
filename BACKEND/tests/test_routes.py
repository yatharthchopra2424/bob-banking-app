"""
test_routes.py — Integration tests for all Flask route handlers.
"""

import pytest


class TestLogin:

    def test_login_page_renders(self, client):
        response = client.get("/login")
        assert response.status_code == 200
        assert b"NexaBank" in response.data

    def test_valid_login_redirects_to_dashboard(self, client):
        response = client.post(
            "/login",
            data={"username": "alice", "password": "password123"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert "/dashboard" in response.headers["Location"]

    def test_invalid_password_shows_error(self, client):
        response = client.post(
            "/login",
            data={"username": "alice", "password": "wrongpass"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Invalid username or password" in response.data

    def test_unknown_user_shows_error(self, client):
        response = client.post(
            "/login",
            data={"username": "ghost", "password": "anything"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Invalid username or password" in response.data

    def test_missing_username_shows_error(self, client):
        response = client.post(
            "/login",
            data={"username": "", "password": "password123"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Username is required" in response.data

    def test_missing_password_shows_error(self, client):
        response = client.post(
            "/login",
            data={"username": "alice", "password": ""},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Password is required" in response.data


class TestLogout:

    def test_logout_clears_session_and_redirects(self, client):
        client.post("/login", data={"username": "alice", "password": "password123"})
        response = client.get("/logout", follow_redirects=False)
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]


class TestRouteProtection:

    def test_unauthenticated_dashboard_redirects(self, client):
        response = client.get("/dashboard", follow_redirects=False)
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]

    def test_unauthenticated_deposit_redirects(self, client):
        response = client.get("/deposit", follow_redirects=False)
        assert response.status_code == 302

    def test_unauthenticated_withdraw_redirects(self, client):
        response = client.get("/withdraw", follow_redirects=False)
        assert response.status_code == 302


class TestDashboard:

    def test_authenticated_dashboard_shows_balance(self, client):
        client.post("/login", data={"username": "alice", "password": "password123"})
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert b"Alice Johnson" in response.data


class TestDeposit:

    def _login(self, client):
        client.post("/login", data={"username": "alice", "password": "password123"})

    def test_deposit_page_renders(self, client):
        self._login(client)
        response = client.get("/deposit")
        assert response.status_code == 200
        assert b"Deposit Funds" in response.data

    def test_valid_deposit_redirects_to_dashboard(self, client):
        self._login(client)
        response = client.post("/deposit", data={"amount": "50"}, follow_redirects=False)
        assert response.status_code == 302
        assert "/dashboard" in response.headers["Location"]

    def test_zero_deposit_shows_error(self, client):
        self._login(client)
        response = client.post("/deposit", data={"amount": "0"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"greater than zero" in response.data

    def test_empty_deposit_shows_error(self, client):
        self._login(client)
        response = client.post("/deposit", data={"amount": ""}, follow_redirects=True)
        assert response.status_code == 200
        assert b"required" in response.data.lower()

    def test_text_deposit_shows_error(self, client):
        self._login(client)
        response = client.post("/deposit", data={"amount": "abc"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"number" in response.data.lower()


class TestWithdraw:

    def _login(self, client):
        client.post("/login", data={"username": "alice", "password": "password123"})

    def test_withdraw_page_renders(self, client):
        self._login(client)
        response = client.get("/withdraw")
        assert response.status_code == 200
        assert b"Withdraw Funds" in response.data

    def test_valid_withdrawal_redirects_to_dashboard(self, client):
        self._login(client)
        response = client.post("/withdraw", data={"amount": "10"}, follow_redirects=False)
        assert response.status_code == 302
        assert "/dashboard" in response.headers["Location"]

    def test_overdraft_shows_error(self, client):
        self._login(client)
        response = client.post("/withdraw", data={"amount": "9999999"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Insufficient funds" in response.data

    def test_zero_withdrawal_shows_error(self, client):
        self._login(client)
        response = client.post("/withdraw", data={"amount": "0"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"greater than zero" in response.data
