from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Run(models.Model):
   #distance in kilometres
   distance = models.FloatField("Distance (km)")
   #duration in minutes
   duration = models.FloatField("Time (minutes)")
   calories = models.FloatField("Calories", default=0)
   def _get_speed(self):
      #Returns speed in kmph
      return round((60 * self.distance)/self.duration, 2)
   
   speed = property(_get_speed)
   
   def _get_pace(self):
      #Returns pace in minutes/km
      return round(self.duration/self.distance, 2)
      
   pace = property(_get_pace)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   date = models.DateTimeField()
   
   def __str__(self):
      return "%s   %s"%(self.date.date(), self.user.username)

class UserInfo(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   #Mass in kilograms
   mass = models.FloatField("Weight (kg)", default=70.0)
   #Height in centimetres
   height = models.FloatField("Height (cm)", default=170.0)
   dob = models.DateField("Date of birth", default=datetime.date.today() - datetime.timedelta(days=(365*30)))

   def _get_age(self):
      #returns age as integer
      delta = datetime.date.today() - self.dob
      return delta.days//365
   
   age = property(_get_age)
      
   
   def __str__(self):
      return "%s info"%self.user.username

@receiver(post_save, sender=User)
def create_userinfo(sender, instance, created, **kwargs):
   if created:
      UserInfo.objects.create(user=instance)
      
@receiver(post_save, sender=User)
def save_userinfo(sender, instance, **kwargs):
   instance.userinfo.save()  
