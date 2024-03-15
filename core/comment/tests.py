from django.test import TestCase
from django.urls import reverse, resolve
from .views import AdminCommentsView, ActivateCommentsView, CommentCreateView


class TestUrl(TestCase):

    def test_admin_comments_url(self):
        url = reverse('comment:admin_comments')
        self.assertEqual(resolve(url).func.view_class, AdminCommentsView)

    def test_admin_active_comment(self):
        url = reverse('comment:activate_comments')
        self.assertEqual(resolve(url).func.view_class, ActivateCommentsView)

    def test_add_comment_url(self):
        url = reverse('comment:comment_create', kwargs={'pk': 'f3b9a1ef-5e16-45e9-8245-2184d5fe18ab'})
        self.assertEqual(resolve(url).func.view_class, CommentCreateView)
