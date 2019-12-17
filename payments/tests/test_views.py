from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.http.response import Http404
from django.db.models import F, Q
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from payments.models import Transfer, Payment
from payments.forms import TransferForm
from payments import views
from pay import utils
import logging


logger = logging.getLogger(__name__)


Account = utils.get_model('accounts', 'Account')

ACCOUNT_BALANCE = 100000
TRANSFER_AMOUNT = 25000
PAYMENT_HOME_URL = reverse('payments:payment-home')
PAYMENT_NEW_TRANSFER_URL = reverse('payments:new-transfer')
STATUS_CODE_200 = 200
STATUS_CODE_302 = 302
STATUS_CODE_403 = 403
STATUS_CODE_404 = 404



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

USER_TEST3 = {
    'username' : 'test_user3',
    'password' : 'Electronique0',
    'email'    : 'testuser3@example.com'
}

def add_middledware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


def add_middledware_to_response(request, middleware_class):
    middleware = middleware_class()
    middleware.process_response(request)
    return request

class PaymentTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.sender = User.objects.create_user(username=USER_TEST1['username'], email=USER_TEST1['email'], password=USER_TEST1['password'])
        self.recipient = User.objects.create_user(username=USER_TEST2['username'], email=USER_TEST2['email'], password=USER_TEST2['password'])
        self.no_transfer_user = User.objects.create_user(username=USER_TEST3['username'], email=USER_TEST3['email'], password=USER_TEST3['password'])
        self.anonymeUser = AnonymousUser()

    
    def test_payment_home(self):
        request =  self.factory.get(reverse('payments:payment-home'))
        request.user = self.anonymeUser
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.payment_home(request)
        self.assertEqual(response.status_code, STATUS_CODE_302)

    
    


class TransferTest(TestCase):
    # status code = 200 --> the request failed and the the same page is shown.
    # status code = 302 (request.user = self.sender--> the request succeed and 
    # the view made a redirection to reverse('payments:transfer-done').
    # status code = 302 (request.user = self.anonymeUser--> the request failed because of the required_login decorator 
    # applied on the view new_transfer. status code 302 is the redirection to the login view.


    def setUp(self):
        self.factory = RequestFactory()
        self.sender = User.objects.create_user(username=USER_TEST1['username'], email=USER_TEST1['email'], password=USER_TEST1['password'])
        self.recipient = User.objects.create_user(username=USER_TEST2['username'], email=USER_TEST2['email'], password=USER_TEST2['password'])
        self.no_transfer_user = User.objects.create_user(username=USER_TEST3['username'], email=USER_TEST3['email'], password=USER_TEST3['password'])
        self.anonymeUser = AnonymousUser()
        self.TEST_TRANSFER_DATA = {
            'amount' : TRANSFER_AMOUNT,
            'details': 'Transfer Description',
            'sender' : self.sender.pk,
            'recipient': self.recipient.pk
        }

        self.TEST_SENDER_IS_RECIPIENT_TRANSFER_DATA = {
            'amount' : TRANSFER_AMOUNT,
            'details': 'Transfer Description',
            'sender' : self.sender.pk,
            'recipient': self.sender.pk
        }

        self.TEST_NO_SENDER_TRANSFER_DATA = {
            'amount' : TRANSFER_AMOUNT,
            'details': 'Transfer Description',
            'recipient': self.recipient.pk
        }
        self.TEST_NO_RECIPIENT_TRANSFER_DATA = {
            'amount' : TRANSFER_AMOUNT,
            'details': 'Transfer Description',
            'sender' : self.sender.pk
        }
        self.TEST__NO_AMOUNT_TRANSFER_DATA = {
            'details': 'Transfer Description',
            'sender' : self.sender.pk,
            'recipient': self.recipient.pk
        }
        self.TEST_NO_DESCRIPTION_TRANSFER_DATA = {
            'amount' : TRANSFER_AMOUNT,
            'sender' : self.sender.pk,
            'recipient': self.recipient.pk
        }
    

    def test_transfer_cannot_create_transfer_anonyme(self):

        request = self.factory.post(path=PAYMENT_NEW_TRANSFER_URL, data=self.TEST_TRANSFER_DATA)

        request.user = self.anonymeUser
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.new_transfer(request=request)
        
        
        self.assertEqual(response.status_code, STATUS_CODE_302) # redirect to login view

    def test_transfer_cannot_create_transfer_no_sender(self):

        request = self.factory.post(path=PAYMENT_NEW_TRANSFER_URL, data=self.TEST_NO_SENDER_TRANSFER_DATA)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.new_transfer(request=request)
        
        
        self.assertEqual(response.status_code, STATUS_CODE_200) # failed to create the transfer. redirect to the same current view Page


    def test_transfer_cannot_create_transfer_recipient_is_sender(self):

        request = self.factory.post(path=PAYMENT_NEW_TRANSFER_URL, data=self.TEST_SENDER_IS_RECIPIENT_TRANSFER_DATA)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.new_transfer(request=request)
        
        
        self.assertEqual(response.status_code, STATUS_CODE_200)
        self.assertFalse(Transfer.objects.exists())

    def test_transfer_cannot_create_transfer_recipient_is_sender(self):

        request = self.factory.post(path=PAYMENT_NEW_TRANSFER_URL, data=self.TEST_SENDER_IS_RECIPIENT_TRANSFER_DATA)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.new_transfer(request=request)
        
        logger.info("test response = [\"%s\"]", response.items)
        [logger.info(x) for x in response.items]
        self.assertEqual(response.status_code, STATUS_CODE_200)
        self.assertFalse(Transfer.objects.exists())

    def test_transfer_cannot_create_transfer_no_recipient(self):
        request = self.factory.post(path=PAYMENT_NEW_TRANSFER_URL, data=self.TEST_NO_RECIPIENT_TRANSFER_DATA)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        response = views.new_transfer(request=request)
        self.assertEqual(response.status_code, STATUS_CODE_200) # failed to create the transfer. redirect to same view
    
    def test_transfer_create_transfer(self):
        request = self.factory.post(path=PAYMENT_NEW_TRANSFER_URL, data=self.TEST_TRANSFER_DATA)
        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        Account.objects.filter(user=self.sender).update(balance=ACCOUNT_BALANCE)
        response = views.new_transfer(request=request)
        
        self.assertEqual(response.status_code, STATUS_CODE_302) # succeed to create the transfer. redirect to 'payments:transfer-done'
        account_sender = Account.objects.get(user=self.sender)
        account_recipient = Account.objects.get(user=self.recipient)
        self.assertEqual(account_recipient.balance, TRANSFER_AMOUNT)
        self.assertEqual(account_sender.balance, ACCOUNT_BALANCE - TRANSFER_AMOUNT)
        
    def test_transfer_detail(self):
        
        self.assertTrue(Transfer.objects.count() == 0)
        transfer = Transfer(**self.TEST_TRANSFER_DATA)
        transfer.full_clean()
        transfer.save()
        self.assertTrue(Transfer.objects.count() == 1)
        self.assertTrue(Transfer.objects.filter(transfer_uuid=transfer.transfer_uuid).exists())

        transfer_url = transfer.get_absolute_url()

        request =  self.factory.get(transfer_url)
        request.user = self.anonymeUser
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        response = views.transfer_details(request, transfer.transfer_uuid )
        self.assertEqual(response.status_code, 302)

        request =  self.factory.get(transfer_url)
        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        response = views.transfer_details(request, transfer.transfer_uuid )
        self.assertEqual(response.status_code, 200)

        request =  self.factory.get(transfer_url)
        request.user = self.recipient
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        response = views.transfer_details(request, transfer.transfer_uuid )
        self.assertEqual(response.status_code, 200)

        request =  self.factory.get(transfer_url)
        request.user = self.no_transfer_user
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        self.assertRaises(Http404, views.transfer_details, request=request, transfer_uuid=transfer.transfer_uuid)