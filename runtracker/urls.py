from django.conf.urls import url

from . import views

urlpatterns = [
   url(r'^$', views.index, name='index'),
   url(r'^login', views.logIn, name='login'),
   url(r'^signup', views.signUp, name='signup'),
   url(r'^logout', views.logOut, name='logout'),
   url(r'^addrun', views.addRun, name='addrun'),
   url(r'^deleterun', views.deleteRun, name='deleterun'),
   url(r'^getrunssince', views.getRunsSince, name='getrunssince'),
   url(r'^getrunsbetween', views.getRunsBetween, name='getrunsbetween')
]
