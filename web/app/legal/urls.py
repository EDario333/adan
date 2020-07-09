from django.conf.urls import url

from . views import \
terms_conditions, license, join_us, privacy

urlpatterns = [
	url(r'^terms-conditions/$', terms_conditions, name='terms-conditions'),
	url(r'^privacy/$', privacy, name='privacy'),
	url(r'^license/$', license, name='software-license'),
	url(r'^join-us/$', join_us, name='join-us'),
]