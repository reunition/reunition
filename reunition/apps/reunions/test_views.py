from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django_webtest import WebTest
from model_mommy import mommy

from reunition.apps.alumni import models as alumni_m

from . import models as m


class Base(WebTest):

    def setUp(self):
        self.reunion = mommy.make(m.Reunion)
        self.reunion_detail_url = reverse('reunions:detail', kwargs=dict(pk=self.reunion.pk))
        self.reunion_rsvp_url = reverse('reunions:rsvp', kwargs=dict(pk=self.reunion.pk))

    def create_user_and_login(self):
        self.user = mommy.make(User, username='user')
        self.user.set_password('password')
        self.user.save()
        self.client.login(username='user', password='password')


class ReunionDetailViewTests(Base):

    def test_has_sign_in_button_when_not_logged_in(self):
        response = self.client.get(self.reunion_detail_url)
        self.assertContains(response, 'Sign in and RSVP')

    def test_has_link_to_rsvp_page_when_logged_in(self):
        self.create_user_and_login()
        response = self.client.get(self.reunion_detail_url)
        self.assertContains(response, 'View or change your RSVP')


class ReunionRsvpViewTests(Base):

    # --- not logged in ---

    def test_redirects_to_login_page_when_not_logged_in(self):
        with self.settings(INSTALLED_APPS=[a for a in settings.INSTALLED_APPS if not a.startswith('socialaccount')]):
            response = self.client.get(self.reunion_rsvp_url)
            self.assertRedirects(response, '/accounts/login/?next={}'.format(self.reunion_rsvp_url))

    # --- initial form ---

    def test_show_initial_form_if_no_rsvp_present(self):
        self.create_user_and_login()
        response = self.client.get(self.reunion_rsvp_url)
        assert 'initial_form' in response.context

    def test_initial_form_auto_fills_from_facebook_profile(self):
        self.create_user_and_login()
        SocialAccount.objects.create(
            user=self.user,
            provider='facebook',
            uid=12345,
            extra_data=dict(
                first_name='Dirk',
                last_name='McGurk',
            ),
        )
        page = self.app.get(self.reunion_rsvp_url, user='user')
        self.assertEqual(page.form['graduation_first_name'].value, 'Dirk')
        self.assertEqual(page.form['graduation_last_name'].value, 'McGurk')

    def test_initial_form_auto_fills_verified_alumni_from_facebook_profile_when_names_change(self):
        mommy.make(
            alumni_m.Person,
            graduating_class=self.reunion.graduating_class,
            graduation_first_name='Bobbie',
            graduation_last_name='Jones',
            current_first_name='Roberta',
            current_last_name='Smith',
            verified=now(),
        )
        self.create_user_and_login()
        SocialAccount.objects.create(
            user=self.user,
            provider='facebook',
            uid=12345,
            extra_data=dict(
                first_name='Roberta',
                last_name='Smith',
            ),
        )
        page = self.app.get(self.reunion_rsvp_url, user='user')
        self.assertEqual(page.form['graduation_first_name'].value, 'Bobbie')
        self.assertEqual(page.form['graduation_last_name'].value, 'Jones')
        self.assertEqual(page.form['current_first_name'].value, 'Roberta')
        self.assertEqual(page.form['current_last_name'].value, 'Smith')

    def test_post_initial_form_creates_new_rsvp_if_no_rsvp_present(self):
        self.create_user_and_login()
        page = self.app.get(self.reunion_rsvp_url, user='user')
        page.form['graduation_first_name'] = 'Jules'
        page.form['graduation_last_name'] = 'Frampton'
        page.form['attending'] = 'Y'
        page.form['contact_method'] = 'email'
        self.assertEqual(m.Rsvp.objects.count(), 0)
        page = page.form.submit()
        self.assertEqual(m.Rsvp.objects.count(), 1)

    def test_post_initial_form_does_nothing_if_rsvp_present(self):
        self.create_user_and_login()
        page = self.app.get(self.reunion_rsvp_url, user='user')
        page.form['graduation_first_name'] = 'Jules'
        page.form['graduation_last_name'] = 'Frampton'
        page.form['attending'] = 'Y'
        page.form['contact_method'] = 'email'
        # Simulate another request making an RSVP before submit is clicked.
        mommy.make(m.Rsvp, created_by=self.user, reunion=self.reunion)
        self.assertEqual(m.Rsvp.objects.count(), 1)
        page = page.form.submit()
        self.assertEqual(m.Rsvp.objects.count(), 1)

    def test_post_initial_form_redirects_to_main_rsvp_view_on_success(self):
        self.create_user_and_login()
        page = self.app.get(self.reunion_rsvp_url, user='user')
        page.form['graduation_first_name'] = 'Jules'
        page.form['graduation_last_name'] = 'Frampton'
        page.form['attending'] = 'Y'
        page.form['contact_method'] = 'email'
        self.assertEqual(m.Rsvp.objects.count(), 0)
        page = page.form.submit()
        self.assertRedirects(page, self.reunion_rsvp_url)

    def test_post_initial_form_links_existing_alumni_when_existing_graduating_name_given(self):
        person = mommy.make(
            alumni_m.Person,
            graduating_class=self.reunion.graduating_class,
            graduation_first_name='Jules',
            graduation_last_name='Frampton',
            current_first_name=None,
            current_last_name=None,
            verified=now(),
        )
        self.create_user_and_login()
        page = self.app.get(self.reunion_rsvp_url, user='user')
        page.form['graduation_first_name'] = 'Jules'
        page.form['graduation_last_name'] = 'Frampton'
        page.form['attending'] = 'Y'
        page.form['contact_method'] = 'email'
        page = page.form.submit()
        rsvp = m.Rsvp.objects.first()
        self.assertEqual(rsvp.rsvpalumniattendee_set.count(), 1)
        alumni_attendee = rsvp.rsvpalumniattendee_set.first()
        self.assertEqual(alumni_attendee.person, person)

    def test_post_initial_form_creates_unverified_alumni_when_nonexistent_graduating_name_given(self):
        self.create_user_and_login()
        page = self.app.get(self.reunion_rsvp_url, user='user')
        page.form['graduation_first_name'] = 'Jules'
        page.form['graduation_last_name'] = 'Frampton'
        page.form['attending'] = 'Y'
        page.form['contact_method'] = 'email'
        page = page.form.submit()
        rsvp = m.Rsvp.objects.first()
        self.assertEqual(rsvp.rsvpalumniattendee_set.count(), 1)
        alumni_attendee = rsvp.rsvpalumniattendee_set.first()
        person = alumni_attendee.person
        self.assertEqual(person.graduation_first_name, 'Jules')
        self.assertEqual(person.graduation_last_name, 'Frampton')
        self.assertIs(person.verified, None)

    def test_post_initial_form_updates_current_names_of_existing_alumni_when_given(self):
        person = mommy.make(
            alumni_m.Person,
            graduating_class=self.reunion.graduating_class,
            graduation_first_name='Jules',
            graduation_last_name='Frampton',
            current_first_name=None,
            current_last_name=None,
            verified=now(),
        )
        self.create_user_and_login()
        page = self.app.get(self.reunion_rsvp_url, user='user')
        page.form['graduation_first_name'] = 'Jules'
        page.form['graduation_last_name'] = 'Frampton'
        page.form['current_first_name'] = 'Julia'
        page.form['current_last_name'] = 'Sampson'
        page.form['attending'] = 'Y'
        page.form['contact_method'] = 'email'
        page = page.form.submit()
        person = alumni_m.Person.objects.get(pk=person.pk)
        self.assertEqual(person.current_first_name, 'Julia')
        self.assertEqual(person.current_last_name, 'Sampson')

    # --- main rsvp view, basic updates ---

    def test_do_not_show_initial_form_if_rsvp_present(self):
        self.create_user_and_login()
        self.reunion.rsvp_set.create(
            created_by=self.user,
            contact_method='email',
        )
        response = self.client.get(self.reunion_rsvp_url)
        assert 'initial_form' not in response.context

    def test_post_attending_updates_rsvp_and_redirects_to_main_rsvp_view(self):
        pass
    
    def test_post_current_city_updates_rsvp_and_redirects_to_main_rsvp_view(self):
        pass

    def test_post_contact_method_updates_rsvp_and_redirects_to_main_rsvp_view(self):
        pass

    def test_post_phone_updates_rsvp_and_redirects_to_main_rsvp_view(self):
        pass

    # --- alumni ---

    def test_post_alumni_add_adds_alumni_attendee(self):
        pass

    def test_post_alumni_cannot_add_person_associated_with_another_rsvp(self):
        pass

    def test_post_alumni_delete_deletes_alumni_attendee(self):
        pass

    def test_post_alumni_update_updates_alumni_names(self):
        pass

    # --- guests ---

    def test_post_guest_add_adds_guest_attendee(self):
        pass

    def test_post_guest_delete_deletes_guest_attendee(self):
        pass
