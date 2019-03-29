from django.urls import resolve
from django.test import TestCase
import unittest
from django.contrib.auth import views as auth_views
from accounts.views import user_account, edit_account, login, logout, register, transactions, services


class AccountPage(TestCase):
    def test_account_root_url_resolve(self):
        found = resolve('/account/')
        self.assertEqual(found.func, user_account)

    def test_edit_account_url(self):
        found = resolve('/account/edit_account/10')
        self.assertEqual(found.func, edit_account)


    def test_account_transactions_url(self):
        found = resolve('/account/transactions/')
        self.assertEqual(found.func, transactions)
    
    def test_account_services_url(self):
        found = resolve('/account/services/')
        self.assertEqual(found.func, services)
    

    def test_login_url(self):
        found = resolve('/account/login/')
        self.assertEqual(found.func, auth_views.LoginView.as_view())
    
    def test_logout_url(self):
        found = resolve('/account/logout/')
        self.assertEqual(found.func, auth_views.LogoutView.as_view())

    def test_register_url(self):
        found = resolve('/account/register/')
        self.assertEqual(found.func, register)
    
