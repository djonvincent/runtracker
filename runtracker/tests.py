from django.test import TestCase
from .models import Run
from django.contrib.auth.models import User
import datetime
from django.test import Client

class RunTestCase(TestCase):
   def setUp(self):
      self.user = User.objects.create_user(
         username = "joebloggs@example.com",
         password = "secret",
         first_name = "Joe",
         last_name = "Bloggs",
      )
      self.user.userinfo.mass = 75
      self.user.save()
      
      c = Client()
      c.login(username="joebloggs@example.com", password="secret")
      
      c.post('/addrun/', {
         'distance': 12,
         'duration': 46 + 32/60,
         'datetime': '2017-02-08T12:00'
      })
      
   
   def test_speed_calculation(self):
      expected = 15.47
      observed = Run.objects.get(pk=1).speed
      self.assertEqual(expected, observed)
      
   def test_pace_calculation(self):
      expected = 3.88
      observed = Run.objects.get(pk=1).pace
      self.assertEqual(expected, observed)
   
   def test_calories_calculation(self):
      expected = 961.08
      observed = Run.objects.get(pk=1).calories
      observed = round(observed, 2)
      self.assertEqual(expected, observed)
