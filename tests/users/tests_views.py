from django.contrib.auth.models import User
from django.test import TestCase


class UserRegistrationViewTestCase(TestCase):
    def test_get(self):
        """ user_registration_view get() method. """
        with self.assertNumQueries(0):
            response = self.client.get('/user/registration/')
        self.assertEqual(response.status_code, 200)

        response_form = response.context['form']
        self.assertCountEqual([f for f in response_form.fields],
                              ['username', 'first_name', 'last_name', 'password1', 'password2'])

    def test_required_fields(self):
        """ user_registration_view post() method required fields. """
        with self.assertNumQueries(0):
            response = self.client.post('/user/registration/', {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['username'].errors, ['This field is required.'])
        self.assertEqual(response.context['form']['first_name'].errors, ['This field is required.'])
        self.assertEqual(response.context['form']['last_name'].errors, ['This field is required.'])
        self.assertEqual(response.context['form']['password1'].errors, ['This field is required.'])
        self.assertEqual(response.context['form']['password2'].errors, ['This field is required.'])

    def test_registration(self):
        """ user_registration_view register a user."""
        with self.assertNumQueries(13):
            response = self.client.post('/user/registration/', {
                'username': 'arya', 'password1': 'p@ssw0rd123', 'password2': 'p@ssw0rd123',
                'first_name': 'Arya', 'last_name': 'Stark'
            }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')

        user = User.objects.get(username='arya')
        self.assertEqual(user.username, 'arya')
        self.assertEqual(user.first_name, 'Arya')
        self.assertEqual(user.last_name, 'Stark')

        # validate tha the user is logged in.
        self.assertTrue(user.is_authenticated)

        # attempt to create a user with the same username.
        # user is already logged in -> redirect to movies list page.
        with self.assertNumQueries(5):
            response = self.client.post('/user/registration/', {
                'username': 'arya', 'password1': 'p@ssw0rd123', 'password2': 'p@ssw0rd123',
                'first_name': 'Arya', 'last_name': 'Stark'
            }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')

        self.client.logout()
        with self.assertNumQueries(1):
            response = self.client.post('/user/registration/', {
                'username': 'arya', 'password1': 'p@ssw0rd123', 'password2': 'p@ssw0rd123',
                'first_name': 'Arya', 'last_name': 'Stark'
            }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['username'].errors, ['A user with that username already exists.'])


class UserLoginViewTestCase(TestCase):
    def test_get(self):
        """ user_login_view get() method. """
        with self.assertNumQueries(0):
            response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)

        response_form = response.context['form']
        self.assertCountEqual([f for f in response_form.fields],
                              ['username', 'password'])

    def test_login_user_redirect(self):
        """ user_login_view get() method redirect an already logged user. """
        user = User.objects.create(username='nick', password='nick@brody', first_name='Nikolas', last_name='Brody')
        self.client.force_login(user)

        with self.assertNumQueries(5):
            response = self.client.get('/user/login/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')

    def test_invalid_credentials(self):
        """ user_login_view post() method invalid credentials. """
        with self.assertNumQueries(0):
            response = self.client.post('/user/login/', {'user_name': 'test', 'password': 'user'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h3 class="has-error">Invalid username or password</h3>')


class UserLogoutViewTestCase(TestCase):
    def test_user_logout(self):
        """ user_logout_view get() method redirect an already logged user. """
        user = User.objects.create(username='nick', password='nick@brody', first_name='Nikolas', last_name='Brody')
        self.client.force_login(user)

        with self.assertNumQueries(5):
            response = self.client.get('/user/logout/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')
