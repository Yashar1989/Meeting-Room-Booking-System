from django.urls import path

from . import views

urlpatterns = [
    path('list-view/<int:id>', views.CommentListView.as_view(), name='comment_list_view'),
    path('create/<uuid:reservation_id>/', views.CommentCreateView.as_view(), name='comment_create'),
    path('update/<uuid:pk>/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('delete/<uuid:pk>/', views.CommentDeleteView.as_view(), name='comment_delete')


]
