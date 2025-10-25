from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post, Comment
from rest_framework.authtoken.models import Token
from rest_framework import status

User = get_user_model()

class PostAPITest(APITestCase):
    def setUp(self):
        # Create and authenticate a user
        self.user = User.objects.create_user(username='catherine', email='cat@example.com', password='pass123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a post
        self.post = Post.objects.create(author=self.user, content='Initial post')

    def test_feed_view(self):
        """Should return paginated feed"""
        url = reverse('user-feed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_list(self):
        """Should return list of posts with filters"""
        url = reverse('post-list')
        response = self.client.get(url, {'search': 'Initial'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create(self):
        """Should create a new post"""
        url = reverse('post-create')
        data = {'content': 'New post content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_detail(self):
        """Should return post details"""
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_update(self):
        """Should update a post"""
        url = reverse('post-update', args=[self.post.id])
        data = {'content': 'Updated content'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_delete(self):
        """Should delete a post"""
        url = reverse('post-delete', args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment_create(self):
        """Should create a comment on a post"""
        url = reverse('comment-create', args=[self.post.id])
        data = {'content': 'Nice post!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_update(self):
        """Should update a comment"""
        comment = Comment.objects.create(post=self.post, author=self.user, content='Original')
        url = reverse('comment-update', args=[self.post.id, comment.id])
        data = {'content': 'Updated comment'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_delete(self):
        """Should delete a comment"""
        comment = Comment.objects.create(post=self.post, author=self.user, content='To delete')
        url = reverse('comment-delete', args=[self.post.id, comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_like_post(self):
        """Should like a post"""
        url = reverse('toggle-like', args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_likes_list(self):
        """Should return list of likes for a post"""
        url = reverse('post-likes-list', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
