from django.db import models

# Create your models here.


class RoomMember(models.Model):
    name = models.CharField(max_length=100)
    uid = models.CharField(max_length=200)
    room_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} in {self.room_name}"