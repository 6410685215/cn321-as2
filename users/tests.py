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
    
    def test_models_student_tostr(self):
        student1 = Student.objects.get(fname="first1")
        self.assertEqual(str(student1),"user1 | user@mail.com")

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

    def test_login_get(self):
        c = Client()
        response = c.get("")
        self.assertEqual(response.status_code, 200)

    def test_login_as_user(self):
        c = Client()
        form = {'username': "user1", 'password' : "password1"}
        response = c.post(reverse('login'), form)
        self.assertEqual(response.status_code, 200)
        
    def login_as_staff(self):
        self.client = Client()
        # form = {'username': "user2", 'password': "password2"}
        # user2 = User.objects.get(username='user2')
        # self.assertEqual(user2.is_staff, True)
        # login_already = c.login(username="user2", password="password2")
        # self.assertEqual(login_already, True)
        # response = c.post(reverse('login'), form)
        # self.assertEqual(response.status_code, 200)
        # Attempt login as staff user
        response = self.client.post(reverse('login'), {'username': 'user2', 'password': 'password2'})
        self.assertEqual(response.status_code, 200)
        # Check if the staff user is logged in
        user = User.objects.get(username='user2')
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.is_staff)


    def test_is_authenticated_wrong_pass(self):
        c = Client()
        form = {'username': "user1", 'password': "wrongpassword"}
        response = c.post(reverse('login'), form)
        self.assertEqual(response.status_code, 200)

    def test_is_authenticated_form_invalid(self):
        c = Client()
        form = {'username': "user1"}
        response = c.post(reverse('login'), form)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        c = Client()
        c.login(username="user1", password="password1")
        response = c.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
