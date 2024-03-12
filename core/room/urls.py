from django.urls import path
from . import views

app_name = 'room'

urlpatterns = [
    path('free_room/', views.room_availability, name='room_availability'),
    path('', views.RoomListView.as_view(), name='index'),
    path('<int:room_no>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('<int:room_no>/create/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('reserved/', views.ReservationListView.as_view(), name='reserved-list'),
]

