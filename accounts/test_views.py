from django.urls import resolve
from django.test import TestCase
import unittest
#from django.contrib.auth import views as auth_views
from accounts import views


class AccountViewsUrlTest(TestCase):
    def test_account_root_url_resolve(self):
        found = resolve('/account/')
        self.assertEqual(found.func, views.user_account)

    def test_edit_account_url(self):
        found = resolve('/account/edit_account/10/')
        self.assertEqual(found.func, views.edit_account)


    def test_account_transactions_url(self):
        found = resolve('/account/transactions/')
        self.assertEqual(found.func, views.transactions)
    
    def test_account_services_url(self):
        found = resolve('/account/services/')
        self.assertEqual(found.func, views.services)
    

    def test_login_url(self):
        found = resolve('/account/login/')
        self.assertEqual(found.func, views.login)
    

    def test_logout_url(self):
        found = resolve('/account/logout/')
        self.assertEqual(found.func, views.logout)


    def test_password_change_url(self):
        found = resolve('/account/password_change/')
        self.assertEqual(found.func, views.password_change_views)
    

    def test_password_change_done_url(self):
        found = resolve('/account/password_change/done/')
        self.assertEqual(found.func, views.password_change_done_views)
    

    def test_register_url(self):
        found = resolve('/account/register/')
        self.assertEqual(found.func, views.register)
    
