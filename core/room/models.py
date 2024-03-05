from django.db import models
import uuid
# Create your models here.

class Room(models.Model):
    id = models.UUIDField(primary_key=True ,default=uuid.uuid4 ,editable=False)
    room_no = models.SmallIntegerField()
    capacity = models.SmallIntegerField()
    description = models.CharField(max_length=256)
    image = models.ImageField(upload_to='room/')