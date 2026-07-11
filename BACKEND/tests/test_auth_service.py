"""
test_auth_service.py — Unit tests for the authentication service.
"""

import pytest
from services.auth_service import verify_credentials


class TestVerifyCredentials:

    def test_valid_credentials_return_customer(self, app_context):
        customer = verify_credentials("alice", "password123")
        assert customer is not None
        assert customer["username"] == "alice"
        assert customer["name"] == "Alice Johnson"

    def test_wrong_password_returns_none(self, app_context):
        result = verify_credentials("alice", "wrongpassword")
        assert result is None

    def test_unknown_username_returns_none(self, app_context):
        result = verify_credentials("nobody", "password123")
        assert result is None

    def test_empty_username_returns_none(self, app_context):
        result = verify_credentials("", "password123")
        assert result is None

    def test_empty_password_returns_none(self, app_context):
        result = verify_credentials("alice", "")
        assert result is None

    def test_none_credentials_return_none(self, app_context):
        result = verify_credentials(None, None)
        assert result is None
