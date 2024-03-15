from django.test import TestCase
from django.urls import reverse, resolve
from .views import (
    RoomListView,
    ReservationListView,
    RoomCreate,
    RoomDetailView,
    ReservationCreateView
)
from .forms import RoomCreatingForm, ReservationForm
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
