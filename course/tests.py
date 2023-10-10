from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Course, Enroll
from users.models import Student

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


# from django.contrib.auth import login, logout

# Create your tests here.
class CourseTestCase(TestCase):
    def setUp(self):
        # create users
        user1 = User.objects.create_user(username="user1",password="password1")
        user2 = User.objects.create_user(username="user2",password="password2", is_staff=True)

        student1 = Student.objects.create(ID=user1, fname="first1", lname="last1", email="user@mail.com")

        course1 = Course.objects.create(ID="CN331", name="Software Engineering", quota=True, enrolled=0)
        course2 = Course.objects.create(ID="CN360", name="Microcontroller", quota=True, enrolled=0)
        course_neg = Course.objects.create(ID="CN321", name="Network", quota= -1, enrolled=0)

        course2.quota -= 1
        course2.enrolled += 1
        course_enroll = Enroll.objects.create(student_id=user1, course_id=course2)

        course_enroll.save()
        course_neg.save()
        course1.save()
        course2.save()
        user1.save()
        user2.save()
        student1.save()
    
    def test_model_course_str(self):
            course = Course.objects.get(ID="CN331")
            self.assertEqual(str(course), "CN331 Software Engineering - 1")

    def test_index(self):
        c = Client()
        c.login(username='user1', password="password1")
        response = c.get(reverse('course'))
        self.assertEqual(response.status_code, 200)

    def test_page_course(self):
        c = Client()
        c.login(username="user1", password="password1")
        response = c.get(reverse('page_course'))
        self.assertEqual(response.status_code, 200)
    
    def test_page_user(self):
        c = Client()
        c.login(username="user1", password="password1")
        response = c.get(reverse('page_user'))
        self.assertEqual(response.status_code, 200)

    def test_page_user_staff(self):
        c = Client()
        c.login(username="user2", password="password2")
        response = c.get(reverse('page_user'))
        self.assertEqual(response.status_code, 200)

    def test_page_board(self):
        c = Client()
        c.login(username="user1", password="password1")
        response = c.get(reverse('page_board'))
        self.assertEqual(response.status_code, 200)

    def test_course_enroll_admin(self):
        c = Client()
        c.login(username="user2", password="password2")
        response = c.get(reverse('course_enroll'))
        self.assertEqual(response.status_code, 200)

    def test_course_enroll_quota_less_zero(self):
        c = Client()
        c.login(username="user1", password="password1")
        response = c.post(reverse('course_enroll'), {"course_id" : "CN321"})
        self.assertEqual(response.status_code, 200)

    def test_course_enroll_success(self):
        c = Client()
        c.login(username="user1", password="password1")
        response = c.post(reverse('course_enroll'), {"course_id" : "CN331"})
        self.assertEqual(response.status_code, 200)

    def test_course_drop_admin(self):
        c = Client()
        c.login(username="user2", password="password2")
        user1 = User.objects.get(username="user1")
        cn360 = Course.objects.get(ID="CN360")
        # # cn360_enroll = Enroll.objects.create(student_id=user1, course_id=cn360)
        # cn360.enrolled += 1
        # cn360.quota -= 1
        # cn360.save()
        self.assertEqual(cn360.enrolled, 1)
        response = c.post(reverse('course_drop'), {"user_id" : "user1", "course_id" : "CN360"})
        # self.assertEqual(cn360.enrolled, 0)
        # course_enroll = Enroll.objects.get(student_id='user1', course_id=course) 
        # course_enroll.delete() 
        self.assertEqual(response.status_code, 200)


    def test_course_drop_user(self):
        c = Client()
        c.login(username="user1", password="password1")
        user1 = User.objects.get(username="user1")
        cn360 = Course.objects.get(ID="CN360")
        self.assertEqual(cn360.enrolled, 1)
        response = c.post(reverse('course_drop'), {"user_id" : "user1", "course_id" : "CN360"})
        self.assertEqual(response.status_code, 200)

    def test_manager_get(self):
        c = Client()
        c.login(username="user2", password="password2")
        response = c.get(reverse('manager'))
        self.assertEqual(response.status_code, 200)


class CourseTestCase_Zero(TestCase):
    def setUp(self):
        # create users
        user1 = User.objects.create_user(username="user1",password="password1")
        user2 = User.objects.create_user(username="user2",password="password2", is_staff=True)

        student1 = Student.objects.create(ID=user1, fname="first1", lname="last1", email="user@mail.com")
        user1.save()
        user2.save()
        student1.save()

    def test_manager_dropdown_zero(self):
        c = Client()
        c.login(username="user2", password="password2")
        response = c.post(reverse('manager'))
        self.assertEqual(response.status_code, 200)