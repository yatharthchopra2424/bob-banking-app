"""
test_account_service.py — Unit tests for deposit and withdraw logic.
"""

import pytest
from services.account_service import get_account, deposit, withdraw


def get_alice(app_context):
    return get_account(1)


class TestGetAccount:

    def test_returns_account_for_valid_customer(self, app_context):
        account = get_account(1)
        assert account is not None
        assert account["customer_name"] == "Alice Johnson"
        assert isinstance(account["balance"], float)

    def test_returns_none_for_unknown_customer(self, app_context):
        account = get_account(9999)
        assert account is None


class TestDeposit:

    def test_valid_deposit_increases_balance(self, app_context):
        account = get_account(1)
        before = account["balance"]
        new_balance = deposit(account["account_id"], 100.00)
        assert new_balance == pytest.approx(before + 100.00, abs=0.01)

    def test_zero_amount_raises_value_error(self, app_context):
        account = get_account(1)
        with pytest.raises(ValueError, match="greater than zero"):
            deposit(account["account_id"], 0)

    def test_negative_amount_raises_value_error(self, app_context):
        account = get_account(1)
        with pytest.raises(ValueError, match="greater than zero"):
            deposit(account["account_id"], -50)

    def test_non_numeric_amount_raises_value_error(self, app_context):
        account = get_account(1)
        with pytest.raises(ValueError, match="must be a number"):
            deposit(account["account_id"], "abc")

    def test_exceeds_maximum_raises_value_error(self, app_context):
        account = get_account(1)
        with pytest.raises(ValueError, match="maximum"):
            deposit(account["account_id"], 2_000_000)


class TestWithdraw:

    def test_valid_withdrawal_decreases_balance(self, app_context):
        account = get_account(1)
        before = account["balance"]
        new_balance = withdraw(account["account_id"], 50.00, before)
        assert new_balance == pytest.approx(before - 50.00, abs=0.01)

    def test_zero_amount_raises_value_error(self, app_context):
        account = get_account(1)
        with pytest.raises(ValueError, match="greater than zero"):
            withdraw(account["account_id"], 0, account["balance"])

    def test_negative_amount_raises_value_error(self, app_context):
        account = get_account(1)
        with pytest.raises(ValueError, match="greater than zero"):
            withdraw(account["account_id"], -10, account["balance"])

    def test_overdraft_raises_value_error(self, app_context):
        account = get_account(1)
        with pytest.raises(ValueError, match="Insufficient funds"):
            withdraw(account["account_id"], account["balance"] + 1, account["balance"])

    def test_exact_balance_withdrawal_succeeds(self, app_context):
        account = get_account(1)
        new_balance = withdraw(account["account_id"], account["balance"], account["balance"])
        assert new_balance == pytest.approx(0.0, abs=0.01)

    def test_non_numeric_amount_raises_value_error(self, app_context):
        account = get_account(1)
        with pytest.raises(ValueError, match="must be a number"):
            withdraw(account["account_id"], "xyz", account["balance"])
