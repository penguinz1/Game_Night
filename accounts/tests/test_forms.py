from django.test import TestCase

from accounts.forms import RegistrationForm, ProfileChangeForm

# Testing for the RegistrationForm
class RegistrationFormTest(TestCase):
    def test_email_field_label(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['email'].label == 'Email')

    def test_first_name_field_label(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['first_name'].label == 'First Name')

    def test_last_name_field_label(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['last_name'].label == 'Last Name')

    def test_email_field_help_text(self):
        form = RegistrationForm()
        self.assertEqual(form.fields['email'].help_text,
            "Enter an email address (optional).")

    def test_first_name_help_text(self):
        form = RegistrationForm()
        self.assertEqual(form.fields['first_name'].help_text,
            "Enter your first name (optional).")

    def test_last_name_help_text(self):
        form = RegistrationForm()
        self.assertEqual(form.fields['last_name'].help_text,
            "Enter your last name (optional).")

    def test_valid_form_no_optionals(self):
        form = RegistrationForm(data = {
            'username': 'user',
            'password1': 'generic123',
            'password2': 'generic123'
        })
        self.assertTrue(form.is_valid())

    def test_valid_form_with_optionals(self):
        form = RegistrationForm(data = {
            'username': 'user',
            'password1': 'generic123',
            'password2': 'generic123',
            'email': 'test@example.com',
            'first_name': 'john',
            'last_name': 'doe'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form_bad_password(self):
        form = RegistrationForm(data = {
            'username': 'user',
            'password1': 'pass',
            'password2': 'pass'
        })
        self.assertFalse(form.is_valid())

    def test_invalid_form_unmatching_passsword(self):
        form = RegistrationForm(data = {
            'username': 'user',
            'password1': 'generic123',
            'password2': 'notgeneric123'
        })
        self.assertFalse(form.is_valid())

# Testing for the ProfileChangeForm
class ProfileChangeFormTest(TestCase):
    def test_email_field_label(self):
        form = ProfileChangeForm()
        self.assertTrue(form.fields['email'].label == 'Email')

    def test_first_name_field_label(self):
        form = ProfileChangeForm()
        self.assertTrue(form.fields['first_name'].label == 'First Name')

    def test_last_name_field_label(self):
        form = ProfileChangeForm()
        self.assertTrue(form.fields['last_name'].label == 'Last Name')

    def test_email_field_help_text(self):
        form = ProfileChangeForm()
        self.assertEqual(form.fields['email'].help_text,
            "Enter an email address (optional).")

    def test_first_name_help_text(self):
        form = ProfileChangeForm()
        self.assertEqual(form.fields['first_name'].help_text,
            "Enter your first name (optional).")

    def test_last_name_help_text(self):
        form = ProfileChangeForm()
        self.assertEqual(form.fields['last_name'].help_text,
            "Enter your last name (optional).")

    def test_valid_form_one_optional(self):
        form = ProfileChangeForm(data = {
            'email': 'test@example.com'
        })
        self.assertTrue(form.is_valid())

    def test_valid_form_with_optionals(self):
        form = ProfileChangeForm(data = {
            'email': 'test@example.com',
            'first_name': 'john',
            'last_name': 'doe'
        })
        self.assertTrue(form.is_valid())