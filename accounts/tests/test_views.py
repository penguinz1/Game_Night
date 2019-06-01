from django.test import TestCase
from django.urls import reverse

# Test for the sign up view
class SignUpViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_accessible(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'signup.html')

# Test for the logout view
class LogoutViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

# Test for the profile view
class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

# Test for the update password view
class UpdatePasswordViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

# Test for the update profile view
class UpdateProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass