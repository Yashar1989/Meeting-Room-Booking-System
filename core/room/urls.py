from django.urls import path
from . import views

app_name = 'room'

urlpatterns = [
    path('', views.RoomListView.as_view(), name='index'),
    path('reserved/', views.ReservationListView.as_view(), name='reserved-list'),
    path('<int:room_no>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('<int:room_no>/create/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('free_room/', views.room_availability, name='room_availability'),
    path('<str:reserve_id>/update/', views.ReservationUpdateView.as_view(), name='reservation_update'),
    path('<str:reserve_id>/change/', views.ActiveReserveView.as_view(), name='active_reserve'),
    path('<str:reserve_id>/delete/', views.DeleteReserve.as_view(), name='delete_reserve'),
    path('add/', views.RoomCreate.as_view(), name='add_room'),
]

