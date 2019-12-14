from django.test import TestCase

from payments.models import (
    Policy, AvailableService, CaseIssue, Service, ServiceCategory, Payment, Transfer
)


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

class PolicyModelTest(TestCase):

    def test_saving_policy(self):
        policy = Policy(**POLICY_DATA)
        policy.save()

        policy_2 = Policy(**POLICY_DATA2)
        policy_2.save()

        policies = Policy.objects.all()

        self.assertEqual(policies.count(), 2)
        self.assertTrue(Policy.objects.filter(policy_uuid=policy.policy_uuid).exists())
        self.assertTrue(Policy.objects.filter(policy_uuid=policy_2.policy_uuid).exists())
