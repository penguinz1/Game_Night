from django.test import TestCase
from django.urls import reverse

from accounts.models import User

# Test for the sign up view
class SignUpViewTest(TestCase):
    def test_view_url_accessible(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'signup.html')

    def test_form_filled_incorrectly_blank(self):
        response = self.client.post(reverse('signup'))
        self.assertFormError(response, 'form', 'username', 'This field is required.')

    def test_form_filled_incorrectly_new_passwords_dont_match(self):
        response = self.client.post(reverse('signup'),
            data = {'username': 'user', 'password1': 'gamma123', 'password2': 'webmaster987'})
        self.assertFormError(response, 'form', 'password2', "The two password fields didn't match.")  

    def test_form_filled_correctly(self):
        response = self.client.post(reverse('signup'),
            data = {'username': 'user', 'password1': 'generic123', 'password2': 'generic123'},
            follow = True)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.all()[0].username, 'user')

# Test for the logout view
class LogoutViewTest(TestCase):
    def test_log_out(self):
        User.objects.create_user(username = 'user', password = 'generic123')
        self.client.login(username = 'user', password = 'generic123')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(reverse('logout') + "?next=" + reverse('index'), follow = True)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertRedirects(response, reverse('index'))
        self.assertContains(response, "Successfully Logged Out!")

# Test for the profile view
class ProfileViewTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('profile'))

    def test_accessible_if_logged_in(self):
        User.objects.create_user(username = 'user', password = 'generic123')
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)     

# Test for the update password view
class UpdatePasswordViewTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('password'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('password'))

    def test_accessible_if_logged_in(self):
        User.objects.create_user(username = 'user', password = 'generic123')
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('password'))
        self.assertEqual(response.status_code, 200)  

    def test_form_filled_incorrectly_blank(self):
        User.objects.create_user(username = 'user', password = 'generic123')
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('password'))
        self.assertFormError(response, 'form', 'old_password', 'This field is required.')  

    def test_form_filled_incorrectly_old_password_wrong(self):
        User.objects.create_user(username = 'user', password = 'generic123')
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('password'),
            data = {'old_password': 'gamma123', 'new_password1': 'webmaster987', 'new_password2': 'webmaster987'})
        self.assertFormError(response, 'form', 'old_password', 
            'Your old password was entered incorrectly. Please enter it again.')  

    def test_form_filled_incorrectly_new_passwords_dont_match(self):
        User.objects.create_user(username = 'user', password = 'generic123')
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('password'),
            data = {'old_password': 'generic123', 'new_password1': 'gamma123', 'new_password2': 'webmaster987'})
        self.assertFormError(response, 'form', 'new_password2', "The two password fields didn't match.")  

    def test_form_filled_correctly(self):
        User.objects.create_user(username = 'user', password = 'generic123')
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('password'),
            data = {'old_password': 'generic123', 'new_password1': 'webmaster987', 'new_password2': 'webmaster987'},
            follow = True)
        self.assertRedirects(response, reverse('profile'))
        self.assertContains(response, "Successfully Changed Password!")

# Test for the update profile view
class UpdateProfileViewTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('profile_change'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('profile_change'))

    def test_accessible_if_logged_in(self):
        User.objects.create_user(username = 'user', password = 'generic123')
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('profile_change'))
        self.assertEqual(response.status_code, 200)    

    def test_form_filled(self):
        User.objects.create_user(username = 'user', password = 'generic123')
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('profile_change'),
            data = {'email': 'test@example.com'}, follow = True)
        self.assertRedirects(response, reverse('profile'))
        self.assertContains(response, "Successfully Updated Profile!")
        self.assertEqual(User.objects.all()[0].email, 'test@example.com')
