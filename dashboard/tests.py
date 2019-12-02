from django.urls import resolve
from django.test import TestCase
import unittest
import uuid
#from django.contrib.auth import views as auth_views
from dashboard import views

uuid_param = uuid.uuid4()

class DashboardViewsUrlTest(TestCase):

    def test_dashboard_home_url(self):
        found = resolve('/dashboard/')
        self.assertEqual(found.func, views.dashboard)

    def test_available_service_url(self):
        found = resolve('/dashboard/available-services/')
        self.assertEqual(found.func, views.available_services)
    
    def test_available_service_create_url(self):
        found = resolve('/dashboard/available-services/create/')
        self.assertEqual(found.func, views.available_service_create)
    
    def test_available_service_update_url(self):
        found = resolve('/dashboard/available-services/update/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.available_service_update)

    def test_available_service_remove_url(self):
        found = resolve('/dashboard/available-services/remove/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.available_service_remove) 
    
    def test_available_service_remove_all_url(self):
        found = resolve('/dashboard/available-services/remove-all/')
        self.assertEqual(found.func, views.available_service_remove_all) 


    def test_available_service_details_url(self):
        found = resolve('/dashboard/available-services/detail/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.available_service_details) 

    def test_cases_url(self):
        found = resolve('/dashboard/cases/')
        self.assertEqual(found.func, views.cases)     


    def test_cases_details_url(self):
        found = resolve('/dashboard/cases/detail/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.case_details)  

    def test_cases_close_url(self):
        found = resolve('/dashboard/cases/close/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.case_close) 

    def test_service_categories_url(self):
        found = resolve('/dashboard/category-services/')
        self.assertEqual(found.func, views.category_services)

    def test_service_categories_details_url(self):
        found = resolve('/dashboard/category-services/detail/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.category_service_details)


    def test_service_categories_create_url(self):
        found = resolve('/dashboard/category-services/create/')
        self.assertEqual(found.func, views.category_service_create)

    def test_service_categories_update_url(self):
        found = resolve('/dashboard/category-services/update/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.category_service_update)

    def test_service_categories_remove_url(self):
        found = resolve('/dashboard/category-services/remove/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.category_service_remove)
    
    def test_service_categories_remove_all_url(self):
        found = resolve('/dashboard/category-services/remove-all/')
        self.assertEqual(found.func, views.category_service_remove_all)
#######################################################################

    def test_groups_url(self):
        found = resolve('/dashboard/groups/')
        self.assertEqual(found.func, views.groups)
    
    def test_group_create_url(self):
        found = resolve('/dashboard/group-create/')
        self.assertEqual(found.func, views.group_create)
    
    def test_group_update_url(self):
        found = resolve('/dashboard/group-update/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.group_update)


    def test_group_detail_url(self):
        found = resolve('/dashboard/group-detail/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.group_detail)

    def test_group_delete_url(self):
        found = resolve('/dashboard/group-delete/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.group_delete)

    def test_policies_url(self):
        found = resolve('/dashboard/policies/')
        self.assertEqual(found.func, views.policies)
    
    def test_policy_details_url(self):
        found = resolve('/dashboard/policies/detail/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.policy_details)

    def test_policy_remove_url(self):
        found = resolve('/dashboard/policies/remove/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.policy_remove)

    def test_policy_remove_all_url(self):
        found = resolve('/dashboard/policies/remove-all/')
        self.assertEqual(found.func, views.policy_remove_all)

    def test_policy_update_url(self):
        found = resolve('/dashboard/policies/update/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.policy_update)


    def test_policy_create_url(self):
        found = resolve('/dashboard/policies/create/')
        self.assertEqual(found.func, views.policy_create)



    def test_services_url(self):
        found = resolve('/dashboard/services/')
        self.assertEqual(found.func, views.services)

    
    def test_service_details_url(self):
        found = resolve('/dashboard/services/detail/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.service_details)

    def test_payments_url(self):
        found = resolve('/dashboard/payments/')
        self.assertEqual(found.func, views.payments)

    
    def test_payment_details_url(self):
        found = resolve('/dashboard/payments/detail/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.payment_details)
    
    def test_transfers_url(self):
        found = resolve('/dashboard/transfers/')
        self.assertEqual(found.func, views.transfers)
    
        
    def test_transfers_details_url(self):
        found = resolve('/dashboard/transfers/detail/{}/'.format(uuid_param))
        self.assertEqual(found.func, views.transfer_details)