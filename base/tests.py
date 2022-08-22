from django.test import Client
from django.test import TestCase
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.urls import reverse

from .models import Task, User
from .forms import UserRegistrationForm


class TaskTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        user1 = User.users.create(
            email="test1@gmail.com", name="Test Case", password=make_password('1234'))
        user2 = User.users.create(
            email="test2@gmail.com", name="Test Task", password=make_password('1234'))
        Task.tasks.create(user=user1, title="Test 1",
                          description="Test Description 1")
        Task.tasks.create(user=user2, title="Test 2",
                          description="Test Description 2")
        Task.tasks.create(user=user1, title="Test 3",
                          description="Test Description 3", complete=True)

    def test_user_tasks_show_only(self):
        user = User.users.get(email="test1@gmail.com")
        tasks = Task.tasks.filter(user=user)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Test 1")
        self.assertEqual(tasks[1].title, "Test 3")
        self.assertTrue(tasks[1].complete)

    def test_create_same_user(self):
        user = User(email="test2@gmail.com", name="Test Task",
                    password=make_password('1234'))
        with self.assertRaises(Exception) as raised:
            user.save()
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_login(self):
        url = reverse('base:login')
        response = self.client.post(
            url, {'username': 'test1@gmail.com', 'password': '1234'}, follow=True)
        self.assertTrue(response.context['user'].is_active)
        self.assertFalse(response.context['user'].is_admin)

    def test_register(self):
        url = reverse('base:register')

        self.client.post(url, {
            'email': 'test3@gmail.com',
            'name': 'Test Register',
            'city': 'Okara',
            'age': 12,
            'password1': 'Abc_1234.',
            'password2': 'Abc_1234.',
        })
        user3 = User.users.get(id=3)
        self.assertEqual(user3.email, 'test3@gmail.com')

        self.client.post(url, {
            'email': 'test4@gmail.com',
            'name': 'Test Register',
            'password1': '1234',
            'password2': '1234',
        })
        with self.assertRaises(Exception) as raised:
            user4 = User.users.get(id=4)
        self.assertEqual(User.DoesNotExist, type(raised.exception))

        self.client.post(url, {
            'email': 'test4@gmail.com',
            'password1': 'Abc_1234.',
            'password2': 'Abc_1234.',
        })
        with self.assertRaises(Exception) as raised:
            user4 = User.users.get(id=4)
        self.assertEqual(User.DoesNotExist, type(raised.exception))


class TestForms(TestCase):
    def test_form_valid_with_all_fields(self):
        form = UserRegistrationForm({
            'email': 'test3@gmail.com',
            'name': 'Test Register',
            'city': 'Okara',
            'age': 12,
            'password1': 'Abc_1234.',
            'password2': 'Abc_1234.',
        })
        self.assertTrue(form.is_valid())

    def test_form_valid__with_required_fields(self):
        form = UserRegistrationForm({
            'email': 'test3@gmail.com',
            'name': 'Test Register',
            'password1': 'Abc_1234.',
            'password2': 'Abc_1234.',
        })
        self.assertTrue(form.is_valid())

    def test_form_without_name(self):
        form = UserRegistrationForm({
            'email': 'test3@gmail.com',
            'password1': 'Abc_1234.',
            'password2': 'Abc_1234.',
        })
        self.assertFalse(form.is_valid())

    def test_form__with_invalid_password(self):
        form = UserRegistrationForm({
            'email': 'test3@gmail.com',
            'name': 'Test Register',
            'password1': '1234',
            'password2': '1234',
        })
        self.assertFalse(form.is_valid())
