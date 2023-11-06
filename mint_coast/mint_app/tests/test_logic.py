from django.test import TestCase
from mint_app.models import MUser, Category
from django.contrib.auth.models import User
import hashlib
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from mint_app.serializers import CategorySerializer


class LogicTestCase(TestCase):
    def test_set_up(self):
        email = 'testmail@mail.ru'
        psw = '123456'
        first_name = 'TestUser'
        last_name = 'TestSurname'
        user = User.objects.create_user(username=email, password=psw, email=email, first_name=first_name, last_name=last_name)
        MUser.objects.create(first_name=first_name, last_name=last_name, password=hashlib.sha384(bytes(psw, 'utf-8')).hexdigest(), email='testmail@mail.ru', user=user)


class CategoryApiTestCase(APITestCase):
    def test_get(self):
        categ1 = Category.objects.create(name="secondary", path="/sec/")
        categ2 = Category.objects.create(name="thirdary", path="/thr/")
        url = reverse('category-list')
        response = self.client.get(url)
        serializer_data = CategorySerializer([categ1, categ2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
