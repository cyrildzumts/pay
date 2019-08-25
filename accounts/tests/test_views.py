from django.urls import resolve
from django.test import TestCase
import unittest
#from django.contrib.auth import views as auth_views
from accounts import views


class AccountViewsUrlTest(TestCase):
    def test_account_root_url_resolve(self):
        found = resolve('/accounts/')
        self.assertEqual(found.func, views.user_account)

    def test_edit_account_url(self):
        found = resolve('/accounts/account_detail/10/')
        self.assertEqual(found.func, views.account_details)


    def test_account_transactions_url(self):
        found = resolve('/accounts/transactions/')
        self.assertEqual(found.func, views.transactions)
    
    def test_account_services_url(self):
        found = resolve('/accounts/services/')
        self.assertEqual(found.func, views.services)
    

    def test_login_url(self):
        found = resolve('/accounts/login/')
        self.assertEqual(found.func, views.login)
    

    def test_logout_url(self):
        found = resolve('/accounts/logout/')
        self.assertEqual(found.func, views.logout)


    def test_password_change_url(self):
        found = resolve('/accounts/password_change/')
        self.assertEqual(found.func, views.password_change_views)
    

    def test_password_change_done_url(self):
        found = resolve('/accounts/password_change_done/')
        self.assertEqual(found.func, views.password_change_done_views)
    

    def test_register_url(self):
        found = resolve('/accounts/register/')
        self.assertEqual(found.func, views.register)

    def test_available_service_url(self):
        found = resolve('/accounts/available_services/')
        self.assertEqual(found.func, views.available_services)

    
    def test_idcards_url(self):
        found = resolve('/accounts/idcards/')
        self.assertEqual(found.func, views.idcards)
    
    def test_service_categories_url(self):
        found = resolve('/accounts/service_categories/')
        self.assertEqual(found.func, views.service_categories)

    def test_transactions_url(self):
        found = resolve('/accounts/transactions/')
        self.assertEqual(found.func, views.transactions)
    
    def test_transaction_details_url(self):
        found = resolve('/accounts/transactions/10/')
        self.assertEqual(found.func, views.transaction_details)
    
    def test_new_transaction_url(self):
        found = resolve('/accounts/new_transaction/')
        self.assertEqual(found.func, views.new_transaction)

    def test_reductions_url(self):
        found = resolve('/accounts/reductions/')
        self.assertEqual(found.func, views.reductions)

    def test_reductions_details_url(self):
        found = resolve('/accounts/reductions/10/')
        self.assertEqual(found.func, views.reduction_details)

    def test_policy_url(self):
        found = resolve('/accounts/policies/')
        self.assertEqual(found.func, views.policies)
    
    def test_policy_details_url(self):
        found = resolve('/accounts/policies/10/')
        self.assertEqual(found.func, views.policy_details)

    def test_cases_url(self):
        found = resolve('/accounts/cases/')
        self.assertEqual(found.func, views.cases)
    
    def test_cases_edit_url(self):
        found = resolve('/accounts/cases/10/')
        self.assertEqual(found.func, views.case_details)

    def test_services_url(self):
        found = resolve('/accounts/services/')
        self.assertEqual(found.func, views.services)

    def test_service_done_url(self):
        found = resolve('/accounts/service_done/')
        self.assertEqual(found.func, views.service_done)
    
    def test_service_details_url(self):
        found = resolve('/accounts/services/10/')
        self.assertEqual(found.func, views.service_details)

    def test_payments_url(self):
        found = resolve('/accounts/payments/')
        self.assertEqual(found.func, views.payments)

    def test_new_payment_url(self):
        found = resolve('/accounts/new_payment/')
        self.assertEqual(found.func, views.new_payment)

    def test_payment_done_url(self):
        found = resolve('/accounts/payment_done/')
        self.assertEqual(found.func, views.payment_done)
    
    def test_payment_details_url(self):
        found = resolve('/accounts/payments/10/')
        self.assertEqual(found.func, views.payment_details)
    

    def test_new_service_url(self):
        found = resolve('/accounts/new_service/2/')
        self.assertEqual(found.func, views.new_service)

    def test_upload_idcard_url(self):
        found = resolve('/accounts/upload_idcard/')
        self.assertEqual(found.func, views.upload_idcard)

    def test_idcard_update_url(self):
        found = resolve('/accounts/idcard/update/10/')
        self.assertEqual(found.func, views.update_idcard)

    def test_upload_idcard_done_url(self):
        found = resolve('/accounts/upload_idcard/upload_idcard_done/')
        self.assertEqual(found.func, views.upload_idcard_done)

    def test_recharge_url(self):
        found = resolve('/accounts/recharge/')
        self.assertEqual(found.func, views.recharge)