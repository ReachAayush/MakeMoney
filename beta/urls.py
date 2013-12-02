from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
	# Registration & Sign In URLs
	url('^signin$', 'beta.views.myLogin'),
	url('^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	url('^register$', 'beta.views.register', name='register'),
	url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'beta.views.confirm_registration', name='confirm'),
	url('^logOut', 'django.contrib.auth.views.logout_then_login'),
	url('^resetPassword$', 'beta.views.resetPassword', name='resetPassword'),
	url('forgotPassword$', 'beta.views.forgotPassword', name='forgotPassword'),
	url(r'^confirm_resetpassword/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 
		'beta.views.confirm_resetpassword', name='resetPassConfirm'),

	# Page URLs
	url('^portfolio$', 'beta.views.thePortfolio'),
	url('^teacherHome$', 'beta.views.teacherHome'),

	# Method URLs
	url('^buy', 'beta.views.buy'),
	url('^sell', 'beta.views.sell'),
	url('^graph', 'beta.views.graph'),
	#url('^table.csv', 'beta.views.tablecsv'),

	# Class URLs
	url('^registerClass$', 'beta.views.registerClass', name='registerClass'),
	url('^registerStudent$', 'beta.views.registerStudent', name='registerStudent'),
	
	# Other
	url('^about$', 'beta.views.about', name="about"),

	# Pending Deprication
	url('^$', 'beta.views.thePortfolio', name='home'),
)