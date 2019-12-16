from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.http.response import Http404
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from payments.models import Transfer, Payment
from payments import views


def add_middledware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


def add_middledware_to_response(request, middleware_class):
    middleware = middleware_class()
    middleware.process_response(request)
    return request


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

class PaymentTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()


    
    def test_payment_home(self):
        request =  self.factory.get('/payments/')
        request.user = AnonymousUser()
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.payment_home(request)
        self.assertEqual(response.status_code, 302)
        
    def test_transfer_detail(self):
        
        sender = User.objects.create_user(username=USER_TEST1['username'], email=USER_TEST1['email'], password=USER_TEST1['password'])
        recipient = User.objects.create_user(username=USER_TEST2['username'], email=USER_TEST2['email'], password=USER_TEST2['password'])
        no_transfer_user = User.objects.create_user(username=USER_TEST3['username'], email=USER_TEST3['email'], password=USER_TEST3['password'])
        TEST_TRANSFER_DATA = {
            'amount' : 25000,
            'details': 'Transfer Description',
            'sender' : sender,
            'recipient': recipient
        }
        self.assertTrue(Transfer.objects.count() == 0)
        transfer = Transfer(**TEST_TRANSFER_DATA)
        transfer.full_clean()
        transfer.save()
        self.assertTrue(Transfer.objects.count() == 1)
        self.assertTrue(Transfer.objects.filter(transfer_uuid=transfer.transfer_uuid).exists())

        transfer_url = transfer.get_absolute_url()

        request =  self.factory.get(transfer_url)
        request.user = AnonymousUser()
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        response = views.transfer_details(request, transfer.transfer_uuid )
        self.assertEqual(response.status_code, 302)

        request =  self.factory.get(transfer_url)
        request.user = sender
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        response = views.transfer_details(request, transfer.transfer_uuid )
        self.assertEqual(response.status_code, 200)

        request =  self.factory.get(transfer_url)
        request.user = recipient
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        response = views.transfer_details(request, transfer.transfer_uuid )
        self.assertEqual(response.status_code, 200)

        request =  self.factory.get(transfer_url)
        request.user = no_transfer_user
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()
        self.assertRaises(Http404, views.transfer_details, request=request, transfer_uuid=transfer.transfer_uuid)
