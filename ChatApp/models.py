from django.db import models

# Create your models here.

class Room(models.Model):
    room_name = models.CharField(max_length=100)

    def __str__(self):
        return self.room_name
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}: {self.message}'
    
class Notification(models.Model):
    message = models.CharField(max_length=100)
    
    def __str__(self):
        return self.message

