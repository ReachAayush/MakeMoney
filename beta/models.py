from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image

# #Person
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    portfolio = models.OneToOneField("Portfolio")

    def __unicode__(self):
    	return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class MyClass(models.Model):
    className = models.CharField(max_length=50)
    teacher = models.ForeignKey(User)
    students = models.ManyToManyField("UserProfile")
    startingCashValue = models.IntegerField(default=100000)
    def __unicode__(self):
        return "Class with teacher: " + self.className + "."

class Portfolio(models.Model):
    owned = models.ManyToManyField("Buy")
    history = models.ManyToManyField("Sell")
    cash = models.IntegerField()
    def __unicode__(self):
        return str(self.cash)

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
        return "Bought " + str(quantity) + " stock(s) of " + tickerSymbol + " at the price of " + str(boughtAt)

class Sell(models.Model):
    tickerSymbol = models.CharField(max_length=5)
    soldAt = models.IntegerField(blank=False)
    quantity = models.IntegerField(blank=True)
    user = models.ForeignKey(User)
    date = models.DateField(auto_now=True)
    def __unicode__(self):
        quantity = self.quantity
        tickerSymbol = self.tickerSymbol
        soldAt = self.soldAt
        return "Sold " + str(quantity) + " stock(s) of " + tickerSymbol + " at the price of " + str(soldAt)
