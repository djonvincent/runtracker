from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

class Run(models.Model):
   #Distance in kilometres
   distance = models.FloatField("Distance (km)")
   #Duration in minutes
   duration = models.FloatField("Time (minutes)")
   #Calories burnt in kcal
   calories = models.FloatField("Calories", default=0)
   #Date and time of run
   date = models.DateTimeField()
   
   #Returns speed in kmph
   def _get_speed(self):
      return round((60 * self.distance)/self.duration, 2)
   
   speed = property(_get_speed)
   
   #Returns pace in minutes/km
   def _get_pace(self):
      return round(self.duration/self.distance, 2)
      
   pace = property(_get_pace)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   
   def __str__(self):
      return "%s   %s"%(self.date.date(), self.user.username)

#Additional information about user
class UserInfo(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   #Mass in kilograms
   mass = models.FloatField("Weight (kg)", default=70.0)
   #Height in centimetres
   height = models.FloatField("Height (cm)", default=170.0)
   dob = models.DateField("Date of birth", default=datetime.date.today() - datetime.timedelta(days=(365*30)))

   #returns age as integer
   def _get_age(self):
      delta = datetime.date.today() - self.dob
      return delta.days//365
   
   age = property(_get_age)
      
   def __str__(self):
      return "%s info"%self.user.username

#Automatically create userinfo when a user is created
@receiver(post_save, sender=User)
def create_userinfo(sender, instance, created, **kwargs):
   if created:
      UserInfo.objects.create(user=instance)

#Automatically save userinfo when user is saved      
@receiver(post_save, sender=User)
def save_userinfo(sender, instance, **kwargs):
   instance.userinfo.save()  
