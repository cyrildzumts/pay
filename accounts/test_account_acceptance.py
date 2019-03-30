from django.test import TestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from accounts.models import Account, Policy
from accounts.account_services import AccountService

import time
import unittest


class UserAccountTest(TestCase):
    """
    Acceptance Tests.
    Verify if has access to the application.
    """
    def test_user_can_create_account(self):
        self.fail("Not implemented yet")
    

    def test_user_can_login(self):
        self.fail("Not implemented yet")

    def test_user_can_logout(self):
        self.fail("Not implemented yet")
    

class UserAccountTransactionsTest(TestCase):
    """
    Acceptance Test:
    Verify that the user can make transactions from his 
    account page.
    """

    def test_can_not_recharge_account(self):
        """
            A user must be logged in before he can make a transaction
        """
        self.fail("Not implemented yet")
    
    def test_logged_in_can_not_recharge_account(self):
        """
            To recharge her account, the user who is logged in needs a valide and an 
            activated voucher code.
        """
        self.fail("Not implemented yet")
    

    def test_can_recharge_account(self):
        """
            A logged in user in pocession of a valide voucher code
            can recharge her account.
        """
        self.fail("Not implemented yet")
    

    def test_user_can_create_case_issue(self):

        self.fail("Not implemented yet")
    

    def test_user_can_validate_transaction(self):
        """
            Every transaction must be validated by the customer before the 
            account is debited.
        """
        self.fail("Not implemented yet")


    def test_user_can_make_a_transfer(self):
        self.fail("Not implemented yet")

    
    def test_user_can_make_a_payment(self):
        self.fail("Not implemented yet")

    
    def test_user_can_make_a_programmed_transfer(self):
        self.fail("Not implemented yet")


    def test_user_can_see_transactions_history(self):
        self.fail("Not implemented yet")


    def test_user_can_see_current_state(self):
        """
        Verify that the user can see the current state of her account 
        from her account page.
        """
        self.fail("Not implemented yet")


        
