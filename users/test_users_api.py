from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status

User = get_user_model()

class UserAPITest(APITestCase):
    def setUp(self):
        # Create and authenticate a user
        self.user = User.objects.create_user(username='user2', email='at@example.com', password='pass123098')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_register_user(self):
        """Should register a new user"""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        """Should log in and return a token"""
        url = reverse('login')
        data = {
            'username': 'user2',
            'password': 'pass123098'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_profile_view(self):
        """Should return authenticated user's profile"""
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_user(self):
        """Should follow another user"""
        other = User.objects.create_user(username='other', email='other@example.com', password='pass456')
        url = reverse('follow-user', args=[other.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unfollow_user(self):
        """Should unfollow a user"""
        other = User.objects.create_user(username='other', email='other@example.com', password='pass456')
        # First, follow the user
        follow_url = reverse('follow-user', args=[other.id])
        follow_response = self.client.post(follow_url)
        self.assertEqual(follow_response.status_code, status.HTTP_201_CREATED)
        # Now, unfollow the user
        unfollow_url = reverse('unfollow-user', args=[other.id])
        unfollow_response = self.client.post(unfollow_url)
        self.assertEqual(unfollow_response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_user_list(self):
        """Should return paginated list of users"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_user_detail(self):
        """Should return details of a specific user"""
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_followers_list(self):
        """Should return followers of a user"""
        url = reverse('followers-list', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_following_list(self):
        """Should return following list of a user"""
        url = reverse('following-list', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
