from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student

# from django.contrib.auth import login, logout

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        # create users
        user1 = User.objects.create_user(username="user1",password="password1")
        user2 = User.objects.create_user(username="user2",password="password2", is_staff=True)
        student1 = Student.objects.create(ID=user1, fname="first1", lname="last1", email="user@mail.com")
        self.staff_user = User.objects.create_user(
            username='admin',
            password='admin1234',
            is_staff=True
        )
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
        
    def test_login_as_staff(self):
        c = Client()
        form = {'username': "admin", 'password' : "admin1234"}
        response = c.post(reverse('login'), form)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue(response.context['user'].is_staff)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course/page_user.html')
        self.assertTrue(response.context['admin'])


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