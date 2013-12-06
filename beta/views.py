# ----- views.py -----
# Complete Backend Implementation of Hustle.
# Developers: 
# Aayush Agarwal
# Rishabh A Singh
# Torrfick 'TK' Abdul
# --------------------


# --------INDEX--------
# Imports
# 
# Global Helpers
# - userType
# - getUserProfile
# 
# Login Method
# - myLogin
# 
# Password Methods
# - resetPassword
# - forgotPassword
# - confirm_resetpassword
# 
# Registration Methods
# - makeUnboundRegistrationForms
# - Solo Registration
#   - register
#   - doRegister
# - Class Registration
#   - registerClass
#   - doRegisterClass
# - Student Registration
#   - registerStudent
#   - doRegisterStudent
# - confirm_registration
# 
# Page Methods
# - Home
#   - drawHomePage
#   - drawTeacherPage
#   - drawStudentPage
#   - drawSoloPage
# - Profile
#   - profile
# - Other
#   - draw404
#   - about
# 
# AJAX Methods
# - buy
# - sell
# - addMessage
# ---------------------




# --- IMPORTS ---
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import datetime
import time

#needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

#Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

#import csrf token
from django.views.decorators.csrf import ensure_csrf_cookie

# Simple JSON for responding to AJAX Requests
from django.utils import simplejson as json

#Used to send mail from within Django
from django.core.mail import send_mail

#Helper function to guess a MIME type from a file name
from mimetypes import guess_type

from django.template import RequestContext

from beta.models import *
from beta.forms import *

from django.core.serializers.json import DjangoJSONEncoder
import random
# ---------------





# --- GLOBAL HELPERS ---

# takes in a particular user as a string and returns
# "solo" if it's a solo user
# "student" if it's a student
# "teacher" if it's a teacher
# "" if it's neither

# TODO - add check for class as well.
def userType(input_str):
  # Check if this user is, in fact a user.
  if (User.objects.filter(username=input_str)):

    classes = MyClass.objects.all()
    teachers = map(lambda c:c.teacher_name(), classes)
    
    # Compares the teachers names of all classes and searches for a match
    isTeacher = reduce(lambda b1,b2: b1 or b2 , [False] + \
      map(lambda t: t == input_str , teachers))

    if not isTeacher:
      # get all students in the database
      allStudents = reduce(lambda l1,l2: l1+l2, [[]] + \
        map(lambda c:c.roster(), classes))

      # check if there's a match
      isStudent = reduce(lambda b1,b2: b1 or b2 , [False] + \
        map(lambda s: s == input_str , allStudents))

      if isStudent:
        return "student"
      else:
        return "solo"
    else:
      return "teacher"
  else:
    return "" 


# Returns the User Profile or 404
def getUserProfile(usr):
  return get_object_or_404(UserProfile, user=usr)




# ------- LOGIN METHODS ----------

# Base Login in /signin page
def myLogin(request):
  context = {}
  
  #ignore registration form but add it to context
  if request.method == 'GET':
    return render(request, 'login.html', context)

  name = request.POST['username']
  pwd = request.POST['pwd']
  
  #check for error
  if name is not None and pwd is not None:
    
    #everything passed
    new_user = authenticate(username=name, password=pwd)

    if new_user is not None:
      if new_user.is_active:
        user_type = userType(new_user.username)
        login(request, new_user)
        return redirect('/')

      else:
        
        errors = []
        context['errors'] = errors
        errors.append("Didn't Confirm Your Email!")
        return render(request, "login.html", context)

    else:
      errors = []
      context['errors'] = errors

      errors.append("Username and Password didn't match")
      return render(request, "login.html", context)

  else:

   #unbound form
   return render(request, "login.html", context)

# --------------------------------





# ------- PASSWORD METHODS ----------

# Handles Reset Password method
@login_required
def resetPassword(request):
  print "--resetPassword"

  context = {}
  errors = []
  context['errors'] = errors
  context['username'] = request.user.username

  if request.method == 'GET':
    form = ResetPasswordForm()
    context['form'] = form
    
    return render(request, 'resetPassword.html', context)

  else: # request.method == POST
    form = ResetPasswordForm(request.POST, request.FILES)
    context['form'] = form
    me = request.user
    print "me = ", me

    if form.is_valid():
      oldPass = form.cleaned_data.get('oldPassword')
      newPass = form.cleaned_data.get('password1')
      
      print "oldPass = ", oldPass

      if me.check_password(oldPass):
        print "got here"
        me.set_password(newPass)
        me.is_active = True
        me.save()
        return redirect('/')
      else:
        print "ohno"
        errors.append("Passoword is incorrect.")
        return render(request, 'resetPassword.html', context)

    return render(request, 'resetPassword.html', context)

# handles Forgot Password Method
def forgotPassword(request):
  context = {}
  messages = []
  context['messages'] = messages
  errors = []
  context['errors'] = errors

  if request.method == 'GET':
    errors.append("This email address does not exist")
    return render(request, 'forgotPassword.html', context)

  else:
    myEmail = request.POST['email']
    me = User.objects.filter(email__exact=myEmail)
    if not me:
      return redirect('forgotPassword')
    me = me[0]
    user = me
    token = default_token_generator.make_token(user)
    newPass = str(random.randrange(1000, 9999, 1))
    me.set_password(newPass)
    me.save()
    link = "/confirm_resetpassword/"+user.username+"/"+str(token)
    
    email_body = """
Your password has been reset to %s.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
"""     % (newPass, request.get_host(), link)

    send_mail(subject="Reset your password",
              message= email_body,
              from_email="WallStreetCoders@myhustle.herokuapp.com",
              recipient_list=[user.email])
    
    
    context['email'] = myEmail
    messages.append("An email with your new password has been sent to you.")

    return render(request, 'forgotPassword.html', context)

# Confirms Password Reset
@transaction.commit_on_success
def confirm_resetpassword(request, username, token):
    user = get_object_or_404(User, username=username)
    # Send 404 error if token is invalid
    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})
# -----------------------------------





# ------- REGISTRATION METHODS -------


# -HELPER-
# For Registration Methods - Creates three unbounded forms for Solo, Student
# and teacher users.
def makeUnboundRegistrationForms():
  # Create a forms key that contains all the three types of forms
  forms = {}

  # Registration Form for a solo user
  soloForm = {} 
  soloForm['form'] = RegistrationForm()
  soloForm['method'] = "register"

  # Registration Form for a user to be in a class
  studentForm = {}
  studentForm['form'] = StudentRegistrationForm()
  studentForm['method'] = "registerStudent"
    
  # Registration Form for a user to be a teacher
  teacherForm = {}
  teacherForm['form'] = ClassRegistrationForm()
  teacherForm['method'] = "registerClass"

  # Add all these forms to a generic form key
  forms['solo'] = soloForm
  forms['student'] = studentForm
  forms['teacher'] = teacherForm

  return forms


# ----SOLO REGISTRATION METHODS-----
def register(request):
  context = {}

  # Add to context
  forms = makeUnboundRegistrationForms()
  context['forms'] = forms
 
  if request.method == 'GET':
    
    # the forms created outside this 'if' block are all unbound,
    # so simply return them. 
    return render(request, 'registration.html', context)
 
  else: # request.method = POST

    # NOTE: This saves the other 2 forms in the context as well, such
    # that the user could try to correctly register as someone else if 
    # (s)he so desires
    form = RegistrationForm(request.POST)

    # Registration Form for a solo user
    soloForm = {} 
    soloForm['form'] = form
    soloForm['method'] = "register"

    forms['solo'] = soloForm
 
    #check for error
    if form.is_valid():
      doRegister(request, form)
      messages = []
      context['messages'] = messages
      messages.append("A confirmation email has been \
        sent to your email address.")
      
      return render(request, "login.html", context)
    
    else:

      # form validation failed, so send over the completed form with errors.
      return render(request, "registration.html", context)

# Implements db management and emails
def doRegister(request, form):
  uName=form.cleaned_data['username'] 
  pwd=form.cleaned_data['password1']
  ema=form.cleaned_data['email']
  default_cash = 100000
  new_user = User.objects.create_user(username=uName, password=pwd, email=ema)

  new_user.is_active = False
  new_user.save()
  portf = Portfolio(cash=default_cash)
  portf.save()
  new_user_profile = UserProfile(user=new_user, portfolio=portf)
  new_user_profile.save()
  token = default_token_generator.make_token(new_user)

  email_body = """
Welcome to the Hustle.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(), 
       reverse('confirm', args=(new_user.username, token)))

  send_mail(subject="Verify your Hustle Account",
              message= email_body,
              from_email="WallStreetCoders@myhustle.herokuapp.com",
              recipient_list=[new_user.email])


# ----CLASS REGISTRATION METHODS-----
def registerClass(request):
  context = {}
 
  # Unbound Forms
  forms = makeUnboundRegistrationForms()
  context['forms'] = forms

  # Mod the teacherform to the filled out form
  form = ClassRegistrationForm(request.POST)

  teacherForm = {}
  teacherForm['form'] = form
  teacherForm['method'] = "registerClass"
  forms['teacher'] = teacherForm
  
  #check for error
  if form.is_valid():
    doRegisterClass(request, form)
    
    messages = []
    context['messages'] = messages
    messages.append("A confirmation email has been sent to your email address.")
    return render(request, "login.html", context)
  
  else:
    return render(request, "registration.html", context)

# Implements db management and emails
def doRegisterClass(request, form):
  uName=form.cleaned_data['username']
  cName=form.cleaned_data['classname']
  pwd=form.cleaned_data['password1']
  ema=form.cleaned_data['email']
  scv=int(form.cleaned_data['cashValue'])

  new_user = User.objects.create_user(username=uName, password=pwd, email=ema)
  new_user.save()
  
  new_class = MyClass(className=cName, teacher=new_user, startingCashValue=scv)
  new_class.save()

  token = default_token_generator.make_token(new_user)
  email_body = """
Welcome to the Hustle.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(), 
       reverse('confirm', args=(new_user.username, token)))

  send_mail(subject="Verify your Hustle Account",
              message= email_body,
              from_email="WallStreetCoders@myhustle.herokuapp.com",
              recipient_list=[new_user.email])


# ----STUDENT REGISTRATION METHODS-----
def registerStudent(request):
  context = {}
 
  form = StudentRegistrationForm(request.POST)

  forms = makeUnboundRegistrationForms()
  context['forms'] = forms

  studentForm = {}
  studentForm['form'] = form
  studentForm['method'] = "registerStudent"  

  forms['student'] = studentForm

  #check for error
  if form.is_valid():
    doRegisterStudent(request, form)
    
    messages = []
    context['messages'] = messages
    messages.append("A confirmation email has been sent to your email address.")

    return render(request, "login.html", context)
  else:
    #unbound form
    return render(request, "registration.html", context)

# Implements db management and emails
def doRegisterStudent(request, form):
  uName=form.cleaned_data['username'] 
  pwd=form.cleaned_data['password1']
  ema=form.cleaned_data['email']
  cName=form.cleaned_data['classname']

  new_user = User.objects.create_user(username=uName, password=pwd, email=ema)
  new_user.save()

  my_class = MyClass.objects.filter(className=cName)[0]

  portf = Portfolio(cash=my_class.startingCashValue)
  portf.save()

  new_student_model = Student(user=new_user, portfolio=portf, 
                              classAttending=my_class)
  new_student_model.save()

  my_class.students.add(new_student_model)
  my_class.save()

  token = default_token_generator.make_token(new_user)

  email_body = """
Welcome to the Hustle.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(), 
       reverse('confirm', args=(new_user.username, token)))

  send_mail(subject="Verify your Hustle Account",
              message= email_body,
              from_email="WallStreetCoders@myhustle.herokuapp.com",
              recipient_list=[new_user.email])


@transaction.commit_on_success
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)
    
    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})

# ------------------------------------





# ---------- PAGE METHODS ------------


# --- HOME PAGE METHODS ---
# Depending on what kind of user logs in, we draw a different html
# page. used so that upon login, there is no URL required. 
@login_required
def drawHomePage(request):

  username = request.user.username
  user_type = userType(username)

  if user_type == 'solo':
    return drawSoloPage(request)

  elif user_type == 'teacher':
    return drawTeacherPage(request)

  elif user_type == 'student':
    return drawStudentPage(request)

  else:
    # Should never get here since authentication has already happened.
    return draw404(request)

# Draws the teacher home.
@login_required
def drawTeacherPage(request):
  context = {}
  
  # Get necessary info
  username = request.user.username
  teachersClass = MyClass.objects.get(teacher=request.user)

  # Create the context to send
  context['username'] = username
  context['class'] = teachersClass.class_name()
  context['students'] = teachersClass.roster()
  context['messages'] = teachersClass.get_log()

  return render(request, 'teacherhome.html', context)

# Draws the Student Home
@login_required
def drawStudentPage(request):
  context = {}

  student = request.user
  studentModel = Student.objects.get(user=student)
  studentClass = studentModel.classAttending 
  messages = studentClass.get_log() 

  context['username'] = request.user.username
  context['class'] = studentClass
  context['messages'] = messages


  return render(request, "studentHome.html", context)

# Draws the Solo home
@login_required
def drawSoloPage(request):
  context = {}
  me = getUserProfile(request.user)

  # Create a contextual object for data in the frontEnd
  context['username'] = request.user.username
  context['cash'] = me.portfolio.cash
  buy_list = me.portfolio.owned.all()
  context['portfolio'] = buy_list

  return render(request, 'soloHome.html', context)


# --- PROFILE PAGE ---
@login_required
def profile(request, user_id):

  # get the user type, and call the appropriate method.
  user_type = userType(user_id)

  if user_type == "teacher":
    return teacherProfile(request, user_id)

  elif (user_type == "solo") or (user_type == "student") :
    return soloProfile(request, user_id)

  elif (user_type == "class"):
    return classProfile(request, user_id)

  else:
    # Since this comes from a free-form URL, the non-existence of a user
    # simply means that this URL does not exist at all. So, send in a 404.
    return draw404(request)


def soloProfile(request, user_id):
  context = {}
  user = User.objects.get(username=user_id)
  user_profile = UserProfile.objects.get(user=user)
  history = user_profile.portfolio.history.all()

  context['username'] = user_id
  context['pastPurchases'] = history

  return render(request, "soloProfile.html", context)

def teacherProfile(request, user_id):
  context = {}
  user = User.objects.get(username=user_id)


  context['username'] = user_id


  return render(request, "soloProfile.html", context)

def classProfile(request, user_id):
  context = {}




  return render(request, "soloProfile.html", context)



# --- OTHER PAGES ---
# Simple "Not Found" page
def draw404(request):
  context = {}
  return render(request, "notFound.html", context)


# Simple about page.
def about(request):
  return render(request, "about.html", {})
# --------------------------------------------





# ---------- AJAX METHODS ------------

# Implements a Buy
@login_required
def buy(request):
  me = request.user;
  now = time.strftime("%m/%d/%Y")

  # myProfile = getUserProfile(me)
  user_type = userType(me.username)

  if user_type == "solo":
    myProfile = getUserProfile(me)
  else: #if not solo then def student
    myProfile = Student.objects.get(user=me)

  stock = request.GET['ticker']

  nm = request.GET['name']
  price = float(request.GET['ask'])
  price = round(price, 2)
  quant = int(request.GET['quant'])

  # theres some way to tell if short/long
  cost = price * quant

  new_buy = Buy(tickerSymbol=stock, companyName=nm,
   date=now, boughtAt=price, \
   quantity=quant, user=me)
  new_buy.save()
  
  myProfile.portfolio.owned.add(new_buy)
  
  cash = int(myProfile.portfolio.cash)
  finalCash = cash - cost
  
  myProfile.portfolio.cash = finalCash
  myProfile.portfolio.save()

  # create a JSON object to return to the frontEnd
  context = {}
  context['cashOnHand'] = int(finalCash)
  context['date'] = now
  data =  json.dumps(context, cls=DjangoJSONEncoder)

  return HttpResponse(data, mimetype="application/json", status=200)

# Implements a Sell
@login_required
def sell(request):
  me = request.user;
  now = time.strftime("%m/%d/%Y")
  # myProfile = getUserProfile(me);
  user_type = userType(me.username)

  if user_type == "solo":
    myProfile = getUserProfile(me)
  else: #if not solo then def student
    myProfile = Student.objects.get(user=me)

  buyId = int(request.GET['index'])
  price = float(request.GET['soldAt'])

  buy = myProfile.portfolio.owned.all()[buyId]
  stock = buy.tickerSymbol
  nm = buy.companyName
  bAt = buy.boughtAt
  quant = buy.quantity
  nP = price - bAt

  new_buy = Sell(tickerSymbol=stock,
   date=now, soldAt=price, \
   quantity=quant, user=me, \
   boughtAt=bAt, netProfit=nP)

  new_buy.save()
  myProfile.portfolio.history.add(new_buy)
  myProfile.portfolio.owned.remove(buy)

  cost = int(quant) * float(price)
  cash = int(myProfile.portfolio.cash)
  finalCash = cash + cost
  myProfile.portfolio.cash = finalCash
  myProfile.portfolio.save()

  # create a JSON object to return to the frontEnd
  context = {}
  context['cashOnHand'] = int(finalCash)
  context['date'] = now
  data =  json.dumps(context, cls=DjangoJSONEncoder)
  return HttpResponse(data, mimetype="application/json", status=200)

# Adds a message to the message log
@login_required
def addMessage(request):
  context = {}

  # get Class name where this message should be added
  user_type = userType(request.user.username)

  if user_type == "teacher":
    myClass = MyClass.objects.get(teacher=request.user)
  else:
    # if not a teacher, then definitely a student
    myClass = Student.objects.get(user=request.user).classAttending

  # construct params for message
  me = request.user
  message = request.GET['message']
  now = time.strftime("%m/%d/%Y | %I:%M:%S %p")

  new_message = Message(messageFrom=me, time=now, message=message)
  new_message.save()

  myClass.messageLog.add(new_message)
  myClass.save()

  # Prepare data to send back
  context['timestamp'] = now
  context['from'] = request.user.username

  data =  json.dumps(context, cls=DjangoJSONEncoder)
  return HttpResponse(data, mimetype="application/json", status=200)
# -----------------------------------------





# ---------- GRAPH METHODS ------------
# # Renders the table.csv url
# @login_required
# def tablecsv(request):
#   return render(request, '/table.csv')

# @login_required
# @ensure_csrf_cookie
# def graph(request):
#   context = {}
#   #print settings.STATIC_ROOT
#   #print settings.APP_ROOT
#   if request.method == 'POST' and request.POST['symbol']:
#     #stocks = stockretriever.StockRetriever()
#     tckr = request.POST['symbol']
#     #print tckr
#     url = 'http://ichart.yahoo.com/table.csv?s=' + tckr

#     #googHist = googStocks.get(tckr, "NASDAQ");
#     #print googHist

#     #hist = stocks.get_historical_info(tckr)
#     #news = stocks.get_news_feed(tckr)
#     #context['symbol'] = tckr
#     #context['hist'] = hist
#     #context['news'] = news

#   return render(request, 'soloHome.html', context)
# -------------------------------------

