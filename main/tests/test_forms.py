import datetime

from django.test import TestCase
from django.utils import timezone

from main.models import EmailAddress
from main.forms import CreateContactForm, GameBringForm
from main.forms import MassEmailForm, TestEmailForm
from main.forms import AddMailForm, ModifyMailForm, DeleteMailForm

# Testing for the CreateContactForm
class CreateContactFormTest(TestCase):
    def test_message_field_label(self):
        form = CreateContactForm()
        self.assertTrue(form.fields['message'].label == None
            or form.fields['message'].label == 'message')

    def test_email_field_label(self):
        form = CreateContactForm()
        self.assertTrue(form.fields['email'].label == None
            or form.fields['email'].label == 'email')

    def test_message_help_text(self):
        form = CreateContactForm()
        self.assertEqual(form.fields['message'].help_text,
            "Enter your message (max 500 characters).")

    def test_email_help_text(self):
        form = CreateContactForm()
        self.assertEqual(form.fields['email'].help_text,
            "Enter your email address (optional). This is best used if you want us to contact you back.")

    def test_valid_form_no_email(self):
        form = CreateContactForm(data = {
            'message': 'a message'
        })
        self.assertTrue(form.is_valid())

    def test_valid_form_with_email(self):
        form = CreateContactForm(data = {
            'message': 'a message',
            'email': 'test@example.com'
        })
        self.assertTrue(form.is_valid())

# Testing for the MassEmailForm
class MassEmailFormTest(TestCase):
    def test_subject_field_label(self):
        form = MassEmailForm()
        self.assertTrue(form.fields['subject'].label == None
            or form.fields['subject'].label == 'subject')

    def test_content_field_label(self):
        form = MassEmailForm()
        self.assertTrue(form.fields['content'].label == None
            or form.fields['content'].label == 'content')

    def test_subject_help_text(self):
        form = MassEmailForm()
        self.assertEqual(form.fields['subject'].help_text,
            "Enter the subject line of the mass email (max 200 characters).")

    def test_content_help_text(self):
        form = MassEmailForm()
        self.assertEqual(form.fields['content'].help_text,
            "Enter the content of the mass email.")

# Testing for the TestEmailForm
class TestEmailFormTest(TestCase):
    def test_recipient_field_label(self):
        form = TestEmailForm()
        self.assertTrue(form.fields['recipient'].label == None
            or form.fields['recipient'].label == 'recipient')

    def test_recipient_help_text(self):
        form = TestEmailForm()
        self.assertEqual(form.fields['recipient'].help_text,
            "Enter an email address that will receive the mass email.")

# Testing for the AddMainForm
class AddMailFormTest(TestCase):
    def test_new_mail_field_label(self):
        form = AddMailForm()
        self.assertTrue(form.fields['new_mail'].label == None
            or form.fields['new_mail'].label == 'new_mail')

    def test_name_field_label(self):
        form = AddMailForm()
        self.assertTrue(form.fields['name'].label == None
            or form.fields['name'].label == 'name')

    def test_new_mail_help_text(self):
        form = AddMailForm()
        self.assertEqual(form.fields['new_mail'].help_text,
            "Enter a new email address to add to the mailing list.")

    def test_name_help_text(self):
        form = AddMailForm()
        self.assertEqual(form.fields['name'].help_text,
            "Enter your name (first and last please).")

    def test_valid_form(self):
        form = AddMailForm(data = {
            'new_mail': 'test@example.com',
            'name': 'john doe'
        })
        self.assertTrue(form.is_valid())

    def test_email_already_in_database(self):
        EmailAddress.objects.create(email = 'test@example.com', name = 'john doe')
        form = AddMailForm(data = {
            'new_mail': 'test@example.com',
            'name': 'jane doe'
        })
        self.assertFalse(form.is_valid())

    def test_unrelated_email_in_database(self):
        EmailAddress.objects.create(email = 'train@example.com', name = 'john doe')
        form = AddMailForm(data = {
            'new_mail': 'test@example.com',
            'name': 'jane doe'
        })
        self.assertTrue(form.is_valid())

# Testing for the ModifyMailForm
class ModifyMailFormTest(TestCase):
    def test_old_mail_field_label(self):
        form = ModifyMailForm()
        self.assertTrue(form.fields['old_mail'].label == None
            or form.fields['old_mail'].label == 'old_mail')

    def test_new_mail_field_label(self):
        form = ModifyMailForm()
        self.assertTrue(form.fields['new_mail'].label == None
            or form.fields['new_mail'].label == 'new_mail')

    def test_old_mail_help_text(self):
        form = ModifyMailForm()
        self.assertEqual(form.fields['old_mail'].help_text,
            "Enter an email address already on the mailing list where you no longer want to receive emails.")

    def test_new_mail_help_text(self):
        form = ModifyMailForm()
        self.assertEqual(form.fields['new_mail'].help_text,
            "Enter a new email address that will replace the old email address on the mailing list.")

    def test_valid_form(self):
        EmailAddress.objects.create(email = 'train@example.com', name = 'john doe')
        form = ModifyMailForm(data = {
            'old_mail': 'train@example.com',
            'new_mail': 'test@example.com'
        })
        self.assertTrue(form.is_valid())

    def test_old_email_not_in_database(self):
        form = ModifyMailForm(data = {
            'old_mail': 'train@example.com',
            'new_mail': 'test@example.com'
        })
        self.assertFalse(form.is_valid())

    def test_new_email_in_database(self):
        EmailAddress.objects.create(email = 'test@example.com', name = 'john doe')
        form = ModifyMailForm(data = {
            'old_mail': 'train@example.com',
            'new_mail': 'test@example.com'
        })
        self.assertFalse(form.is_valid())

    def test_old_and_new_email_in_database(self):
        EmailAddress.objects.create(email = 'train@example.com', name = 'john doe')
        EmailAddress.objects.create(email = 'test@example.com', name = 'john doe')
        form = ModifyMailForm(data = {
            'old_mail': 'train@example.com',
            'new_mail': 'test@example.com'
        })
        self.assertFalse(form.is_valid())

# Testing for the DeleteMailForm
class DeleteMailFormTest(TestCase):
    def test_delete_mail_field_label(self):
        form = DeleteMailForm()
        self.assertTrue(form.fields['delete_mail'].label == None
            or form.fields['delete_mail'].label == 'delete_mail')

    def test_delete_mail_help_text(self):
        form = DeleteMailForm()
        self.assertEqual(form.fields['delete_mail'].help_text,
            "Enter an email address to be deleted from the mailing list.")

    def test_valid_form(self):
        EmailAddress.objects.create(email = 'test@example.com', name = 'john doe')
        form = DeleteMailForm(data = {
            'delete_mail': 'test@example.com'
        })
        self.assertTrue(form.is_valid())

    def test_delete_email_not_in_database(self):
        form = DeleteMailForm(data = {
            'delete_mail': 'test@example.com'
        })
        self.assertFalse(form.is_valid())

    def test_unrelated_email_in_database(self):
        EmailAddress.objects.create(email = 'train@example.com', name = 'john doe')
        form = DeleteMailForm(data = {
            'delete_mail': 'test@example.com'
        })
        self.assertFalse(form.is_valid())

# Testing for the GameBringForm
class GameBringFormTest(TestCase):
    def test_game_field_label(self):
        form = GameBringForm()
        self.assertTrue(form.fields['game'].label == None
            or form.fields['game'].label == 'game')

    def test_person_field_label(self):
        form = GameBringForm()
        self.assertTrue(form.fields['person'].label == None
            or form.fields['person'].label == 'person')

    def test_game_help_text(self):
        form = GameBringForm()
        self.assertEqual(form.fields['game'].help_text,
            "Enter a game that you will bring to the next meeting (max 100 characters).")

    def test_person_help_text(self):
        form = GameBringForm()
        self.assertEqual(form.fields['person'].help_text,
            "Enter your name (optional).")

    def test_valid_form_no_person(self):
        form = GameBringForm(data = {
            'game': 'generic game'
        })
        self.assertTrue(form.is_valid())

    def test_valid_form_with_person(self):
        form = GameBringForm(data = {
            'game': 'generic game',
            'person': 'john doe'
        })
        self.assertTrue(form.is_valid())
