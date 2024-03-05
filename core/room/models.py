from django.db import models
import uuid

class Room(models.Model):
    id = models.UUIDField(primary_key=True ,default=uuid.uuid4 ,editable=False)
    room_no = models.SmallIntegerField()
    capacity = models.SmallIntegerField()
    description = models.CharField(max_length=256)
    image = models.ImageField(upload_to='room/')

    
# create Reservation model
class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)