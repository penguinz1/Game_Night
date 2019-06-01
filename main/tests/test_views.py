import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from accounts.models import User

# Test for the index view
class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_accessible(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

# Test for the space game view
class SpaceGameViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_accessible(self):
        response = self.client.get(reverse('space_game'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('space_game'))
        self.assertTemplateUsed(response, 'main/space_game.html')

# Test for the contact view
class ContactViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_accessible(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('contact'))
        self.assertTemplateUsed(response, 'main/create_contact.html')

# Test for the mass mail view
class MassMailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

# Test for the mass mail submit view
class MassMailSubmitViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

# Test for the mass mail test view
class MassMailTestViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

# Test for the email list index view
class EmailListIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_accessible(self):
        response = self.client.get(reverse('email_list_index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('email_list_index'))
        self.assertTemplateUsed(response, 'main/email_list_index.html')

# Test for the time-location view
class TimeLocationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_accessible(self):
        response = self.client.get(reverse('time_location'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('time_location'))
        self.assertTemplateUsed(response, 'main/time_location.html')

# Test for the add email view
class EmailListAddViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_accessible(self):
        response = self.client.get(reverse('add_email'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('add_email'))
        self.assertTemplateUsed(response, 'main/email_list_add.html')

# Test for the modify email view
class EmailListModifyViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_accessible(self):
        response = self.client.get(reverse('modify_email'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('modify_email'))
        self.assertTemplateUsed(response, 'main/email_list_modify.html')

# Test for the delete email view
class EmailListDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_accessible(self):
        response = self.client.get(reverse('delete_email'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('delete_email'))
        self.assertTemplateUsed(response, 'main/email_list_delete.html')

# Test for the random view
class RandomViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_accessible(self):
        response = self.client.get(reverse('random'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('random'))
        self.assertTemplateUsed(response, 'main/random.html')

# Test for the experimental view
class ExperimentalViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_accessible(self):
        response = self.client.get(reverse('experimental'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('experimental'))
        self.assertTemplateUsed(response, 'main/experimental.html')

# Test for the games view
class GamesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_accessible(self):
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('games'))
        self.assertTemplateUsed(response, 'main/games.html')

# Test for the game bring view
class GameBringViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass