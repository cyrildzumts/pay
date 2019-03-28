from django.test import TestCase
from accounts.models import Account
import unittest

# Create your tests here.

user1 = {
    'username' : 'unitTest1',
    'password': 'unitestpassword',
    'email' : 'user1@unittest.com',
    'first_name': 'user1',
    'date_of_birth' : '2000-12-12',
    'last_name': 'user_lastname1',
    'country' : 'Cameroun',
    'city': 'Douala',
    'province': 'Littoral',
    'address': 'rue manguier',
    'zip_code': '10561',
    'telefon': '+237699457812',
    'account_type': 'P'
}
user2 = {
    'username' : 'unitTest2',
    'password': 'unitestpassword',
    'email' : 'user1@unittest.com',
    'first_name': 'user2',
    'date_of_birth' : '2001-03-06',
    'last_name': 'user_lastname2',
    'country' : 'Cameroun',
    'city': 'Douala',
    'province': 'Littoral',
    'address': 'Mokolo',
    'zip_code': '10561',
    'telefon': '+237699457814',
    'account_type': 'P'
}

user3 = {
    'username' : 'unitTest3',
    'password': 'unitestpassword',
    'email' : 'user1@unittest.com',
    'first_name': 'user3',
    'date_of_birth' : '2000-06-05',
    'last_name': 'user_lastname3',
    'country' : 'Cameroun',
    'city': 'Douala',
    'province': 'Littoral',
    'address': 'rue manguier',
    'zip_code': '10561',
    'telefon': '+237699457812',
    'account_type': 'B'
}

class DefaultAccountTestCase(unittest.TestCase):
    pass

class AccountTestCase(TestCase):
    def setUp(self):
        Account.objects.create(**user1)
        Account.objects.create(**user2)
        Account.objects.create(**user3)

    def test_account_creation(self):
        """ We should have 3 users in the database"""
        self.assertEqual(Account.objects.count() , 3, msg="There are 3 users account in the database")
        self.assertEqual(first=Account.objects.filter(username=user1['username']).count(), 1)
        self.assertEqual(first=Account.objects.filter(username=user2['username']).count(), 1)
        self.assertEqual(first=Account.objects.filter(username=user3['username']).count(), 1)
