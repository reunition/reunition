from django import forms as f

from . import models as m


class NoteAddForm(f.Form):

    notes = f.CharField(label='Notes', widget=f.Textarea)
    contacted = f.ChoiceField(label='Did you make contact with this person?',
                              required=False,
                              choices=m.Note.CONTACTED_CHOICES)
