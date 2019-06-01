from django.test import TestCase
from django.utils import timezone
from main.models import Alert, Location, Contact, ContactNotificant
from main.models import QuoteOfDay, VideoOfDay
from main.models import MassEmail, EmailAddress

# TODO: finish tests

# Testing for the Alert model
class AlertModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up non-modified objects used by all test methods
        Alert.objects.create(message = "Testing", time = timezone.now())

    def test_message_label(self):
        alert = Alert.objects.get(id = 1)
        field_label = alert._meta.get_field('message').verbose_name
        self.assertEquals(field_label, 'message')

    def test_time_label(self):
        alert = Alert.objects.get(id = 1)
        field_label = alert._meta.get_field('time').verbose_name
        self.assertEquals(field_label, 'time')

    def test_seen_label(self):
        alert = Alert.objects.get(id = 1)
        field_label = alert._meta.get_field('seen').verbose_name
        self.assertEquals(field_label, 'seen')

    def test_severity_label(self):
        alert = Alert.objects.get(id = 1)
        field_label = alert._meta.get_field('severity').verbose_name
        self.assertEquals(field_label, 'severity')

    def test_message_max_length(self):
        alert = Alert.objects.get(id = 1)
        max_length = alert._meta.get_field('message').max_length
        self.assertEquals(max_length, 250)

    def test_string_representation(self):
        alert = Alert.objects.get(id = 1)
        self.assertEquals(str(alert), 'Testing')

    def test_default(self):
        alert = Alert.objects.get(id = 1)
        self.assertEquals(alert.severity, '2a')

    def test_ordering(self):
        Alert.objects.create(message = "Testing2", time = timezone.now(), severity = '3w')
        alert2 = Alert.objects.get(id = 2)
        self.assertEquals(alert2, Alert.objects.all()[0])

# Testing for the MassEmail model
class MassEmailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up non-modified objects used by all test methods
        MassEmail.objects.create(subject = "no subject", content = "interesting content")

    def test_subject_label(self):
        mass_email = MassEmail.objects.get(id = 1)
        field_label = mass_email._meta.get_field('subject').verbose_name
        self.assertEquals(field_label, 'subject')

    def test_content_label(self):
        mass_email = MassEmail.objects.get(id = 1)
        field_label = mass_email._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'content')

    def test_last_edit_label(self):
        mass_email = MassEmail.objects.get(id = 1)
        field_label = mass_email._meta.get_field('last_edit').verbose_name
        self.assertEquals(field_label, 'last edit')

    def test_editor_label(self):
        mass_email = MassEmail.objects.get(id = 1)
        field_label = mass_email._meta.get_field('editor').verbose_name
        self.assertEquals(field_label, 'editor')

    def test_is_sent_label(self):
        mass_email = MassEmail.objects.get(id = 1)
        field_label = mass_email._meta.get_field('is_sent').verbose_name
        self.assertEquals(field_label, 'is sent')

    def test_subject_max_length(self):
        mass_email = MassEmail.objects.get(id = 1)
        max_length = mass_email._meta.get_field('subject').max_length
        self.assertEquals(max_length, 200)

    def test_content_max_length(self):
        mass_email = MassEmail.objects.get(id = 1)
        max_length = mass_email._meta.get_field('content').max_length
        self.assertEquals(max_length, 2000)

    def test_string_representation(self):
        mass_email = MassEmail.objects.get(id = 1)
        self.assertEquals(str(mass_email), 'no subject')

# Testing for the EmailAddress model
class EmailAddressTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up non-modified objects used by all test methods
        EmailAddress.objects.create(email = "fake@example.com", name = "fake name")

    def test_email_label(self):
        email_address = EmailAddress.objects.get(id = 1)
        field_label = email_address._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email')

    def test_namelabel(self):
        email_address = EmailAddress.objects.get(id = 1)
        field_label = email_address._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_string_representation(self):
        email_address = EmailAddress.objects.get(id = 1)
        self.assertEquals(str(email_address), 'fake@example.com')

# Testing for the Location model
class LocationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up non-modified objects used by all test methods
        Location.objects.create(place = "APlace", latitude = 0, longitude = 0)

    def test_place_label(self):
        location = Location.objects.get(id = 1)
        field_label = location._meta.get_field('place').verbose_name
        self.assertEquals(field_label, 'place')

    def test_latitude_label(self):
        location = Location.objects.get(id = 1)
        field_label = location._meta.get_field('latitude').verbose_name
        self.assertEquals(field_label, 'latitude')

    def test_longitude_label(self):
        location = Location.objects.get(id = 1)
        field_label = location._meta.get_field('longitude').verbose_name
        self.assertEquals(field_label, 'longitude')

    def test_place_max_length(self):
        location = Location.objects.get(id = 1)
        max_length = location._meta.get_field('place').max_length
        self.assertEquals(max_length, 200)

    def test_string_representation(self):
        location = Location.objects.get(id = 1)
        self.assertEquals(str(location), 'APlace')

# Testing for the Contact model
class ContactModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up non-modified objects used by all test methods
        Contact.objects.create(message = "Hello World")

    def test_message_label(self):
        contact = Contact.objects.get(id = 1)
        field_label = contact._meta.get_field('message').verbose_name
        self.assertEquals(field_label, 'message')

    def test_email_label(self):
        contact = Contact.objects.get(id = 1)
        field_label = contact._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email address')

    def test_seen_label(self):
        contact = Contact.objects.get(id = 1)
        field_label = contact._meta.get_field('seen').verbose_name
        self.assertEquals(field_label, 'seen')

    def test_string_representation(self):
        contact = Contact.objects.get(id = 1)
        self.assertEquals(str(contact), 'Hello World')

    def test_default(self):
        contact = Contact.objects.get(id = 1)
        self.assertEquals(contact.seen, False)

    def test_ordering(self):
        Contact.objects.create(message = "Goodbye World", seen = True)
        contact2 = Contact.objects.get(id = 2)
        self.assertEquals(contact2, Contact.objects.all()[1])

# Testing for the ContactNotificant model
class ContactNotificantTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up non-modified objects used by all test methods
        ContactNotificant.objects.create(email = "test@example.com")

    def test_email_label(self):
        contact_notificant = ContactNotificant.objects.get(id = 1)
        field_label = contact_notificant._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email')

    def test_string_representation(self):
        contact_notificant = ContactNotificant.objects.get(id = 1)
        self.assertEquals(str(contact_notificant), 'test@example.com')

# Testing for the QuoteOfDay model
class QuoteOfDayTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up non-modified objects used by all test methods
        QuoteOfDay.objects.create(quote = "AQuote", speaker = "ASpeaker", time = timezone.now())

    def test_quote_label(self):
        quote_of_day = QuoteOfDay.objects.get(id = 1)
        field_label = quote_of_day._meta.get_field('quote').verbose_name
        self.assertEquals(field_label, 'quote')

    def test_speaker_label(self):
        quote_of_day = QuoteOfDay.objects.get(id = 1)
        field_label = quote_of_day._meta.get_field('speaker').verbose_name
        self.assertEquals(field_label, 'speaker')

    def test_time_label(self):
        quote_of_day = QuoteOfDay.objects.get(id = 1)
        field_label = quote_of_day._meta.get_field('time').verbose_name
        self.assertEquals(field_label, 'time')

    def test_quote_max_length(self):
        quote_of_day = QuoteOfDay.objects.get(id = 1)
        max_length = quote_of_day._meta.get_field('quote').max_length
        self.assertEquals(max_length, 500)

    def test_speaker_max_length(self):
        quote_of_day = QuoteOfDay.objects.get(id = 1)
        max_length = quote_of_day._meta.get_field('speaker').max_length
        self.assertEquals(max_length, 200)

    def test_string_representation(self):
        quote_of_day = QuoteOfDay.objects.get(id = 1)
        self.assertEquals(str(quote_of_day), 'ASpeaker - AQuote')

# Testing for the VideoOfDay model
class VideoOfDayTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up non-modified objects used by all test methods
        VideoOfDay.objects.create(link = "alink.com", visible_text = "funny video", time = timezone.now())

    def test_link_label(self):
        video_of_day = VideoOfDay.objects.get(id = 1)
        field_label = video_of_day._meta.get_field('link').verbose_name
        self.assertEquals(field_label, 'link')

    def test_visible_text_label(self):
        video_of_day = VideoOfDay.objects.get(id = 1)
        field_label = video_of_day._meta.get_field('visible_text').verbose_name
        self.assertEquals(field_label, 'visible text')

    def test_description_label(self):
        video_of_day = VideoOfDay.objects.get(id = 1)
        field_label = video_of_day._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_time_label(self):
        video_of_day = VideoOfDay.objects.get(id = 1)
        field_label = video_of_day._meta.get_field('time').verbose_name
        self.assertEquals(field_label, 'time')

    def test_link_max_length(self):
        video_of_day = VideoOfDay.objects.get(id = 1)
        max_length = video_of_day._meta.get_field('link').max_length
        self.assertEquals(max_length, 1000)

    def test_visible_text_max_length(self):
        video_of_day = VideoOfDay.objects.get(id = 1)
        max_length = video_of_day._meta.get_field('visible_text').max_length
        self.assertEquals(max_length, 500)

    def test_description_max_length(self):
        video_of_day = VideoOfDay.objects.get(id = 1)
        max_length = video_of_day._meta.get_field('description').max_length
        self.assertEquals(max_length, 1000)

    def test_string_representation(self):
        video_of_day = VideoOfDay.objects.get(id = 1)
        self.assertEquals(str(video_of_day), 'funny video')
