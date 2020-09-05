from django.test import TestCase

from users.forms import UserRegistrationForm


class UserRegistrationFormTestCase(TestCase):
    def test_form_validation(self):
        form = UserRegistrationForm(data={'username': 'test_user'})
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {
            'password1': ['This field is required.'],
            'password2': ['This field is required.'],
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
        })

        form = UserRegistrationForm(data={
            'username': 'test_user',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Arya',
            'last_name': 'Stark'
        })
        self.assertTrue(form.is_valid())
