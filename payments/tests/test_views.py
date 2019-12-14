from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from payments import views


def add_middledware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


def add_middledware_to_response(request, middleware_class):
    middleware = middleware_class()
    middleware.process_response(request)
    return request



class PaymentHomeTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()


    
    def test_payment_home(self):
        request =  self.factory.get('/payments/')
        request.user = AnonymousUser()
        request = add_middledware_to_request(request, SessionMiddleware)
        request.session.save()

        response = views.payment_home(request)