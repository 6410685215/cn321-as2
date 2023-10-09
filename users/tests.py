from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from .forms import LoginForm

# from django.contrib.auth import login, logout

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        # create users
        user1 = User.objects.create_user(username="user1",password="password1")
        user2 = User.objects.create_user(username="user2",password="password2", is_staff=True)

        student1 = Student.objects.create(ID=user1, fname="first1", lname="last1", email="user@mail.com")


        user1.save()
        user2.save()

        student1.save()
    

    def test_annoymous(self):
        c = Client()
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_already_user(self):
        c = Client()
        c.login(username="user1", password="password1")
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_already_staff(self):
        c = Client()
        c.login(username="user2", password="password2")
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def login_get(self):
        self.client = Client()
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(, LoginForm())

    def login_as_user(self):
        self.client = Client()
        # password = make_password("password1")
        form = {'username': "user1", 'password' : "password1"}
        # c.login(username="user1", password="password1")
        # user = User.objects.get(username="user1")
        # self.assertEqual(user.is_staff, False)
        response = self.client.post(reverse('login'), form)

        self.assertEqual(response.status_code, 200)
        
    def login_as_staff(self):
        self.client = Client()
        # password = make_password("password2")
        form = {'username': "user2", 'password': "password2"}
        # c.login(username="user2", password="password2")
        # user = User.objects.get(username="user2")
        # self.assertEqual(user.is_staff, True)
        response = self.client.post(reverse('login'), form)
        self.assertEqual(response.status_code, 200)

    def test_is_authenticated_wrong_pass(self):
        c = Client()
        form = {'username': "user1", 'password': "wrongpassword"}
        # c.login(username="user1", password="wrongpassword")
        response = c.post(reverse('login'), form)
        self.assertEqual(response.status_code, 200)

    def test_is_authenticated_form_invalid(self):
        c = Client()
        form = {'username': "user1"}
        # c.login(username="user1", password="wrongpassword")
        response = c.post(reverse('login'), form)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        c = Client()
        c.login(username="user1", password="password1")
        response = c.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
