import os
import django

from django.test import Client, TestCase
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from rest_framework import status

from app.models import Machine, Wallet


class TestMachine(TestCase):
    """
        Test methods for creating machines and wallets
    """
  

    def setUp(self):
        Machine.objects.create(
            name='Westfield',
            password=make_password('west123', salt=None, hasher='pbkdf2_sha256'),
            token='LuGYrgCauTUVSwwLlfzmMcTjaTjoPQftigwcnfaFDbZNotmJiDRAShiDbqrfWFnx'
        )
        Machine.objects.create(
            name='Piccadilly',
            password=make_password('pic123', salt=None, hasher='pbkdf2_sha256'),
            token='yfUEOszruEoHTGrpzfegPETnzQQWuWzsBFcNlvNfBSFxlgrFaAkufLeiOnRGzCSW	'
        )
        Machine.objects.create(
            name='Green Park',
            password=make_password('green123', salt=None, hasher='pbkdf2_sha256'),
            token='KtrlsZzCjEmrZTEHNrFjlWqMNLkBJSqWgipqXnRYnNNQfjXQEzgakExFgiOixStR'
        )
        machine_01 = Machine.objects.get(name='Westfield')
        machine_02 = Machine.objects.get(name='Piccadilly')

        list_wallet_units = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
        for i in list_wallet_units:
            Wallet.objects.create(machine=machine_01, units=i)
            Wallet.objects.create(machine=machine_02, units=i)

    machine_01 = Machine.objects.get(name='Westfield')
    machine_02 = Machine.objects.get(name='Piccadilly')

    def test_password_token(self):

        self.assertTrue(check_password('west123', self.machine_01.password))
        self.assertTrue(check_password('pic123', self.machine_02.password))

        self.assertEqual('LuGYrgCauTUVSwwLlfzmMcTjaTjoPQftigwcnfaFDbZNotmJiDRAShiDbqrfWFnx', self.machine_01.token)
        self.assertEqual('yfUEOszruEoHTGrpzfegPETnzQQWuWzsBFcNlvNfBSFxlgrFaAkufLeiOnRGzCSW	', self.machine_02.token)

    def test_wallets(self):
        list_wallet = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
        for i in list_wallet:
            Wallet.objects.create(machine=self.machine_01, units=i)

        wallet_list = Wallet.objects.filter(machine=self.machine_01)
        wallet_1 = wallet_list.get(units=1)
        wallet_2 = wallet_list.get(units=1000)
        self.assertEqual(wallet_list.count(), 12)
        self.assertEqual(wallet_1.amount, 0)
        self.assertEqual(wallet_2.amount, 0)

    def test_create_machine(self):
        client = Client()
        data = {'name': 'Machine name 923',
                'password': 'test923'}
        response = client.post(reverse('create_machine'),
                               data=data,
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auth_machine(self):
        client = Client()
        data = {'name': 'Machine Test33',
                'password': 'test33'}
        response = client.post(reverse('get_token'),
                               data=data,
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_machine_without_token(self):
        client = Client()
        response = client.get(reverse('send_money'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_machine_with_token(self):
        client = Client()
        response = client.get(reverse('send_money'),
                              content_type='application/json',
                              HTTP_AUTHORIZATION='JWT LuGYrgCauTUVSwwLlfzmMcTjaTjoPQftigwcnfaFDbZNotmJiDRAShiDbqrfWFnx')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_password(self):
        client = Client()
        data = {'password': 'new_pass123'}
        response_1 = client.post(reverse('set_password'),
                                 data=data,
                                 content_type='application/json',
                                 HTTP_AUTHORIZATION='JWT test333token333machine333pic123')
        response_2 = client.post(reverse('set_password'),
                                 data=data,
                                 content_type='application/json',
                                 HTTP_AUTHORIZATION='JWT bad_token')

        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_403_FORBIDDEN)

    def test_check_password(self):
        client = Client()
        data = {'password': 'pic123'}
        response = client.post(reverse('check_password'),
                               data=data,
                               content_type='application/json',
                               HTTP_AUTHORIZATION='JWT yfUEOszruEoHTGrpzfegPETnzQQWuWzsBFcNlvNfBSFxlgrFaAkufLeiOnRGzCSW	')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wallet(self):
        client = Client()
        data = {"1 pence": 1, "2 pence": 2, "5 pence": 3, "10 pence": 4, "20 pence": 5, "50 pence": 6,
                "1 pound": 7, "2 pound": 8, "5 pound": 9, "10 pound": 11, "20 pound": 12, "50 pound": 13}
        response = client.post(reverse('update_wallet'),
                               data=data,
                               content_type='application/json',
                               HTTP_AUTHORIZATION='JWT yfUEOszruEoHTGrpzfegPETnzQQWuWzsBFcNlvNfBSFxlgrFaAkufLeiOnRGzCSW	')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_send_money(self):
        client = Client()
        data = {'send_money': {"1 pence": 1, "2 pence": 2, "5 pence": 3, "10 pence": 4, "20 pence": 5, "50 pence": 6,
                "1 pound": 7, "2 pound": 8, "5 pound": 9, "10 pound": 11, "20 pound": 12, "50 pound": 13}}
        response = client.post(reverse('send_money'),
                               data=data,
                               content_type='application/json',
                               HTTP_AUTHORIZATION='JWT yfUEOszruEoHTGrpzfegPETnzQQWuWzsBFcNlvNfBSFxlgrFaAkufLeiOnRGzCSW	')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
