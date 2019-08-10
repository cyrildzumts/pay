from django.urls import resolve
from django.test import TestCase
import unittest
#from django.contrib.auth import views as auth_views
from dashboard import views


class DashboardViewsUrlTest(TestCase):

    def test_dashboard_home_url(self):
        found = resolve('/dashboard/')
        self.assertEqual(found.func, views.dashboard)

    def test_available_service_url(self):
        found = resolve('/dashboard/available_services/')
        self.assertEqual(found.func, views.available_services)
    
    def test_available_service_create_url(self):
        found = resolve('/dashboard/available_services/create/')
        self.assertEqual(found.func, views.available_service_create)
    
    def test_available_service_update_url(self):
        found = resolve('/dashboard/available_services/update/10')
        self.assertEqual(found.func, views.available_service_update)

    def test_available_service_remove_url(self):
        found = resolve('/dashboard/available_services/remove/10')
        self.assertEqual(found.func, views.available_service_remove) 
    

    def test_available_service_details_url(self):
        found = resolve('/dashboard/available_services/details/10')
        self.assertEqual(found.func, views.available_service_details) 

    def test_cases_url(self):
        found = resolve('/dashboard/cases/')
        self.assertEqual(found.func, views.cases)     


    def test_cases_details_url(self):
        found = resolve('/dashboard/cases/details/10/')
        self.assertEqual(found.func, views.case_details)  

    def test_cases_close_url(self):
        found = resolve('/dashboard/cases/close/10/')
        self.assertEqual(found.func, views.case_close) 

    def test_service_categories_url(self):
        found = resolve('/dashboard/service_categories/')
        self.assertEqual(found.func, views.category_services)

    def test_service_categories_details_url(self):
        found = resolve('/dashboard/service_categories/details/10/')
        self.assertEqual(found.func, views.category_service_details)


    def test_service_categories_create_url(self):
        found = resolve('/dashboard/service_categories/create/')
        self.assertEqual(found.func, views.category_service_create)

    def test_service_categories_update_url(self):
        found = resolve('/dashboard/service_categories/update/10/')
        self.assertEqual(found.func, views.category_service_update)

    def test_service_categories_remove_url(self):
        found = resolve('/dashboard/service_categories/remove/10/')
        self.assertEqual(found.func, views.category_service_remove)
#######################################################################

    

    def test_policies_url(self):
        found = resolve('/dashboard/policies/')
        self.assertEqual(found.func, views.policies)
    
    def test_policy_details_url(self):
        found = resolve('/dashboard/policies/details/10/')
        self.assertEqual(found.func, views.policy_details)

    def test_policy_remove_url(self):
        found = resolve('/dashboard/policies/remove/10/')
        self.assertEqual(found.func, views.policy_remove)

    def test_policy_update_url(self):
        found = resolve('/dashboard/policies/update/10/')
        self.assertEqual(found.func, views.policy_update)


    def test_policy_create_url(self):
        found = resolve('/dashboard/policies/create/')
        self.assertEqual(found.func, views.policy_create)



    def test_services_url(self):
        found = resolve('/dashboard/services/')
        self.assertEqual(found.func, views.services)

    
    def test_service_details_url(self):
        found = resolve('/dashboard/services/details/10/')
        self.assertEqual(found.func, views.service_details)

    def test_payments_url(self):
        found = resolve('/dashboard/payments/')
        self.assertEqual(found.func, views.payments)

    
    def test_payment_details_url(self):
        found = resolve('/dashboard/payments/details/10/')
        self.assertEqual(found.func, views.payment_details)
    
    def test_transfers_url(self):
        found = resolve('/dashboard/transfer/')
        self.assertEqual(found.func, views.transfers)
    
        
    def test_transfers_details_url(self):
        found = resolve('/dashboard/transfers/details/10/')
        self.assertEqual(found.func, views.transfer_details)