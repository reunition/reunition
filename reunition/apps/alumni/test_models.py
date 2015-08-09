from django.test import TestCase
from model_mommy import mommy


class PersonTests(TestCase):

    def test_display_name(self):

        person = mommy.make(
            'alumni.Person',
            graduation_first_name='Bobbie',
            graduation_last_name='Smith',
        )
        self.assertEqual(person.display_name, 'Bobbie Smith')

        person = mommy.make(
            'alumni.Person',
            graduation_first_name='Bobbie',
            graduation_last_name='Smith',
            current_first_name='Roberta',
        )
        self.assertEqual(person.display_name, 'Roberta (Bobbie) Smith')

        person = mommy.make(
            'alumni.Person',
            graduation_first_name='Bobbie',
            graduation_last_name='Smith',
            current_last_name='Jones',
        )
        self.assertEqual(person.display_name, 'Bobbie Jones (Smith)')

        person = mommy.make(
            'alumni.Person',
            graduation_first_name='Bobbie',
            graduation_last_name='Smith',
            current_first_name='Roberta',
            current_last_name='Jones',
        )
        self.assertEqual(person.display_name, 'Roberta Jones (Bobbie Smith)')
