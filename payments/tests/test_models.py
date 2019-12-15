from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
import logging
from payments.models import (
    Policy, AvailableService, CaseIssue, Service, ServiceCategory, Payment, Transfer
)

logger = logging.getLogger(__name__)

POLICY_DATA = {
    'daily_limit' : 15000,
    'weekly_limit' : 150000,
    'monthly_limit' : 500000,
    'commission' : 0.3
}

POLICY_DATA2 = {
    'daily_limit' : 150000,
    'weekly_limit' : 500000,
    'monthly_limit' : 1000000,
    'commission' : 0.25
}

NEW_USER_TEST1 = {
    'username' : 'test_user1',
    'first_name': 'User 1',
    'last_name' : 'User 1 Lastname',
    'password' : 'Electronique0',
    'email'    : 'testuser1@example.com'
}

NEW_USER_TEST2 = {
    'username' : 'test_user2',
    'first_name': 'User 2',
    'last_name' : 'User 2 Lastname',
    'password' : 'Electronique0',
    'email'    : 'testuser2@example.com'
}

USER_TEST1 = {
    'username' : 'test_user1',
    'password' : 'Electronique0',
    'email'    : 'testuser1@example.com'
}

USER_TEST2 = {
    'username' : 'test_user2',
    'password' : 'Electronique0',
    'email'    : 'testuser2@example.com'
}




class PolicyModelTest(TestCase):

    def test_saving_policy(self):
        policy = Policy(**POLICY_DATA)
        policy.save()

        policy_2 = Policy(**POLICY_DATA2)
        policy_2.save()

        policies = Policy.objects.all()
        count = policies.count()
        self.assertEqual(count, 2)
        self.assertTrue(Policy.objects.filter(policy_uuid=policy.policy_uuid).exists())
        self.assertTrue(Policy.objects.filter(policy_uuid=policy_2.policy_uuid).exists())
    
    def test_delete_policy(self):
        count = Policy.objects.all().count()
        self.assertEqual(count, 0)
        policy = Policy(**POLICY_DATA)
        policy.save()

        policy_2 = Policy(**POLICY_DATA2)
        policy_2.save()

        new_count = Policy.objects.all().count()
        self.assertEqual(new_count, 2)
        self.assertTrue(Policy.objects.filter(policy_uuid=policy.policy_uuid).exists())
        self.assertTrue(Policy.objects.filter(policy_uuid=policy_2.policy_uuid).exists())
        policy.delete()
        policy_2.delete()
        new_count = Policy.objects.all().count()
        self.assertEqual(new_count, 0)
        self.assertFalse(Policy.objects.filter(policy_uuid=policy.policy_uuid).exists())
        self.assertFalse(Policy.objects.filter(policy_uuid=policy_2.policy_uuid).exists())

    
    def test_saving_payment(self):
        sender = User.objects.create_user(username=USER_TEST1['username'], email=USER_TEST1['email'], password=USER_TEST1['password'])
        recipient = User.objects.create_user(username=USER_TEST2['username'], email=USER_TEST2['email'], password=USER_TEST2['password'])
        TEST_PAYMENT_DATA = {
            'amount' : 25000,
            'details': 'Payment Description',
            'sender' : sender,
            'recipient': recipient
        }
        self.assertTrue(Payment.objects.count() == 0)
        payment = Payment(**TEST_PAYMENT_DATA)
        payment.save()
        self.assertTrue(Payment.objects.count() == 1)
        self.assertTrue(Payment.objects.get(payment_uuid=payment.payment_uuid, is_validated=False).exists())

    def test_delete_payment(self):
        sender = User.objects.create_user(username=USER_TEST1['username'], email=USER_TEST1['email'], password=USER_TEST1['password'])
        recipient = User.objects.create_user(username=USER_TEST2['username'], email=USER_TEST2['email'], password=USER_TEST2['password'])
        TEST_PAYMENT_DATA = {
            'amount' : 25000,
            'details': 'Payment Description',
            'sender' : sender,
            'recipient': recipient
        }
        self.assertTrue(Payment.objects.count() == 0)
        payment = Payment(**TEST_PAYMENT_DATA)
        payment.save()
        self.assertTrue(Payment.objects.count() == 1)
        self.assertTrue(Payment.objects.get(payment_uuid=payment.payment_uuid, is_validated=False).exists())
        payment.delete()
        self.assertTrue(Payment.objects.count() == 0)
        self.assertFalse(Payment.objects.get(payment_uuid=payment.payment_uuid, is_validated=False).exists())
    
        
    def test_saving_transfer(self):
        sender = User.objects.create_user(username=USER_TEST1['username'], email=USER_TEST1['email'], password=USER_TEST1['password'])
        recipient = User.objects.create_user(username=USER_TEST2['username'], email=USER_TEST2['email'], password=USER_TEST2['password'])
        TEST_TRANSFER_DATA = {
            'amount' : 25000,
            'details': 'Transfer Description',
            'sender' : sender,
            'recipient': recipient
        }
        self.assertTrue(Transfer.objects.count() == 0)
        transfer = Transfer(**TEST_TRANSFER_DATA)
        transfer.save()
        self.assertTrue(Transfer.objects.count() == 1)
        self.assertTrue(Transfer.objects.get(transfer_uuid=transfer.transfer_uuid, is_validated=False).exists())

    def test_delete_transfer(self):
        sender = User.objects.create_user(username=USER_TEST1['username'], email=USER_TEST1['email'], password=USER_TEST1['password'])
        recipient = User.objects.create_user(username=USER_TEST2['username'], email=USER_TEST2['email'], password=USER_TEST2['password'])
        TEST_TRANSFER_DATA = {
            'amount' : 25000,
            'details': 'Transfer Description',
            'sender' : sender,
            'recipient': recipient
        }
        self.assertTrue(Transfer.objects.count() == 0)
        transfer = Transfer(**TEST_TRANSFER_DATA)
        transfer.save()
        self.assertTrue(Transfer.objects.count() == 1)
        self.assertTrue(Transfer.objects.get(transfer_uuid=transfer.transfer_uuid).exists())
        transfer.delete()
        self.assertTrue(Transfer.objects.count() == 0)
        self.assertFalse(Transfer.objects.get(transfer_uuid=transfer.transfer_uuid, is_validated=False).exists())


