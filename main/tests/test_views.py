import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from accounts.models import User

from main.models import Location, Meeting, Alert
from main.models import QuoteOfDay, VideoOfDay
from main.models import Contact, GameScore

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

    def test_alerts_work(self):
        Alert.objects.create(message = "This is a test", 
            time = timezone.now() + datetime.timedelta(days = 1))
        response = self.client.get(reverse('index'))
        self.assertContains(response, "This is a test")

    def test_alerts_can_be_dismissed(self):
        user = User.objects.create_user(username = 'user', password = 'generic123')
        alert = Alert.objects.create(message = "This is a test", 
            time = timezone.now() + datetime.timedelta(days = 1))
        alert.seen.add(user)
        alert.save()
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, "This is a test")

    def test_quote_of_day_scheduled_in_past(self):
        QuoteOfDay.objects.create(quote = "This is a ridiculous quote",
            speaker = "Al the man",
            time = timezone.now() - datetime.timedelta(days = 1))
        response = self.client.get(reverse('index'))
        self.assertContains(response, "This is a ridiculous quote")
        self.assertContains(response, "Al the man")

    def test_quote_of_day_scheduled_in_future(self):
        QuoteOfDay.objects.create(quote = "This is a ridiculous quote",
            speaker = "Al the man",
            time = timezone.now() + datetime.timedelta(days = 1))
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, "This is a ridiculous quote")
        self.assertNotContains(response, "Al the man")

    def test_video_of_day_scheduled_in_past(self):
        VideoOfDay.objects.create(link = "funnysite.com",
            visible_text = "A very very funny video",
            time = timezone.now() - datetime.timedelta(days = 1))
        response = self.client.get(reverse('index'))
        self.assertContains(response, "A very very funny video")
        self.assertContains(response, "href=\"funnysite.com\"")

    def test_video_of_day_scheduled_in_future(self):
        VideoOfDay.objects.create(link = "funnysite.com",
            visible_text = "A very very funny video",
            time = timezone.now() + datetime.timedelta(days = 1))
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, "A very very funny video")
        self.assertNotContains(response, "href=\"funnysite.com\"")

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

    def test_site_best_and_drifters_works(self):
        GameScore.objects.create(score = 50, drifters = 20)
        GameScore.objects.create(score = 15, drifters = 10)
        response = self.client.get(reverse('space_game'))
        self.assertContains(response, "50")
        self.assertContains(response, "20")
        self.assertNotContains(response, "15")

    def test_personal_best_works(self):
        user = User.objects.create_user(username = 'user', password = 'generic123')
        GameScore.objects.create(score = 50, drifters = 20)
        GameScore.objects.create(score = 15, drifters = 10, player = user)
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('space_game'))
        self.assertContains(response, "15")

    def test_score_post_no_user(self):
        response = self.client.post(reverse('space_game'),
            data = {'score': 42, 'drifters': 22})
        self.assertEqual(GameScore.objects.all().count(), 1)
        self.assertEqual(GameScore.objects.all()[0].score, 42)
        self.assertEqual(GameScore.objects.all()[0].drifters, 22)

    def test_score_post_with_user(self):
        user = User.objects.create_user(username = 'user', password = 'generic123')
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('space_game'),
            data = {'score': 42, 'drifters': 22})
        self.assertEqual(GameScore.objects.all()[0].player, user)

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

    def test_form_filled_correctly_no_email(self):
        response = self.client.post(reverse('contact'),
            data = {'message': 'my message'})
        self.assertEqual(Contact.objects.all().count(), 1)

    def test_form_filled_correctly_with_email(self):
        response = self.client.post(reverse('contact'),
            data = {'message': 'my message', 'email': 'test@example.com'})
        self.assertEqual(Contact.objects.all().count(), 1)

    def test_form_filled_incorrectly_blank(self):
        response = self.client.post(reverse('contact'))
        self.assertFormError(response, 'form', 'message', 'This field is required.')
        self.assertEqual(Contact.objects.all().count(), 0)

    def test_form_filled_incorrectly_no_message(self):
        response = self.client.post(reverse('contact'),
            data = {'email': 'test@example.com'})
        self.assertFormError(response, 'form', 'message', 'This field is required.')
        self.assertEqual(Contact.objects.all().count(), 0)

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

    def test_inaccessible_without_meeting(self):
        response = self.client.get(reverse('game_bring'))
        self.assertEqual(response.status_code, 404)

    def test_inaccessible_with_past_meeting(self):
        # meeting in the past
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        Meeting.objects.create(time = timezone.now() - datetime.timedelta(days = 1), location = location)
        response = self.client.get(reverse('game_bring'))
        self.assertEqual(response.status_code, 404)

    def test_accessible_with_future_meeting(self):
        # meeting in the past
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), location = location)
        response = self.client.get(reverse('game_bring'))
        self.assertEqual(response.status_code, 200)

