# --- FORMS.py ----
# Necessary forms for working implementation of Hustle
# Principal Developer: Aayush Agarwal 
# Secondary Developer: Rishabh A Singh
# -----------------

# -- IMPORTS --
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.validators import *
from models import *

# -- Regex Validators --
# allows an alphanumeric input
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric \
 characters are allowed.')

# allows a numeric input
numeric = RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')

# -- FORMS --

# - REGISTRATION FORMS -

# Solo Registration Form - to register a solo user
class RegistrationForm(forms.Form):
  username = forms.CharField(max_length=20, 
    required=True, validators=[alphanumeric],
                            widget = forms.TextInput(attrs={
                              'class':'form-control', 
                              'type':'text', 
                              'placeholder':'Username', 
                              'required':'on',
                              'autofocus':'on'}))

  email = forms.EmailField(max_length=200, 
                          required = True, 
                          widget = forms.TextInput(attrs={
                            'class':'form-control', 
                            'type':'text', 
                            'placeholder':'Email address', 
                            'required':'on'}))

  password1 = forms.CharField(max_length = 200, 
                              required = True,
                              widget = forms.PasswordInput(attrs={
                                'class':'form-control', 
                                'type':'password', 
                                'placeholder':'Password', 
                                'required':'on'}))

  password2 = forms.CharField(max_length = 200, 
                              required = True,
                              widget = forms.PasswordInput(attrs={
                                'class':'form-control', 
                                'type':'password', 
                                'placeholder':'Confirm Password', 
                                'required':'on'}))

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
      raise forms.ValidationError("Enter a valid user name.")
    elif User.objects.filter(username__exact=username):
      print "username is already taken!!"
      raise forms.ValidationError("Sorry, Username is already taken.")

    # Confirms that an email was entered and is not already taken
    email = cleaned_data.get('email')
    if email is None or not email:
      raise forms.ValidationError("Enter an email.")
    elif User.objects.filter(email__exact=email):
      raise forms.ValidationError("Email is already registered with another account.")

    # We must return the cleaned data we got from our parent.
    return cleaned_data

# Class Registration Form - Disguised as teacher sign up form that instantiates 
# a class
class ClassRegistrationForm(forms.Form):
  username = forms.CharField(max_length = 20, 
                            required = True,
                            validators=[alphanumeric],
                            widget = forms.TextInput(attrs={
                              'class':'form-control', 
                              'type':'text', 
                              'placeholder':'Username', 
                              'autofocus':'on', 
                              'required':'on'}))

  email = forms.EmailField(max_length=200, 
                            required = True,
                            widget = forms.TextInput(attrs={
                              'class':'form-control', 
                              'type':'text', 
                              'placeholder':'Email address', 
                              'required':'on'}))

  password1 = forms.CharField(max_length = 200, 
                              required = True,
                              widget = forms.PasswordInput(attrs={
                                'class':'form-control', 
                                'type':'password', 
                                'placeholder':'Password', 
                                'required':'on'}))

  password2 = forms.CharField(max_length = 200, 
                              required = True,
                              widget = forms.PasswordInput(attrs={
                                'class':'form-control', 
                                'type':'password', 
                                'placeholder':'Confirm Password', 
                                'required':'on'}))

  classname = forms.CharField(max_length = 200, 
                              required = True,
                              validators=[alphanumeric],
                              widget = forms.TextInput(attrs={
                                'class':'form-control', 
                                'type':'text', 
                                'placeholder':'Class Name', 
                                'autofocus':'on', 
                                'required':'on'}))

  cashValue = forms.CharField(max_length = 20, 
                              required = True,
                              validators=[numeric],
                              widget = forms.TextInput(attrs={
                                'class':'form-control', 
                                'type':'text', 
                                'placeholder':'Starting Cash Value for Students', 
                                'required':'on'}))

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
      raise forms.ValidationError("Enter a valid user name.")
    elif User.objects.filter(username__exact=username):
      raise forms.ValidationError("Username is already taken.")

  # Confirms that an email was entered and is not already taken
    email = cleaned_data.get('email')
    if email is None or not email:
      raise forms.ValidationError("Enter an email.")
    elif User.objects.filter(email__exact=email):
      raise forms.ValidationError("Email is already registered with another account.")

    cash_value = cleaned_data.get('cashValue')
    if cash_value is None or not cash_value:
      raise forms.ValidationError("Please enter a valid cash value.")

  # We must return the cleaned data we got from our parent.
    return cleaned_data

# Student Registration Form - registers a student into a class.
class StudentRegistrationForm(forms.Form):
  classname = forms.CharField(max_length = 20, 
                              required = True,
                              validators=[alphanumeric],
                              widget = forms.TextInput(attrs={
                                'class':'form-control', 
                                'type':'text', 
                                'placeholder':'Your Class Name', 
                                'autofocus':'on', 
                                'required':'on'}))

  username = forms.CharField(max_length = 20, 
                              required = True,
                              validators=[alphanumeric],
                              widget = forms.TextInput(attrs={
                                'class':'form-control', 
                                'type':'text', 
                                'placeholder':'Username', 
                                'required':'on'}))

  email = forms.EmailField(max_length=200, 
                            required = True,
                            widget = forms.TextInput(attrs={
                              'class':'form-control', 
                              'type':'text', 
                              'placeholder':'Email address', 
                              'required':'on'}))

  password1 = forms.CharField(max_length = 200, 
                              required = True,
                              widget = forms.PasswordInput(attrs={
                                'class':'form-control', 
                                'type':'password', 
                                'placeholder':'Password', 
                                'required':'on'}))

  password2 = forms.CharField(max_length = 200, 
                              required = True,
                              widget = forms.PasswordInput(attrs={
                                'class':'form-control', 
                                'type':'password', 
                                'placeholder':'Confirm Password', 
                                'required':'on'}))

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

    className = cleaned_data.get('classname')

    if className is None or not className:
      raise forms.ValidationError("Enter a valid class name.")

    # elif not re.match(r'^[A-Za-z0-9]*$',className): 
    #   raise forms.ValidationError("Only Alpha-Numeric Characters are allowed")

    elif not MyClass.objects.filter(className__exact=className):
      raise forms.ValidationError("This class does not exist.")


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
      raise forms.ValidationError("Email is already registered with another account.")

  # We must return the cleaned data we got from our parent.
    return cleaned_data

# - PASSWORD FORMS -

# Reset Password Form
class ResetPasswordForm(forms.Form):
    oldPassword = forms.CharField(max_length = 200, 
                                label='Current Password', 
                                widget = forms.PasswordInput(attrs={
                                  'class':'form-control',
                                  'placeholder':'Old Password..',
                                  'required':'on'
                                  }))

    password1 = forms.CharField(max_length = 200, 
                                label='New Password', 
                                widget = forms.PasswordInput(attrs={
                                  'class':'form-control',
                                  'placeholder':'New Password..',
                                  'required':'on'
                                  }))

    password2 = forms.CharField(max_length = 200, 
                                label='Confirm New password',  
                                widget = forms.PasswordInput(attrs={
                                  'class':'form-control',
                                  'placeholder':'Confirm New Password..',
                                  'required':'on'
                                  }))


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
