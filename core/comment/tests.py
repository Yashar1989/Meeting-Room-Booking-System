from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import AdminCommentsView, ActivateCommentsView, CommentCreateView
from .models import Comment
from .forms import CommentForm
from user.models import CustomUser
from room.models import Room, Reservation
from datetime import datetime


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


class CommentFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = CustomUser.objects.create_superuser(username='admin1', password='!@#WSXqaz')
        self.user = CustomUser.objects.create_user(username='yashar1', password='!@#WSXqaz')
        self.room = Room.objects.create(room_no=2, capacity=100, description='test')
        self.reserve = Reservation.objects.create(
            user=self.user,
            room_id=self.room.id,
            reserve_date='2024-03-15',
            available_time='8:00-10:00',
            created_date=datetime.now()
        )

    def test_comment_form_with_valid_data(self):
        """
        create comment with CommentForm and validated data
        """
        form = CommentForm(data={
            'reserve_id': self.reserve.id,
            'user_id': self.user.id,
            'comment': 'test',
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_with_invalid_data(self):
        """
        create comment with CommentForm and validated data
        """
        form = CommentForm(data={
        })
        self.assertFalse(form.is_valid())


class CommentModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = CustomUser.objects.create_superuser(username='admin2', password='!@#WSXqaz')
        self.user = CustomUser.objects.create_user(username='yashar2', password='!@#WSXqaz')
        self.room = Room.objects.create(room_no=3, capacity=100, description='test')
        self.reserve = Reservation.objects.create(
            user=self.user,
            room_id=self.room.id,
            reserve_date='2024-03-15',
            available_time='8:00-10:00',
            created_date=datetime.now()
        )

    def test_comment_model(self):
        comment = Comment.objects.create(
            user_id=self.user,
            reserve_id=self.reserve,
            comment='this is a comment',
        )
        self.assertEqual(comment.user_id.id, self.user.id)
        self.assertEqual(comment.user_id.username, 'yashar2')
        self.assertEqual(comment.reserve_id.id, self.reserve.id)
        self.assertEqual(comment.comment, 'this is a comment')
