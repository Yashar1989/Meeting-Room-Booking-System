from django.contrib.auth import get_user_model
from django.db import models
from room.models import Reservation
import uuid


# Create your models here.


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reserve_id = models.ForeignKey(to=Reservation, on_delete=models.CASCADE)
    user_id = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies')
    is_active = models.BooleanField(default=False, null=True)
