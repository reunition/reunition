from django import forms as f

from . import models as m


GRADUATION_FIRST_NAME_FIELD = lambda : f.CharField(max_length=100, label='First name at graduation')
GRADUATION_LAST_NAME_FIELD = lambda : f.CharField(max_length=100, label='Last name at graduation')
CURRENT_FIRST_NAME_FIELD = lambda : f.CharField(max_length=100, required=False, label='Current first name (if different)')
CURRENT_LAST_NAME_FIELD = lambda : f.CharField(max_length=100, required=False, label='Current last name (if different)')
CURRENT_CITY_FIELD = lambda : f.CharField(max_length=200, required=False, label='Current city/state/country', help_text='Optional; used for anonymous "where are they now" map')
ATTENDING_FIELD = lambda : f.ChoiceField([('', '(Select one)')] + m.Rsvp.ATTENDING_CHOICES, label='Will you be attending the reunion?')
CONTACT_METHOD_FIELD = lambda : f.ChoiceField([('', '(Select one)')] + m.Rsvp.CONTACT_METHOD_CHOICES, label='How would you like us to contact you?')
PHONE_FIELD = lambda : f.CharField(max_length=100, required=False, help_text='Optional; for text or phone call updates')
FIRST_NAME_FIELD = lambda : f.CharField(max_length=100)
LAST_NAME_FIELD = lambda : f.CharField(max_length=100, required=False)
RELATIONSHIP_FIELD = lambda : f.ChoiceField([('', '(Select one)')] + m.RsvpGuestAttendee.RELATIONSHIP_CHOICES, required=False)


class InitialForm(f.Form):

    graduation_first_name = GRADUATION_FIRST_NAME_FIELD()
    graduation_last_name = GRADUATION_LAST_NAME_FIELD()
    current_first_name = CURRENT_FIRST_NAME_FIELD()
    current_last_name = CURRENT_LAST_NAME_FIELD()
    current_city = CURRENT_CITY_FIELD()
    attending = ATTENDING_FIELD()
    contact_method = CONTACT_METHOD_FIELD()
    phone = PHONE_FIELD()


class UpdateForm(f.Form):

    attending = ATTENDING_FIELD()
    current_city = CURRENT_CITY_FIELD()
    contact_method = CONTACT_METHOD_FIELD()
    phone = PHONE_FIELD()


class AlumniAddForm(f.Form):

    graduation_first_name = GRADUATION_FIRST_NAME_FIELD()
    graduation_last_name = GRADUATION_LAST_NAME_FIELD()
    current_first_name = CURRENT_FIRST_NAME_FIELD()
    current_last_name = CURRENT_LAST_NAME_FIELD()


class AlumniUpdateForm(f.Form):

    current_first_name = CURRENT_FIRST_NAME_FIELD()
    current_last_name = CURRENT_LAST_NAME_FIELD()


class GuestForm(f.Form):

    first_name = FIRST_NAME_FIELD()
    last_name = LAST_NAME_FIELD()
    relationship = RELATIONSHIP_FIELD()
