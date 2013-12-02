from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from models import *

class RegistrationForm(forms.Form):
  username = forms.CharField(max_length = 20,
                            required = True,
                            widget = forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder':'Username', 'autofocus':'on'}))
  email = forms.EmailField(max_length=200,
                            required = True,
                            widget = forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder':'Email address'}))
  password1 = forms.CharField(max_length = 200, 
                              #label='Password',
                              required = True,
                              widget = forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'Password'}))
  password2 = forms.CharField(max_length = 200, 
                              #label='Confirm password',
                              required = True,
                              widget = forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'Confirm Password'}))

  # Customizes form validation for properties that apply to more
  # than one field.  Overrides the forms.Form.clean function.
  def clean(self):
    # Calls our parent (forms.Form) .clean function, gets a dictionary
    # of cleaned data as a result
    cleaned_data = super(RegistrationForm, self).clean()

    # Confirms that the two password fields match
    password1 = cleaned_data.get('password1')
    password2 = cleaned_data.get('password2')
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError("Passwords did not match.")

  # Customizes form validation for the username field.
    # Confirms that the username is not already present in the
    # User model database.
    username = cleaned_data.get('username')
    if username is None or not username:
      raise forms.ValidationError("Enter a user name.")
    elif User.objects.filter(username__exact=username):
      raise forms.ValidationError("Username is already taken.")

  # Confirms that an email was entered and is not already taken
    email = cleaned_data.get('email')
    if email is None or not email:
      raise forms.ValidationError("Enter an email.")
    elif User.objects.filter(email__exact=email):
      raise forms.ValidationError("Email is already registered.")

  # We must return the cleaned data we got from our parent.
    return cleaned_data
     
class BuyForm(forms.Form):
  stock = forms.CharField(max_length=5)
  quantity = forms.IntegerField(initial=0)

  def clean(self):
    cleaned_data = super(BuyForm, self).clean()
    stock = cleaned_data.get('stock')
    quantity = cleaned_data.get('quantity')
    if stock and quantity and quantity > 0 and stock.length() < 5:
      raise forms.ValidationError("something is wrong here....")
    return cleaned_data

class SellForm(forms.Form):
  stock = forms.CharField(max_length=5)
  quantity = forms.IntegerField(initial=0)

  def clean(self):
    cleaned_data = super(SellForm, self).clean()
    stock = cleaned_data.get('stock')
    quantity = cleaned_data.get('quantity')
    
    if stock and quantity and quantity > 0 and stock.length() < 7:
      raise forms.ValidationError("something is wrong here....")
  
    return cleaned_data
#---------------reset password----------------#
class ResetPasswordForm(forms.Form):
    oldPassword = forms.CharField(max_length = 200, 
                                label='Current Password', 
                                widget = forms.PasswordInput())
    password1 = forms.CharField(max_length = 200, 
                                label='New Password', 
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm New password',  
                                widget = forms.PasswordInput())


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(ResetPasswordForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        oldPassword = cleaned_data.get('oldPassword')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

#-----------------class forms.py -------------#

class ClassRegistrationForm(forms.Form):
  username = forms.CharField(max_length = 20,
                            required = True,
                            widget = forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder':'Username', 'autofocus':'on'}))
  email = forms.EmailField(max_length=200,
                            required = True,
                            widget = forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder':'Email address'}))
  password1 = forms.CharField(max_length = 200, 
                              #label='Password',
                              required = True,
                              widget = forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'Password'}))
  password2 = forms.CharField(max_length = 200, 
                              #label='Confirm password',
                              required = True,
                              widget = forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'Confirm Password'}))
  classname = forms.CharField(max_length = 20,
                            required = True,
                            widget = forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder':'Class Name', 'autofocus':'on'}))
  cashValue = forms.CharField(max_length = 20,
                            required = True,
                            widget = forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder':'Starting Cash Value for Students'}))

  # Customizes form validation for properties that apply to more
  # than one field.  Overrides the forms.Form.clean function.
  def clean(self):
    # Calls our parent (forms.Form) .clean function, gets a dictionary
    # of cleaned data as a result
    cleaned_data = super(ClassRegistrationForm, self).clean()

    # Confirms that the two password fields match
    password1 = cleaned_data.get('password1')
    password2 = cleaned_data.get('password2')
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError("Passwords did not match.")

  # Customizes form validation for the username field.
    # Confirms that the username is not already present in the
    # User model database.
    username = cleaned_data.get('username')
    if username is None or not username:
      raise forms.ValidationError("Enter a user name.")
    elif User.objects.filter(username__exact=username):
      raise forms.ValidationError("Username is already taken.")

  # Confirms that an email was entered and is not already taken
    email = cleaned_data.get('email')
    if email is None or not email:
      raise forms.ValidationError("Enter an email.")
    elif User.objects.filter(email__exact=email):
      raise forms.ValidationError("Email is already registered.")

  # We must return the cleaned data we got from our parent.
    return cleaned_data

#---------------------------------------------#

class StudentRegistrationForm(forms.Form):
  classname = forms.CharField(max_length = 20,
                            required = True,
                            widget = forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder':'Your Class Name', 'autofocus':'on'}))
  username = forms.CharField(max_length = 20,
                            required = True,
                            widget = forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder':'Username'}))
  email = forms.EmailField(max_length=200,
                            required = True,
                            widget = forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder':'Email address'}))
  password1 = forms.CharField(max_length = 200, 
                              #label='Password',
                              required = True,
                              widget = forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'Password'}))
  password2 = forms.CharField(max_length = 200, 
                              #label='Confirm password',
                              required = True,
                              widget = forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'Confirm Password'}))

  # Customizes form validation for properties that apply to more
  # than one field.  Overrides the forms.Form.clean function.
  def clean(self):
    # Calls our parent (forms.Form) .clean function, gets a dictionary
    # of cleaned data as a result
    cleaned_data = super(StudentRegistrationForm, self).clean()

    # Confirms that the two password fields match
    password1 = cleaned_data.get('password1')
    password2 = cleaned_data.get('password2')
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError("Passwords did not match.")

  # Customizes form validation for the username field.
    # Confirms that the username is not already present in the
    # User model database.
    username = cleaned_data.get('username')
    if username is None or not username:
      raise forms.ValidationError("Enter a user name.")
    elif User.objects.filter(username__exact=username):
      raise forms.ValidationError("Username is already taken.")

  # Confirms that an email was entered and is not already taken
    email = cleaned_data.get('email')
    if email is None or not email:
      raise forms.ValidationError("Enter an email.")
    elif User.objects.filter(email__exact=email):
      raise forms.ValidationError("Email is already registered.")

  # We must return the cleaned data we got from our parent.
    return cleaned_data