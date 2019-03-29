from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account, Policy
import unittest

# Create your tests here.

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

class DefaultAccountTestCase(unittest.TestCase):
    pass

class AccountTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        #cls.user1 = User.objects.create(**user1)
        #cls.user2 = User.objects.create(**user2)
        #cls.user3 = User.objects.create(**user3)
        cls.users = [User.objects.create(**userdata) for userdata in users]


    def test_account_creation(self):
        """ We should have 3 users in the database"""
        account_set = Account.objects.all()
        self.assertEqual(first=account_set.count() , second=3, msg="There are 3 users account in the database")
        self.assertEqual(first=account_set.filter(user__username=users[0]['username']).count(), second=1,msg="any user account in the database must be unique")
        self.assertEqual(first=account_set.filter(user__username=users[1]['username']).count(), second=1,msg="any user account in the database must be unique")
        self.assertEqual(first=account_set.filter(user__username=users[2]['username']).count(), second=1,msg="any user account in the database must be unique")


    def test_account_default_state(self):
        """ By default account are created  not ready to be used as the user has not filled the 
            the need information. This unit test checks that the default settings are applied
        """
        account_set = Account.objects.all()
        self.assertTrue(account_set.filter(account_type='P').count() == 3)
        self.assertTrue(account_set.filter(account_type='B').count() == 0)
    

    def test_update_account(self):
        account_set = Account.objects.all()
        account_set.filter(user__username=users[0]['username']).update(**account1)
        account_set.filter(user__username=users[1]['username']).update(**account2)
        account_set.filter(user__username=users[2]['username']).update(**account3)

        #account_set = Account.objects.all()
        self.assertTrue(account_set.filter(account_type='P').count() == 2)
        self.assertTrue(account_set.filter(account_type='B').count() == 1)





class PolicyTestCase(TestCase):
    """
    This unit test checks if the app starts with the default Policy created
    By default 3 Policies must be available to offer basics services.
    """

    @classmethod
    def setUpTestData(cls):
        cls.policies = [Policy.objects.create(**policy) for policy in policies]
    
    def test_policy_creation(self):
        self.assertTrue(Policy.objects.count() == 4, msg="There should be 4 Policy Entries in the database")