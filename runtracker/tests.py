from django.test import TestCase
from .models import Run
from django.contrib.auth.models import User
import datetime
from django.test import Client

class SignUpTestCase(TestCase):
   def test_sign_up(self):
      c = Client()
      c.post('/signup/', {
         'username': 'billybob@spam.com',
         'password': '123456',
         'password2': '123456',
         'first_name': 'billy',
         'last_name': 'bob',
         'mass': '97.5'
      })
      user = User.objects.get(username="billybob@spam.com")
      self.assertIsNotNone(user)
      
   def test_mismatching_passwords(self):
      c = Client()
      c.post('/signup/', {
         'username': 'keenrunnerb@sports.com',
         'password': '123456',
         'password2': '123457',
         'first_name': 'billy',
         'last_name': 'bob',
         'mass': '97.5'
      })
      with self.assertRaises(User.DoesNotExist):
         User.objects.get(username="billybob@spam.com")
   

class LogInTestCase(TestCase):
   def setUp(self):
      user = User.objects.create(
         username = "joebloggs@example.com",
         password = "secret"
      )
      user.save()
      
   def test_login(self):
      c = Client()
      response = c.post('/login/', {
         'username': 'joebloggs@example.com',
         'password': 'secret'
      })
      user = User.objects.get(username="joebloggs@example.com")
      self.assertTrue(user.is_authenticated())
   
class RunTestCase(TestCase):
   def setUp(self):
      user = User.objects.create_user(
         username = "joebloggs@example.com",
         password = "secret",
         first_name = "Joe",
         last_name = "Bloggs",
      )
      user.userinfo.mass = 75
      user.save()
      
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

