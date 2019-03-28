from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account
import unittest

# Create your tests here.


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

class DefaultAccountTestCase(unittest.TestCase):
    pass

class AccountTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(**user1)
        cls.user2 = User.objects.create(**user2)
        cls.user3 = User.objects.create(**user3)

    def test_account_creation(self):
        """ We should have 3 users in the database"""
        account_set = Account.objects.all()
        self.assertEqual(first=account_set.count() , second=3, msg="There are 3 users account in the database")
        self.assertEqual(first=account_set.filter(user__username=user1['username']).count(), second=1,msg="any user account in the database must be unique")
        self.assertEqual(first=account_set.filter(user__username=user2['username']).count(), second=1,msg="any user account in the database must be unique")
        self.assertEqual(first=account_set.filter(user__username=user3['username']).count(), second=1,msg="any user account in the database must be unique")


    def test_account_default_state(self):
        """ By default account are created  not ready to be used as the user has not filled the 
            the need information. This unit test checks that the default settings are applied
        """
        account_set = Account.objects.all()
        are_all_private_account_flags = [account.account_type == 'P' for account in account_set]
        no_business_account = [account.account_type == 'B' for account in account_set]
        self.assertTrue(all(are_all_private_account_flags))
        self.assertFalse(any(no_business_account))
    

    def test_update_account(self):
        account_set = Account.objects.all()
        account_set.filter(user=self.user1).update(**account1)
        account_set.filter(user=self.user2).update(**account2)
        account_set.filter(user=self.user3).update(**account3)

        account_set = Account.objects.all()
        no_all_private_account_flags = [account.account_type == 'P' for account in account_set]
        one_business_account = [account.account_type == 'B' for account in account_set]
        self.assertFalse(all(no_all_private_account_flags))
        self.assertTrue(any(one_business_account))