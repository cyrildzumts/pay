from django.urls import resolve
from django.test import TestCase
import unittest
from accounts.views import user_account, edit_account, login, logout, register, transactions, services


class AccountPage(TestCase):
    def test_account_root_url_resolve(self):
        found = resolve('/account/')
        self.assertEqual(found.func, user_account)

    def test_edit_account_url(self):
        found = resolve('/account/edit_account')
        self.assertEqual(found.func, edit_account)


    def test_account_transactions_url(self):
        found = resolve('/account/transactions')
        self.assertEqual(found.func, transactions)
    
    def test_account_services_url(self):
        found = resolve('/account/services')
        self.assertEqual(found.func, services)
    

    def test_login_url(self):
        found = resolve('/account/login')
        self.assertEqual(found.func, login)
    
    def test_logout_url(self):
        found = resolve('/account/logout')
        self.assertEqual(found.func, logout)

    def test_register_url(self):
        found = resolve('/account/register')
        self.assertEqual(found.func, register)
    
