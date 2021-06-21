from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime
# Create your models here.

class CustomUser(AbstractUser):
  pass
  class Meta:
    db_table = 'CustomUser'

class RecogData(models.Model):
  data = models.TextField
  def __str__(self):
    return self.data

class ConversationData(models.Model):
  user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  data = models.TextField(blank=True, null=True, max_length=1000)
  time = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.user.username + ":" + self.data

class Classroom(models.Model):
  name = models.CharField(max_length=32)
  def __str__(self):
    return self.name

class Lecture(models.Model):
  list = [
    (0,'MON'),
    (1,'TUE'),
    (2,'WED'),
    (3,'THU'),
    (4,'FRI'),
    (5,'SAT'),
  ]

  name = models.CharField(max_length=64)
  room = models.CharField(max_length=32)
  weeK_of_day = models.IntegerField(choices=list,default=0)
  timed = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
  def __str__(self):
    return self.name

class RoomData(models.Model):
  user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  room = models.CharField(max_length=32)
  enter_at = models.DateTimeField(auto_now_add=True)
  leave_at = models.DateTimeField(null=True, blank=True)
  def __str__(self):
    return self.user.username + "=" + self.room + "=" + str(localtime(self.enter_at))