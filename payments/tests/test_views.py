from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.http.response import Http404
from django.db.models import F, Q
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from payments.models import Transfer, Payment, Service, ServiceCategory, AvailableService, Policy
from payments.forms import TransferForm
from payments import views
from payments.tests import user_test_data, policy_test_data
from pay import utils
import logging


logger = logging.getLogger(__name__)


Account = utils.get_model('accounts', 'Account')

POLICY_DATA = {
    'daily_limit' : 150000,
    'weekly_limit' : 350000,
    'monthly_limit' : 550000,
    'commission' : 0.03
}

ACCOUNT_BALANCE = 100000

# TRANSFER

TRANSFER_AMOUNT = 25000
TRANSFER_AMOUNT_BIGGER_THAN_ACCOUNT_BALANCE = ACCOUNT_BALANCE + 1
PAYMENT_HOME_URL = reverse('payments:payment-home')
PAYMENT_NEW_TRANSFER_URL = reverse('payments:new-transfer')

#PAYMENT
PAYMENT_AMOUNT = 25000
PAYMENT_AMOUNT_BIGGER_THAN_ACCOUNT_BALANCE = ACCOUNT_BALANCE + 1
PAYMENT_HOME_URL = reverse('payments:payment-home')
PAYMENT_NEW_PAYMENT_URL = reverse('payments:new-payment')

# SERVICE CONSTANTS
EMPTY_STRING = ''

SERVICE_PRICE = 25000
SERVICE_PRICE_STR = '234KD0'
SERVICE_COMMISSION = 0.29
SERVICE_NAME = "TEST SERVICE"
SERVICE_NAME_EMPTY = ''
SERVICE_CUSTOMER_REFERENCE = '14587AF2514'
SERVICE_REFERENCE_NUMBER   = '14781254'
SERVICE_ISSUED_AT          = '2019-07-23'
SERVICE_DESCRIPTION        = 'TEST SERVICE DESCRIPTION'
PAYMENT_NEW_SERVICE_URL    = 'payments:new-service'

# CATEGORY CONSTANTS

CATEGORY_NAME      = 'TEST CAT'
CATEGORY_CODE      = 150

CATEGORY_DATA = {
    'category_name' : CATEGORY_NAME,
    'category_code' : CATEGORY_CODE,
    'is_active'     : True
}

# AVAILABLESERVICE

AVAILABLE_SERVICE_NAME = 'TEST AVAILABLE SERVICE'
SERVICE_CODE       = 175
AVAILABLE_SERVICE_DESCRIPTION        = 'TEST AVAILABLE SERVICE DESCRIPTION'

STATUS_CODE_200 = 200
STATUS_CODE_302 = 302
STATUS_CODE_403 = 403
STATUS_CODE_404 = 404


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
        self.sender = User.objects.create_user(username=user_test_data.USER_TEST1['username'], email=user_test_data.USER_TEST1['email'], password=user_test_data.USER_TEST1['password'])
        self.recipient = User.objects.create_user(username=user_test_data.USER_TEST2['username'], email=user_test_data.USER_TEST2['email'], password=user_test_data.USER_TEST2['password'])
        self.pay_user = User.objects.create_user(username=user_test_data.PAY_USER_TEST['username'], email=user_test_data.PAY_USER_TEST['email'], password=user_test_data.PAY_USER_TEST['password'])
        self.no_payment_user = User.objects.create_user(username=user_test_data.USER_TEST3['username'], email=user_test_data.USER_TEST3['email'], password=user_test_data.USER_TEST3['password'])
        self.anonymeUser = AnonymousUser()
        
        self.TEST_PAYMENT_DATA = {
            'amount' : PAYMENT_AMOUNT,
            'details': 'Payment Description',
            'sender' : self.sender.pk,
            'recipient': self.recipient.pk
        }

        self.TEST_PAYMENT_DATA_SENDER_NOT_FOUND = {
            'amount' : PAYMENT_AMOUNT,
            'details': 'Payment Description',
            'sender' : user_test_data.USER_NOT_FOUND_PK,
            'recipient': self.recipient.pk
        }

        self.TEST_PAYMENT_DATA_RECIPIENT_NOT_FOUND = {
            'amount' : PAYMENT_AMOUNT,
            'details': 'Payment Description',
            'sender' : self.sender.pk,
            'recipient': user_test_data.USER_NOT_FOUND_PK
        }

        self.TEST_INSUFFICIENT_PAYMENT_DATA = {
            'amount' : PAYMENT_AMOUNT_BIGGER_THAN_ACCOUNT_BALANCE,
            'details': 'Payment Description',
            'sender' : self.sender.pk,
            'recipient': self.recipient.pk
        }

        self.TEST_DETAIL_PAYMENT_DATA = {
            'amount' : PAYMENT_AMOUNT,
            'details': 'Payment Description',
            'sender' : self.sender,
            'recipient': self.recipient
        }

        self.TEST_SENDER_IS_RECIPIENT_PAYMENT_DATA = {
            'amount' : PAYMENT_AMOUNT,
            'details': 'Payment Description',
            'sender' : self.sender.pk,
            'recipient': self.sender.pk
        }

        self.TEST_NO_SENDER_PAYMENT_DATA = {
            'amount' : PAYMENT_AMOUNT,
            'details': 'Payment Description',
            'recipient': self.recipient.pk
        }
        self.TEST_NO_RECIPIENT_PAYMENT_DATA = {
            'amount' : PAYMENT_AMOUNT,
            'details': 'Payment Description',
            'sender' : self.sender.pk
        }
        self.TEST__NO_AMOUNT_PAYMENT_DATA = {
            'details': 'Payment Description',
            'sender' : self.sender.pk,
            'recipient': self.recipient.pk
        }
        self.TEST_NO_DESCRIPTION_PAYMENT_DATA = {
            'amount' : PAYMENT_AMOUNT,
            'sender' : self.sender.pk,
            'recipient': self.recipient.pk
        }

    
    def test_payment_home(self):
        request =  self.factory.get(reverse('payments:payment-home'))
        request.user = self.anonymeUser
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        login_url = reverse('accounts:login')
        response = views.payment_home(request)
        #self.assertRedirects(response, expected_url=login_url)
        self.assertEqual(response.status_code, STATUS_CODE_302)
    
    def test_payment_cannot_create_payment_anonyme(self):

        request = self.factory.post(path=PAYMENT_NEW_PAYMENT_URL, data=self.TEST_PAYMENT_DATA)

        request.user = self.anonymeUser
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.new_payment(request=request)
        
        self.assertFalse(Payment.objects.exists())
        self.assertEqual(response.status_code, STATUS_CODE_302) # redirect to login view

    def test_payment_cannot_create_payment_no_sender(self):

        request = self.factory.post(path=PAYMENT_NEW_PAYMENT_URL, data=self.TEST_NO_SENDER_PAYMENT_DATA)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.new_payment(request=request)
        
        self.assertFalse(Payment.objects.exists())
        self.assertEqual(response.status_code, STATUS_CODE_200) # failed to create the payment. redirect to the same current view Page


    
    def test_payment_cannot_create_payment_no_recipient(self):
        request = self.factory.post(path=PAYMENT_NEW_PAYMENT_URL, data=self.TEST_NO_RECIPIENT_PAYMENT_DATA)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        response = views.new_payment(request=request)
        self.assertFalse(Payment.objects.exists())
        self.assertEqual(response.status_code, STATUS_CODE_200) # failed to create the payment. redirect to same view
    
    def test_payment_cannot_create_payment_recipient_is_sender(self):

        request = self.factory.post(path=PAYMENT_NEW_PAYMENT_URL, data=self.TEST_SENDER_IS_RECIPIENT_PAYMENT_DATA)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.new_payment(request=request)
        
        
        self.assertEqual(response.status_code, STATUS_CODE_200)
        self.assertFalse(Payment.objects.exists())

    def test_payment_cannot_create_payment_recipient_is_request_user_is_not_sender(self):

        request = self.factory.post(path=PAYMENT_NEW_PAYMENT_URL, data=self.TEST_PAYMENT_DATA)

        request.user = self.no_payment_user
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.new_payment(request=request)
        
        self.assertEqual(response.status_code, STATUS_CODE_200)
        self.assertFalse(Payment.objects.exists())

    
    def test_payment_cannot_create_payment_sender_insufficient_balance(self):

        request = self.factory.post(path=PAYMENT_NEW_PAYMENT_URL, data=self.TEST_INSUFFICIENT_PAYMENT_DATA)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        Account.objects.filter(user=self.sender).update(balance=ACCOUNT_BALANCE)
        response = views.new_payment(request=request)
        
        
        account_sender = Account.objects.get(user=self.sender)
        account_recipient = Account.objects.get(user=self.recipient)
        self.assertEqual(response.status_code, STATUS_CODE_200)
        self.assertFalse(Payment.objects.exists())
        self.assertEqual(account_recipient.balance, 0)
        self.assertEqual(account_sender.balance, ACCOUNT_BALANCE)

    def test_payment_cannot_create_payment_sender_not_found(self):

        request = self.factory.post(path=PAYMENT_NEW_PAYMENT_URL, data=self.TEST_PAYMENT_DATA_SENDER_NOT_FOUND)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        Account.objects.filter(user=self.sender).update(balance=ACCOUNT_BALANCE)
        response = views.new_payment(request=request)
        
        
        account_sender = Account.objects.get(user=self.sender)
        account_recipient = Account.objects.get(user=self.recipient)
        self.assertEqual(response.status_code, STATUS_CODE_200)
        self.assertFalse(Payment.objects.exists())
        self.assertEqual(account_recipient.balance, 0)
        self.assertEqual(account_sender.balance, ACCOUNT_BALANCE)

    
    def test_payment_cannot_create_payment_recipient_not_found(self):

        request = self.factory.post(path=PAYMENT_NEW_PAYMENT_URL, data=self.TEST_PAYMENT_DATA_RECIPIENT_NOT_FOUND)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        Account.objects.filter(user=self.sender).update(balance=ACCOUNT_BALANCE)
        response = views.new_payment(request=request)
        
        
        account_sender = Account.objects.get(user=self.sender)
        account_recipient = Account.objects.get(user=self.recipient)
        self.assertEqual(response.status_code, STATUS_CODE_200)
        self.assertFalse(Payment.objects.exists())
        self.assertEqual(account_recipient.balance, 0)
        self.assertEqual(account_sender.balance, ACCOUNT_BALANCE)
        
    
    def test_payment_create_payment(self):
        request = self.factory.post(path=PAYMENT_NEW_PAYMENT_URL, data=self.TEST_PAYMENT_DATA)
        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        policy = Policy(**policy_test_data.POLICY_DATA)
        policy.save()
        policy.users.add(self.pay_user)
        Account.objects.filter(user=self.sender).update(balance=ACCOUNT_BALANCE)
        response = views.new_payment(request=request)
        
        self.assertEqual(response.status_code, STATUS_CODE_302) # succeed to create the payment. redirect to 'payments:payment-done'
        account_sender = Account.objects.get(user=self.sender)
        account_recipient = Account.objects.get(user=self.recipient)
        #self.assertEqual(account_recipient.balance, PAYMENT_AMOUNT)
        self.assertEqual(account_sender.balance, ACCOUNT_BALANCE - PAYMENT_AMOUNT)
        self.assertTrue(Payment.objects.exists())
        
    def test_payment_detail(self):
        
        self.assertFalse(Payment.objects.exists())
        payment = Payment(**self.TEST_DETAIL_PAYMENT_DATA)
        payment.full_clean()
        payment.save()
        self.assertTrue(Payment.objects.exists())
        self.assertTrue(Payment.objects.filter(payment_uuid=payment.payment_uuid).exists())

        payment_url = payment.get_absolute_url()

        request =  self.factory.get(payment_url)
        request.user = self.anonymeUser
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        response = views.payment_details(request, payment.payment_uuid )
        self.assertEqual(response.status_code, 302)

        request =  self.factory.get(payment_url)
        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        response = views.payment_details(request, payment.payment_uuid )
        self.assertEqual(response.status_code, 200)

        request =  self.factory.get(payment_url)
        request.user = self.recipient
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        response = views.payment_details(request, payment.payment_uuid )
        self.assertEqual(response.status_code, 200)

        request =  self.factory.get(payment_url)
        request.user = self.no_payment_user
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        self.assertRaises(Http404, views.payment_details, request=request, payment_uuid=payment.payment_uuid)

    
    


class TransferTest(TestCase):
    # status code = 200 --> the request failed and the the same page is shown.
    # status code = 302 (request.user = self.sender--> the request succeed and 
    # the view made a redirection to reverse('payments:transfer-done').
    # status code = 302 (request.user = self.anonymeUser--> the request failed because of the required_login decorator 
    # applied on the view new_transfer. status code 302 is the redirection to the login view.


    def setUp(self):
        self.factory = RequestFactory()
        self.sender = User.objects.create_user(username=user_test_data.USER_TEST1['username'], email=user_test_data.USER_TEST1['email'], password=user_test_data.USER_TEST1['password'])
        self.recipient = User.objects.create_user(username=user_test_data.USER_TEST2['username'], email=user_test_data.USER_TEST2['email'], password=user_test_data.USER_TEST2['password'])
        self.no_transfer_user = User.objects.create_user(username=user_test_data.USER_TEST3['username'], email=user_test_data.USER_TEST3['email'], password=user_test_data.USER_TEST3['password'])
        self.anonymeUser = AnonymousUser()
        self.TEST_TRANSFER_DATA = {
            'amount' : TRANSFER_AMOUNT,
            'details': 'Transfer Description',
            'sender' : self.sender.pk,
            'recipient': self.recipient.pk
        }

        self.TEST_TRANSFER_DATA_SENDER_NOT_FOUND = {
            'amount' : TRANSFER_AMOUNT,
            'details': 'Transfer Description',
            'sender' : user_test_data.USER_NOT_FOUND_PK,
            'recipient': self.recipient.pk
        }

        self.TEST_TRANSFER_DATA_RECIPIENT_NOT_FOUND = {
            'amount' : TRANSFER_AMOUNT,
            'details': 'Transfer Description',
            'sender' : self.sender.pk,
            'recipient': user_test_data.USER_NOT_FOUND_PK
        }

        self.TEST_INSUFFICIENT_TRANSFER_DATA = {
            'amount' : TRANSFER_AMOUNT_BIGGER_THAN_ACCOUNT_BALANCE,
            'details': 'Transfer Description',
            'sender' : self.sender.pk,
            'recipient': self.recipient.pk
        }

        self.TEST_DETAIL_TRANSFER_DATA = {
            'amount' : TRANSFER_AMOUNT,
            'details': 'Transfer Description',
            'sender' : self.sender,
            'recipient': self.recipient
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
        
        self.assertFalse(Transfer.objects.exists())
        self.assertEqual(response.status_code, STATUS_CODE_302) # redirect to login view

    def test_transfer_cannot_create_transfer_no_sender(self):

        request = self.factory.post(path=PAYMENT_NEW_TRANSFER_URL, data=self.TEST_NO_SENDER_TRANSFER_DATA)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.new_transfer(request=request)
        
        self.assertFalse(Transfer.objects.exists())
        self.assertEqual(response.status_code, STATUS_CODE_200) # failed to create the transfer. redirect to the same current view Page


    
    def test_transfer_cannot_create_transfer_no_recipient(self):
        request = self.factory.post(path=PAYMENT_NEW_TRANSFER_URL, data=self.TEST_NO_RECIPIENT_TRANSFER_DATA)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        response = views.new_transfer(request=request)
        self.assertFalse(Transfer.objects.exists())
        self.assertEqual(response.status_code, STATUS_CODE_200) # failed to create the transfer. redirect to same view
    
    def test_transfer_cannot_create_transfer_recipient_is_sender(self):

        request = self.factory.post(path=PAYMENT_NEW_TRANSFER_URL, data=self.TEST_SENDER_IS_RECIPIENT_TRANSFER_DATA)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.new_transfer(request=request)
        
        
        self.assertEqual(response.status_code, STATUS_CODE_200)
        self.assertFalse(Transfer.objects.exists())

    def test_transfer_cannot_create_transfer_recipient_is_request_user_is_not_sender(self):

        request = self.factory.post(path=PAYMENT_NEW_TRANSFER_URL, data=self.TEST_TRANSFER_DATA)

        request.user = self.no_transfer_user
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.new_transfer(request=request)
        
        self.assertEqual(response.status_code, STATUS_CODE_200)
        self.assertFalse(Transfer.objects.exists())

    
    def test_transfer_cannot_create_transfer_sender_insufficient_balance(self):

        request = self.factory.post(path=PAYMENT_NEW_TRANSFER_URL, data=self.TEST_INSUFFICIENT_TRANSFER_DATA)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        Account.objects.filter(user=self.sender).update(balance=ACCOUNT_BALANCE)
        response = views.new_transfer(request=request)
        
        
        account_sender = Account.objects.get(user=self.sender)
        account_recipient = Account.objects.get(user=self.recipient)
        self.assertEqual(response.status_code, STATUS_CODE_200)
        self.assertFalse(Transfer.objects.exists())
        self.assertEqual(account_recipient.balance, 0)
        self.assertEqual(account_sender.balance, ACCOUNT_BALANCE)

    def test_transfer_cannot_create_transfer_sender_not_found(self):

        request = self.factory.post(path=PAYMENT_NEW_TRANSFER_URL, data=self.TEST_TRANSFER_DATA_SENDER_NOT_FOUND)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        Account.objects.filter(user=self.sender).update(balance=ACCOUNT_BALANCE)
        response = views.new_transfer(request=request)
        
        
        account_sender = Account.objects.get(user=self.sender)
        account_recipient = Account.objects.get(user=self.recipient)
        self.assertEqual(response.status_code, STATUS_CODE_200)
        self.assertFalse(Transfer.objects.exists())
        self.assertEqual(account_recipient.balance, 0)
        self.assertEqual(account_sender.balance, ACCOUNT_BALANCE)

    
    def test_transfer_cannot_create_transfer_recipient_not_found(self):

        request = self.factory.post(path=PAYMENT_NEW_TRANSFER_URL, data=self.TEST_TRANSFER_DATA_RECIPIENT_NOT_FOUND)

        request.user = self.sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        Account.objects.filter(user=self.sender).update(balance=ACCOUNT_BALANCE)
        response = views.new_transfer(request=request)
        
        
        account_sender = Account.objects.get(user=self.sender)
        account_recipient = Account.objects.get(user=self.recipient)
        self.assertEqual(response.status_code, STATUS_CODE_200)
        self.assertFalse(Transfer.objects.exists())
        self.assertEqual(account_recipient.balance, 0)
        self.assertEqual(account_sender.balance, ACCOUNT_BALANCE)
        
    
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
        self.assertTrue(Transfer.objects.exists())
        
    def test_transfer_detail(self):
        
        self.assertFalse(Transfer.objects.exists())
        transfer = Transfer(**self.TEST_DETAIL_TRANSFER_DATA)
        transfer.full_clean()
        transfer.save()
        self.assertTrue(Transfer.objects.exists())
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


class ServiceTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.customer = User.objects.create_user(username=user_test_data.USER_TEST1['username'], email=user_test_data.USER_TEST1['email'], password=user_test_data.USER_TEST1['password'])
        self.operator = User.objects.create_user(username=user_test_data.USER_TEST2['username'], email=user_test_data.USER_TEST2['email'], password=user_test_data.USER_TEST2['password'])
        self.pay_user = User.objects.create_user(username=user_test_data.PAY_USER_TEST['username'], email=user_test_data.PAY_USER_TEST['email'], password=user_test_data.PAY_USER_TEST['password'])
        self.dummy_user = User.objects.create_user(username=user_test_data.USER_TEST3['username'], email=user_test_data.USER_TEST3['email'], password=user_test_data.USER_TEST3['password'])
        self.policy = Policy.objects.create(**POLICY_DATA)
        self.category = ServiceCategory.objects.create(**CATEGORY_DATA)
        

        self.AVAILABLE_SERVICE_DATA = {
                'name': AVAILABLE_SERVICE_NAME, 
                'service_code': SERVICE_CODE, 
                'description': AVAILABLE_SERVICE_DESCRIPTION,
                'category' : self.category,
                'operator' : self.operator,
                'is_active': True
        }
        self.available_service = AvailableService.objects.create(**self.AVAILABLE_SERVICE_DATA)

        self.anonymeUser = AnonymousUser()
        self.TEST_SERVICE_DATA = {
            'name'   : SERVICE_NAME,
            'price' : SERVICE_PRICE,
            'description': SERVICE_DESCRIPTION,
            'customer' : self.customer.pk,
            'operator': self.operator.pk,
            'customer_reference' : SERVICE_CUSTOMER_REFERENCE,
            'reference_number' : SERVICE_REFERENCE_NUMBER,
            'category' : self.category.pk,
            'service_instance' : self.available_service.pk,
            'issued_at' : SERVICE_ISSUED_AT,
            'commission' : SERVICE_COMMISSION
        }

        self.TEST_SERVICE_DATA_EMPTY_NAME = {
            'name'   : EMPTY_STRING,
            'price' : SERVICE_PRICE,
            'description': SERVICE_DESCRIPTION,
            'customer' : self.customer.pk,
            'operator': self.operator.pk,
            'customer_reference' : SERVICE_CUSTOMER_REFERENCE,
            'reference_number' : SERVICE_REFERENCE_NUMBER,
            'category' : self.category.pk,
            'service_instance' : self.available_service.pk,
            'issued_at' : SERVICE_ISSUED_AT,
            'commission' : SERVICE_COMMISSION
        }

        self.TEST_SERVICE_DATA_NO_NAME = {
            'price' : SERVICE_PRICE,
            'description': SERVICE_DESCRIPTION,
            'customer' : self.customer.pk,
            'operator': self.operator.pk,
            'customer_reference' : SERVICE_CUSTOMER_REFERENCE,
            'reference_number' : SERVICE_REFERENCE_NUMBER,
            'category' : self.category.pk,
            'service_instance' : self.available_service.pk,
            'issued_at' : SERVICE_ISSUED_AT,
            'commission' : SERVICE_COMMISSION
        }


        self.TEST_SERVICE_DATA_NO_CUSTOMER_REFERENCE = {
            'name'   : SERVICE_NAME,
            'price' : SERVICE_PRICE,
            'description': SERVICE_DESCRIPTION,
            'customer' : self.customer.pk,
            'operator': self.operator.pk,
            'reference_number' : SERVICE_REFERENCE_NUMBER,
            'category' : self.category.pk,
            'service_instance' : self.available_service.pk,
            'issued_at' : SERVICE_ISSUED_AT,
            'commission' : SERVICE_COMMISSION
        }

        self.TEST_SERVICE_DATA_NO_COMMISSION = {
            'name'   : SERVICE_NAME,
            'price' : SERVICE_PRICE,
            'description': SERVICE_DESCRIPTION,
            'customer' : self.customer.pk,
            'operator': self.operator.pk,
            'customer_reference' : SERVICE_CUSTOMER_REFERENCE,
            'reference_number' : SERVICE_REFERENCE_NUMBER,
            'category' : self.category.pk,
            'service_instance' : self.available_service.pk,
            'issued_at' : SERVICE_ISSUED_AT,
        }


        self.TEST_SERVICE_DATA_NO_PRICE = {
            'name'   : SERVICE_NAME,
            'description': SERVICE_DESCRIPTION,
            'customer' : self.customer.pk,
            'operator': self.operator.pk,
            'customer_reference' : SERVICE_CUSTOMER_REFERENCE,
            'reference_number' : SERVICE_REFERENCE_NUMBER,
            'category' : self.category.pk,
            'service_instance' : self.available_service.pk,
            'issued_at' : SERVICE_ISSUED_AT,
            'commission' : SERVICE_COMMISSION
        }

        self.TEST_SERVICE_DATA_NO_OPERATOR_NOT_FOUND = {
            'name'   : SERVICE_NAME,
            'price' : SERVICE_PRICE,
            'description': SERVICE_DESCRIPTION,
            'customer' : self.customer.pk,
            'operator': user_test_data.USER_NOT_FOUND_PK,
            'customer_reference' : SERVICE_CUSTOMER_REFERENCE,
            'reference_number' : SERVICE_REFERENCE_NUMBER,
            'category' : self.category.pk,
            'service_instance' : self.available_service.pk,
            'issued_at' : SERVICE_ISSUED_AT,
            'commission' : SERVICE_COMMISSION
        }

        self.TEST_SERVICE_DATA_CUSTOMER_NOT_FOUND = {
            'name'   : SERVICE_NAME,
            'price' : SERVICE_PRICE,
            'description': SERVICE_DESCRIPTION,
            'customer' : user_test_data.USER_NOT_FOUND_PK,
            'operator': self.operator.pk,
            'customer_reference' : SERVICE_CUSTOMER_REFERENCE,
            'reference_number' : SERVICE_REFERENCE_NUMBER,
            'category' : self.category.pk,
            'service_instance' : self.available_service.pk,
            'issued_at' : SERVICE_ISSUED_AT,
            'commission' : SERVICE_COMMISSION
        }
        # reference_number must be present
        self.TEST_SERVICE_DATA_NO_REFERENCE_NUMBER = {
            'name'   : SERVICE_NAME,
            'price' : SERVICE_PRICE,
            'description': SERVICE_DESCRIPTION,
            'customer' : self.customer.pk,
            'operator': self.operator.pk,
            'customer_reference' : SERVICE_CUSTOMER_REFERENCE,
            'category' : self.category.pk,
            'service_instance' : self.available_service.pk,
            'issued_at' : SERVICE_ISSUED_AT,
            'commission' : SERVICE_COMMISSION
        }

    
    def test_cannot_create_service_no_reference_number(self):
        request = self.factory.post(path=reverse(PAYMENT_NEW_SERVICE_URL, kwargs={'available_service_uuid' : self.available_service.available_uuid}), data=self.TEST_SERVICE_DATA_NO_REFERENCE_NUMBER)

        request.user = self.customer
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.new_service(request=request, available_service_uuid=self.available_service.available_uuid)
        
        self.assertFalse(Service.objects.exists())
        self.assertEqual(response.status_code, STATUS_CODE_200) # redirect to login view