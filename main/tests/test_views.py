import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import User

from main.models import Location, Meeting, Alert
from main.models import QuoteOfDay, VideoOfDay, GameOfWeek
from main.models import Contact, GameScore, MassEmail, EmailAddress, GameBring

from main.views import get_next_meeting

# Test for the index view
class IndexViewTest(TestCase):
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

    def test_alert_expired(self):
        Alert.objects.create(message = "This is a test", 
            time = timezone.now() - datetime.timedelta(days = 1))
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, "This is a test")

    def test_alert_top_three_by_severity(self):
        Alert.objects.create(message = "This is a test1", 
            time = timezone.now() + datetime.timedelta(days = 1))
        Alert.objects.create(message = "This is a test2", 
            time = timezone.now() + datetime.timedelta(days = 1))
        Alert.objects.create(message = "This is a test3", 
            time = timezone.now() + datetime.timedelta(days = 1))
        Alert.objects.create(message = "This is a test4", 
            time = timezone.now() + datetime.timedelta(days = 1), severity = '1m') # low severity - lower priority
        response = self.client.get(reverse('index'))
        self.assertContains(response, "This is a test1")
        self.assertContains(response, "This is a test2")
        self.assertContains(response, "This is a test3")
        self.assertNotContains(response, "This is a test4")

    def test_alert_top_three_by_date(self):
        Alert.objects.create(message = "This is a test1", 
            time = timezone.now() + datetime.timedelta(days = 2)) # latest date - lower priority
        Alert.objects.create(message = "This is a test2", 
            time = timezone.now() + datetime.timedelta(days = 1))
        Alert.objects.create(message = "This is a test3", 
            time = timezone.now() + datetime.timedelta(days = 1))
        Alert.objects.create(message = "This is a test4", 
            time = timezone.now() + datetime.timedelta(days = 1))
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, "This is a test1")
        self.assertContains(response, "This is a test2")
        self.assertContains(response, "This is a test3")
        self.assertContains(response, "This is a test4")

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

# Test for updating alerts
class AlertUpdateTest(TestCase):
    def test_alert_update_works(self):
        alert = Alert.objects.create(message = 'an alert', 
            time = timezone.now() + datetime.timedelta(days = 1))
        user = User.objects.create_user(username = 'user', password = 'generic123')
        self.assertEqual(Alert.objects.filter(seen__in = [user]).count(), 0)

        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('alert'), data = {'id': 1, 'next': reverse('index')})
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Alert.objects.filter(seen__in = [user]).count(), 1)

# Test for the get_next_meeting() function
class GetNextMeetingTest(TestCase):
    def test_no_meetings(self):
        self.assertEqual(get_next_meeting(), None)

    def test_past_meeting(self):
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        Meeting.objects.create(time = timezone.now() - datetime.timedelta(days = 1), location = location)
        self.assertEqual(get_next_meeting(), None)

    def test_future_meeting(self):
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        meeting = Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), location = location)
        self.assertEqual(get_next_meeting(), meeting)

    def test_bag_of_meetings(self):
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 5), location = location)
        meeting = Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), location = location)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 3), location = location)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 4), location = location)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 2), location = location)
        Meeting.objects.create(time = timezone.now() - datetime.timedelta(days = 1), location = location)
        self.assertEqual(get_next_meeting(), meeting)

# Test for the space game view
class SpaceGameViewTest(TestCase):
    def test_view_url_accessible(self):
        response = self.client.get(reverse('space_game'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('space_game'))
        self.assertTemplateUsed(response, 'main/space_game.html')

    def test_site_best_and_drifters_works(self):
        GameScore.objects.create(score = 50, drifters = 21)
        GameScore.objects.create(score = 15, drifters = 10)
        response = self.client.get(reverse('space_game'))
        self.assertContains(response, "50") # display best score
        self.assertContains(response, "31") # display total drifters destroyed (21 + 10)
        self.assertNotContains(response, "Personal Best") # don't display a personal best score

    def test_personal_best_works(self):
        user = User.objects.create_user(username = 'user', password = 'generic123')
        GameScore.objects.create(score = 50, drifters = 20)
        GameScore.objects.create(score = 15, drifters = 10, player = user)
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('space_game'))
        self.assertContains(response, "Personal Best") # display a personal best score
        self.assertContains(response, "15") # display that score

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

    def test_form_filled_correctly_redirect(self):
        response = self.client.post(reverse('contact'),
            data = {'message': 'my message'}, follow = True)
        self.assertRedirects(response, reverse('index'))
        self.assertContains(response, 'Contact Successfully Sent!')

    def test_form_filled_incorrectly_blank(self):
        response = self.client.post(reverse('contact'))
        self.assertFormError(response, 'form', 'message', 'This field is required.')
        self.assertEqual(Contact.objects.all().count(), 0)

    def test_form_filled_incorrectly_no_message(self):
        response = self.client.post(reverse('contact'),
            data = {'email': 'test@example.com'})
        self.assertFormError(response, 'form', 'message', 'This field is required.')
        self.assertEqual(Contact.objects.all().count(), 0)

# Test for the mass mail view redirects
class MassMailViewRedirectTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('mass_mail'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('mass_mail'))

    def test_redirect_if_no_permissions(self):
        user = User.objects.create_user(username = 'user', password = 'generic123')
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('mass_mail'))

class MassMailViewNoNextMeetingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up a user with permission
        user = User.objects.create_user(username = 'user', password = 'generic123')
        permission = Permission.objects.get(name='Abilty to send club emails')
        user.user_permissions.add(permission)

    def test_access_if_has_permissions(self):
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/mass_mail.html')

    def test_display_no_next_meeting(self):
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail'))
        self.assertContains(response, 'The next meeting is not scheduled')

    def test_display_with_next_meeting_in_past(self):
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        Meeting.objects.create(time = timezone.now() - datetime.timedelta(days = 1), location = location)
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail'))
        self.assertContains(response, 'The next meeting is not scheduled')

class MassMailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up a user with permission
        user = User.objects.create_user(username = 'user', password = 'generic123')
        permission = Permission.objects.get(name='Abilty to send club emails')
        user.user_permissions.add(permission)

        # set up a meeting in the future
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), location = location)

    def test_display_with_next_meeting_in_future(self):
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail'))
        self.assertNotContains(response, 'The next meeting is not scheduled')

    def test_form_filled_incorrectly_blank(self):
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('mass_mail'))
        self.assertFormError(response, 'form', 'subject', 'This field is required.')
        self.assertFormError(response, 'form', 'content', 'This field is required.')
        self.assertEqual(MassEmail.objects.all().count(), 0)

    def test_form_filled_incorrectly_no_subject(self):
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('mass_mail'),
            data = {'content': 'This is an email'})
        self.assertFormError(response, 'form', 'subject', 'This field is required.')
        self.assertEqual(MassEmail.objects.all().count(), 0)

    def test_form_filled_incorrectly_no_content(self):
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('mass_mail'),
            data = {'subject': 'Meeting next week'})
        self.assertFormError(response, 'form', 'content', 'This field is required.')
        self.assertEqual(MassEmail.objects.all().count(), 0)

    def test_form_filled_correctly(self):
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('mass_mail'),
            data = {'subject': 'Meeting next week', 'content': 'This is an email'})
        self.assertEqual(MassEmail.objects.all().count(), 1)
        self.assertContains(response, 'Email Successfully Saved!')

    def test_form_filled_correctly_with_existing_mail(self):
        email = MassEmail.objects.create(subject = 'a subject', content = 'some content')
        meeting = Meeting.objects.get(id = 1)
        meeting.email = email
        meeting.save()
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('mass_mail'),
            data = {'subject': 'Meeting next week', 'content': 'This is an email'})
        self.assertEqual(MassEmail.objects.all().count(), 1)
        self.assertEqual(MassEmail.objects.all()[0].subject, 'Meeting next week')
        self.assertContains(response, 'Email Successfully Saved!')

    def test_form_populated_with_existing_mail(self):
        email = MassEmail.objects.create(subject = 'a very interesting subject', 
            content = 'some content')
        meeting = Meeting.objects.get(id = 1)
        meeting.email = email
        meeting.save()
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail'))
        self.assertTemplateUsed(response, 'main/mass_mail.html')
        self.assertContains(response, 'a very interesting subject')
        self.assertContains(response, 'some content')

    def test_mail_already_sent(self):
        email = MassEmail.objects.create(subject = 'a very interesting subject', 
            content = 'some content', is_sent = True)
        meeting = Meeting.objects.get(id = 1)
        meeting.email = email
        meeting.save()
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail'))
        self.assertTemplateUsed(response, 'main/mass_mail_sent.html')

    def test_form_save_and_redirect_to_submit(self):
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('mass_mail'),
            data = {'subject': 'Meeting next week', 'content': 'This is an email', 'submit': True})
        self.assertEqual(MassEmail.objects.all().count(), 1)
        self.assertRedirects(response, reverse('mass_mail_submit'))

    def test_form_save_and_redirect_to_test_email(self):
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('mass_mail'),
            data = {'subject': 'Meeting next week', 'content': 'This is an email', 'test': True})
        self.assertEqual(MassEmail.objects.all().count(), 1)
        self.assertRedirects(response, reverse('mass_mail_test'))

# Test for the mass mail submit view redirects
class MassMailSubmitViewRedirectTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('mass_mail_submit'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('mass_mail_submit'))

    def test_redirect_if_no_permissions(self):
        user = User.objects.create_user(username = 'user', password = 'generic123')
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail_submit'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('mass_mail_submit'))

# Test for the mass mail submit view
class MassMailSubmitViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up a user with permission
        user = User.objects.create_user(username = 'user', password = 'generic123')
        permission = Permission.objects.get(name='Abilty to send club emails')
        user.user_permissions.add(permission)

    def test_404_if_no_meeting(self):
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail_submit'))
        self.assertEqual(response.status_code, 404)

    def test_404_if_no_email(self):
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), location = location)
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail_submit'))
        self.assertEqual(response.status_code, 404)

    def test_404_if_email_already_sent(self):
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        email = MassEmail.objects.create(subject = 'a very interesting subject', 
            content = 'some content', is_sent = True)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), 
            location = location, email = email)
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail_submit'))
        self.assertEqual(response.status_code, 404)

    def test_accessible(self):
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        email = MassEmail.objects.create(subject = 'a very interesting subject', 
            content = 'some content', is_sent = False)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), 
            location = location, email = email)
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail_submit'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_after_sending(self):
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        email = MassEmail.objects.create(subject = 'a very interesting subject', 
            content = 'some content', is_sent = False)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), 
            location = location, email = email)
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('mass_mail_submit'), 
            data = {'submit': True}, follow = True)
        self.assertRedirects(response, reverse('mass_mail'))
        self.assertContains(response, 'Email Successfully Sent!')
        self.assertTemplateUsed(response, 'main/mass_mail_sent.html')

# Test for the mass mail test view redirects
class MassMailTestViewRedirectTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('mass_mail_test'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('mass_mail_test'))

    def test_redirect_if_no_permissions(self):
        user = User.objects.create_user(username = 'user', password = 'generic123')
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail_test'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('mass_mail_test'))

# Test for the mass mail test view
class MassMailTestViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up a user with permission
        user = User.objects.create_user(username = 'user', password = 'generic123')
        permission = Permission.objects.get(name='Abilty to send club emails')
        user.user_permissions.add(permission)

    def test_404_if_no_meeting(self):
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail_test'))
        self.assertEqual(response.status_code, 404)

    def test_404_if_no_email(self):
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), location = location)
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail_test'))
        self.assertEqual(response.status_code, 404)

    def test_accessible(self):
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        email = MassEmail.objects.create(subject = 'a very interesting subject', 
            content = 'some content', is_sent = False)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), 
            location = location, email = email)
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.get(reverse('mass_mail_test'))
        self.assertEqual(response.status_code, 200)

    def test_form_filled_incorrectly_blank(self):
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        email = MassEmail.objects.create(subject = 'a very interesting subject', 
            content = 'some content', is_sent = False)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), 
            location = location, email = email)
        self.client.login(username = 'user', password = 'generic123')
        response = self.client.post(reverse('mass_mail_test'))
        self.assertFormError(response, 'form', 'recipient', 'This field is required.')

# Test for the email list index view
class EmailListIndexViewTest(TestCase):
    def test_view_url_accessible(self):
        response = self.client.get(reverse('email_list_index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('email_list_index'))
        self.assertTemplateUsed(response, 'main/email_list_index.html')

# Test for the time-location view
class TimeLocationViewTest(TestCase):
    def test_view_url_accessible(self):
        response = self.client.get(reverse('time_location'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('time_location'))
        self.assertTemplateUsed(response, 'main/time_location.html')

    def test_display_no_meeting(self):
        response = self.client.get(reverse('time_location'))
        self.assertContains(response, 'No Meetings Scheduled!')

    def test_display_with_meeting(self):
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), location = location)
        response = self.client.get(reverse('time_location'))
        self.assertNotContains(response, 'No Meetings Scheduled!')

# Test for the add email view
class EmailListAddViewTest(TestCase):
    def test_view_url_accessible(self):
        response = self.client.get(reverse('add_email'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('add_email'))
        self.assertTemplateUsed(response, 'main/email_list_add.html')

    def test_add_email_valid(self):
        response = self.client.post(reverse('add_email'),
            data = {'new_mail': 'test@example.com', 'name': 'john doe'}, follow = True)
        self.assertRedirects(response, reverse('email_list_index'))
        self.assertContains(response, 'Email Successfully Added!')
        self.assertEqual(EmailAddress.objects.all().count(), 1)

    def test_add_email_invalid(self):
        EmailAddress.objects.create(email = 'test@example.com', name = 'john doe')
        response = self.client.post(reverse('add_email'),
            data = {'new_mail': 'test@example.com', 'name': 'john doe'})
        self.assertFormError(response, 'form', 'new_mail', 'Email already exists')
        self.assertEqual(EmailAddress.objects.all().count(), 1)

# Test for the modify email view
class EmailListModifyViewTest(TestCase):
    def test_view_url_accessible(self):
        response = self.client.get(reverse('modify_email'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('modify_email'))
        self.assertTemplateUsed(response, 'main/email_list_modify.html')

    def test_modify_email_valid(self):
        EmailAddress.objects.create(email = 'train@example.com', name = 'john doe')
        response = self.client.post(reverse('modify_email'),
            data = {'old_mail': 'train@example.com', 'new_mail': 'test@example.com'}, follow = True)
        self.assertRedirects(response, reverse('email_list_index'))
        self.assertContains(response, 'Email Successfully Modified!')
        self.assertEqual(EmailAddress.objects.all().count(), 1)

    def test_modify_email_invalid_old_mail_missing(self):
        response = self.client.post(reverse('modify_email'),
            data = {'old_mail': 'train@example.com', 'new_mail': 'test@example.com'})
        self.assertFormError(response, 'form', 'old_mail', "Old email doesn't exist")
        self.assertEqual(EmailAddress.objects.all().count(), 0)

    def test_modify_email_invalid_new_mail_exists(self):
        EmailAddress.objects.create(email = 'train@example.com', name = 'john doe')
        EmailAddress.objects.create(email = 'test@example.com', name = 'jane doe')
        response = self.client.post(reverse('modify_email'),
            data = {'old_mail': 'train@example.com', 'new_mail': 'test@example.com'})
        self.assertFormError(response, 'form', 'new_mail', "New email already exists")
        self.assertEqual(EmailAddress.objects.all().count(), 2)

# Test for the delete email view
class EmailListDeleteViewTest(TestCase):
    def test_view_url_accessible(self):
        response = self.client.get(reverse('delete_email'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('delete_email'))
        self.assertTemplateUsed(response, 'main/email_list_delete.html')

    def test_delete_email_valid(self):
        EmailAddress.objects.create(email = 'test@example.com', name = 'john doe')
        response = self.client.post(reverse('delete_email'),
            data = {'delete_mail': 'test@example.com'}, follow = True)
        self.assertRedirects(response, reverse('email_list_index'))
        self.assertContains(response, 'Email Successfully Deleted!')
        self.assertEqual(EmailAddress.objects.all().count(), 0)

    def test_delete_email_invalid(self):
        EmailAddress.objects.create(email = 'train@example.com', name = 'john doe')
        response = self.client.post(reverse('delete_email'),
            data = {'delete_mail': 'test@example.com'})
        self.assertFormError(response, 'form', 'delete_mail', "Email doesn't exist")
        self.assertEqual(EmailAddress.objects.all().count(), 1)

# Test for the random view
class RandomViewTest(TestCase):
    def test_view_url_accessible(self):
        response = self.client.get(reverse('random'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('random'))
        self.assertTemplateUsed(response, 'main/random.html')

# Test for the experimental view
class ExperimentalViewTest(TestCase):
    def test_view_url_accessible(self):
        response = self.client.get(reverse('experimental'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('experimental'))
        self.assertTemplateUsed(response, 'main/experimental.html')

# Test for the games view
class GamesViewTest(TestCase):
    def test_view_url_accessible(self):
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('games'))
        self.assertTemplateUsed(response, 'main/games.html')

    def test_view_without_meeting(self):
        response = self.client.get(reverse('games'))
        self.assertContains(response, "No Meetings Scheduled!")

    def test_view_with_meeting_without_games(self):
        # meeting in the future
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), location = location)
        response = self.client.get(reverse('games'))
        self.assertContains(response, "No games to show. Be the first to bring one!")

    def test_view_with_meeting_with_games(self):
        # meeting in the future
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        meeting = Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), location = location)
        GameBring.objects.create(game = 'Settlers of Catan', meeting = meeting)
        response = self.client.get(reverse('games'))
        self.assertContains(response, "Settlers of Catan")

    def test_view_with_game_of_week(self):
        image = SimpleUploadedFile(name = 'test_image.jpg', 
            content = open('main/static/images/stock.jpeg', 'rb').read(), content_type='image/jpeg')
        game_of_week = GameOfWeek.objects.create(game = "Settlers of Catan", image = image,
            time = timezone.now() - datetime.timedelta(days = 1))
        response = self.client.get(reverse('games'))
        self.assertContains(response, "Settlers of Catan")
        self.assertContains(response, "<img")
        game_of_week.delete()

    def test_pagination(self):
        # meeting in the future
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        meeting = Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), location = location)
        for i in range(50):
            GameBring.objects.create(game = f'Game {i}', meeting = meeting)
        response = self.client.get(reverse('games'))
        self.assertContains(response, 'class="pagination"')
        self.assertContains(response, "next")

# Test for the game bring view
class GameBringViewTest(TestCase):
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
        # meeting in the future
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), location = location)
        response = self.client.get(reverse('game_bring'))
        self.assertEqual(response.status_code, 200)

    def test_form_filled_correctly_redirect(self):
        # meeting in the future
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), location = location)
        response = self.client.post(reverse('game_bring'),
            data = {'game': 'Settlers of Catan', 'person': 'me'}, follow = True)
        self.assertRedirects(response, reverse('games'))
        self.assertContains(response, 'Game Successfully Added!')
        self.assertEqual(GameBring.objects.all().count(), 1)

    def test_form_filled_incorrectly_blank(self):
        # meeting in the future
        location = Location.objects.create(place = "APlace", latitude = 0, longitude = 0)
        Meeting.objects.create(time = timezone.now() + datetime.timedelta(days = 1), location = location)
        response = self.client.post(reverse('game_bring'))
        self.assertFormError(response, 'form', 'game', 'This field is required.')

# Test for the changelog view
class ChangelogViewTest(TestCase):
    def test_view_url_accessible(self):
        response = self.client.get(reverse('changelog'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('changelog'))
        self.assertTemplateUsed(response, 'changelog.html')
