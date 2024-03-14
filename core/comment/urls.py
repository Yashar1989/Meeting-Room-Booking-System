from django.urls import path

from . import views

urlpatterns = [
    path('list-view/<uuid:pk>/', views.RoomCommentsListView.as_view(), name='comment_list_view'),
    path('create/<uuid:pk>/', views.CommentCreateView.as_view(), name='comment_create'),
    path('update/<uuid:pk>/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('delete/<uuid:pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('admin/comments/', views.AdminCommentsView.as_view(), name='admin_comments'),
    path('admin/comments/activate/', views.ActivateCommentsView.as_view(), name='activate_comments'),


]
