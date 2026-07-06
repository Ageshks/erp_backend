from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase


class AuthAPITests(APITestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')
        self.forgot_password_url = reverse('accounts:forgot-password')
        self.reset_password_url = reverse('accounts:reset-password')

    def test_signup_returns_tokens_and_redirect_url(self):
        payload = {
            'email': 'newuser@example.com',
            'password': 'StrongPass123!',
            'full_name': 'Jane Doe',
        }

        response = self.client.post(self.signup_url, payload, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['redirect_url'], '/')
        self.assertEqual(response.data['user']['full_name'], 'Jane Doe')
        user = self.user_model.objects.get(email='newuser@example.com')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')

    def test_signup_requires_full_name(self):
        response = self.client.post(self.signup_url, {
            'email': 'newuser@example.com',
            'password': 'StrongPass123!',
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('full name', response.data['detail'].lower())

    def test_login_returns_tokens_for_existing_user(self):
        self.user_model.objects.create_user(email='login@example.com', password='StrongPass123!')

        response = self.client.post(self.login_url, {
            'email': 'login@example.com',
            'password': 'StrongPass123!'
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['redirect_url'], '/')

    def test_forgot_password_and_reset_password_work(self):
        self.user_model.objects.create_user(email='reset@example.com', password='StrongPass123!')

        forgot_response = self.client.post(self.forgot_password_url, {'email': 'reset@example.com'}, format='json')
        self.assertEqual(forgot_response.status_code, 200)
        self.assertIn('reset_token', forgot_response.data)

        reset_response = self.client.post(self.reset_password_url, {
            'email': 'reset@example.com',
            'token': forgot_response.data['reset_token'],
            'new_password': 'NewStrongPass123!'
        }, format='json')

        self.assertEqual(reset_response.status_code, 200)
        user = self.user_model.objects.get(email='reset@example.com')
        self.assertTrue(user.check_password('NewStrongPass123!'))

    def test_forgot_password_reports_unknown_email(self):
        response = self.client.post(self.forgot_password_url, {'email': 'unknown@example.com'}, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('not registered', response.data['detail'].lower())

    def test_protected_dashboard_requires_valid_jwt(self):
        user = self.user_model.objects.create_user(email='secure@example.com', password='StrongPass123!')
        token = self.client.post(self.login_url, {
            'email': 'secure@example.com',
            'password': 'StrongPass123!'
        }, format='json').data['access']

        response = self.client.get(reverse('accounts:dashboard'), HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['email'], user.email)

    def test_superuser_can_access_admin_user_list(self):
        superuser = self.user_model.objects.create_superuser(email='admin@example.com', password='Admin@123456')
        self.client.force_login(superuser)

        response = self.client.get('/admin/accounts/user/')
        self.assertEqual(response.status_code, 200)

    def test_refresh_and_logout_endpoints_work(self):
        self.user_model.objects.create_user(email='session@example.com', password='StrongPass123!')

        login_response = self.client.post(self.login_url, {
            'email': 'session@example.com',
            'password': 'StrongPass123!'
        }, format='json')
        refresh_token = login_response.data['refresh']

        refresh_response = self.client.post(reverse('accounts:token-refresh'), {'refresh': refresh_token}, format='json')
        self.assertEqual(refresh_response.status_code, 200)
        self.assertIn('access', refresh_response.data)

        logout_response = self.client.post(reverse('accounts:logout'), {'refresh': refresh_token}, format='json')
        self.assertEqual(logout_response.status_code, 200)
