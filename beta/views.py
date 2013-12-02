#views.py

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
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


#--- LOGIN METHODS ---

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
    print "got here"
    new_user = authenticate(username=name, password=pwd)
    print "new_user=", new_user
    if new_user is not None:
      if new_user.is_active:
        print "all classes: ", MyClass.objects.all()
        search = MyClass.objects.filter(teacher=new_user)
        print "search= ", search
        if len(search) != 0:
          curClass = search[0]
          login(request, new_user)
          print 'redirecting teacher login'
          return redirect('/teacherHome')

        login(request, new_user)
        print 'redirecting'
        return redirect('/portfolio')

      else:

        # TODO: Add a check here to see if the username
        # exists, adn if not then add a different error message
        
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
#---------------------

# EDITED BY RISHABH 11/26 4:56 AM
#--- REGISTER METHODS ---
def register(request):
  context = {}

  #ignore login form but add it to context
  # context['registrationForm'] = RegistrationForm()
 
  if request.method == 'GET':
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

    # Add to context
    context['forms'] = forms
   
    return render(request, 'registration.html', context)
 
  else: # request.method = POST
    form = RegistrationForm(request.POST)
    context['registrationForm'] = form
 
    #check for error
    if form.is_valid():
      doRegister(request, form)
      messages = []
      context['messages'] = messages
      messages.append("A confirmation email has been sent to your email address.")
      
      return render(request, "login.html", context)
    
    else:
      #unbound form
      return render(request, "registration.html", context)



def doRegister(request, form):
  uName=form.cleaned_data['username'] 
  pwd=form.cleaned_data['password1']
  ema=form.cleaned_data['email']
  #default_cash = form.cleaned_data['cash']
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
              from_email="aayusha+devnull@andrew.cmu.edu",
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
    ####----SEND THIS TO A PAGE THAT SAYS YOU ARE FULLY REGISTERED----#########
    return render(request, 'confirmed.html', {})

#---------------------


def teacherHome(request):
  context = {}
  username = request.user.username
  students = MyClass.objects.filter(teacher=request.user)[0].students
  context['username'] = username
  context['students'] = students
  print "students = "
  print students
  return render(request, 'teacherhome.html', context)

#-------CSV FILE -----#
@login_required
def tablecsv(request):
  print 'hereee'
  return render(request, '/table.csv')

  #--------GRAPH------#
@login_required
@ensure_csrf_cookie
def graph(request):
  context = {}
  #print settings.STATIC_ROOT
  #print settings.APP_ROOT
  if request.method == 'POST' and request.POST['symbol']:
    #stocks = stockretriever.StockRetriever()
    tckr = request.POST['symbol']
    #print tckr
    url = 'http://ichart.yahoo.com/table.csv?s=' + tckr

    #googHist = googStocks.get(tckr, "NASDAQ");
    #print googHist

    #hist = stocks.get_historical_info(tckr)
    #news = stocks.get_news_feed(tckr)
    #context['symbol'] = tckr
    #context['hist'] = hist
    #context['news'] = news

  return render(request, 'portfolio.html', context)

  #----------BUY------------#
@login_required
def buy(request):
  me = request.user;
  now = time.strftime("%m/%d/%Y")
  myProfile = getUserProfile(me);
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
  print "Bought " + str(quant) + " stock(s) of " + stock + \
  " at the price of " + str(price)
  print "cost     =", cost
  print "cash_old =", cash
  print "cash_new =", myProfile.portfolio.cash

  # create a JSON object to return to the frontEnd
  context = {}
  context['cashOnHand'] = int(finalCash)
  context['date'] = now
  data =  json.dumps(context, cls=DjangoJSONEncoder)

  return HttpResponse(data, mimetype="application/json", status=200)
  #-------------------------#

#-----------SELL----------------#
@login_required
def sell(request):
  me = request.user;
  now = time.strftime("%m/%d/%Y")
  myProfile = getUserProfile(me);

  buyId = int(request.GET['index'])
  price = float(request.GET['soldAt'])
  print "price = ", price

  buy = myProfile.portfolio.owned.all()[buyId]
  stock = buy.tickerSymbol
  nm = buy.companyName
  quant = buy.quantity


  new_buy = Sell(tickerSymbol=stock,
   date=now, soldAt=price, \
   quantity=quant, user=me)
  new_buy.save()
  myProfile.portfolio.history.add(new_buy)
  myProfile.portfolio.owned.remove(buy)

  cost = int(quant) * float(price)
  cash = int(myProfile.portfolio.cash)
  finalCash = cash + cost
  myProfile.portfolio.cash = finalCash
  myProfile.portfolio.save()
  print "Sold " + str(quant) + " stock(s) of " + stock + \
  " at the price of " + str(price)
  print "cost     =", cost
  print "cash_old =", cash
  print "cash_new =", myProfile.portfolio.cash

  # create a JSON object to return to the frontEnd
  context = {}
  context['cashOnHand'] = int(finalCash)
  context['date'] = now
  data =  json.dumps(context, cls=DjangoJSONEncoder)
  return HttpResponse(data, mimetype="application/json", status=200)
#-------------------------------#

#------------LOGGED IN HOME-------------------#
@login_required
def thePortfolio(request):
  context = {}

  if len(MyClass.objects.filter(teacher=request.user)) != 0:
    print "logged in home as teacher!"
    return render(request, 'inprogress.html', context)
  me = getUserProfile(request.user)

  # Create a contextual object for data in the frontEnd
  context['username'] = request.user.username
  context['cash'] = me.portfolio.cash
  buy_list = me.portfolio.owned.all()
  # TODO: Aayush, I also need the user's current portfolio
  # as an array of BUYs they own, so that I can appropriately
  # draw the same on the front end. 
  context['portfolio'] = buy_list

  return render(request, 'portfolio.html', context)

#---------------------------------------------#

#------------helpful--------------------------#
def getUserProfile(usr):
  return get_object_or_404(UserProfile, user=usr)
#---------------------------------------------#

#------------CLASS----------------------------#

#----------teacher reg------------------------#
def registerClass(request):

  print "----registerClass----"

  context = {}
  
  # Don't really need this since we're going to login.html

  # forms = {}

  # # Registration Form for a user to be a teacher
  # teacherForm = {}
  # teacherForm['form'] = ClassRegistrationForm()
  # teacherForm['method'] = "registerClass"

  # # Add all these forms to a generic form key
  # forms['teacher'] = teacherForm
 
  # form = ClassRegistrationForm(request.POST)
  # context['registrationForm'] = form
 
  form = ClassRegistrationForm(request.POST)

  #check for error
  if form.is_valid():
    doRegisterClass(request, form)
    
    messages = []
    context['messages'] = messages
    messages.append("A confirmation email has been sent to your email address.")
    return render(request, "login.html", context)
  
  else:
    #unbound form

    # Coming here also means that there were errors. Look into that - Rishabh 11/29 9:55 PM
    print "Something went wrong with the form"

    return render(request, "registration.html", context)

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
              from_email="aayusha+devnull@andrew.cmu.edu",
              recipient_list=[new_user.email])


#--------------teacher reg-------------------#

#--------------student reg-------------------#
def registerStudent(request):
  context = {}
  context['registrationForm'] = StudentRegistrationForm()
 
  form = StudentRegistrationForm(request.POST)
  context['registrationForm'] = form
 
  #check for error
  if form.is_valid():
    print 'form is valid';
    doRegisterStudent(request, form)
    
    messages = []
    context['messages'] = messages
    messages.append("A confirmation email has been sent to your email address.")

    return render(request, "login.html", context)
  else:
    #unbound form
    return render(request, "registration.html", context)

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
  new_user_profile = UserProfile(user=new_user, portfolio=portf)
  new_user_profile.save()
  my_class.students.add(new_user_profile)
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
              from_email="aayusha+devnull@andrew.cmu.edu",
              recipient_list=[new_user.email])

#--------------student reg-------------------#


#---------------------------------------------#

@login_required
def resetPassword(request):
	if request.method == 'GET':
		context = {}
		form = ResetPasswordForm()
		context['form'] = form
		context['username'] = request.user.username
		return render(request, 'resetPassword.html', context)
	else:
		form = ResetPasswordForm(request.POST, request.FILES)
		me = getUserProfile(request.user)
		if form.is_valid():
			oldPass = form.cleaned_data.get('oldPassword')
			newPass = form.cleaned_data.get('password1')
			if me.user.check_password(oldPass):
				me.user.set_password(newPass)
				me.is_active = True
				me.user.save()
			return redirect('/portfolio')
		return redirect('resetPassword')

def forgotPassword(request):
	if request.method == 'GET':
		context = {}
		return render(request, 'forgotPassword.html', context)
	else:
		myEmail = request.POST['email']
		me = User.objects.filter(email=myEmail)[0]
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
              from_email="aayusha+devnull@andrew.cmu.edu",
              recipient_list=[user.email])
        context = {}
        context['email'] = myEmail
        return render(request, 'needs-confirmation.html', context)

@transaction.commit_on_success
def confirm_resetpassword(request, username, token):
    user = get_object_or_404(User, username=username)
    # Send 404 error if token is invalid
    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})



# Added by Rishabh

# Simple about page.
def about(request):
  return render(request, "about.html", {})



