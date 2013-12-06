# --- MODELS.py ---
# Models used to maintain databases for Hustle.
# Principal Developer: Aayush Agarwal
# Secondary Developer: Rishabh A Singh
# -----------------

# -- IMPORTS --
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# -- MODELS --

# - USER MODEL HELPERS -

# Portfolio of a given User
class Portfolio(models.Model):
    owned = models.ManyToManyField("Buy")
    history = models.ManyToManyField("Sell")
    cash = models.IntegerField()

    def __unicode__(self):
        return str(self.cash)

# Messaging for Class
class Message(models.Model):
    messageFrom = models.ForeignKey(User)

    # Used a charfield here for formatting purposes. The items
    # are added to the log in chronological order anyway.
    time = models.CharField(max_length=200)
    message = models.CharField(max_length=500)

    def __unicode__(self):
        return self.message



# - USER MODELS -

# Solo Hustle User (Hustlr)
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    portfolio = models.OneToOneField("Portfolio")

    def __unicode__(self):
    	return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

# Student User
class Student(models.Model):
    user = models.ForeignKey(User)
    portfolio = models.OneToOneField("Portfolio")
    classAttending = models.OneToOneField("MyClass")

    def __unicode__(self):
        return self.user.username

# Class (Made inside teacher form)
class MyClass(models.Model):
    className = models.CharField(max_length=50)
    teacher = models.ForeignKey(User)
    students = models.ManyToManyField("Student")
    startingCashValue = models.IntegerField(default=100000)
    messageLog = models.ManyToManyField("Message")

    # returns a list of student names in the class
    def roster(self):
        allStudentObjects = list(self.students.all())
        return map(lambda s:s.user.username,allStudentObjects)

    # prints out the class name.
    def class_name(self):
        return self.className

    # prints out teacher name
    def teacher_name(self):
        return self.teacher.username

    def get_log(self):
        allMsgObjs = list(self.messageLog.all())

        # given a msg, converts to JSON
        def msg_json(m):
            ans = {}

            ans['from'] = m.messageFrom
            ans['date'] = m.time
            ans['message'] = m.message

            return ans

        return map(msg_json, allMsgObjs)

    def __unicode__(self):
        return self.className


# - PORTFOLIO MODELS -

# Buy Instance
class Buy(models.Model):
    tickerSymbol = models.CharField(max_length=5)
    companyName = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    boughtAt = models.IntegerField(blank=False)
    quantity = models.IntegerField(blank=True)
    user = models.ForeignKey(User)
    def __unicode__(self):
        quantity = self.quantity
        tickerSymbol = self.tickerSymbol
        boughtAt = self.boughtAt
        return "Bought " + str(quantity) + " stock(s) of " + \
         tickerSymbol + " at the price of " + str(boughtAt)

# Sell Instance
class Sell(models.Model):
    date = models.DateField(auto_now=True)
    tickerSymbol = models.CharField(max_length=5)
    boughtAt = models.IntegerField(blank=False)
    quantity = models.IntegerField(blank=True)
    soldAt = models.IntegerField(blank=False)
    netProfit = models.IntegerField(blank=False)
    
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        quantity = self.quantity
        tickerSymbol = self.tickerSymbol
        soldAt = self.soldAt
        return "Sold " + str(quantity) + " stock(s) of " + tickerSymbol + \
         " at the price of " + str(soldAt)
