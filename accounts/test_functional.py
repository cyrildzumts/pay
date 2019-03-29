from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account, Policy
import unittest
from accounts.account_services import AccountService




# users data for creating new user
user1 = {
    'username' : 'unitTest1',
    'password': 'unitestpassword',
    'email' : 'user1@unittest.com',
    'first_name': 'user1',
    'last_name': 'user_lastname1',
}
user2 = {
    'username' : 'unitTest2',
    'password': 'unitestpassword',
    'email' : 'user1@unittest.com',
    'first_name': 'user2',
    'last_name': 'user_lastname2',

}

user3 = {
    'username' : 'unitTest3',
    'first_name': 'user3',
    'last_name': 'user_lastname3',
    'password': 'unitestpassword',
    'email' : 'user1@unittest.com',
}

users  = [user1, user2, user3]

# account data for creating new Accounts
account1 = {
    'date_of_birth' : '2000-12-12',
    'country' : 'Cameroun',
    'city': 'Douala',
    'province': 'Littoral',
    'address': 'rue manguier',
    'zip_code': '10561',
    'telefon': '+237699457812',
    'account_type': 'P'
}
account2 = {
    'date_of_birth' : '2001-03-06',
    'country' : 'Cameroun',
    'city': 'Douala',
    'province': 'Littoral',
    'address': 'Mokolo',
    'zip_code': '10561',
    'telefon': '+237699457814',
    'account_type': 'P'
}

account3 = {
    'date_of_birth' : '2000-06-05',
    'country' : 'Cameroun',
    'city': 'Douala',
    'province': 'Littoral',
    'address': 'rue manguier',
    'zip_code': '10561',
    'telefon': '+237699457812',
    'account_type': 'B'
}
accounts_data = [account1, account2, account3]

# Policies data for creating Policy models

policy1 = {
    'daily_limit': '100000',
    'weekly_limit': '450000',
    'monthly_limit': '800000',
    'commission' : '3.5'
}
policy2 = {
    'daily_limit': '250000',
    'weekly_limit': '750000',
    'monthly_limit': '950000',
    'commission' : '3.0'
}
policy3 = {
    'daily_limit': '500000',
    'weekly_limit': '1000000',
    'monthly_limit': '1500000',
    'commission' : '2.8'
}

policy4 = {
    'daily_limit': '1000000',
    'weekly_limit': '5000000',
    'monthly_limit': '15000000',
    'commission' : '2.5'
}

policies = [policy1, policy2, policy3, policy4]

class AccountServiceTest(TestCase):

    def test_create_account(self):

        created = AccountService.create_account(accountdata=account1, userdata=user1)
        self.assertTrue(created == (Account.objects.filter(user__username=user1['username']).filter(**account1).count() == 1 ))
        created = AccountService.create_account(accountdata=account1, userdata=user1)
        self.assertFalse(created)
    
    def test_create_policy(self):
        created = AccountService.create_policy(policy_data=policy1)
        self.assertTrue(created == (Policy.objects.filter(**policy1).count() == 1 ))
        created = AccountService.create_policy(policy_data=policy1)
        self.assertFalse(created)
