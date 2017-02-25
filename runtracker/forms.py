from django import forms
from django.contrib.auth.models import User

#Create form used when adding a run to the database
class AddRunForm(forms.Form):
   distance = forms.FloatField(min_value=0)
   duration = forms.FloatField(min_value=0)
   #Use the datetime widget for inputing the date
   datetime = forms.DateTimeField(input_formats = ['%Y-%m-%dT%H:%M'])

#Form used when filtering runs by data
class GetRunsBetweenForm(forms.Form):
   lowerdate = forms.DateField(input_formats = ['%Y-%m-%d'], required=False)
   upperdate = forms.DateField(input_formats = ['%Y-%m-%d'], required=False)

#Form used for creating an account
class SignUpForm(forms.ModelForm):
   class Meta:
      #Use the fields already defined in the User model
      model = User
      fields = ['username', 'first_name', 'last_name']
      #Use email input for username
      widgets = {
         'username': forms.EmailInput()
      }
   username = forms.EmailField(label="Email address")
   password = forms.CharField(widget = forms.PasswordInput(), min_length=6)
   #Confirm password field
   password2 = forms.CharField(label="Confirm password", widget = forms.PasswordInput(), min_length=6)
   mass = forms.FloatField(min_value=10, required=False, label="Mass (kg)")
   
   #Function called when getting cleaned data from the form
   def clean(self):
      cleaned_data = super(SignUpForm, self).clean()
      password = cleaned_data['password']
      password2 = cleaned_data['password2']
      
      #If both password and password2 are valid
      if password and password2:
         #Raise error if passwords don't match
         if password != password2:
            raise forms.ValidationError("Passwords do not match.", code="invalid")
            
