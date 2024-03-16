from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.urls import reverse

class Room(models.Model):
    """
    model for adding room
    """
    AVAILABILITY_CHOICES = (
        ('8:00-10:00', '8:00-10:00'),
        ('10:00-12:00', '10:00-12:00'),
        ('12:00-14:00', '12:00-14:00'),
        ('14:00-16:00', '14:00-16:00'),
        ('16:00-18:00', '16:00-18:00'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_no = models.SmallIntegerField(unique=True)
    capacity = models.SmallIntegerField()
    description = models.CharField(max_length=256)
    available_time = models.CharField(max_length=256, choices=AVAILABILITY_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to='room/', null=True, blank=True)

    def __str__(self):
        return f'{self.room_no}'

    def get_absolute_url(self):
        return reverse('room:room-detail', kwargs={'room_no': self.room_no})

    class Meta:
        unique_together = ['room_no']
        ordering = ('room_no',)

    
# create Reservation model
class Reservation(models.Model):
    """
    model for creating reservation
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    reserve_date = models.DateField(null=True, blank=True)
    available_time = models.CharField(max_length=256, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ['room', 'reserve_date', 'available_time']
        ordering = ('-created_date',)
