from django.urls import resolve
from django.test import TestCase
import unittest
#from django.contrib.auth import views as auth_views
from voucher import views


class VouchersViewsUrlTest(TestCase):
    def test_voucher_home_url(self):
        found = resolve('/voucher/')
        self.assertEqual(found.func, views.voucher_home)

    def test_vouchers_url(self):
        found = resolve('/voucher/vouchers/')
        self.assertEqual(found.func, views.vouchers)


    def test_voucher_details_url(self):
        found = resolve('/voucher/voucher_details/10/')
        self.assertEqual(found.func, views.voucher_details)


    def test_used_vouchers_url(self):
        found = resolve('/voucher/used_vouchers/')
        self.assertEqual(found.func, views.used_vouchers)


    def test_used_voucher_details_url(self):
        found = resolve('/voucher/used_voucher_details/10/')
        self.assertEqual(found.func, views.used_voucher_details)

    
    def test_sold_vouchers_url(self):
        found = resolve('/voucher/sold_vouchers/')
        self.assertEqual(found.func, views.sold_vouchers)


    def test_sold_voucher_details_url(self):
        found = resolve('/voucher/sold_voucher_details/10/')
        self.assertEqual(found.func, views.sold_voucher_details)

