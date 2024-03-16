from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import (
    RoomListView,
    ReservationListView,
    RoomCreate,
    RoomDetailView,
    ReservationCreateView,
    room_availability
)
from .forms import RoomCreatingForm, ReservationForm
from user.models import CustomUser
from .models import Room, Reservation
from datetime import datetime
# Create your tests here.


class TestUrl(TestCase):
    def test_room_index_url(self):
        """
        check index url view name
        """
        url = reverse('room:index')
        self.assertEqual(resolve(url).func.view_class, RoomListView)

    def test_reserve_list_url(self):
        """
        check reserve list url view name
        """
        url = reverse('room:reserved-list')
        self.assertEqual(resolve(url).func.view_class, ReservationListView)

    def test_add_room_url(self):
        """
        check add room url view name
        """
        url = reverse('room:add_room')
        self.assertEqual(resolve(url).func.view_class, RoomCreate)

    def test_room_detail_view_url(self):
        """
        check room detail url view name
        """
        url = reverse('room:room-detail', kwargs={'room_no': 12})
        self.assertEqual(resolve(url).func.view_class, RoomDetailView)

    def test_reservation_create_url(self):
        """
        check reservation create url view name
        """
        url = reverse('room:reservation_create', kwargs={'room_no': 12})
        self.assertEqual(resolve(url).func.view_class, ReservationCreateView)

    def test_room_availability_url(self):
        """
        check room_availability url view name
        """
        url = reverse('room:room_availability')
        self.assertEqual(resolve(url).func, room_availability)


class TestPostForm(TestCase):
    def test_create_room_with_valid_data(self):
        """
        check create room form validation
        """
        form = RoomCreatingForm(data={
            'room_no': 1000,
            'capacity': 10,
            'description': 'test description'
        })
        self.assertTrue(form.is_valid())

    def test_create_reservation(self):
        """
        check reservation create form validation
        """
        form = ReservationForm(data={
            'user': 1,
            'room': 1000,
            'reserve_date': '2024-03-01',
            'available_time': '8:00-10:00'
        })
        self.assertTrue(form.is_valid())


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = CustomUser.objects.create_superuser(username='admin', password='!@#WSXqaz')
        self.user = CustomUser.objects.create_user(username='yashar', password='!@#WSXqaz')
        self.room = Room.objects.create(room_no=1, capacity=100, description='test')
        self.reserve = Reservation.objects.create(
            user=self.user,
            room_id=self.room.id,
            reserve_date='2024-03-15',
            available_time='8:00-10:00',
            created_date=datetime.now()
        )

    def test_room_index_url_get_response_200(self):
        """
        test index on project, list of rooms views
        """
        url = reverse('room:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='room/index.html')

    def test_add_room_url_non_superuser_response(self):
        """
        test add room views for non superuser
        """
        self.client.force_login(user=self.user)
        # should be return 302 (redirect)
        url = reverse('room:add_room')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_add_room_url_superuser_response(self):
        """
        test add room views for superuser
        """
        self.client.force_login(user=self.superuser)
        # should be return 200 (redirect)
        url = reverse('room:add_room')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_change_reserve_to_active_non_superuser_response(self):
        """
        test access to activate reservation for non superuser
        """
        self.client.force_login(user=self.user)
        # should be return 302 (redirect)
        url = reverse('room:active_reserve', kwargs={'reserve_id': self.reserve.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_change_reserve_to_active_superuser_response(self):
        """
        test access to activate reservation for superuser
        """
        self.client.force_login(user=self.superuser)
        # should be return 200 (redirect)
        url = reverse('room:active_reserve', kwargs={'reserve_id': self.reserve.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.route, '<str:reserve_id>/change/')


class TestRoomModel(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = CustomUser.objects.create_superuser(username='admin4', password='!@#WSXqaz')
        self.user = CustomUser.objects.create_user(username='yashar4', password='!@#WSXqaz')

    def test_create_room(self):
        room = Room.objects.create(
            room_no=10,
            capacity=20,
            description='room number 10'
        )
        self.assertEqual(room.room_no, 10)
        self.assertEqual(room.description, 'room number 10')

    def test_create_reserve(self):
        room = Room.objects.create(
                        room_no=10,
                        capacity=20,
                        description='room number 10'
                    )
        reserve = Reservation.objects.create(
            user=self.user,
            room_id=room.id,
            reserve_date='2024-03-15',
            available_time='8:00-10:00',
            created_date=datetime.now()
        )
        self.assertEqual(reserve.reserve_date, '2024-03-15')
        self.assertEqual(reserve.available_time, '8:00-10:00')
