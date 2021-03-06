from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
	# Sign-In and Password Handling URLs
	url(r'^signin$', 'beta.views.myLogin'),
	url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	url(r'^logOut', 'django.contrib.auth.views.logout_then_login'),
	url(r'^resetPassword$', 'beta.views.resetPassword', name='resetPassword'),
	url(r'forgotPassword$', 'beta.views.forgotPassword', name='forgotPassword'),
	url(r'^confirm_resetpassword/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 
		'beta.views.confirm_resetpassword', name='resetPassConfirm'),

	# Registration
	url(r'^register$', 'beta.views.register', name='register'),
	url(r'^registerClass$', 'beta.views.registerClass', name='registerClass'),
	url(r'^registerStudent$', 'beta.views.registerStudent', name='registerStudent'),
	url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'beta.views.confirm_registration', name='confirm'),
	
	# Method URLs
	url(r'^buy', 'beta.views.buy'),
	url(r'^sell', 'beta.views.sell'),
	# url(r'^graph', 'beta.views.graph'),
	url(r'^addMessage', 'beta.views.addMessage'),

	# Other
	url(r'^about$', 'beta.views.about', name="about"),

	# Universal Home Page
	url(r'^$', 'beta.views.drawHomePage', name='home'),

	# Profile - note this accepts any url pattern
	url(r'^(?P<user_id>[a-zA-Z0-9_@\+\-]+)$', 'beta.views.profile', name='profile'),
)